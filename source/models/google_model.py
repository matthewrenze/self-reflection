# Import libraries
import os
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Content, Part
import time
from models.model import Model
from models.response import Response

class GoogleModel(Model):

    def __init__(self, name: str):
        super().__init__(name)
        self.region = os.getenv("GOOGLE_REGION")
        self.project_id = os.getenv("GOOGLE_PROJECT_ID")

    # Define a function to get the experiments from the Open AI API
    def get_response(self, dialog):

        response = Response()

        messages = []
        for i, message in enumerate(dialog.get_all()):
            role = "model" if message.role == "assistant" else "user"
            part = Part.from_text(message.content)
            content = Content(role=role, parts=[part])
            messages.append(content)

            # NOTE: Gemini requires pair-wise prompt and response (i.e. no system prompt).
            if i == 0:
                text = "I understand the instructions. Please proceed."
                parts = [Part.from_text(text)]
                content = Content(role="model", parts=parts)
                messages.append(content)


        old_messages = messages[:-1]
        new_message = messages[-1]

        try:
            vertexai.init(
                project=self.project_id,
                location=self.region)
            config = GenerationConfig(
                temperature=0.0)
            model = GenerativeModel(
                model_name=self.name,
                generation_config=config)
            chat = model.start_chat(
                history=old_messages)

            new_text = new_message.parts[0].text
            api_response = chat.send_message(new_text)

            # Note: Set tokens first in case there is an error below
            response.input_tokens = api_response._raw_response.usage_metadata.prompt_token_count
            response.output_tokens = api_response._raw_response.usage_metadata.candidates_token_count
            response.total_tokens = api_response._raw_response.usage_metadata.total_token_count

            if api_response.candidates[0].finish_reason == "SAFETY":
                raise Exception("Content safety filter was triggered.")

            if api_response.candidates[0].finish_reason == "MAX_TOKENS":
                raise Exception("Maximum response length was exceeded.")

            response.text = api_response.candidates[0].content.parts[0].text
            response.text = response.text.replace("\n\n", "\n")

        except Exception as e:
            response.has_error = True
            response.text = f"Error: {str(e)}"

        finally:
            # NOTE: Gemini Pro 1.5 current has a quota of 5 requests per minute.
            if self.name == "gemini-1.5-pro-preview-0409":
                time.sleep(15)

            return response
