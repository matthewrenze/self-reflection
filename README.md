# Self-Reflection in LLM Agents: Effects on Problem-Solving Performance

## Abstract
In this study, we investigated the effects of self-reflection in large language models (LLMs) on problem-solving performance. We instructed nine popular LLMs to answer a series of multiple-choice questions to provide a performance baseline. Then, for each incorrectly answered question, we instructed eight types of self-reflecting LLM agents to reflect on their mistakes and provide themselves with guidance to improve problem-solving. Then, using this guidance, each self-reflecting agent attempted to re-answer the same questions again. Our results indicate that LLM agents are able to significantly improve their problem-solving performance through self-reflection. In addition, we compared the various types of self-reflection to determine their individual contribution to performance. 

## Documents
 - [Research paper](https://arxiv.org/abs/2405.06682)
 - [Presentation video](https://youtu.be/VvhpKAXe_Mc)
 - [Presentation slides](https://matthewrenze.com/wp-content/uploads/presentations/self-reflection.pdf)
 - [Research homepage](https://matthewrenze.com/research/self-reflection-in-llm-agents/)

## Code
1. [Solve with Baseline](source/1_solve_with_baseline.py) - answers all questions using the baseline agent
2. [Reflect on Solution](source/2_reflect_on_solutions.py) - self-reflects on incorrectly answered problems given the correct answer
3. [Save Reflections](source/3_save_reflections.py) - separates reflections by type, redacts answers, and saves reflection text
4. [Solve with Reflection](source/4_solve_with_reflections.py) - re-answers all incorrectly answered questions using the reflections
5. [Plot Accuracy](source/5_plot_accuracy.py) - plots the accuracy for each agent
6. [Plot Accuracy by Model and Agent](source/6_plot_accuracy_by_model_and_agent.py) - plots the accuracy by model and agent
7. [Plot Accuracy by Exam and Agent](source/7_plot_accuracy_by_exam_and_agent.py) - plots the accuracy for each model by exam and agent
8. [Analyze Details](source/8_analyze_details.py) - performs the McNemar test and creates a table of the results
9. [Analyze Keywords](source/9_analyze_keywords.py) - analyzes the error keywords produced by the self-reflections

## Data
 - [Details](data/details/) - the low-level level details for each question answered in CSV format
 - [Dialogs](data/dialogs/) - the dialog for each question answered in JSON format
 - [Exams](data/exams/) - the exams containing MCQA problems in JSONL format
 - [Logs](data/logs/) - the log files for each question answered and self-reflection in plain-text format
 - [Plots](data/plots/) - the data visualizations of the results in PDF format
 - [Reflections](data/reflections/) - the text generated during the self-reflections process stored as plain text files
 - [Results](data/results/) - the results from the experiment in CSV format
 - [Tables](data/tables/) - the tabular results of the analysis stored as CSV files

