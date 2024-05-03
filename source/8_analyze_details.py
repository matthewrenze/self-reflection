# Import libraries
import os
import numpy as np
import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Set the file paths
input_file_path = "../data/details"
output_file_path = "../data/tables"

# Set the models
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

# Set the agents
baseline_agent_names = [
    "baseline"]

agent_names = [
    "retry",
    "keywords",
    "advice",
    "instructions",
    "explanation",
    "solution",
    "composite",
    "unredacted"
]

# Set the exams
# Note: Don't use comprehensive 100 for analysis
exam_names = [
    # "comprehensive-100",
    "aqua-rat-100",
    "logiqa-en-100",
    "lsat-ar-100",
    "lsat-lr-100",
    "lsat-rc-100",
    "sat-en-100",
    "sat-math-100",
    "arc-challenge-100",
    "hella-swag-100",
    "med-mcqa-100"
]

results = pd.DataFrame(columns=[
    "Model Name",
    "Agent Name",
    "Num Problems",
    "Baseline Score",
    "Agent Score",
    "Difference Score",
    "Baseline Accuracy",
    "Agent Accuracy",
    "Difference Accuracy",
    "Test Statistic",
    "p-value"])

baseline_results = pd.DataFrame()

for model_name in model_names:

    baseline_table = pd.DataFrame()
    for exam_name in exam_names:
        baseline_file_name = f"{model_name} - baseline - {exam_name}.csv"
        baseline_file_path = f"{input_file_path}/{baseline_file_name}"
        baseline_data = pd.read_csv(baseline_file_path)
        baseline_table = pd.concat([baseline_table, baseline_data])

    for agent_name in agent_names:
        agent_table = baseline_table.copy()
        agent_table = agent_table.set_index(["source", "source_id"])
        for exam_name in exam_names:
            agent_file_name = f"{model_name} - {agent_name} - {exam_name}.csv"
            agent_file_path = f"{input_file_path}/{agent_file_name}"
            agent_data = pd.read_csv(agent_file_path)
            agent_data = agent_data.set_index(["source", "source_id"])
            agent_table.update(agent_data)


        # Sort by model_name, agent_name, exam_name, and problem_id
        sort_columns = ["exam_name", "problem_id"]
        baseline_table = baseline_table.sort_values(by=sort_columns)
        agent_table = agent_table.sort_values(by=sort_columns)

        # # DEBUG:
        # baseline_table = baseline_table.drop(columns=["id"])
        # agent_table = agent_table.drop(columns=["id"])
        # baseline_table = baseline_table.set_index(["source", "source_id"])
        # baseline_table = baseline_table.reset_index()
        # agent_table = agent_table.reset_index()
        # baseline_table.to_csv(f"{output_file_path}/{model_name} - baseline.csv")
        # agent_table.to_csv(f"{output_file_path}/{model_name} - {agent_name}.csv")

        baseline_scores = baseline_table["score"]
        agent_scores = agent_table["score"]
        total_rows = len(baseline_table)
        baseline_sum = baseline_scores.sum()
        agent_sum = agent_scores.sum()
        difference_sum = agent_sum - baseline_sum
        baseline_accuracy = baseline_sum / total_rows
        agent_accuracy = agent_sum / total_rows
        difference_accuracy = agent_accuracy - baseline_accuracy

        # Verify the data
        assert len(baseline_table) == len(agent_table)
        assert baseline_sum <= agent_sum

        # Create a contingency table
        table = np.zeros((2, 2))
        for a, b in zip(baseline_scores, agent_scores):
            table[a, b] += 1
        print(table)

        # Perform a McNemar test
        test_result = mcnemar(table, exact=False)

        print(f"Model: {model_name}, Agent: {agent_name}")
        print(f"Total rows: {len(baseline_table)} | {len(agent_table)}")
        print(f"Scores: {baseline_scores.sum()} | {agent_scores.sum()} -> {difference_sum}")
        print(f"Accuracy: {baseline_accuracy} | {agent_accuracy} -> {difference_accuracy}")
        print(f"McNemar: stat: {test_result.statistic:.3f}, p-value: {test_result.pvalue:.3e}")
        is_significant = test_result.pvalue < 0.05
        p_value_text = f"< 0.001" if is_significant else f"{test_result.pvalue:.3e}"

        results = results._append({
            "Model Name": model_name,
            "Agent Name": agent_name,
            "Num Problems": total_rows,
            "Baseline Score": baseline_sum,
            "Agent Score": agent_sum,
            "Difference Score": difference_sum,
            "Baseline Accuracy": baseline_accuracy,
            "Agent Accuracy": agent_accuracy,
            "Difference Accuracy": difference_accuracy,
            "Test Statistic": test_result.statistic,
            "p-value": f"{test_result.pvalue:.3e}",
            "p-value-text": p_value_text
        }, ignore_index=True)

    baseline_results = baseline_results._append({
        "Model Name": model_name,
        "Accuracy": baseline_accuracy
    }, ignore_index=True)

results.to_csv(f"{output_file_path}/results_by_model_and_agent.csv", index=False)


# Pivot the results so that model is on the rows, agent is on the columns, and accuracy is the value
pivot_results = results.pivot(index="Model Name", columns="Agent Name", values="Agent Accuracy")

# Sort the columns by model name
pivot_results = pivot_results.sort_values(by="Model Name")
baseline_results = baseline_results.sort_values(by="Model Name")

# Append the baseline results as a column
pivot_results["baseline"] = baseline_results.set_index("Model Name")["Accuracy"]

# reorder the columns based on the order found in the agent names list
pivot_results = pivot_results[["baseline"] + agent_names]

# Capitalize the first letter of each column name
pivot_results.columns = [col.capitalize() for col in pivot_results.columns]

# Save the pivot results
pivot_results.to_csv(f"{output_file_path}/pivot_results_by_model_and_agent.csv")

