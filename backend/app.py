# ============================================================
# app.py — The main Flask server. Central hub of the entire bot.
# ============================================================
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, request, jsonify, render_template
from config import DEBUG, PORT
from ai_engine import get_ai_reply
from classifier import classify_message
from sheets_handler import log_ticket, get_conversation_history, save_message, get_all_tickets
from telegram_handler import send_telegram_message, extract_message_from_webhook

# Smart template folder — works on BOTH local and Render/Railway
# On your laptop: backend/ and frontend/ are separate folders
# On Render/Railway: everything is copied into one place
def get_template_folder():
    if os.path.exists('../frontend/pages'):
        return '../frontend/pages'  # Local development
    return 'templates'  # Render/Railway production

def get_static_folder():
    if os.path.exists('../frontend/static'):
        return '../frontend/static'  # Local development
    return 'static'  # Render/Railway production

app = Flask(__name__, 
            template_folder=get_template_folder(),
            static_folder=get_static_folder())

@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "running",
        "message": "AI Support Bot is online",
        "version": "1.0"
    }), 200

@app.route("/webhook", methods=["POST"])
def receive_telegram_message():
    payload = request.get_json()
    if not payload:
        return "Bad Request", 400

    chat_id, message_text = extract_message_from_webhook(payload)
    if not chat_id or not message_text:
        return "OK", 200

    category = classify_message(message_text)
    is_escalated = (category == "escalate")
    history = get_conversation_history(chat_id)
    ai_reply = get_ai_reply(message_text, history)
    log_ticket(chat_id, message_text, category, is_escalated)
    save_message(chat_id, "user", message_text)
    save_message(chat_id, "model", ai_reply)
    send_telegram_message(chat_id, ai_reply)
    return "OK", 200

@app.route("/chat", methods=["POST"])
def web_chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    message_text = data["message"].strip()
    session_id = data.get("session_id", "web-user")
    category = classify_message(message_text)
    is_escalated = (category == "escalate")
    history = get_conversation_history(session_id)
    ai_reply = get_ai_reply(message_text, history)
    log_ticket(session_id, message_text, category, is_escalated)
    save_message(session_id, "user", message_text)
    save_message(session_id, "model", ai_reply)
    return jsonify({
        "reply": ai_reply,
        "category": category,
        "escalated": is_escalated
    }), 200

@app.route("/tickets", methods=["GET"])
def get_tickets():
    tickets = get_all_tickets()
    return jsonify({"tickets": tickets, "count": len(tickets)}), 200

@app.route("/chat-page", methods=["GET"])
def chat_page():
    return render_template("chat.html")

@app.route("/about", methods=["GET"])
def about_page():
    return render_template("about.html")

@app.route("/dashboard", methods=["GET"])
def dashboard_page():
    return render_template("dashboard.html")

if __name__ == "__main__":
    print("=" * 50)
    print(" AI Support Bot — Starting up")
    print(f" Running on http://localhost:{PORT}")
    print(f" Debug mode: {DEBUG}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
