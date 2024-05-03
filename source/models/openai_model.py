# Import libraries
import os
from openai import AzureOpenAI
import time
from models.model import Model
from models.response import Response

class OpenAIModel(Model):

    def __init__(self, name: str):
        super().__init__(name)
        self.api_base = os.getenv("AZURE_OPENAI_URL")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = "2024-02-01"
        self.model_name = name + "-self-reflection"

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

        try:

            client = AzureOpenAI(
                azure_endpoint=self.api_base,
                api_key=self.api_key,
                api_version=self.api_version)

            # NOTE: Need to use "model" for Open AI and "engine" for Azure AI
            api_response = client.chat.completions.create(
                model=self.model_name,
                # engine=self.model_model,
                messages=messages,
                temperature=0.0)

            # Note: Set tokens first in case there is an error below
            response.input_tokens = api_response.usage.prompt_tokens
            response.output_tokens = api_response.usage.completion_tokens
            response.total_tokens = api_response.usage.total_tokens

            if api_response.choices[0].finish_reason == "content_filter":
                raise Exception("Content filter was triggered.")

            if api_response.choices[0].finish_reason == "length":
                raise Exception("Maximum response length was exceeded.")

            response.text = api_response.choices[0].message.content
            response.text = response.text.replace("\n\n", "\n")

        except Exception as e:
            response.has_error = True
            response.text = f"Error: {str(e)}"

        finally:
            if self.name == 'gpt-4' \
                    or self.name == 'gpt-4-turbo':
                time.sleep(1)

            return response
