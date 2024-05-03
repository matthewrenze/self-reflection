import json
from dialogs.dialog import Dialog
from dialogs.message import Message

class DialogReader:
    def read(self, file_path: str) -> Dialog:
        with open(file_path, "r", encoding="utf8") as input_file:
            messages_json = json.load(input_file)
            dialog = Dialog()
            for message_json in messages_json:
                message = Message(message_json["role"], message_json["content"])
                dialog.append(message)
        return dialog



