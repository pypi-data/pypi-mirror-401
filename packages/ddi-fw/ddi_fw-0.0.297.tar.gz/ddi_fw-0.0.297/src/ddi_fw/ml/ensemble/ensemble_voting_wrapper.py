import numpy as np
from ddi_fw.ml.wrappers.model_wrapper import ModelWrapper
from ddi_fw.ml.evaluation_helper import Metrics, evaluate


class VotingWrapper(ModelWrapper):
    def __init__(self, wrappers, name="voting_ensemble"):
        self.wrappers = wrappers
        self.name = name
        self.individual_metrics = {}  # Store metrics for each wrapper
        self.ensemble_metrics = None   # Store ensemble metrics
        self.metrics_log = []         # List to collect metrics entries instead of printing

    def predict(self, X_test, y_test):
        """
        Generate predictions from all individual wrappers and the ensemble.
        Measure metrics for each wrapper and the ensemble. Metrics are stored
        in self.metrics_log and self.individual_metrics / self.ensemble_metrics.
        """
        individual_predictions = []
        individual_metrics_list = []

        # Get predictions and metrics from each wrapper
        for idx, wrapper in enumerate(self.wrappers):
            wrapper_name = wrapper.name if hasattr(wrapper, 'name') else f"wrapper_{idx}"

            # Get predictions from individual wrapper
            y_pred = wrapper.predict(X_test)
            individual_predictions.append(y_pred)

            # Evaluate individual wrapper
            wrapper_metrics = evaluate(y_test, y_pred)
            self.individual_metrics[wrapper_name] = wrapper_metrics
            individual_metrics_list.append(wrapper_metrics)

            # Append metrics to log as a structured dict
            self.metrics_log.append({
                "type": "individual",
                "name": wrapper_name,
                "metrics": self._metrics_to_dict(wrapper_metrics)
            })

        # Ensemble prediction (voting/averaging)
        ensemble_pred = self._ensemble_prediction(individual_predictions)

        # Evaluate ensemble
        self.ensemble_metrics = evaluate(y_test, ensemble_pred)

        # Append ensemble metrics to log
        self.metrics_log.append({
            "type": "ensemble",
            "name": self.name,
            "metrics": self._metrics_to_dict(self.ensemble_metrics)
        })

        return ensemble_pred

    def _ensemble_prediction(self, predictions):
        """
        Combine individual predictions using voting (for classification).
        Can be extended for regression or other aggregation strategies.
        """
        predictions_array = np.array(predictions)

        # For classification: majority voting
        if predictions_array.ndim == 2:  # Probabilities
            ensemble_pred = np.mean(predictions_array, axis=0)
        else:  # Class labels
            # Majority voting
            ensemble_pred = np.apply_along_axis(
                lambda x: np.bincount(x.astype(int)).argmax(),
                axis=0,
                arr=predictions_array
            )

        return ensemble_pred

    def _metrics_to_dict(self, metrics: Metrics):
        """
        Convert Metrics object or dict to plain dict for logging/serialization.
        """
        if isinstance(metrics, dict):
            return metrics
        result = {}
        for attr in dir(metrics):
            if not attr.startswith('_'):
                value = getattr(metrics, attr)
                if not callable(value):
                    try:
                        result[attr] = float(value)
                    except Exception:
                        result[attr] = value
        return result

    def _print_metrics(self, metrics: Metrics):
        """
        Legacy pretty-printer kept for compatibility; does not append to log.
        """
        if isinstance(metrics, dict):
            for key, value in metrics.items():
                print(f"{key}: {value:.4f}")
        else:
            for attr in dir(metrics):
                if not attr.startswith('_'):
                    value = getattr(metrics, attr)
                    if not callable(value):
                        print(f"{attr}: {value:.4f}")

    def get_metrics_summary(self):
        """
        Return a summary of all metrics (individual + ensemble) and the metrics log list.
        """
        summary = {
            "individual": self.individual_metrics,
            "ensemble": self.ensemble_metrics,
            "log": self.metrics_log
        }
        return summary