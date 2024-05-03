from problems.choices import Choices

class Problem:
    def __init__(self, json):
        self.id = json["id"]
        self.source = json["source"]
        self.source_id = json["source_id"]
        self.topic = json["topic"]
        self.subtopic = json["subtopic"]
        self.context = json["context"]
        self.question = json["question"]
        self.choices = Choices(json["choices"])
        self.answer = json["answer"]
        self.solution = json["solution"]

    def __str__(self) -> str:
        problem_text = ""
        if self.topic is not None \
                and self.topic != "":
            problem_text += f"Topic: {self.topic}\n"
        if self.subtopic is not None \
                and self.subtopic != "":
            problem_text += f"Subtopic: {self.subtopic}\n"
        if self.context is not None \
                and self.context != "":
            problem_text += f"Context: {self.context}\n"
        problem_text += f"Question: {self.question}\n"
        problem_text += str(self.choices)

        return problem_text
