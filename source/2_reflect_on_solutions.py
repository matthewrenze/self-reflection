# Import packages
import os
import pandas as pd
import openai
from models.model_factory import ModelFactory
from agents.agent_factory import AgentFactory
from problems.exam_reader import ExamReader
from details.details_reader import DetailsReader
from dialogs.dialog_reader import DialogReader
from dialogs.dialog_writer import DialogWriter
from logs.log import Log
from logs.log_level import LogLevel

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

# Set the agent name
agent_name = "reflection"

# Set the exams
exam_names = [
    "comprehensive-100",
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

# Set the attempt id
attempt_id = 1

# Set the logging level
log_level = LogLevel.DEBUG

# Create the components
model_factory = ModelFactory()
agent_factory = AgentFactory()
exam_reader = ExamReader()
details_reader = DetailsReader()
dialog_reader = DialogReader()
dialog_writer = DialogWriter()

# Loop through each model
for model_name in model_names:

    # Loop through each exam
    for exam_name in exam_names:

        # Set file and folder paths
        start_time = pd.Timestamp.now()
        previous_experiment_name = f"{model_name} - baseline - {exam_name}"
        current_reflection_name = f"{model_name} - {agent_name} - {exam_name}"
        exam_file_path = f"../data/exams/{exam_name}.jsonl"
        details_file_path = f"../data/details/{previous_experiment_name}.csv"
        problem_dialogs_folder_path = f"../data/dialogs/{previous_experiment_name}"
        reflection_dialogs_folder_path = f"../data/dialogs/{current_reflection_name}"
        log_name_prefix = start_time.strftime("%Y-%m-%d %H-%M-%S")
        log_folder_path = f"../data/logs/{log_name_prefix} - {current_reflection_name}"

        # Create the folders
        os.makedirs(reflection_dialogs_folder_path, exist_ok=True)
        os.makedirs(log_folder_path, exist_ok=True)

        # Load the exam
        exam = exam_reader.read(exam_file_path)

        # Loop through each exam problem
        for i, problem in enumerate(exam.problems):
            problem_id = i + 1

            # # DEBUG: Answer only the first n problems
            # if i >= 10:
            #      break

            # Create the log file
            log_file_path = f"{log_folder_path}/Problem {problem_id}.txt"
            log = Log(log_level)
            log.open(log_file_path)
            log.head(f"Model: {model_name} | Agent: {agent_name} | Exam: {exam_name} | Problem {problem_id} of {len(exam.problems)}")

            # Skip the problem if it was already answered correctly
            if details_reader.is_correct(details_file_path, problem_id):
                log.info(f"Skipping problem {problem_id} because it was already answered correctly.")
                log.close()
                continue

            # Create the agent
            model = model_factory.create(model_name)
            reflect_agent = agent_factory.create(agent_name, model, problem.topic)

            # Create the new dialog
            reflect_agent.create_dialog()
            log.subhead("System:")
            log.info(reflect_agent.dialog.get_all()[0].content)
            log.subhead("User 1:")
            log.info(reflect_agent.dialog.get_all()[1].content)
            log.subhead("Assistant 1:")
            log.info(reflect_agent.dialog.get_all()[2].content)

            # Load the previous dialog
            reflection_dialog_file_path = f"{problem_dialogs_folder_path}/Problem {problem_id}.json"
            dialog = dialog_reader.read(reflection_dialog_file_path)

            # Create the user prompt
            log.subhead("User 2:")
            problem_text = str(problem)
            solution_text = dialog.get_all()[4].content
            correct_answer = problem.answer
            user_prompt = problem_text + "\n"
            user_prompt += solution_text + "\n"
            user_prompt += "\n --- \n"
            user_prompt += f"Correct Answer: {correct_answer}\n"
            if not details_reader.has_agent_answer(details_file_path, problem_id):
                user_prompt += "Error: You did not provide your answer in the correct format.\n"
                user_prompt += "Your answer must be stated as 'Action: Answer(\"[ANSWER_CHOICE]\")';\n"
                user_prompt += "where [ANSWER_CHOICE] is the letter of the correct answer choice.\n"
            log.info(user_prompt)

            # Get the agent's reflection
            log.subhead("Assistant 2:")
            reflection_response = reflect_agent.reflect(user_prompt)
            log.info(f"Response:\n{reflection_response.text}")

            # Save the dialog
            reflection_dialog_file_path = f"{reflection_dialogs_folder_path}/Problem {problem_id}.json"
            dialog_writer.write(reflection_dialog_file_path, reflect_agent.dialog)
            log.close()
