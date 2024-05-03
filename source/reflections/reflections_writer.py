class ReflectionsWriter:

    def write(self, file_path: str, section: str, content: str):
        with open(file_path, "w", encoding="utf-8") as file:
            reflection_content = f"{section}\n"
            reflection_content += content
            file.write(reflection_content)