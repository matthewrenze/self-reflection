from datetime import datetime

class Experiment:

    def __init__(self, model_name, agent_type, exam_name, attempt_id):
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.name = f"{model_name} - {agent_type} - {exam_name}"
        self.model_name = model_name
        self.agent_name = agent_type
        self.exam_name = exam_name
        self.attempt_id = attempt_id

    def start(self, start_time: datetime):
        self.start_time = start_time

    def end(self, end_time: datetime):
        self.end_time = end_time
        self.duration = int((self.end_time - self.start_time).total_seconds())

    def __str__(self):
        text = (
            f"Start Time: {self.start_time}\n"
            f"End Time: {self.end_time}\n"
            f"Duration: {self.duration}\n"
            f"Experiment: {self.name}\n"
            f"Model Name: {self.model_name}\n"
            f"Agent Name: {self.agent_name}\n"
            f"Exam Name: {self.exam_name}\n")

        return text