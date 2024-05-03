# Import the packages
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shared
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Set the model names
model_names = [
    "gpt-35-turbo",
    "gpt-4",
    "llama-2-7b-chat",
    "llama-2-70b-chat",
    "mistral-large",
    "cohere-command-r-plus",
    "gemini-1.0-pro",
    "gemini-1.5-pro-preview-0409",
    "claude-3-opus-20240229"
]

# Set the parameters
agent_name = None
exam_name = None
input_file = f"../data/results/results.csv"

# Load the data
results = pd.read_csv(input_file)
duplicate_results = results[results.duplicated(subset=["Name"], keep=False)]
assert len(duplicate_results) == 0, "There are duplicate results."

# Summarize the metrics by model
baselines_by_model = results[results["Agent Name"] == "baseline"] \
    .groupby(["Model Name"]).agg({
    "Questions": "sum"}) \
    .reset_index()
assert len(baselines_by_model[baselines_by_model["Questions"] != 1100]) == 0, \
    "The number of questions for the baseline agents is not equal to 1100."

model_names = results["Model Name"].unique()
agent_names = results["Agent Name"].unique()
exam_names = results["Exam Name"].unique()

assert len(model_names) == 9, "The number of models is not correct."
assert len(agent_names) == 9, "The number of agents is not correct."
assert len(exam_names) == 11, "The number of exams is not correct."

for model_name in model_names:
    for agent in agent_names:
        for exam in exam_names:
            row = results[
                (results["Model Name"] == model_name) &
                (results["Agent Name"] == agent) &
                (results["Exam Name"] == exam)]
            # print(f"{model_name} - {agent} - {exam}")
            assert len(row) == 1, f"There is not a single row for {model_name}, {agent}, {exam}."

print("All the results are correct.")
