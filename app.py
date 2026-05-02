# ============================================================
# app.py — The main Flask server. Central hub of the entire bot.
# Owned by Member 1.
# Routes:
#   GET  /          → Health check (confirm server is running)
#   GET  /webhook   → Meta verification handshake (one-time setup)
#   POST /webhook   → Receives incoming WhatsApp messages (live traffic)
#   POST /chat      → Web chat interface used by Member 4's frontend
# ============================================================

from flask import Flask, request, jsonify
from config import VERIFY_TOKEN, DEBUG, PORT
from ai_engine import get_ai_reply
from classifier import classify_message
from sheets_handler import log_ticket, get_conversation_history, save_message
from whatsapp_handler import send_whatsapp_message, extract_message_from_webhook

app = Flask(__name__)


# ────────────────────────────────────────────────────────────
# Route 1: Health check
# Visit http://localhost:5000/ in browser to confirm server runs
# ────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "running",
        "message": "AI Support Bot is online",
        "version": "1.0"
    }), 200


# ────────────────────────────────────────────────────────────
# Route 2: Meta Webhook Verification (GET /webhook)
# Meta calls this ONCE when you register your webhook URL.
# It sends a challenge number — we echo it back to prove ownership.
# After this succeeds once, you never need it again.
# ────────────────────────────────────────────────────────────
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("[Webhook] Meta verification successful")
        return challenge, 200  # Echo the challenge back — this is required
    else:
        print("[Webhook] Verification failed — token mismatch")
        return "Forbidden", 403


# ────────────────────────────────────────────────────────────
# Route 3: Receive WhatsApp Messages (POST /webhook)
# Every time a customer sends a WhatsApp message, Meta POSTs
# the message data here. We process it and send a reply.
# ────────────────────────────────────────────────────────────
@app.route("/webhook", methods=["POST"])
def receive_whatsapp_message():
    payload = request.get_json()

    if not payload:
        return "Bad Request", 400

    print(f"[Webhook] Received payload: {payload}")

    # Step 1: Extract phone number and message text from Meta's payload
    phone, message_text = extract_message_from_webhook(payload)

    if not phone or not message_text:
        # Not a message event (could be a status update) — ignore it
        return "OK", 200

    print(f"[Webhook] Message from {phone}: {message_text}")

    # Step 2: Classify the message
    category = classify_message(message_text)
    is_escalated = (category == "escalate")
    print(f"[Classifier] Category: {category}")

    # Step 3: Get this customer's conversation history for context
    history = get_conversation_history(phone)

    # Step 4: Get AI reply
    ai_reply = get_ai_reply(message_text, history)
    print(f"[AI] Reply: {ai_reply}")

    # Step 5: Log the ticket to Google Sheets
    ticket_id = log_ticket(phone, message_text, category, is_escalated)
    print(f"[Sheets] Ticket created: {ticket_id}")

    # Step 6: Save this exchange to conversation history
    save_message(phone, "user", message_text)
    save_message(phone, "model", ai_reply)

    # Step 7: Send the AI reply back to the customer on WhatsApp
    sent = send_whatsapp_message(phone, ai_reply)
    if not sent:
        print(f"[WhatsApp] Failed to send reply to {phone}")

    # Always return 200 to Meta — otherwise they'll keep retrying
    return "OK", 200


# ────────────────────────────────────────────────────────────
# Route 4: Web Chat (POST /chat)
# Used by Member 4's web frontend (index.html).
# The browser sends a message here, gets an AI reply back.
# This is the backup demo interface if WhatsApp has issues.
# ────────────────────────────────────────────────────────────
@app.route("/chat", methods=["POST"])
def web_chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    message_text = data["message"].strip()
    session_id = data.get("session_id", "web-user")  # Browser session identifier

    # Classify and get history
    category = classify_message(message_text)
    is_escalated = (category == "escalate")
    history = get_conversation_history(session_id)

    # Get AI reply
    ai_reply = get_ai_reply(message_text, history)

    # Log ticket
    log_ticket(session_id, message_text, category, is_escalated)

    # Save history
    save_message(session_id, "user", message_text)
    save_message(session_id, "model", ai_reply)

    return jsonify({
        "reply": ai_reply,
        "category": category,
        "escalated": is_escalated
    }), 200


# ────────────────────────────────────────────────────────────
# Start the server
# ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print(" AI Support Bot — Starting up")
    print(f" Running on http://localhost:{PORT}")
    print(f" Debug mode: {DEBUG}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
