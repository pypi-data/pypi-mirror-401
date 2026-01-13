
from typing import Any, Dict, List, Optional

import numpy as np
from ddi_fw import utils
from ddi_fw.ml.ensemble.ensemble_strategy import AveragingStrategy, EnsembleStrategy, StackingStrategy, VotingStrategy
from ddi_fw.ml.evaluation_helper import Metrics, evaluate
from ddi_fw.ml.wrappers.model_wrapper import ModelWrapper, Result


class GenericEnsembleWrapper(ModelWrapper):
    """Generic ensemble wrapper supporting multiple strategies"""

    STRATEGY_MAP = {
        "voting": VotingStrategy,
        "averaging": AveragingStrategy,
        "stacking": StackingStrategy
    }

    def __init__(
        self,
        base_wrappers: List[ModelWrapper],
        meta_learners: List[ModelWrapper],
        meta_learner_processors: Dict[str, Any],
        ensemble_strategies: str,          # now comma separated input
        name: str = "ensemble",
        tracking_service: Optional[Any] = None,
        date: Optional[str] = None
    ):
        self.base_wrappers = base_wrappers
        self.name = name
        self.tracking_service = tracking_service
        self.date = date or utils.utc_time_as_string_simple_format()
        self.ensemble_strategies = ensemble_strategies
        self.meta_learners = meta_learners
        self.meta_learner_processors = meta_learner_processors

        # prediction cache so we don't recompute
        self.wrapper_predictions: Dict[str, np.ndarray] = {}

        self.individual_metrics = {}
        self.ensemble_metrics: Dict[str, Metrics] = {}
        self.result = Result()

    # ---------------------------------------------------------
    # FIT
    # ---------------------------------------------------------
    def fit(self):
        train_label, test_label = None, None

        # if any(getattr(wrapper, 'best_model', None) is not None for wrapper in self.base_wrappers):
        #     # At least one wrapper has best_model set
        #     pass

        train_label, test_label = None, None
        train_idx_arr, val_idx_arr = None, None
        val_labels = []
        inputs = []

        for wrapper in self.base_wrappers:
            train_label = wrapper.train_label
            test_label = wrapper.test_label

            train_idx_arr = wrapper.train_idx_arr
            val_idx_arr = wrapper.val_idx_arr

            if not val_labels:
                for i, (train_idx, val_idx) in enumerate(zip(train_idx_arr, val_idx_arr)):
                    fold_val_labels = train_label[val_idx]
                    val_labels.append(fold_val_labels)
            # Convert the list of arrays to a single numpy array
            all_fold_val_labels = np.concatenate(val_labels)

            print(f"Training base model: {wrapper.descriptor}")
            best_model, _, val_preds_dict = wrapper.fit()
            num_classes = wrapper.num_classes
            wrapper.best_model = best_model
            # pred_train = wrapper.predict()
            # if val_preds_dict is not None:
            print("val_preds_dict")
            print(val_preds_dict)
            for key, value in val_preds_dict.items():
                print(f"Key: {key}, Value shape: {value.shape}")
            # stacked_values = np.concatenate(list(val_preds_dict.values()))
            # stacked_values = np.stack(list(val_preds_dict.values()), axis=1)
            stacked_values = np.vstack(list(val_preds_dict.values()))

            inputs.append(stacked_values)
            # inputs.append(list(val_preds_dict.values()))
      
        # inputs = np.concatenate(inputs, axis=1)
        print("shape of inputs for meta-learner:")
        print(inputs[0].shape)
        self.num_classes = num_classes
        self.test_label = test_label
        print("val labels")
        print(len(val_labels))
        # X_meta_train = np.stack(inputs, axis=1)
        # y_meta_train = train_label
        y_meta_train = all_fold_val_labels
        # print("X_meta_train shape:", X_meta_train.shape)
        print(y_meta_train)
        print("y_meta_train shape:", y_meta_train.shape)

        # Step 3: set the meta-learner's training data
        for meta_learner in self.meta_learners:
            
            # meta_learner.train_data = X_meta_train
            meta_learner.train_data = inputs
            meta_learner.train_label = y_meta_train
            meta_learner.train_idx_arr = train_idx_arr
            meta_learner.val_idx_arr = val_idx_arr
            meta_learner.test_label = test_label
            meta_learner.num_classes = num_classes

        # Parse comma-separated strategies
        self.selected_strategies: List[EnsembleStrategy] = []
        for s in self.ensemble_strategies.split(","):
            s = s.strip().lower()
            if s not in self.STRATEGY_MAP:
                raise ValueError(f"Unknown strategy '{s}'")
            if s == "stacking":
                if not self.meta_learners:
                    raise ValueError(
                        "Meta-learner must be provided for stacking strategy")
                for meta_learner in self.meta_learners:
                    processor_dict = self.meta_learner_processors.get(meta_learner.descriptor)
                    processor = processor_dict.get("processor") if processor_dict else None
                    processor_config = processor_dict.get("processor_config") if processor_dict else None
                    print("processor_dict for stacking:")
                    print(processor_dict)
                    if processor is None:
                        raise ValueError(
                            f"Processor must be provided for meta-learner '{meta_learner.descriptor}' in stacking strategy")
                    
                    if processor_config is None:
                        raise ValueError(
                            f"Processor config must be provided for meta-learner '{meta_learner.descriptor}' in stacking strategy")
                    
                    self.selected_strategies.append(StackingStrategy(descriptor=meta_learner.descriptor,
                                                                     meta_learner=meta_learner, 
                                                                     base_wrappers=self.base_wrappers,
                                                                     processor=processor,
                                                                     processor_config=processor_config))
            else:
                self.selected_strategies.append(self.STRATEGY_MAP[s]())

    # ---------------------------------------------------------
    # PREDICT — with prediction caching
    # ---------------------------------------------------------

    def _compute_and_cache_predictions(self):
        """Compute wrapper predictions only once."""
        if self.wrapper_predictions:
            return  # already computed

        for wrapper in self.base_wrappers:
            descriptor = wrapper.descriptor

            y_pred = wrapper.predict()
            print(f"Predictions from wrapper {descriptor}:")
            print(y_pred)
            print("Shape:")
            print(y_pred.shape)

            # Store raw predictions (strategies want raw data)
            self.wrapper_predictions[descriptor] = y_pred

            # Evaluation for individual wrapper
            y_pred_cat = utils.convert_to_categorical(y_pred, self.num_classes)
            _, wrapper_metrics = evaluate(self.test_label, y_pred_cat)
            wrapper_metrics.set_time(wrapper.elapsed_time)
            wrapper_metrics.format_float()

            self.result.add_metric(descriptor, wrapper_metrics)
            self.individual_metrics[descriptor] = wrapper_metrics
        print(self.wrapper_predictions)
    # ---------------------------------------------------------
    # MAIN PREDICTION PIPELINE
    # ---------------------------------------------------------

    def predict(self):
        # Compute predictions only once
        self._compute_and_cache_predictions()

        pred_list = list(self.wrapper_predictions.values())

        ensemble_outputs = {}

        for strategy in self.selected_strategies:
            strategy_name = strategy.get_strategy_name()

            # Combine predictions
            ensemble_pred = strategy.combine_predictions(pred_list)
            ensemble_pred = utils.convert_to_categorical(
                ensemble_pred, self.num_classes)

            # Evaluate ensemble
            _, metrics = evaluate(self.test_label, ensemble_pred)
            if type(strategy) is StackingStrategy:
                metrics.set_time(strategy.meta_learner.elapsed_time)

            metrics.format_float()

            # token = f"ensemble_{strategy_name}"
            token = strategy_name
            self.ensemble_metrics[token] = metrics
            self.result.add_metric(token, metrics)

            ensemble_outputs[token] = ensemble_pred

        return ensemble_outputs   # multiple ensemble predictions

    # ---------------------------------------------------------
    # FIT AND EVALUATE
    # ---------------------------------------------------------
    def fit_and_evaluate(self):
        self.fit()
        ensemble_preds = self.predict()
        return None, self.result, ensemble_preds
