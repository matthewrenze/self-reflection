import pandas as pd
from experiments.experiment import Experiment

class Result:
    def __init__(self, experiment: Experiment, details: pd.DataFrame, pricing: tuple):
        self.questions = len(details)
        self.correct = details["score"].sum()
        self.incorrect = self.questions - self.correct
        self.accuracy = self.correct / self.questions
        self.num_errors = details.error.apply(lambda x: 1 if x != "" else 0).sum()
        self.input_tokens = details.input_tokens.sum()
        self.output_tokens = details.output_tokens.sum()
        self.total_tokens = details.total_tokens.sum()
        self.tokens_per_question = self.total_tokens / self.questions
        input_cost = pricing[0] * self.input_tokens / 1000
        output_cost = pricing[1] * self.output_tokens / 1000
        self.total_cost = input_cost + output_cost
        self.cost_per_question = self.total_cost / self.questions
        self.runtime = (experiment.end_time - experiment.start_time).total_seconds()
        self.runtime_per_question = self.runtime / self.questions

    def __str__(self):
        text = (
            f"Questions: {self.questions}\n"
            f"Correct: {self.correct}\n"
            f"Incorrect: {self.incorrect}\n"
            f"Accuracy: {self.accuracy:.4f}\n"
            f"Errors: {self.num_errors}\n"
            f"Input Tokens: {self.input_tokens}\n"
            f"Output Tokens: {self.output_tokens}\n"
            f"Total Tokens: {self.total_tokens}\n"
            f"Tokens per Question: {self.tokens_per_question}\n"
            f"Total Cost: ${self.total_cost:.2f}\n"
            f"Cost per question: ${self.cost_per_question:.4f}\n"
            f"Total Runtime: {self.runtime:.2f} seconds\n"
            f"Runtime per question: {self.runtime_per_question:.2f} seconds\n")
        return text

