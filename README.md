# Excel_interviewer
Small LLM Powered Project


A proof-of-concept AI-powered agent that conducts a mock technical interview to assess a user's skills in Microsoft Excel. This application is built with Python, Google's Gemini API, and Streamlit.

**Status:** Proof-of-Concept

[Live App on Streamlit Community Cloud](https://excelinterviewer-2025.streamlit.app/)

-----

### Key Features ✨

  * **Dynamic Question Generation:** Uses the Gemini API to generate unique, foundational Excel questions on-the-fly.
  * **Intelligent Answer Evaluation:** The AI evaluates user responses for correctness, clarity, and completeness, providing instant, constructive feedback.
  * **Hybrid Assessment Model:** Tests both theoretical knowledge through conversational questions and practical skills via a hands-on task.
  * **Practical Task Verification:** Asks the user to perform a task in a public Google Sheet and programmatically verifies the result.
  * **Final Performance Summary:** Provides a concise summary of the candidate's strengths and areas for improvement at the end of the interview.
  * **Interactive Web Interface:** Deployed as a user-friendly chat application using Streamlit.

-----

### Technology Stack 🛠️

  * **Backend:** Python
  * **AI Model:** Google Gemini API (`gemini-1.5-flash-latest`)
  * **Web Framework:** Streamlit
  * **Data Handling:** Pandas (for reading the public Google Sheet)

-----

### Setup and Installation (Local)  लोकल

To run this project on your local machine, follow these steps:

**1. Prerequisites:**

  * Python 3.8+
  * A Google Gemini API Key.

**2. Clone the Repository:**

```bash
git clone https://github.com/YOUR_USERNAME/excel-interviewer.git
cd excel-interviewer
```

**3. Create a Virtual Environment (Recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

**4. Install Dependencies:**

```bash
pip install -r requirements.txt
```

**5. Add Your API Key:**

  * Create a file named `.env` in the root of the project folder.
  * Add your Gemini API key to this file:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

**6. Run the Application:**

  * To run the command-line version:
    ```bash
    python main.py
    ```
  * To run the interactive web app version:
    ```bash
    streamlit run app.py
    ```

-----

### Configuration ⚙️

You can easily configure the interview settings by modifying the `config.py` file:

  * **`INTERVIEW_LENGTH_CONVERSATIONAL`**: Change this number to set how many theory questions are asked.
  * **`PRACTICAL_TASK`**: Update the dictionary to change the practical question, the Google Sheet URL, and the expected answer.

## Rate Limit for API calls:
  * Gemini api keys has less api limits in its free tier better use paid version.
