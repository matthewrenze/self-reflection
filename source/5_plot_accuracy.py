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

# DEBUG: Filter the results
# results = results[results["Model Name"] == "gpt-35-turbo"]
# results = results[results["Exam Name"] == "comprehensive-100"]
results = results[results["Exam Name"] != "comprehensive-100"]

retry_results = results[results["Agent Name"] == "retry"]

# Summarize the metrics
summary = results.groupby(["Model Name", "Agent Name"]).agg({
    "Questions": "sum",
    "Correct": "sum",
    "Incorrect": "sum",
    "Num Errors": "sum",
    "Accuracy": "mean"}) \
    .reset_index()

# Process the data
summary = shared.add_baseline_results(summary)
summary = shared.set_agent_titles(summary)
summary = shared.sort_by_agent(summary)

for model_name in model_names:

    output_folder = f"../data/plots/{model_name}"
    os.makedirs(output_folder, exist_ok=True)

    model_summary = summary[summary["Model Name"] == model_name]

    # Plot the accuracy by agent type (bar plot)
    plt.figure(figsize=(10, 5))
    barplot = sns.barplot(
        x="Agent Title",
        y="Accuracy",
        data=model_summary,
        color=sns.color_palette()[0])
    plt.title(f"Accuracy by Agent for {shared.get_model_title(model_name)}")
    plt.xlabel("Agent")
    plt.ylabel("Accuracy")
    plt.xticks(rotation=15, ha="right")
    plt.ylim(0.0, 1.1)
    for p in barplot.patches:
        barplot.annotate(
            format(p.get_height(), '.2f'),
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center',
            va='center',
            xytext=(0, 7),
            textcoords='offset points')
    plt.tight_layout()
    plt.savefig(f"{output_folder}/accuracy-by-agent.pdf")
    plt.show()

    # Plot the improvement by agent type (bar plot)
    plt.figure(figsize=(10, 5))
    barplot = sns.barplot(
        x="Agent Title",
        y="Improvement",
        data=model_summary,
        color=sns.color_palette()[0])
    plt.title(f"Improvement by Agent for {shared.get_model_title(model_name)}")
    plt.xlabel("Agent")
    plt.ylabel("Improvement (%)")
    plt.xticks(rotation=15, ha="right")
    plt.ylim(0, 100)
    for p in barplot.patches:
        barplot.annotate(
            format(p.get_height(), '.2f'),
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center',
            va='center',
            xytext=(0, 7),
            textcoords='offset points')
    plt.tight_layout()
    plt.savefig(f"{output_folder}/improvement-by-agent.pdf")
    plt.show()
