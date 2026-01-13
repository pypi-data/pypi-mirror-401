import numpy as np
from ddi_fw import utils
from ddi_fw.ml.wrappers.model_wrapper import ModelWrapper
from ddi_fw.ml.evaluation_helper import Metrics, evaluate
 

class StackingWrapper(ModelWrapper):
    def __init__(self, date, descriptor, base_wrappers, meta_model_wrapper, tracking_service=None):
        """
        Args:
            base_wrappers (list): list of instantiated base model wrappers (TF or XGBoost)
            meta_model_wrapper (ModelWrapper): instantiated meta model wrapper
            tracking_service: optional tracking service
        """
        super().__init__(date, descriptor, None)
        self.base_wrappers = base_wrappers
        self.meta_model_wrapper = meta_model_wrapper
        self.tracking_service = tracking_service

    def fit(self):
        # Step 1: Train base models and collect softmax outputs
        inputs = []
        train_label, test_label = None, None
        train_idx_arr, val_idx_arr = None, None
        num_classes = None
        for wrapper in self.base_wrappers:
            train_label = wrapper.train_label
            test_label = wrapper.test_label
            
            # wrapper.train_data = self.train_data
            # wrapper.train_label = self.train_label
            train_idx_arr = wrapper.train_idx_arr
            val_idx_arr = wrapper.val_idx_arr
            # wrapper.train_idx_arr = self.train_idx_arr
            # wrapper.test_data = self.test_data
            # wrapper.test_label = self.test_label

            print(f"Training base model: {wrapper.descriptor}")
            best_model, _, val_preds_dict = wrapper.fit()
            num_classes = wrapper.num_classes
            wrapper.best_model = best_model
            # pred_train = wrapper.predict()
            # if val_preds_dict is not None:
            print("val_preds_dict")
            print(val_preds_dict)
            stacked_values = np.concatenate(list(val_preds_dict.values()))
            # Use validation predictions for training meta-model
            inputs.append(stacked_values)

            # pred_val = wrapper.predict()
            # base_test_outputs.append(pred_val)

        # Step 2: Prepare meta-model input
        # shape: (n_samples, num_classes * num_base_models)
        # X_meta_train = np.hstack(inputs)
        X_meta_train = np.stack(inputs, axis=1)
        y_meta_train = train_label

        # Step 3: Train meta-model
        self.meta_model_wrapper.train_data = X_meta_train
        self.meta_model_wrapper.train_label = y_meta_train
        self.meta_model_wrapper.train_idx_arr = train_idx_arr
        self.meta_model_wrapper.val_idx_arr = val_idx_arr
        self.num_classes = num_classes
        # self.meta_model_wrapper.val_idx_arr = None
        preds = [b.predict() for b in self.base_wrappers]
        self.meta_model_wrapper.test_data = np.stack(preds, axis=1) 
        
        # self.meta_model_wrapper.test_data = np.hstack(
        #     [b.predict() for b in self.base_wrappers])
        
        self.meta_model_wrapper.test_label = test_label

        print("Training meta-learner...")
        best_meta_model, best_meta_key, _ = self.meta_model_wrapper.fit()
        self.meta_model_wrapper.best_model = best_meta_model
        # self.best_model = best_meta_model

        return best_meta_model, best_meta_key

    def predict(self):
        # Step 3: Feed into meta-model
        pred = self.meta_model_wrapper.predict()
        return pred

    def fit_and_evaluate(self, print_detail=False):
        best_model, best_key = self.fit()
        pred = self.predict()
        pred_as_cat = utils.convert_to_categorical(pred, self.num_classes)
        logs, metrics = evaluate(
            self.meta_model_wrapper.test_label, pred_as_cat, info=self.descriptor, print_detail=print_detail)
        metrics.format_float()
        return logs, metrics, pred
