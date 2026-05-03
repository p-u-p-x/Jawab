# ============================================================
# telegram_handler.py — Sends Telegram messages back to customer.
# Replaces whatsapp_handler.py — uses Telegram Bot API (free)
# ============================================================
import requests
from config import TELEGRAM_TOKEN

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_telegram_message(chat_id: str, message_text: str) -> bool:
    """
    Send a Telegram message to a chat ID.
    """
    try:
        response = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": message_text}
        )
        return response.status_code == 200
    except Exception as e:
        print(f"[Telegram ERROR] {e}")
        return False

def extract_message_from_webhook(payload: dict) -> tuple:
    """
    Pull the chat ID and message text out of Telegram webhook payload.
    Returns (chat_id, message_text) or (None, None)
    """
    try:
        message = payload["message"]
        chat_id = str(message["chat"]["id"])
        text = message["text"]
        return chat_id, text
    except (KeyError, IndexError):
        return None, None
