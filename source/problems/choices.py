class Choices(dict):

    def __init__(self, json):
        super().__init__(json)

    def __str__(self) -> str:
        problem_text = ""
        if len(self) == 0:
            return problem_text

        problem_text += f"Choices:\n"
        for choice in self:
           problem_text += f"  {choice}: {self[choice]}\n"

        return problem_text