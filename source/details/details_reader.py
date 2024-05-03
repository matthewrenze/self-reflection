import pandas as pd

# NOTE: These methods are inefficient but effective for this experiment
class DetailsReader:

    def is_correct(self, file_path: str, problem_id: int) -> bool:
        details = pd.read_csv(file_path)
        row = details[details["problem_id"] == problem_id].iloc[0]
        is_correct = row["score"] == 1
        return is_correct

    def get_agent_answer(self, file_path: str, problem_id: int) -> str:
        details = pd.read_csv(file_path)
        row = details[details["problem_id"] == problem_id].iloc[0]
        agent_answer = row["agent_answer"]
        return agent_answer

    def has_agent_answer(self, file_path: str, problem_id: int) -> bool:
        agent_answer = self.get_agent_answer(file_path, problem_id)
        if pd.isna(agent_answer):
            return False
        if pd.isnull(agent_answer):
            return False
        if agent_answer is None:
            return False
        if agent_answer == "":
            return False
        return True