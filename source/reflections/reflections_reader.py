# TODO: This needs to be refactored to read multiple reflections
class ReflectionReader:
    def read(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()