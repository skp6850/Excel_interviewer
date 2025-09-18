import streamlit as st
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import time


try:
    # Use Streamlit's secrets when deployed
    api_key = st.secrets["GEMINI_API_KEY"]
    print("[Attempting to configure Gemini API via Streamlit Secrets...]")
except:
    # Fallback to .env for local development
    print("[Streamlit secrets not found. Falling back to .env file...]")
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

try:
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file or Streamlit Secrets.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print("[Gemini API configured successfully!]")
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")
    model = None



def call_llm(prompt_template, variables={}):
    """
    Calls the Gemini model with a formatted prompt.
    """
    if not model:
        return "Error: Gemini model is not initialized. Check your API key."

    # Format the final prompt with the provided variables
    final_prompt = prompt_template.format(**variables)

    try:
        print("\n[Calling Gemini API...]")
        response = model.generate_content(final_prompt)
        
        # Clean up the response text, as Gemini can sometimes wrap it in markdown
        cleaned_text = response.text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:-3].strip()
        elif cleaned_text.startswith("`"):
             cleaned_text = cleaned_text.strip("`")
             
        time.sleep(1)
        return cleaned_text

    except Exception as e:
        print(f"[An error occurred with the Gemini API call: {e}]")
        # Provide a fallback error message
        if "evaluate" in prompt_template.lower():
             # Return a valid JSON structure on error to prevent crashes
            return json.dumps({
                "correctness": 1, "clarity": 1, "completeness": 1,
                "feedback": "An API error occurred during evaluation."
            })
        else:
            return "Sorry, an error occurred while generating the next question."