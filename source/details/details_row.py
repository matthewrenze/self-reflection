from models.response import Response
from experiments.experiment import Experiment
from problems.problem import Problem

class DetailsRow(dict):

    ID = "id"
    DATE_TIME = "date_time"
    MODEL_NAME = "model_name"
    AGENT_NAME = "agent_name"
    EXAM_NAME = "exam_name"
    SOURCE = "source"
    SOURCE_ID = "source_id"
    PROBLEM_ID = "problem_id"
    ATTEMPT_ID = "attempt_id"
    TOPIC = "topic"
    PROBLEM = "problem"
    CHOICES = "choices"
    SOLUTION = "solution"
    RESPONSE = "response"
    AGENT_ANSWER = "agent_answer"
    CORRECT_ANSWER = "correct_answer"
    SCORE = "score"
    INPUT_TOKENS = "input_tokens"
    OUTPUT_TOKENS = "output_tokens"
    TOTAL_TOKENS = "total_tokens"
    ERROR = "error"

    def __init__(self) -> None:
        super().__init__()
        self[self.ID] = id
        self[self.DATE_TIME] = ""
        self[self.MODEL_NAME] = ""
        self[self.AGENT_NAME] = ""
        self[self.EXAM_NAME] = ""
        self[self.SOURCE] = ""
        self[self.SOURCE_ID] = ""
        self[self.PROBLEM_ID] = ""
        self[self.ATTEMPT_ID] = 0
        self[self.TOPIC] = ""
        self[self.PROBLEM] = ""
        self[self.CHOICES] = ""
        self[self.RESPONSE] = ""
        self[self.SOLUTION] = ""
        self[self.AGENT_ANSWER] = ""
        self[self.CORRECT_ANSWER] = ""
        self[self.SCORE] = 0
        self[self.INPUT_TOKENS] = 0
        self[self.OUTPUT_TOKENS] = 0
        self[self.TOTAL_TOKENS] = 0
        self[self.ERROR] = ""

    def create(self, id: int, date_time: str, experiment: Experiment, problem: Problem) -> None:
        self[self.ID] = id
        self[self.DATE_TIME] = date_time
        self[self.MODEL_NAME] = experiment.model_name
        self[self.AGENT_NAME] = experiment.agent_name
        self[self.EXAM_NAME] = experiment.exam_name
        self[self.SOURCE] = problem.source
        self[self.SOURCE_ID] = problem.source_id
        self[self.PROBLEM_ID] = problem.id
        self[self.ATTEMPT_ID] = experiment.attempt_id
        self[self.TOPIC] = problem.topic
        self[self.PROBLEM] = problem.question + "\n" + str(problem.choices)
        self[self.CHOICES] = problem.choices
        self[self.SOLUTION] = problem.solution
        self[self.CORRECT_ANSWER] = problem.answer

    def update_answer(self, response: Response, answer: str, score: int) -> None:
        self[self.RESPONSE] = response.text
        self[self.AGENT_ANSWER] = answer
        self[self.SCORE] = score
        self[self.INPUT_TOKENS] += response.input_tokens
        self[self.OUTPUT_TOKENS] += response.output_tokens
        self[self.TOTAL_TOKENS] += response.total_tokens
        if response.has_error:
            self[self.ERROR] += response.text + "\n"



