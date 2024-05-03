# Import libraries
from logs.log_level import LogLevel
from colorama import init

# Initialize colorama for automatic style reset
init(autoreset=True)

# Define the ANSI colors
BOLD_WHITE = "\033[97m"
BOLD_YELLOW = "\033[93;1m"
BOLD_RED = "\033[91;1m"
WHITE = "\033[38;5;250m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# TESTING
ORANGE = "\033[38;5;208m"
BOLD_ORANGE = "\033[38;5;208;1m"
GREY = "\033[38;5;240m"
BOLD_GREY = "\033[38;5;245;1m"

# Define the keywords to bold
keywords = [
    "Task:",
    "Topic:",
    "Question:",
    "Choices:",
    "Response:",
    "Thought:",
    "Action:",
    "Agent Answer:",
    "Correct Answer:",
    "Score:",
    "Similarity:",
    "Reflection:",
    "Advice:",
    "Error Keywords:",
    "Explanation:",
    "Instructions:",
    "Solution:",
    "Composite",
    "Tokens:",
    "### Results ###",]

class Log:

    def __init__(self, log_level: LogLevel):
        self.log_level = log_level
        self.log_file = None

    def open(self, log_file_path: str) -> None:
        self.log_file = open(log_file_path, "w", encoding="utf8")

    def _format(self, message):
        if message.startswith("##"):
            return f"\n{BOLD_WHITE}{message}{RESET}"

        if message.startswith("#"):
            return f"{BOLD_WHITE}{message}{RESET}"

        if message.startswith("Debug:"):
            return f"{BOLD_GREY}Debug:{GREY}{message[len('Debug:'):]}{RESET}"

        if message.startswith("Warning:"):
            return f"{BOLD_ORANGE}Warning:{BOLD_ORANGE}{message[len('Warning:'):]}{RESET}"

        if message.startswith("Error:"):
            return f"{BOLD_RED}Error:{RED}{message[len('Error:'):]}{RESET}"

        for keyword in keywords:
            if message.startswith(keyword) \
                    or "\n" + keyword in message:
                message = message.replace(keyword, f"{BOLD_WHITE}{keyword}{RESET}")

        return f"{message}{RESET}"

    def _print(self, message):
        print(message)

    def _log(self, message):
        message = message.rstrip('\n')
        self.log_file.write(message + '\n')
        message = self._format(message)
        self._print(message)

    def head(self, message):
        message = "# " + message
        self._log(message)

    def subhead(self, message):
        message = "## " + message
        self._log(message)

    def debug(self, message):
        if self.log_level.value > LogLevel.DEBUG.value:
            return

        if not message.startswith("Debug:"):
            message = "Debug: " + message
        self._log(message)

    def info(self, message):
        if self.log_level.value > LogLevel.INFO.value:
            return

        self._log(message)

    def object(self, obj):
        if self.log_level.value > LogLevel.INFO.value:
            return

        self._log(str(obj))

    def warning(self, message):
        if self.log_level.value > LogLevel.WARNING.value:
            return

        if not message.startswith("Warning:"):
            message = "Warning: " + message
        self._log(message)

    def error(self, message):
        if self.log_level.value > LogLevel.ERROR.value:
            return

        if not message.startswith("Error:"):
            message = "Error: " + message
        self._log(message)

    def close(self):
        self._log("\n")
        self.log_file.flush()
        self.log_file.close()


