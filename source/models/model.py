from models.response import Response
from dialogs.dialog import Dialog

class Model:
    def __init__(self, name: str):
        self.name = name

    def get_response(self, dialog: Dialog) -> Response:
        raise NotImplementedError("Subclasses must implement this method")
