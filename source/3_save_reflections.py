import os
from datetime import datetime
from logs.log import Log, LogLevel
from problems.exam_reader import ExamReader
from details.details_reader import DetailsReader
from dialogs.dialog_reader import DialogReader
from reflections.reflections_writer import ReflectionsWriter

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

# Set the exam paths
exam_names = {
    "comprehensive-100": "General Knowledge",
    "aqua-rat-100": "Math",
    "logiqa-en-100": "Logic",
    "lsat-ar-100": "Law",
    "lsat-lr-100": "Law",
    "lsat-rc-100": "Law",
    "sat-en-100": "English",
    "sat-math-100": "Math",
    "arc-challenge-100": "Science",
    "hella-swag-100": "General Knowledge",
    "med-mcqa-100": "Medicine"
}

# Set the attempt id
attempt_id = 1

# Set the section headings
section_headings = {
    "Explanation:": "explanation",
    "Error Keywords:": "keywords",
    "Solution:": "solution",
    "Instructions:": "instructions",
    "Advice:": "advice"}

# Set the logging level
log_level = LogLevel.DEBUG

# Create the components
exam_reader = ExamReader()
details_reader = DetailsReader()
dialog_reader = DialogReader()
reflection_writer = ReflectionsWriter()

for model_name in model_names:

    for exam_name_and_topic in exam_names:

        # Get the exam name and topic
        exam_name = exam_name_and_topic
        topic = exam_names[exam_name_and_topic]

        # Set the paths
        exam_file_path = f"../data/exams/{exam_name}.jsonl"
        details_file_path = f"../data/details/{model_name} - baseline - {exam_name}.csv"
        dialogs_folder_path = f"../data/dialogs/{model_name} - reflection - {exam_name}"
        reflections_folder_root = f"../data/reflections"
        file_date_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        log_folder_path = f"../data/logs/{file_date_time} - {model_name} - save_reflections - {exam_name}"
        os.makedirs(log_folder_path, exist_ok=True)

        # Load the exam
        exam = exam_reader.read(exam_file_path)

        # Loop through each exam problem
        for i, problem in enumerate(exam.problems):
            problem_id = i + 1

            # # DEBUG: Only process n problems
            # if i >= 10:
            #     break

            # Create the log file
            log_file_path = f"{log_folder_path}/Problem {problem_id}.txt"
            log = Log(log_level)
            log.open(log_file_path)
            log.head(f"Model: {model_name} | Task: save_reflection | Exam: {exam_name} | Problem {i + 1} of {len(exam.problems)}")

            # Skip the problems if it was already answered correctly
            if details_reader.is_correct(details_file_path, problem_id):
                log.info(f"Skipping problem {problem_id} because it was already answered correctly.")
                log.close()
                continue

            # Load the dialog
            dialog_file_path = f"{dialogs_folder_path}/Problem {problem_id}.json"
            dialog = dialog_reader.read(dialog_file_path)

            # Get the reflection
            log.subhead("Get Reflection:")
            unredacted_message = dialog.get_all()[4].content
            reflection_message = unredacted_message
            log.info(reflection_message)

            # Redact the answer choices and text
            for choice in problem.choices:
                choice_text = problem.choices[choice]
                reflection_message = reflection_message.replace(choice + " ", "[REDACTED] ")
                reflection_message = reflection_message.replace(choice + "\"", "[REDACTED]\"")
                reflection_message = reflection_message.replace(choice + ".", "[REDACTED].")
                reflection_message = reflection_message.replace(choice + ",", "[REDACTED],")
                reflection_message = reflection_message.replace(choice + ":", "[REDACTED]:")
                reflection_message = reflection_message.replace(choice + ";", "[REDACTED];")
                reflection_message = reflection_message.replace(choice_text, "[REDACTED]")

            # Get the reflection types
            log.subhead("Parse Reflections:")
            section_contents = {heading: "" for heading in section_headings}
            current_section = None
            lines = reflection_message.split("\n")
            for line in lines:
                trimmed_line = line.strip()
                if trimmed_line in section_headings:
                    current_section = trimmed_line
                elif current_section:
                    section_contents[current_section] += line + "\n"

            # Save the reflections
            log.subhead("Save Reflections:")
            for section in section_contents:
                reflection_name = section_headings[section]
                reflection_file_name = f"Problem {problem_id}.txt"
                reflections_folder_name = f"{model_name} - {reflection_name} - {exam_name}"
                reflections_folder_path = f"{reflections_folder_root}/{reflections_folder_name}"
                reflection_file_path = f"{reflections_folder_path}/{reflection_file_name}"
                os.makedirs(reflections_folder_path, exist_ok=True)
                log.info(f"Saving {reflection_name} reflection")
                content = section_contents[section]
                reflection_writer.write(reflection_file_path, section, content)

            # Save the composite reflection
            log.info("Saving composite reflection")
            composite_reflection = ""
            for section in section_contents:
                composite_reflection += f"{section}\n{section_contents[section]}"
            reflection_file_name = f"Problem {problem_id}.txt"
            reflections_folder_name = f"{model_name} - composite - {exam_name}"
            reflections_folder_path = f"{reflections_folder_root}/{reflections_folder_name}"
            reflection_file_path = f"{reflections_folder_path}/{reflection_file_name}"
            os.makedirs(reflections_folder_path, exist_ok=True)
            with open(reflection_file_path, "w", encoding="utf-8") as file:
                file.write(composite_reflection)

            # Save the composite reflection
            log.info("Saving unredacted reflection")
            reflection_file_name = f"Problem {problem_id}.txt"
            reflections_folder_name = f"{model_name} - unredacted - {exam_name}"
            reflections_folder_path = f"{reflections_folder_root}/{reflections_folder_name}"
            reflection_file_path = f"{reflections_folder_path}/{reflection_file_name}"
            os.makedirs(reflections_folder_path, exist_ok=True)
            with open(reflection_file_path, "w", encoding="utf-8") as file:
                file.write(unredacted_message)

            log.close()
