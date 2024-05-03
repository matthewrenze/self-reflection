from agents.agent import Agent
from dialogs.dialog import Dialog
from dialogs.message import Message
from models.response import Response

# TODO: I need to add an section for error keywords to the reflection agent
# TODO: I might need to refactor the explanation section to be more generic
system_prompt = """
You are an expert in {{topic}}.
You have incorrectly answered the following multiple-choice question.
Your task is to reflect on the problem, your solution, and the correct answer.
You will then use this information help you answer the same question in the future.
First, explain why you answered the question incorrectly.
Second, list the keywords that describe the type of your errors from most general to most specific. 
Third, solve the problem again, step-by-step, based on your knowledge of the correct answer.
Fourth, create a list of detailed instructions to help you correctly solve this problem in the future.
Finally, create a list of general advice to help you solve similar types of problems in the future.  
Be concise in your response; however, capture all of the essential information.  
For guidance, I will provide you with a single generic example problem and reflection (below).
"""

example_input = """
Topic: Geography and Math
Question: What is the product of the number of letters contained in the name of the city where Iowa State University is located multiplied by the number of letters contained in the name of the state?
Choices:
    A: 16
    B: 20
    C: 24
    D: 32
Thought:
Iowa State University is located in the city of Ames
ISU is located in the state of Iowa.
Action: Answer("D")
---
Correct Answer: A
"""

example_output = """
Explanation:
I miscalculated the product of the number of letters in the city and state names. 
The gap in my knowledge was not in geography but in basic arithmetic. 
I knew the correct city and state but made a calculation error.
Error Keywords:
 - Calculation error
 - Arithmetic error
 - Multiplication error
Solution:
Iowa State University is located in the city of Ames
Iowa State University is located in the state of Iowa.
The city name "Ames" contains 4 letters.
The state name "Iowa" contains 4 letters.
The product of 4*4 is 16.
Instructions:
1. Identify the city where the university is located.
2. Identify the state where the university is located.
3. Count the number of letters in the name of the city.
4. Count the number of letters in the name of the state.
5. Multiply the number of letters in the city by the number of letters in the state.
6. Work step-by-step through your mathematical calculations.
7. Double-check your calculations to ensure accuracy.
8. Choose the answer that matches your calculated result.
Advice:
 - Always read the question carefully and understand the problem.
 - Always decompose complex problems into multiple simple steps.
 - Always think through each subproblem step-by-step.
 - Never skip any steps; be explicit in each step of your reasoning.
 - Always double-check your calculations and final answer.
 - Remember that the product of two numbers is the result of multiplying them together, not adding them.
"""

class ReflectionAgent(Agent):

    def __init__(self, model, topic):
        super().__init__(model, topic)

    # TODO: Should I move this into the constructor?
    # NOTE: If so, I need to create an "add_content" method
    def create_dialog(self) -> None:
        prompt = system_prompt.replace("{{topic}}", self.topic)
        self.dialog = Dialog()
        self.dialog.append(Message("system", prompt.strip()))
        self.dialog.append(Message("user", example_input.strip()))
        self.dialog.append(Message("assistant", example_output.strip()))

    def reflect(self, prompt) -> Response:
        # TODO: Should I add the correct solution to the reflect prompt?
        prompt = prompt.strip()
        message = Message("user", prompt)
        self.dialog.append(message)

        response = self.model.get_response(self.dialog)

        message = Message("assistant", response.text)
        self.dialog.append(message)

        return response



