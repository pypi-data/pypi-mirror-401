from typing import Optional
from typing import Any, Callable
from ddi_fw.ml.wrappers.model_wrapper import ModelWrapper
import tensorflow as tf
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
import numpy as np
from ddi_fw.ml.evaluation_helper import Metrics, evaluate
from ddi_fw.ml.tracking_service import TrackingService
import ddi_fw.utils as utils

try:
    import xgboost as xgb
except ImportError:
    raise ImportError(
        "xgboost is required for XGBoostModelWrapper. "
        "Please install it with: pip install xgboost"
    )
 

class XGBoostModelWrapper(ModelWrapper):

    def __init__(self, date, descriptor, model_func, tracking_service: Optional[TrackingService] = None, **kwargs):
        super().__init__(date, descriptor, model_func, **kwargs)
        self.tracking_service = tracking_service
        self.num_rounds = kwargs.get('num_rounds', 5)
        self.early_stopping_rounds = kwargs.get('early_stopping_rounds', 10)
        # self.params = kwargs.get('params', {})
        self.params = kwargs
        if not self.params:
            print("Using default XGBoost parameters.")
            self.params = {
                'objective': 'multi:softmax',  # Use 'multi:softprob' for probabilities
                'eval_metric': 'mlogloss',     # Multi-class log loss
                'max_depth': 3,                # Depth of each tree
                'eta': 0.1,                    # Learning rate
                'silent': 1,                   # Suppress messages
                'subsample': 0.8,              # Subsampling ratio
                'colsample_bytree': 0.8        # Column subsampling ratio
            }

    def fit_model(self, X_train, y_train, X_valid, y_valid):
        # Create DMatrix for XGBoost

        X_train = np.array(X_train)
        X_valid = np.array(X_valid)

        # Convert one-hot encoded labels to class indices (should already be 1D)
        # Convert to 1D class indices
        y_train_indices = np.argmax(y_train, axis=1)
        # Convert to 1D class indices
        y_valid_indices = np.argmax(y_valid, axis=1)

        # # Flatten the arrays if they contain sequences (embeddings)
        # if X_train.dtype == 'object' and X_train.ndim == 2 and X_train.shape[1] == 1:
        #     X_train = np.vstack(X_train[:, 0])
        # if X_valid.dtype == 'object' and X_valid.ndim == 2 and X_valid.shape[1] == 1:
        #     X_valid = np.vstack(X_valid[:, 0])

        dtrain = xgb.DMatrix(X_train, label=y_train_indices)
        dvalid = xgb.DMatrix(
            X_valid, label=y_valid_indices) if X_valid is not None else None

        # Set up the evaluation list
        evals = [(dtrain, 'train')]
        if dvalid is not None:
            evals.append((dvalid, 'valid'))
        evals_result = {}
        # Number of classes (as per the one-hot encoding)
        if not 'num_class' in self.params:
            self.num_classes = y_train.shape[1]
            self.params['num_class'] = self.num_classes
        else:
            self.num_classes = self.params['num_class']

        # Train the model
        model = xgb.train(
            self.params,
            dtrain,
            num_boost_round=self.num_rounds,
            evals=evals,
            evals_result=evals_result,
            early_stopping_rounds=self.early_stopping_rounds,
            verbose_eval=True
        )
        val_pred = model.predict(dvalid)
        return model, evals_result, val_pred

    def fit(self):
        print(f"Training {self.descriptor} model...")
        models = {}
        models_val_acc = {}
        val_preds_dict = {}
        if self.train_idx_arr and self.val_idx_arr:
            for i, (train_idx, val_idx) in enumerate(zip(self.train_idx_arr, self.val_idx_arr)):
                print(f"Validation {i}")
                X_train_cv = self.train_data[train_idx]
                y_train_cv = self.train_label[train_idx]
                X_valid_cv = self.train_data[val_idx]
                y_valid_cv = self.train_label[val_idx]

                def fit_model_cv_func():
                    model, evals_result, val_pred = self.fit_model(
                        X_train_cv, y_train_cv, X_valid_cv, y_valid_cv)
                    return model, evals_result, val_pred

                if self.tracking_service:
                    model, evals_result, val_pred = self.tracking_service.run(
                        run_name=f'Validation {i}', description='CV models', nested_run=True, func=fit_model_cv_func)
                else:
                    model, evals_result, val_pred = fit_model_cv_func()

                val_preds_dict[f'{self.descriptor}_validation_{i}'] = val_pred
                models[f'{self.descriptor}_validation_{i}'] = model
                # Here you can extract validation metrics from the model
                # Assuming the validation set is provided, we get accuracy as an example:
                if 'valid' in evals_result:
                    # val_acc = evals_result['valid']['rmse'][self.early_stopping_rounds-1]
                    val_acc = evals_result['valid']['mlogloss'][-1]
                    models_val_acc[f'{self.descriptor}_validation_{i}'] = val_acc

        else:
            def fit_model_func():
                model, evals_result,_ = self.fit_model(
                    self.train_data, self.train_label, None, None)
                return model, evals_result, None

            if self.tracking_service:
                model, evals_result,_ = self.tracking_service.run(
                    run_name=f'Training', description='Training', nested_run=True, func=fit_model_func)
            else:
                model, evals_result,_ = fit_model_func()

            models[self.descriptor] = model
            # Extract validation accuracy if available
            models_val_acc[self.descriptor] = model.attributes.get(
                'best_score', [0])[-1]  # or any metric you prefer
        print(model.attributes())
        print(models_val_acc)
        # Return the best model based on validation accuracy
        if models_val_acc:
            best_model_key = min(models_val_acc, key=models_val_acc.get)
            print("best model key:", best_model_key)
            best_model = models[best_model_key]
            return best_model, best_model_key, val_preds_dict
        print(models.keys())
        return models[self.descriptor], None, val_preds_dict

    def _predict(self, X):
        dtest = xgb.DMatrix(X)
        pred = self.best_model.predict(dtest)
        return pred

    def predict(self):
        # Assuming the model is already trained
        # Ensure X_train and X_test are numpy arrays (they should be, but let's confirm)
        # X_train = np.array(X_train)
        # X_test = np.array(X_test)

        # if X_test.dtype == 'object' and X_test.ndim == 2 and X_test.shape[1] == 1:
        #     X_test = np.vstack(X_test[:, 0])
        dtest = xgb.DMatrix(self.test_data)
        pred = self.best_model.predict(dtest)
        return pred

    def fit_and_evaluate(self, print_detail=False) -> tuple[dict[str, Any], Metrics, Any]:
        """
        Fit the model, evaluate it, and log results using the tracking service.

        Args:
            print_detail (bool): Whether to print detailed evaluation logs.

        Returns:
            tuple: A tuple containing logs, metrics, and predictions.
        """
        self.best_model: xgb.Booster = None

        def evaluate_and_log(artifact_uri=None):
            # Fit the model
            best_model, best_model_key, _  = self.fit()
            self.best_model = best_model

            # Make predictions
            pred = self.predict()
            pred = utils.convert_to_categorical(
                pred.astype(np.int32), self.num_classes)
            actual = self.test_label

            # Evaluate the model
            logs, metrics = evaluate(
                actual=actual, pred=pred, info=self.descriptor, print_detail=print_detail
            )
            metrics.format_float()

            if self.tracking_service:
                # Log metrics and parameters
                self.tracking_service.log_metrics(logs)
                self.tracking_service.log_param('best_cv', best_model_key)

                # Save metrics to the artifact URI if provided
                if artifact_uri:
                    utils.compress_and_save_data(
                        metrics.__dict__, artifact_uri, f'{self.date}_metrics.gzip'
                    )
                    self.tracking_service.log_artifact(
                        f'{artifact_uri}/{self.date}_metrics.gzip'
                    )

            return logs, metrics, pred

        # Use the tracking service to run the evaluation
        if self.tracking_service:
            return self.tracking_service.run(
                run_name=self.descriptor,
                description="Fit and evaluate the model",
                nested_run=True,
                func=evaluate_and_log
            )
        else:
            # If no tracking service is provided, run the evaluation directly
            return evaluate_and_log()
