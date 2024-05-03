import json
from problems.exam import Exam
from problems.problem import Problem

class ExamReader:

    def read(self, file_path: str) -> Exam:
        exam = Exam()
        with open(file_path, "r", encoding="utf8") as input_file:
            for line in input_file:
                problem_json = json.loads(line.strip())
                exam.problems.append(Problem(problem_json))
        return exam