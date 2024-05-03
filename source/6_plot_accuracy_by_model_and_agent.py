# Import the packages
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shared
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Set the parameters
model_name = "gpt-4"
# model_name = "gpt-35-turbo"
# model_name = "llama-2-7b-chat"
# model_name = "llama-2-70b-chat"
# model_name = "mistral-large"
# model_name = "cohere-command-r-plus"
agent_name = None
exam_name = None
input_file = f"../data/results/results.csv"
output_folder = f"../data/plots"

# Create the output folder
os.makedirs(output_folder, exist_ok=True)

# Load the data
results = pd.read_csv(input_file)

# DEBUG: Filter the results
# results = results[results["Exam Name"] == "comprehensive-100"]
results = results[results["Exam Name"] != "comprehensive-100"]

# Process the results
results = shared.add_baseline_results(results)
results = shared.set_model_titles(results)
results = shared.set_agent_titles(results)
results = shared.sort_by_agent(results)
results = shared.sort_by_model(results)

# Create a custom color palette (swap the last two colors)
palette = sns.color_palette("tab10")
palette[7], palette[8] = palette[8], palette[7]

# Plot the accuracy by model and agent
plt.figure(figsize=(10, 5))
sns.barplot(
    x="Model Title",
    y="Accuracy",
    hue="Agent Title",
    data=results,
    ci=None,
    palette=palette)
plt.title("Accuracy by Model and Agent")
plt.xlabel("Model")
plt.ylabel("Accuracy")
plt.ylim(0.0, 1.0)
plt.xticks(rotation=15)
plt.subplots_adjust(bottom=0.2)
plt.legend(title="Agent", loc="lower right")
plt.tight_layout()
plt.savefig(f"{output_folder}/accuracy-by-model-and-agent.pdf")
plt.show()

# Plot the improvement by model and agent
plt.figure(figsize=(10, 5))
sns.barplot(
    x="Model Title",
    y="Improvement",
    hue="Agent Title",
    data=results,
    ci=None,
    palette=palette)
plt.title("Improvement by Model and Agent")
plt.xlabel("Model")
plt.ylabel("Improvement (%)")
plt.ylim(0, 100)
plt.xticks(rotation=15)
plt.subplots_adjust(bottom=0.2)
plt.legend(title="Agent", loc="upper right")
plt.tight_layout()
plt.savefig(f"{output_folder}/improvement-by-model-and-agent.pdf")
plt.show()