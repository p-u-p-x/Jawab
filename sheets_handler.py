# ============================================================
# sheets_handler.py — Google Sheets connection.
# Owned by Member 3. This is a STUB so Member 1's app.py
# can import it without crashing. M3 fills in the real code.
# ============================================================

# Member 3: Replace this entire file with your real implementation.
# Your file should connect to Google Sheets using gspread
# and expose the functions below.


def log_ticket(phone: str, message: str, category: str, escalated: bool) -> str:
    """
    Write a new ticket row to Google Sheets.
    Returns the Ticket ID string.
    Member 3 implements this.
    """
    # STUB — prints to console until M3 implements
    import datetime
    ticket_id = f"TKT-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"[Sheets STUB] Ticket logged: {ticket_id} | {phone} | {category} | escalated={escalated}")
    return ticket_id


def get_conversation_history(phone: str) -> list:
    """
    Retrieve last N messages for this phone number.
    Returns list in Gemini format: [{"role": "user/model", "parts": ["text"]}]
    Member 3 implements this.
    """
    # STUB — returns empty history until M3 implements
    return []


def save_message(phone: str, role: str, text: str):
    """
    Save a single message to conversation history.
    role is either "user" or "model"
    Member 3 implements this.
    """
    # STUB
    print(f"[Sheets STUB] Saved message: [{role}] {text[:50]}")