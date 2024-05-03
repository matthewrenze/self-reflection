import re
from agents.agent import Agent
from dialogs.dialog import Dialog
from dialogs.message import Message
from problems.problem import Problem
from models.response import Response

system_prompt = """
You are an expert in {{topic}}.
Your task is to answer the following multiple-choice questions.
Think step-by-step to ensure you have the correct answer.
Then, answer the question using the following format 'Action: Answer("[choice]")'  
The parameter [choice] is the letter or number of the answer you want to select (e.g. "A", "B", "C", or "D")
For example, 'Answer("C")' will select the choice "C" as the best answer.
You MUST select one of the available choices; the answer CANNOT be "None of the Above".
Be concise in your response but include any essential information.
"""

example_problem = """
Topic: Geography
Question: What is the capital of the state where Johns Hopkins University is located?
Choices:
  A: Baltimore
  B: Annapolis
  C: Des Moines
  D: Las Vegas
"""

example_solution = """
Thought: 
Johns Hopkins University is located in Baltimore, Maryland.
The capital of Maryland is Annapolis.
Action: Answer("B")  
"""

# TODO: Should I add the number of times the question was answered incorrectly?
reflection_prefix = """
Reflection:
You previously answered this question incorrectly.
Then you reflected on the problem, your solution, and the correct answer.
Use your self-reflection (below) to help you answer this question.
Any information that you are not allowed to see will be marked [REDACTED].
"""

class AnswerAgent(Agent):

    def __init__(self, model, topic):
        super().__init__(model, topic)

    # TODO: Should I move this into the constructor?
    def create_dialog(self) -> None:
        prompt = system_prompt.replace("{{topic}}", self.topic)
        self.dialog = Dialog()
        self.dialog.append(Message("system", prompt.strip()))
        self.dialog.append(Message("user", example_problem.strip()))
        self.dialog.append(Message("assistant", example_solution.strip()))

    def set_problem(self, problem: Problem) -> None:
        content = str(problem)
        message = Message("user", content)
        self.dialog.append(message)

    def set_reflection(self, reflection: str) -> None:
        message = self.dialog.get_all()[-1]
        problem_content = message.content
        reflection_content = reflection_prefix.strip() + "\n"
        reflection_content += reflection + "\n"
        content = problem_content + reflection_content
        message.content = content

    def get_answer(self) -> Response:
        response = self.model.get_response(self.dialog)
        message = Message("assistant", response.text)
        self.dialog.append(message)
        return response

    def get_answer_choice(self, action: str):
        agent_answer = None
        agent_answer_match = re.search(r'Answer\("([^"]*)"\)', action)
        if agent_answer_match is not None:
            agent_answer = agent_answer_match.group(1)
            agent_answer = agent_answer.strip()
            if agent_answer != "":
                agent_answer = agent_answer[0].upper()
        return agent_answer
