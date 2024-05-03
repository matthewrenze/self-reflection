import json
from dialogs.message import Message

class Dialog:
    def __init__(self, messages: list[Message] = []):
        self._messages = []

    def append(self, message: Message):
        self._messages.append(message)

    def append_all(self, messages: list[Message]):
        self._messages.extend(messages)

    def get(self, index: int) -> Message:
        return self._messages[index]

    def get_all(self) -> list[Message]:
        return self._messages[:]
