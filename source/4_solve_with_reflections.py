# Import packages
import os
from datetime import datetime
import pandas as pd
from models.model_factory import ModelFactory
from agents.agent_factory import AgentFactory
from problems.exam_reader import ExamReader
from details.details_reader import DetailsReader
from reflections.reflections_reader import ReflectionReader
from experiments.experiment import Experiment
from experiments.result import Result
from experiments.experiments_file import ExperimentsFile
from details.details_writer import DetailsWriter
from details.details_row import DetailsRow
from dialogs.dialog_writer import DialogWriter
from models.pricing import get_pricing
from logs.log import Log
from logs.log_level import LogLevel

# Set the models
model_names = [
    # "gpt-35-turbo",
    # "gpt-4",
    # "llama-2-7b-chat",
    # "llama-2-70b-chat",
    # "mistral-large",
    # "cohere-command-r-plus",
    # "gemini-1.0-pro",
    # "gemini-1.5-pro-preview-0409",
    # "claude-3-opus-20240229"
]

# Set the agents
baseline_agent_names = [
    "baseline"]

agent_names = [
    "retry",
    # "advice",
    # "instructions",
    # "keywords",
    # "explanation",
    # "solution",
    # "composite",
    # "unredacted"
]

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

# Set attempt id
attempt_id = 2

# Set the logging level
log_level = LogLevel.DEBUG

# Create the components
model_factory = ModelFactory()
agent_factory = AgentFactory()
exam_reader = ExamReader()
details_reader = DetailsReader()
reflection_reader = ReflectionReader()
dialog_writer = DialogWriter()

# Loop through each model
for model_name in model_names:

    # Loop through each agent
    for agent_name in agent_names:

        # Loop through each exam
        for exam_name in exam_names:

            # Set the experiment parameters
            start_time = pd.Timestamp.now()
            experiment = Experiment(model_name, agent_name, exam_name, attempt_id)
            experiment.start(start_time)

            # Set file and folder paths
            exam_path = f"../data/exams/{exam_name}.jsonl"
            previous_details_file_path = f"../data/details/{model_name} - baseline - {exam_name}.csv"
            reflections_folder_path = f"../data/reflections/{model_name} - {agent_name} - {exam_name}"
            dialogs_folder_path = f"../data/dialogs/{experiment.name}"
            details_file_path = f"../data/details/{experiment.name}.csv"
            results_file_path = f"../data/results/results.csv"
            log_name_prefix = start_time.strftime("%Y-%m-%d %H-%M-%S")
            log_folder_path = f"../data/logs/{log_name_prefix} - {experiment.name}"

            # Create the folders
            os.makedirs(dialogs_folder_path, exist_ok=True)
            os.makedirs(os.path.dirname(details_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(results_file_path), exist_ok=True)
            os.makedirs(log_folder_path, exist_ok=True)

            # Create the details table
            details = []

            # Load the exam
            exam = exam_reader.read(exam_path)

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
                log.head(f"Model: {experiment.model_name} | Agent: {experiment.agent_name} | Exam: {experiment.exam_name} | Problem {i + 1} of {len(exam.problems)}")

                # Skip the problem if it was already answered correctly
                if details_reader.is_correct(previous_details_file_path, problem_id):
                    log.info(f"Skipping problem {problem_id} because it was already answered correctly.")
                    log.close()
                    continue

                # Load the reflection
                if agent_name == "retry":
                    reflection = "No reflection information provided."
                else:
                    reflection_file_path = f"{reflections_folder_path}/Problem {problem_id}.txt"
                    reflection = reflection_reader.read(reflection_file_path)

                # Create the details row
                details_row = DetailsRow()
                episode_start_time = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                details_row.create(problem_id, episode_start_time, experiment, problem)

                # Create the agent
                model = model_factory.create(experiment.model_name)
                agent = agent_factory.create(experiment.agent_name, model, problem.topic)

                # Create the dialog
                log.subhead("System:")
                agent.create_dialog()
                log.info(agent.dialog.get_all()[0].content)
                log.subhead("User 1:")
                log.info(agent.dialog.get_all()[1].content)
                log.subhead("Assistant 1:")
                log.info(agent.dialog.get_all()[2].content)

                # Set the problem and reflections
                log.subhead("User 2:")
                agent.set_problem(problem)
                agent.set_reflection(reflection)
                log.info(agent.dialog.get_all()[3].content)

                # Get the agent's answer
                log.subhead("Assistant 2:")
                answer_response = agent.get_answer()
                answer = agent.get_answer_choice(answer_response.text)
                log.info(agent.dialog.get_all()[4].content)

                # Log the agent's answer
                log.subhead("Result:")
                is_correct = answer == problem.answer
                score = 1 if is_correct else 0
                details_row.update_answer(answer_response, answer, score)
                log.info(f"Agent Answer: {answer}")
                log.info(f"Correct Answer: {problem.answer}")
                log.info(f"Score: {score}")

                # Save the dialog
                dialog_file_path = f"{dialogs_folder_path}/Problem {problem_id}.json"
                dialog_writer.write(dialog_file_path, agent.dialog)
                details.append(details_row)

            # End the experiment
            experiment.end(datetime.now())
            details_table = pd.DataFrame(details)
            pricing = get_pricing(model_name)
            results = Result(experiment, details_table, pricing)

            # Record the experiment details
            details_writer = DetailsWriter()
            details_writer.write(details, details_file_path)

            # Record the experiment results
            experiments = ExperimentsFile()
            experiments.load(results_file_path)
            experiments.add_row(experiment, results)
            experiments.save(results_file_path)

            # Log the experiments
            log_file_path = f"{log_folder_path}/Results.txt"
            log = Log(LogLevel.INFO)
            log.open(log_file_path)
            log.head("Results")
            log.object(results)
            log.close()
