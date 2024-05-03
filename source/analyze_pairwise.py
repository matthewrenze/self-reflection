# Import the packages
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore', category=pd.errors.ParserWarning)

# Set the parameters
model_type = "gpt-4"
agent_name = None
exam_set = "test"
exam_name = None
input_folder = f"../data/details"
output_folder = f"../data/plots"

# Create the output folder
os.makedirs(output_folder, exist_ok=True)

# Load the data
details = pd.DataFrame()
for file in os.listdir(input_folder):
    input_file = os.path.join(input_folder, file)
    file_details = pd.read_csv(input_file, index_col=False)
    details = pd.concat([details, file_details])

# Filter the details
if model_type is not None:
    details = details[details["model"] == model_type]
if agent_name is not None:
    details = details[details["agent"] == agent_name]
if exam_set is not None:
    details = details[details["set"] == exam_set]
if exam_name is not None:
    details = details[details["exam"] == exam_name]

# Filter out the comprehensive-100 exam
# details = details[details["exam"] != "comprehensive-100"]
details = details[details["exam"] == "comprehensive-100"]

# Sort the data by agent
details["agent"] = pd.Categorical(details["agent"], ["baseline", "composite"])

# Group the data by model, set, exam, and problem_id
details = details.groupby(["model", "set", "exam", "problem_id"]).agg({
    "score": "sum",
    "agent": "first",
    "reflection_1_score": "max"
}).reset_index()

# Get the rows where score is 1
correct = details[details["score"] == 0]
incorrect = details[details["score"] == 1]

# Sort by model, set, exam, problem_id, and score
incorrect = incorrect.sort_values(by=["model", "set", "exam", "problem_id", "score"])

#Get the average top reflection scores by exam
correct_avg = correct.groupby(["model", "set", "exam"]).agg({
    "reflection_1_score": "mean"
}).reset_index()
incorrect_avg = incorrect.groupby(["model", "set", "exam"]).agg({
    "reflection_1_score": "mean"
}).reset_index()