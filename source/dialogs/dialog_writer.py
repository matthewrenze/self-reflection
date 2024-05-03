import json
from dialogs.dialog import Dialog

class DialogWriter:

    def write(self, file_path: str, dialog: Dialog) -> None:
        pretty_json = self._format(dialog)
        self._write_to_file(file_path, pretty_json)

    def _format(self, dialog: Dialog) -> str:
        ordered_messages = [{
            "role": message.role,
            "content": message.content}
            for message in dialog.get_all()]
        return json.dumps(ordered_messages, indent=4, ensure_ascii=False)

    def _write_to_file(self, file_path: str, pretty_json: str) -> None:
        with open(file_path, "w", encoding="utf8") as output_file:
            output_file.write(pretty_json)
