# g_sheets_service.py
"""
Handles interaction with Google Sheets API for practical tasks.
"""
import time

def check_practical_task(sheet_url, user_answer, expected_answer):
    """
    MOCK FUNCTION: In a real app, this would use the gspread library
    or Google Sheets API to read a cell value from the actual sheet.
    """
    print(f"[Verifying answer in Google Sheet: {sheet_url}]")
    time.sleep(1.5)
    
    if user_answer.strip() == expected_answer:
        print("[Verification successful!]")
        return True
    else:
        print("[Verification failed. The value in the sheet is not correct.]")
        return False