import os
import pandas as pd
from experiments.experiment import Experiment
from experiments.result import Result

class ExperimentsFile:
    def __init__(self):
        self.results = pd.DataFrame()

    def load(self, file_path: str):
        if os.path.exists(file_path):
            self.results = pd.read_csv(file_path)
        else:
            self.results = pd.DataFrame()

    def add_row(self, experiment: Experiment, result: Result):
        experiment_dict = experiment.__dict__
        result_dict = result.__dict__
        row_dict = {**experiment_dict, **result_dict}
        row_dict = {key.replace("_", " ").title(): value for key, value in row_dict.items()}
        row_dict = {key.replace("Per", "per"): value for key, value in row_dict.items()}
        self.results = self.results._append(row_dict, ignore_index=True)

    def save(self, file_path: str):

        try:
            self.results.to_csv(file_path, index=False)
        except:
            # Note: If I can't overwrite the original file, then save as a one-off file
            date_time = pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = f"{file_path}_{date_time}.csv"
            self.results.to_csv(file_path, index=False)