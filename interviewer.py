# interviewer.py
"""
Contains the core ExcelInterviewer class that manages interview state and logic.
UPDATED with a retry loop to ensure unique questions.
"""
import json
from llm_service import call_llm
from g_sheets_service import check_practical_task
import prompts
import config

class ExcelInterviewer:
    def __init__(self):
        self.asked_questions = []
        self.history = []

    def get_conversational_question(self):
        """
        Gets a unique conversational question from the LLM.
        It will retry up to 3 times if a duplicate question is generated.
        """
        max_retries = 3
        for attempt in range(max_retries):
            # Generate a question using the list of already asked questions as context
            question = call_llm(
                prompts.PROMPT_GENERATE_QUESTION,
                {"asked_questions": self.asked_questions}
            )
            
            # If the question is new, add it to our list and return it
            if question not in self.asked_questions:
                self.asked_questions.append(question)
                return question
            
            # If the question was a duplicate, print a message and the loop will run again
            print("[AI generated a repeated question. Retrying for a unique one...]")
        
        # If the loop finishes after 3 failed attempts, use a fallback question
        print("[AI failed to generate a unique question. Using a fallback.]")
        fallback_question = "What is the purpose of the IFERROR function in Excel?"
        self.asked_questions.append(fallback_question)
        return fallback_question


    def evaluate_conversational_answer(self, question, answer):
        """Evaluates a text-based answer using the LLM."""
        evaluation_str = call_llm(
            prompts.PROMPT_EVALUATE_ANSWER,
            {"question": question, "answer": answer}
        )
        evaluation = json.loads(evaluation_str)
        self.history.append({"question": question, "answer": answer, "evaluation": evaluation})
        return evaluation

    def get_practical_question(self):
        """Returns the details for the practical task."""
        return config.PRACTICAL_TASK

    def evaluate_practical_answer(self, user_answer):
        """Verifies the practical task answer."""
        task = config.PRACTICAL_TASK
        is_correct = check_practical_task(task["sheet_url"], user_answer, task["expected_answer"])
        self.history.append({"question": task["question"], "answer": user_answer, "evaluation": {"correct": is_correct}})
        return is_correct

    def get_summary(self):
        """Generates a final summary of the interview."""
        summary = call_llm(prompts.PROMPT_SUMMARY, {"history": self.history})
        return summary