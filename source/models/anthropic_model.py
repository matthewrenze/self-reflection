# Import libraries
import os
import anthropic
import time
from models.model import Model
from models.response import Response

class AnthropicModel(Model):

    def __init__(self, name: str):
        super().__init__(name)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    # Define a function to get the experiments from the Open AI API
    def get_response(self, dialog):

        response = Response()

        # TODO: Should this be moved into the Dialog class?
        messages = []
        for message in dialog.get_all():
            messages.append({
                'role': message.role,
                'content': message.content
            })

        # Pop the system prompt
        system_message = messages.pop(0)

        try:

            client = anthropic.Anthropic(
                api_key=self.api_key)

            api_response = client.messages.create(
                model=self.name,
                max_tokens=4000,
                temperature=0.0,
                system=system_message["content"],
                messages=messages)

            # Note: Set tokens first in case there is an error below
            response.input_tokens = api_response.usage.input_tokens
            response.output_tokens = api_response.usage.output_tokens
            response.total_tokens = response.input_tokens + response.output_tokens

            if api_response.stop_reason == "max_tokens":
                raise Exception("Maximum response length was exceeded.")

            response.text = api_response.content[0].text
            response.text = response.text.replace("\n\n", "\n")

        except Exception as e:
            response.has_error = True
            response.text = f"Error: {str(e)}"

        finally:

            return response
