# ============================================================
# sheets_handler.py — Real Google Sheets integration.
# Works with BOTH local credentials.json AND environment variable.
# ============================================================

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import SHEET_ID, CREDENTIALS_FILE, MAX_CONVERSATION_HISTORY
from datetime import datetime
import uuid
import json
import os

# Connect to Google Sheets — smart auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Check if credentials are in environment variable (production)
creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
if creds_json:
    # Use credentials from environment variable
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
else:
    # Use local credentials.json file (development)
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)

client = gspread.authorize(creds)

# Open the ticket sheet and history sheet
ticket_sheet = client.open_by_key(SHEET_ID).sheet1

try:
    history_sheet = client.open_by_key(SHEET_ID).worksheet("Conversation_History")
except gspread.WorksheetNotFound:
    history_sheet = client.open_by_key(SHEET_ID).add_worksheet(
        title="Conversation_History", rows="1000", cols="4"
    )
    history_sheet.append_row(["Phone", "Role", "Message", "Timestamp"])


def log_ticket(phone: str, message: str, category: str, escalated: bool) -> str:
    ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Escalated" if escalated else "Open"
    row = [ticket_id, phone, message[:500], category, status, timestamp, "YES" if escalated else "NO"]
    try:
        ticket_sheet.append_row(row)
        print(f"[Sheets] Ticket logged: {ticket_id}")
    except Exception as e:
        print(f"[Sheets ERROR] Could not log ticket: {e}")
    return ticket_id


def get_conversation_history(phone: str) -> list:
    try:
        all_rows = history_sheet.get_all_values()
        user_rows = [row for row in all_rows[1:] if row[0] == phone]
        recent = user_rows[-MAX_CONVERSATION_HISTORY:]
        history = []
        for row in recent:
            role = row[1]
            text = row[2]
            history.append({"role": role, "parts": [text]})
        return history
    except Exception as e:
        print(f"[Sheets ERROR] Could not get history: {e}")
        return []


def save_message(phone: str, role: str, text: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        history_sheet.append_row([phone, role, text[:1000], timestamp])
        print(f"[Sheets] Saved message: [{role}] {text[:40]}...")
    except Exception as e:
        print(f"[Sheets ERROR] Could not save message: {e}")


def get_all_tickets() -> list:
    try:
        rows = ticket_sheet.get_all_values()
        if len(rows) <= 1:
            return []
        headers = rows[0]
        tickets = []
        for row in rows[1:]:
            ticket = {}
            for i, header in enumerate(headers):
                ticket[header] = row[i] if i < len(row) else ""
            tickets.append(ticket)
        return tickets
    except Exception as e:
        print(f"[Sheets ERROR] Could not get tickets: {e}")
        return []
