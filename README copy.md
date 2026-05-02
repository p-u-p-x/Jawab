# AI Customer Support Bot 🤖

A WhatsApp + Web AI support bot for Pakistani SMEs. Replies in Urdu and English, classifies complaints, escalates to humans, and logs tickets.

## Stack (100% free)
- **Flask** — Python web server
- **Gemini 1.5 Flash** — AI brain (free tier)
- **Meta WhatsApp Cloud API** — messaging
- **Google Sheets** — ticket database
- **Render** — hosting

## Project Structure
```
ai-support-bot/
├── app.py                 # Main Flask server (Member 1)
├── ai_engine.py           # Gemini AI integration (Member 1)
├── classifier.py          # Message categorisation (Member 1)
├── config.py              # Central settings (Member 1)
├── whatsapp_handler.py    # WhatsApp send/receive (Member 2)
├── sheets_handler.py      # Google Sheets logging (Member 3)
├── templates/
│   ├── index.html         # Web chat UI (Member 4)
│   └── dashboard.html     # Ticket dashboard (Member 4)
├── static/
│   ├── style.css          # Styling (Member 4)
│   └── script.js          # Frontend logic (Member 4)
├── requirements.txt
├── .env                   # SECRET — never uploaded
└── .gitignore
```

## Setup

### 1. Clone and install
```bash
git clone https://github.com/YOUR_USERNAME/ai-support-bot.git
cd ai-support-bot
pip install -r requirements.txt
```

### 2. Create your .env file
Copy `.env` and fill in your keys:
```
GEMINI_API_KEY=your_key_here
WHATSAPP_TOKEN=your_token_here
PHONE_NUMBER_ID=your_id_here
VERIFY_TOKEN=mysecretverifytoken123
SHEET_ID=your_sheet_id_here
```

### 3. Run locally
```bash
python app.py
```
Visit `http://localhost:5000` to confirm it's running.

### 4. Test with ngrok (for WhatsApp webhook)
```bash
ngrok http 5000
```
Use the ngrok HTTPS URL as your Meta webhook URL.

## Team
- Member 1 — Backend + AI
- Member 2 — WhatsApp Integration
- Member 3 — Database + Tickets
- Member 4 — Frontend + Demo
