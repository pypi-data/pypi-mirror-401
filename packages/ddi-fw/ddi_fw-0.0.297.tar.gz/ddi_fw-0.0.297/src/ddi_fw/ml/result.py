class Result:
    def __init__(self) -> None:
        self.log_dict = {}
        self.metric_dict = {}

    def add_log(self, key, logs):
        self.log_dict[key] = logs

    def add_metric(self, key, metrics):
        self.metric_dict[key] = metrics