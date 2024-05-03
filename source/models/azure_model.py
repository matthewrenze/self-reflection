# Import libraries
import time
import requests
import json
import os
from models.model import Model
from dialogs.dialog import Dialog
from models.response import Response

class AzureModel(Model):

    def __init__(self, name: str):
        super().__init__(name)
        self.api_key = os.getenv(f"{name.upper().replace('-', '_')}_API_KEY")
        self.api_url = os.getenv(f"{name.upper().replace('-', '_')}_URL")

    def get_response(self, dialog: Dialog) -> Response:

        # Create the response
        response = Response()

        messages = []
        for message in dialog.get_all():
            messages.append({
                'role': message.role,
                'content': message.content
            })

        try:

            # Set the API parameters
            url = self.api_url + "/v1/chat/completions"

            # Create the headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "Content-type": "application/json"}

            # Create the body
            body = {
                "messages": messages,
                "temperature": 0.0}

            # Get the API response
            api_response = requests.post(url, headers=headers, json=body)

            # Get the API response body (json)
            api_response_body = api_response.content.decode("utf-8")
            api_response_body = json.loads(api_response_body)

            # Get the response
            response.text = api_response_body["choices"][0]["message"]["content"]

            # Get the tokens
            response.input_tokens = api_response_body["usage"]["prompt_tokens"]
            response.output_tokens = api_response_body["usage"]["completion_tokens"]
            response.total_tokens = response.input_tokens + response.output_tokens

        except Exception as e:

            # Add the error message
            response.has_error = True
            response.text = f"Error: {str(e)}"

        finally:

            return response
