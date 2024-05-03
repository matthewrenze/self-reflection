from models.response import Response

class Agent:

    def __init__(self, model, topic):
        self.model = model
        self.topic = topic
        self.dialog = None
        self.system_prompt_template = ""
        self.example_problem = ""
        self.example_solution = ""
