import numpy as np
from typing import Optional, Any
from ddi_fw.ml.wrappers.model_wrapper import ModelWrapper
from ddi_fw.ml.tracking_service import TrackingService
from ddi_fw.ml.evaluation_helper import Metrics, evaluate
import ddi_fw.utils as utils
from sklearn.ensemble import RandomForestClassifier
from typing import Optional, Any
import numpy as np
 

class RandomForestModelWrapper(ModelWrapper):

    def __init__(self, date, descriptor, model_func=None,
                 tracking_service: Optional[TrackingService] = None,
                 **kwargs):

        super().__init__(date, descriptor, model_func, **kwargs)
        self.tracking_service = tracking_service

        # Extract parameters or set defaults
        self.params = kwargs if kwargs else {
            'n_estimators': 200,
            'max_depth': None,
            'min_samples_split': 2,
            'min_samples_leaf': 1,
            'max_features': 'sqrt',
            'bootstrap': True,
            'random_state': 42,
            'n_jobs': -1
        }

    # ---------------------------------------------------------
    # FIT MODEL (single fold)
    # ---------------------------------------------------------
    def fit_model(self, X_train, y_train, X_valid, y_valid):

        # Convert numpy arrays
        X_train = np.array(X_train)
        X_valid = np.array(X_valid) if X_valid is not None else None

        # Convert one-hot → class indices
        y_train_indices = np.argmax(y_train, axis=1)
        y_valid_indices = np.argmax(
            y_valid, axis=1) if y_valid is not None else None

        # Build model
        model = RandomForestClassifier(**self.params)

        # Fit
        model.fit(X_train, y_train_indices)

        # Validation accuracy
        evals_result = {}
        if X_valid is not None:
            val_pred = model.predict(X_valid)
            val_acc = (val_pred == y_valid_indices).mean()
            evals_result['valid'] = {'accuracy': [val_acc]}

        return model, evals_result

    # ---------------------------------------------------------
    # FIT WITH CV
    # ---------------------------------------------------------
    def fit(self):
        print(f"Training {self.descriptor} model...")

        models = {}
        models_val_acc = {}   # store validation accuracies

        if self.train_idx_arr and self.val_idx_arr:
            # Cross-validation case
            for i, (train_idx, val_idx) in enumerate(zip(self.train_idx_arr, self.val_idx_arr)):
                print(f"Validation {i}")

                X_train_cv = self.train_data[train_idx]
                y_train_cv = self.train_label[train_idx]
                X_valid_cv = self.train_data[val_idx]
                y_valid_cv = self.train_label[val_idx]

                def fit_model_cv_func():
                    model, evals_result = self.fit_model(
                        X_train_cv, y_train_cv, X_valid_cv, y_valid_cv
                    )
                    return model, evals_result

                if self.tracking_service:
                    model, evals_result = self.tracking_service.run(
                        run_name=f"Validation {i}",
                        description="CV models",
                        nested_run=True,
                        func=fit_model_cv_func
                    )
                else:
                    model, evals_result = fit_model_cv_func()

                models[f"{self.descriptor}_validation_{i}"] = model

                # extract validation accuracy
                if 'valid' in evals_result:
                    val_acc = evals_result['valid']['accuracy'][-1]
                    models_val_acc[f"{self.descriptor}_validation_{i}"] = val_acc

        else:
            # No CV case
            def fit_model_func():
                model, evals_result = self.fit_model(
                    self.train_data, self.train_label, None, None
                )
                return model, evals_result

            if self.tracking_service:
                model, evals_result = self.tracking_service.run(
                    run_name="Training",
                    description="Training",
                    nested_run=True,
                    func=fit_model_func
                )
            else:
                model, evals_result = fit_model_func()

            models[self.descriptor] = model
            models_val_acc[self.descriptor] = 0  # No validation: default

        # Select best model
        if models_val_acc:
            # maximize accuracy
            best_model_key = max(models_val_acc, key=models_val_acc.get)
            best_model = models[best_model_key]
            print("Best model key:", best_model_key)
            return best_model, best_model_key

        return models[self.descriptor], None

    # ---------------------------------------------------------
    # PREDICT
    # ---------------------------------------------------------
    def predict(self):
        X_test = np.array(self.test_data)
        pred = self.best_model.predict(X_test)
        return pred

    # ---------------------------------------------------------
    # FIT + EVALUATE
    # ---------------------------------------------------------
    def fit_and_evaluate(self, print_detail=False):

        self.best_model = None

        def evaluate_and_log(artifact_uri=None):

            best_model, best_model_key, _ = self.fit()
            self.best_model = best_model

            # Predict
            pred = self.predict()
            num_classes = self.train_label.shape[1]

            # Convert to one-hot
            pred = utils.convert_to_categorical(pred.astype(np.int32), num_classes)

            actual = self.test_label

            # Evaluation
            logs, metrics = evaluate(
                actual=actual, pred=pred, info=self.descriptor, print_detail=print_detail
            )
            metrics.format_float()

            # Tracking
            if self.tracking_service:
                self.tracking_service.log_metrics(logs)
                self.tracking_service.log_param("best_cv", best_model_key)

                if artifact_uri:
                    utils.compress_and_save_data(
                        metrics.__dict__, artifact_uri, f"{self.date}_metrics.gzip"
                    )
                    self.tracking_service.log_artifact(
                        f"{artifact_uri}/{self.date}_metrics.gzip"
                    )

            return logs, metrics, pred

        # If tracking service is present
        if self.tracking_service:
            return self.tracking_service.run(
                run_name=self.descriptor,
                description="Fit and evaluate",
                nested_run=True,
                func=evaluate_and_log
            )

        # Otherwise direct run
        return evaluate_and_log()
