# main.py
"""
The main entry point for the Excel Mock Interviewer application.
UPDATED to save a transcript of each interview to a .txt file.
"""
from interviewer import ExcelInterviewer
import config
import datetime # Import the datetime library

def main():
    """Runs the full interview process from start to finish."""
    print("--- Welcome to your Automated Excel Mock Interview ---")
    print("I will ask you a few questions to assess your skills.")
    
    agent = ExcelInterviewer()

    # --- Part 1: Conversational Questions ---
    for i in range(config.INTERVIEW_LENGTH_CONVERSATIONAL):
        print(f"\n--- Conversational Question {i+1} ---")
        question = agent.get_conversational_question()
        print(f"\nInterviewer: {question}")
        
        answer = input("Your Answer: ")
        
        evaluation = agent.evaluate_conversational_answer(question, answer)
        print(f"\n[Feedback: {evaluation['feedback']}]")

    # --- Part 2: Practical Task ---
    print("\n--- Practical Task ---")
    task = agent.get_practical_question()
    print(f"\nInterviewer: {task['question']}")
    print(f"Here is the link: {task['sheet_url']}")
    
    practical_answer = input("Your Answer (the final value): ")
    
    is_correct = agent.evaluate_practical_answer(practical_answer)
    if is_correct:
        print("[Result: Correct! You have successfully completed the task.]")
    else:
        print("[Result: Incorrect. Let's move on for now.]")

    # --- Part 3: Final Summary ---
    print("\n--- Interview Complete ---")
    print("Generating your final performance summary...")
    
    summary = agent.get_summary()
    print("\n--- Final Evaluation ---")
    print(summary)
    
    # --- NEW: Part 4: Save Transcript ---
    print("\n--- Saving Transcript ---")
    try:
        # Create a unique filename with a timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"transcripts/transcript_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("--- Excel Mock Interview Transcript ---\n")
            f.write(f"Date and Time: {timestamp}\n\n")
            
            # Write each Q&A from the history
            for entry in agent.history:
                f.write(f"Interviewer: {entry['question']}\n")
                f.write(f"Candidate: {entry['answer']}\n")
                
                # Format the evaluation nicely
                if "feedback" in entry['evaluation']:
                    feedback = entry['evaluation']['feedback']
                    f.write(f"[Feedback]: {feedback}\n\n")
                elif "correct" in entry['evaluation']:
                    result = "Correct" if entry['evaluation']['correct'] else "Incorrect"
                    f.write(f"[Result]: {result}\n\n")
            
            # Write the final summary
            f.write("--- Final Evaluation ---\n")
            f.write(summary)
        
        print(f"Transcript saved successfully to: {filename}")
        
    except Exception as e:
        print(f"An error occurred while saving the transcript: {e}")


if __name__ == "__main__":
    main()