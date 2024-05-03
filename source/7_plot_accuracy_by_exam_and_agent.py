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

# DEBUG: Filter results
# results = results[results["Model Name"] == "gpt-35-turbo"]
# results = results[results["Exam Name"] == "comprehensive-100"]
results = results[results["Exam Name"] != "comprehensive-100"]

# Process the data
results = shared.add_baseline_results(results)
results = shared.set_model_titles(results)
results = shared.set_agent_titles(results)
results = shared.set_exam_titles(results)
results = shared.sort_by_agent(results)
results = shared.sort_by_model(results)

# Create a custom color palette (swap the last two colors)
palette = sns.color_palette("tab10")
palette[7], palette[8] = palette[8], palette[7]

for model_name in model_names:

    # Create the output folder
    output_folder = f"../data/plots/{model_name}"
    os.makedirs(output_folder, exist_ok=True)

    # Filter the results by model_name
    model_results = results[results["Model Name"] == model_name]

    # Plot the accuracy by agent and exam
    plt.figure(figsize=(10, 5))
    sns.barplot(
        x="Exam Title",
        y="Accuracy",
        hue="Agent Title",
        data=model_results,
        ci=None,
        palette=palette)
    plt.title(f"Accuracy by Exam and Agent for {shared.get_model_title(model_name)}")
    plt.xlabel("Exam")
    plt.ylabel("Accuracy")
    plt.xticks(rotation=15, ha="right")
    plt.ylim(0, 1.1)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/accuracy-by-exam-and-agent.pdf")
    plt.show()

    # Create a table of accuracy by exam and agent
    # Place the agent on the rows and the exam on the columns

    # Create a pivot table
    pivot_table = model_results.pivot_table(
        index="Agent Title",
        columns="Exam Title",
        values="Accuracy",
        aggfunc="mean")

    # Save the table to a CSV file
    pivot_table.to_csv(f"../data/tables/accuracy-by-exam-and-agent-for-{model_name}.csv")

