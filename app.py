#The main Streamlit application for the Excel Mock Interviewer.

import streamlit as st
from interviewer import ExcelInterviewer
import config


st.set_page_config(page_title="Excel Mock Interviewer", page_icon="🐦‍🔥")

st.title("🤖 Excel Mock Interviewer")

# --- Session State Initialization ---
if 'stage' not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.interviewer = ExcelInterviewer()
    st.session_state.messages = []
    st.session_state.question_count = 0

# --- Helper Functions ---
def display_chat():
    """Displays the entire chat history."""
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def handle_answer(user_answer):
    """Processes all user answers, conversational or practical."""
    # Add user's answer to chat
    st.session_state.messages.append({"role": "user", "content": user_answer})
    
    # Check if we are in the conversational part of the interview
    if st.session_state.question_count < config.INTERVIEW_LENGTH_CONVERSATIONAL:
        question = st.session_state.last_question
        with st.spinner("Evaluating your answer..."):
            evaluation = st.session_state.interviewer.evaluate_conversational_answer(question, user_answer)
        feedback = f"**Feedback:** {evaluation['feedback']}"
        st.session_state.messages.append({"role": "assistant", "content": feedback})
        st.session_state.question_count += 1
        st.session_state.stage = "asking" 
    
    else:
        with st.spinner("Verifying your answer..."):
            is_correct = st.session_state.interviewer.evaluate_practical_answer(user_answer)
        result_text = "✅ **Result:** Correct! You've successfully completed the task." if is_correct else "❌ **Result:** Incorrect. Let's move on for now."
        st.session_state.messages.append({"role": "assistant", "content": result_text})
        st.session_state.stage = "summary" # Move to summary stage



# Stage 1: Start Button
if st.session_state.stage == "start":
    st.write("Welcome! I will ask you a series of questions. Click 'Start' to begin.")
    if st.button("Start Interview"):
        st.session_state.stage = "asking"
        st.rerun()

# Stage 2: Asking Questions)
if st.session_state.stage == "asking":
    display_chat() # Display existing chat
    with st.spinner("Generating question..."):
        # Ask conversational questions
        if st.session_state.question_count < config.INTERVIEW_LENGTH_CONVERSATIONAL:
            question = st.session_state.interviewer.get_conversational_question()
            st.session_state.last_question = question
            st.session_state.messages.append({"role": "assistant", "content": question})
        # Ask the practical question
        else:
            task = st.session_state.interviewer.get_practical_question()
            st.session_state.last_question = task["question"]
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"{task['question']}\n\n**Here is the link:** {task['sheet_url']}"
            })
   
    st.session_state.stage = "waiting_for_answer"
    st.rerun()

# Stage 3: Waiting for user's answer
if st.session_state.stage == "waiting_for_answer":
    display_chat()
    user_answer = st.chat_input("Your Answer")
    if user_answer:
        handle_answer(user_answer)
        st.rerun()

# Stage 4: Generate and Display Summary
if st.session_state.stage == "summary":
    display_chat()
    with st.spinner("Generating your final summary..."):
        summary = st.session_state.interviewer.get_summary()
    st.session_state.messages.append({"role": "assistant", "content": f"**--- Final Evaluation ---**\n\n{summary}"})
    st.session_state.stage = "complete"
    st.rerun()

# Stage 5: Interview Complete
if st.session_state.stage == "complete":
    display_chat()
    st.success("Interview complete! Thank you.")
    if st.button("Start New Interview"):
        st.session_state.clear()
        st.rerun()