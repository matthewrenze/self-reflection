from models.model import Model
from models.openai_model import OpenAIModel
from models.azure_model import AzureModel
from models.google_model import GoogleModel
from models.anthropic_model import AnthropicModel

class ModelFactory:

    def create(self, model_name: str) -> Model:
        model_types = {
            "gpt-35-turbo": "openai",
            "gpt-4": "openai",
            "llama-2-7b-chat": "azure",
            "llama-2-70b-chat": "azure",
            "mistral-large": "azure",
            "cohere-command-r-plus": "azure",
            "gemini-1.0-pro": "google",
            "gemini-1.5-pro-preview-0409": "google",
            "claude-3-opus-20240229": "anthropic"
        }

        model_type = model_types[model_name]

        if model_type == "openai":
            return OpenAIModel(model_name)

        elif model_type == "azure":
            return AzureModel(model_name)

        elif model_type == "google":
            return GoogleModel(model_name)

        elif model_type == "anthropic":
            return AnthropicModel(model_name)

        else:
            raise Exception(f"Unknown model type: {model_name}")

