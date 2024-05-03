# Import the packages
import os
import re
import pandas as pd

# Set the parameters
input_folder = f"../details"
output_folder = f"../details"

# Create a table for the details
details = pd.DataFrame()

# Get the files recursively
file_paths = []
for root, dirs, file_names in os.walk(input_folder):

    # Skip the "_archive" folder
    if "_archive" in root:
        continue

    # Loop through each file
    for file_name in file_names:

        # Skip the all-details file
        if file_name == "all-details.csv":
            continue

        # Get the file name
        file_path = f"{root}/{file_name}"
        file_path = file_path.replace("\\", "/")
        file_paths.append(file_path)

# Include only csv files
file_paths = [file for file in file_paths if file.endswith(".csv")]

# Loop through each file
for file_path in file_paths:

        # Load the file
        details_file = pd.read_csv(file_path)

        # Add the file to the table
        details = pd.concat([details, details_file])

# Rename "gpt-35-turbo" to "gpt-3.5"
details["Model"] = details["Model"].str.replace("gpt-35-turbo", "gpt-3.5")

# Rename prompts
details["Prompt"] = details["Prompt"].str.replace("baseline", "Answer Only")
details["Prompt"] = details["Prompt"].str.replace("concise", "Concise CoT")
details["Prompt"] = details["Prompt"].str.replace("chain_of_thought", "Verbose CoT")
details["Prompt"] = details["Prompt"].str.replace("composite", "Composite")

# Create Accuracy column
details["Accuracy"] = details.apply(
    lambda row: sum([row[f"Answer {i}"] == row["Correct Answer"] for i in range(1, 11)]) / 10,
    axis=1)

# Save the details to a csv file
details.to_csv(f"{output_folder}/all-details.csv", index=False)