import os

class InstructionsFile:

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def read(self, topic, use_instructions):
        instructions_file_path = f"{self.folder_path}/{topic.lower()}.txt"
        if not use_instructions:
            return None
        if not os.path.exists(instructions_file_path):
            raise FileNotFoundError(f"Instructions file not found: {instructions_file_path}")
        with open(instructions_file_path, "r") as file:
            instructions = file.read()
            return instructions

    def write(self, exam_name, instructions):
        instructions_file_path = f"{self.folder_path}/{exam_name.lower()}.txt"
        with open(instructions_file_path, "w") as file:
            file.write(instructions)
