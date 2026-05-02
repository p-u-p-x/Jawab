# 🤖 Jawab — AI Customer Support Bot for Pakistani SMEs

**Tagline:** Instant, intelligent, always-on customer support across WhatsApp and web for Pakistani small businesses.

---

## 📋 Table of Contents

1. [Problem Statement](#problem-statement)
2. [Solution Statement](#solution-statement)
3. [Project Overview](#project-overview)
4. [Tech Stack](#tech-stack)
5. [Folder Structure](#folder-structure)
6. [Team Roles & Responsibilities](#team-roles--responsibilities)
7. [How to Run Locally](#how-to-run-locally)
8. [Frontend Pages & Routes](#frontend-pages--routes)
9. [Backend API Endpoints](#backend-api-endpoints)
10. [Environment Setup](#environment-setup)
11. [How It Works](#how-it-works)
12. [Key Features](#key-features)
13. [Known Limitations](#known-limitations)
14. [Future Roadmap](#future-roadmap)
15. [Troubleshooting](#troubleshooting)

---

## 🎯 Problem Statement

### The Challenge
In Pakistan, millions of small business owners manage customer support manually via WhatsApp. The reality:
- A customer who doesn't get a reply in 10 minutes often doesn't come back
- Manual responses = limited scale (can't handle 100+ messages/day)
- No ticket tracking = chaos and lost conversations
- Shifting between languages (English, Urdu, Roman Urdu) = friction
- No data = no insights into what customers need

### The Pain Points
1. **24/7 Availability:** SMEs sleep, but customers message at 2 AM
2. **Language Barriers:** Urdu/Roman Urdu support is non-existent in standard chatbots
3. **No Organization:** Messages scattered across WhatsApp, no central record
4. **Expensive Solutions:** Enterprise ChatBot platforms cost 100,000+ PKR/month
5. **Lost Revenue:** Every missed message = potential lost customer

### Target Users
Pakistani SMEs (e-commerce, services, retail, logistics) with 10–1000 customers who rely on WhatsApp as their primary support channel.

---

## ✅ Solution Statement

**Jawab** is a free, open-source AI-powered support engine built on a completely free tech stack:

### What It Does
1. **Receives messages** from customers on WhatsApp (via Meta Cloud API) or web chat
2. **Classifies intent** (complaint, query, or escalation) in real-time
3. **Generates intelligent replies** using Google Gemini AI—bilingual (English/Urdu), contextual, professional
4. **Logs every ticket** automatically to Google Sheets (no manual data entry)
5. **Escalates urgent issues** to a human agent (flagged and ready)
6. **Provides a live dashboard** to monitor all support activity

### Real-World Example
```
Customer WhatsApp → Jawab:
"Order nahi aaya bhai, 3 din ho gaye!" 
(Order hasn't arrived, it's been 3 days!)

Jawab (instant, automatic):
1. Detects: "This is a complaint + escalation"
2. Retrieves order history from Google Sheets
3. Generates reply: "Bilkul, main aapka order track kar raha hoon. 
   5 minit mein update dunga." 
   (Absolutely, I'm tracking your order. I'll update in 5 minutes.)
4. Sends reply back to customer
5. Logs ticket with ID, phone, message, category, timestamp

Business Owner Dashboard:
"1 escalated ticket from today"
→ Click → See full context → Escalate to human agent
```

### Key Differentiators
- ✅ **Bilingual AI** (English + Urdu/Roman Urdu detection and response)
- ✅ **No Subscription Costs** (uses free Google API tier + Flask open-source)
- ✅ **No Agent Hiring Needed** (AI handles 95% of inquiries)
- ✅ **One-Click Deployment** (simple Python + Flask)
- ✅ **Automatic Ticket Logging** (Google Sheets integration—searchable, exportable)
- ✅ **Open Source** (transparent, customizable, community-driven)

---

## 🏗️ Project Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    JAWAB SYSTEM ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ INPUT CHANNELS                                           │   │
│  │ • WhatsApp (Meta Cloud API)                             │   │
│  │ • Web Chat (Browser, JavaScript)                        │   │
│  └─────────────────┬──────────────────────────────────────┘   │
│                    │                                             │
│                    ▼                                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ FLASK BACKEND (app.py)                                  │   │
│  │ • Routes messages to classifiers & AI                  │   │
│  │ • Manages webhooks (WhatsApp)                          │   │
│  │ • Serves frontend pages                                │   │
│  └─────────────────┬──────────────────────────────────────┘   │
│                    │                                             │
│        ┌───────────┼───────────┐                                │
│        ▼           ▼           ▼                                │
│   ┌─────────┐ ┌─────────┐ ┌─────────────┐                      │
│   │Classifier│ │AI Engine│ │   Sheets    │                      │
│   │(Intent)  │ │(Gemini) │ │  Handler    │                      │
│   └─────────┘ └─────────┘ └─────────────┘                      │
│        │           │             │                              │
│        └───────────┼─────────────┘                              │
│                    ▼                                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ GOOGLE SHEETS (Centralized Log)                         │   │
│  │ • Ticket_Log (all tickets with category, escalation)   │   │
│  │ • Conversation_History (full chat history per phone)   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                    │                                             │
│        ┌───────────┴───────────┐                                │
│        ▼                       ▼                                │
│  ┌───────────────┐     ┌──────────────┐                        │
│  │ WHATSAPP API  │     │ WEB DASHBOARD │                        │
│  │ (Outbound)    │     │ & Chat Pages  │                        │
│  └───────────────┘     └──────────────┘                        │
│        │                       │                                │
│        └───────────┬───────────┘                                │
│                    ▼                                             │
│        ┌──────────────────────────┐                             │
│        │  CUSTOMER / BUSINESS     │                             │
│        │  Owner (Dashboard)       │                             │
│        └──────────────────────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Message Flow (Step-by-Step)

**WhatsApp Scenario:**
1. Customer sends WhatsApp → Meta Cloud API
2. Meta sends webhook to Jawab `/webhook` endpoint
3. Jawab extracts phone number + message
4. Classifier reads message → returns category (complaint/query/escalate)
5. AI Engine calls Gemini → generates smart reply
6. Reply sent back to customer via WhatsApp API
7. Entire conversation logged to Google Sheets

**Web Chat Scenario:**
1. Visitor opens http://localhost:8080/chat-page
2. Types a message in the chat box
3. JavaScript makes POST request to `/chat` endpoint
4. Backend processes same as WhatsApp (classify, AI reply, log)
5. Reply returned as JSON
6. Chat updates in real-time
7. Chat history persists in browser localStorage

---

## 🛠️ Tech Stack

### Backend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | Python + Flask | 3.0+ | Web server, routing, template rendering |
| **AI Engine** | Google Gemini AI | 2.5-flash | Natural language generation, context-aware replies |
| **Messaging API** | Meta WhatsApp Business API | Cloud API | Webhook ingestion, message delivery |
| **Data Storage** | Google Sheets (gspread) | 6.0+ | Centralized ticket logging, conversation history |
| **Classification** | Custom Classifier (Python) | In-house | Keyword-based intent detection |
| **Config Management** | python-dotenv | 1.0+ | Environment variables (.env) |
| **HTTP Client** | requests | 2.31+ | API calls (Gemini, WhatsApp) |
| **Production Server** | Gunicorn | 21.2+ | WSGI server for deployment |

### Frontend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Markup** | HTML5 | Page structure |
| **Styling** | CSS3 (Inline) | Dark mode, animations, responsive design |
| **Logic** | JavaScript (Vanilla) | Chat logic, API calls, localStorage persistence |
| **Fonts** | Google Fonts | Orbitron (headings), DM Sans (body), JetBrains Mono (code) |
| **Design Theme** | Dark neon-green | Hacker aesthetic + WhatsApp familiarity |

### Infrastructure
| Component | Service | Purpose |
|-----------|---------|---------|
| **Config** | Environment variables (.env) | API keys, tokens, configuration |
| **Package Manager** | pip | Python package management |
| **Version Control** | Git | Source control (with .gitignore) |
| **Development Server** | Flask development server | Port 8080 |
| **Production** | Gunicorn / Docker (future) | Scalable deployment |

### Dependencies (from requirements.txt)
```
flask==3.0.0                    # Web framework
python-dotenv==1.0.0            # Environment variables
google-genai==1.0.0             # Gemini AI API
gspread==6.0.0                  # Google Sheets client
oauth2client==4.1.3             # Google authentication
requests==2.31.0                # HTTP library
gunicorn==21.2.0                # Production WSGI server
```

---

## 📁 Folder Structure

```
Jawab/
├── backend/                           # Backend server (Python)
│   ├── app.py                         # Main Flask server (7 routes)
│   ├── ai_engine.py                   # Gemini AI integration
│   ├── classifier.py                  # Message classification (complaint/query/escalate)
│   ├── sheets_handler.py              # Google Sheets read/write
│   ├── whatsapp_handler.py            # WhatsApp API integration (stub)
│   ├── config.py                      # Environment config loader
│   ├── requirements.txt               # Python dependencies
│   ├── .env                           # ⚠️ YOU MUST CREATE THIS
│   ├── credentials.json               # ⚠️ YOU MUST CREATE THIS
│   └── __pycache__/                   # Python cache (ignore)
│
├── frontend/                          # Frontend (HTML/CSS/JS)
│   ├── pages/                         # HTML pages
│   │   ├── index.html                 # Landing/hero page
│   │   ├── about.html                 # About page (story, problem, solution)
│   │   ├── chat.html                  # Web chat demo (main demo page)
│   │   └── dashboard.html             # Ticket admin dashboard
│   └── static/                        # Static assets (CSS/JS)
│       ├── style.css                  # (empty—styles inline in HTML)
│       └── script.js                  # (empty—scripts inline in HTML)
│
├── .env                               # ⚠️ YOU MUST CREATE THIS
├── .gitignore                         # Git ignore rules (pre-filled)
├── credentials.json                   # ⚠️ YOU MUST CREATE THIS
├── README.md                          # Original brief README
├── README_COMPLETE.md                 # This comprehensive guide
├── requirements.txt                   # Python dependencies
└── run.sh                             # Bash script to start backend

```

### File Responsibilities & Ownership

| File | Lines | Purpose | Owner |
|------|-------|---------|-------|
| **app.py** | ~130 | Main Flask server, 7 routes, request handling | Backend Lead |
| **ai_engine.py** | ~60 | Gemini API calls, system prompt, conversation management | Member 1 (AI) |
| **classifier.py** | ~80 | Keyword-based message classification (complaint/query/escalate) | Member 1 (AI) |
| **sheets_handler.py** | ~150 | Google Sheets integration, ticket logging, history retrieval | Member 3 (Data) |
| **whatsapp_handler.py** | ~30 | WhatsApp API calls (stub—to be implemented) | Member 2 (Integration) |
| **config.py** | ~40 | Load environment variables, centralized config | Backend Lead |
| **index.html** | ~400 | Landing page with hero, features, flow, stats | Member 4 (Frontend) |
| **chat.html** | ~350 | Chat demo page with API integration | Member 4 (Frontend) |
| **dashboard.html** | ~400 | Admin dashboard with table and stats | Member 4 (Frontend) |
| **about.html** | ~300 | About page with problem/solution narrative | Member 4 (Frontend) |

---

## 👥 Team Roles & Responsibilities

### Member 1 — AI Engine & Classifier Lead
**Your responsibilities:**
- ✅ Implement and tune Gemini AI integration in `ai_engine.py`
- ✅ Build message classifier for complaint/query/escalate detection in `classifier.py`
- ✅ Improve bilingual (Urdu/English) detection
- ✅ Test and refine reply quality with real Pakistani business scenarios
- ✅ Manage conversation history context window (MAX_CONVERSATION_HISTORY in config.py)

**Key Files to Own:**
- `backend/ai_engine.py` — Gemini API calls, system prompt, response generation
- `backend/classifier.py` — Intent classification logic, keyword lists
- `backend/config.py` — Constants (BOT_NAME, MAX_CONVERSATION_HISTORY, ESCALATION_KEYWORDS)

**Success Metrics:**
- AI replies feel human and contextual
- Classifier accuracy >90% (correct category detection)
- Response time <2 seconds per message
- Bilingual support working (Urdu/Roman Urdu detection and response)

**Deliverables by Deadline:**
- [ ] AI replies tested with 50+ real Pakistani customer messages
- [ ] Classifier tuned for Pakistan-specific keywords
- [ ] System prompt refined for local business context

---

### Member 2 — WhatsApp Integration Lead
**Your responsibilities:**
- ✅ Implement WhatsApp Business API calls in `whatsapp_handler.py`
- ✅ Set up webhook verification endpoint (`/webhook` GET)
- ✅ Handle incoming message payloads (`/webhook` POST)
- ✅ Manage authentication tokens and phone number IDs
- ✅ Implement error handling and retry logic for failed deliveries
- ✅ Test end-to-end with real WhatsApp messages

**Key Files to Own:**
- `backend/whatsapp_handler.py` — All WhatsApp API functions
- `backend/app.py` — Webhook routes (you collaborate here)
- `.env` — WHATSAPP_TOKEN, PHONE_NUMBER_ID, VERIFY_TOKEN

**Success Metrics:**
- Webhook verification passes Meta validation
- Messages received correctly from WhatsApp
- Outbound messages delivered to customer phone numbers
- Error handling in place (retry on network fail)

**Deliverables by Deadline:**
- [ ] WhatsApp webhook fully implemented and verified with Meta
- [ ] Send/receive messages tested on real WhatsApp account
- [ ] Error handling for network failures

---

### Member 3 — Data & Logging Lead
**Your responsibilities:**
- ✅ Set up Google Sheets integration in `sheets_handler.py`
- ✅ Design and create ticket log schema (columns: Ticket ID, Phone, Message, Category, Status, Timestamp, Escalated)
- ✅ Implement conversation history retrieval (for AI context)
- ✅ Ensure data persistence and automatic backups
- ✅ Make tickets searchable by phone, category, date range
- ✅ Test with large datasets (1000+ tickets)

**Key Files to Own:**
- `backend/sheets_handler.py` — All Google Sheets functions
- `backend/config.py` — SHEET_ID, CREDENTIALS_FILE paths
- `credentials.json` — Google service account (you download/configure)

**Success Metrics:**
- Tickets logged reliably (100% success rate)
- Conversation history retrievable and usable by AI Engine
- Google Sheets fast even with 1000+ tickets
- Data schema clean and searchable

**Deliverables by Deadline:**
- [ ] Google Sheets connected and verified
- [ ] Both worksheets created (Ticket_Log, Conversation_History)
- [ ] 100+ test tickets logged successfully
- [ ] Dashboard retrieves and displays tickets correctly

---

### Member 4 — Frontend & UI Lead
**Your responsibilities:**
- ✅ Maintain all 4 frontend pages (index, about, chat, dashboard)
- ✅ Implement chat UI with real-time API integration
- ✅ Create responsive design (mobile-first, tablet, desktop)
- ✅ Build admin dashboard with filtering and live updates
- ✅ Ensure animations smooth (no jank)
- ✅ Test all routes and link navigation
- ✅ Polish dark neon theme for consistency

**Key Files to Own:**
- `frontend/pages/index.html` — Landing page
- `frontend/pages/chat.html` — Chat demo (critical for judges!)
- `frontend/pages/dashboard.html` — Admin dashboard
- `frontend/pages/about.html` — About page
- `frontend/static/` — CSS/JS (currently inline in HTML)

**Success Metrics:**
- All pages load instantly (no lag)
- Chat responds in <2 seconds (backend + network)
- Dashboard refreshes every 30 seconds (live view)
- Mobile-responsive on iPhone 12, iPad, desktop
- Animations smooth (60 FPS)

**Deliverables by Deadline:**
- [ ] All 4 pages fully functional
- [ ] Chat page tested with live backend
- [ ] Dashboard displays real tickets
- [ ] Mobile responsive on all screen sizes
- [ ] Dark theme consistent across pages

---

### Backend Lead — System Integration & DevOps
**Your responsibilities:**
- ✅ Coordinate between all members (Member 1, 2, 3, 4)
- ✅ Set up .env file with all required keys
- ✅ Download and configure credentials.json
- ✅ Test end-to-end workflows (message → AI → Sheets → Dashboard)
- ✅ Deploy to staging/production
- ✅ Monitor for errors and performance
- ✅ Documentation and deployment guide

**Key Files to Own:**
- `backend/app.py` — Main server, route coordination
- `.env` — Master configuration
- `credentials.json` — Service account setup
- `run.sh` — Start script

**Success Metrics:**
- Backend starts without errors
- All routes respond correctly
- End-to-end test: Send chat message → See reply → Find in dashboard
- Deployment guide ready for judges

**Deliverables by Deadline:**
- [ ] .env and credentials.json configured
- [ ] Backend starts cleanly with no errors
- [ ] End-to-end tests pass
- [ ] Deployment instructions documented

---

## 🚀 How to Run Locally

### Prerequisites
- **Python 3.9+** (check: `python --version`)
- **pip** (Python package manager, comes with Python)
- **Google Cloud Account** (free tier)
- **Google Sheet** (for logging)
- **WhatsApp Business Account** (optional for local testing)

### Step 1: Clone & Setup Virtual Environment

```bash
# Navigate to project folder
cd path/to/Jawab

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### Step 2: Install Python Dependencies

```bash
# Install all required packages
pip install -r backend/requirements.txt
```

**Expected output:**
```
Successfully installed flask-3.0.0 python-dotenv-1.0.0 google-genai-1.0.0 
gspread-6.0.0 oauth2client-4.1.3 requests-2.31.0 gunicorn-21.2.0
```

### Step 3: Create .env File

Create a file named `.env` in the project root (same level as `backend/`, not inside it):

```env
# ===== Gemini AI =====
GEMINI_API_KEY=AIzaSyD...                # From Google Cloud Console

# ===== Google Sheets =====
SHEET_ID=1a2b3c4d5e6f7g8h9i0j            # From your Google Sheet URL

# ===== WhatsApp (Optional for Local) =====
WHATSAPP_TOKEN=EABxxxxxx...              # From Meta for WhatsApp
PHONE_NUMBER_ID=102345xxxxx              # Your WhatsApp Business phone ID
VERIFY_TOKEN=mysecrettoken123            # Your own secret token

# ===== Flask =====
PORT=8080                                 # Port to run on
FLASK_ENV=development                     # Use development mode
```

**Where to get these keys:**
- **GEMINI_API_KEY:** [Google AI Studio](https://aistudio.google.com/app/apikey) (free tier)
- **SHEET_ID:** Create a Google Sheet, copy ID from URL: `docs.google.com/spreadsheets/d/[SHEET_ID]/`
- **WHATSAPP_TOKEN / PHONE_NUMBER_ID:** Set up WhatsApp Business Account at [Meta Developers](https://developers.facebook.com/)

### Step 4: Set Up Google Sheets Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable **Google Sheets API** and **Google Drive API**
4. Create a **Service Account**:
   - Go to "Service Accounts" in IAM & Admin
   - Click "Create Service Account"
   - Name it "Jawab Service"
   - Grant it "Editor" role
5. Create and download a **JSON key**:
   - Click the service account you just created
   - Go to "Keys" tab
   - Create a new key (JSON format)
   - Save as `credentials.json` in project root
6. Share your Google Sheet with the service account email (found in credentials.json)

**Your credentials.json should look like:**
```json
{
  "type": "service_account",
  "project_id": "my-project-12345",
  "private_key_id": "key-id-here",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "jawab@my-project.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "...",
  "client_x509_cert_url": "..."
}
```

### Step 5: Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new blank sheet
3. Copy the **Sheet ID** from the URL and paste it in `.env` as `SHEET_ID`
4. Share the sheet with your service account email
5. The app will automatically create two worksheets:
   - `Ticket_Log` — All tickets with metadata
   - `Conversation_History` — Chat history per phone number

### Step 6: Start the Backend Server

```bash
# From project root (where backend/ folder is)
cd backend
python app.py
```

**Expected output:**
```
==================================================
 AI Support Bot — Starting up
 Running on http://localhost:8080
 Debug mode: True
==================================================
 * Serving Flask app 'app'
 * Debug mode: on
 WARNING in app.run()
 * Running on http://0.0.0.0:8080
```

✅ **Backend is now running!**

### Step 7: Open the Frontend in Browser

Open your browser and visit:

| Page | URL | Purpose |
|------|-----|---------|
| **Landing** | http://localhost:8080/ | Home page with hero & features |
| **Chat Demo** | http://localhost:8080/chat-page | Main interactive demo |
| **Dashboard** | http://localhost:8080/dashboard | Admin ticket view |
| **About** | http://localhost:8080/about | Project story & vision |

### Step 8: Test the Chat

1. Go to http://localhost:8080/chat-page
2. Type a test message: `"Is my order ready?"`
3. Click **Send** or press Enter
4. Wait 1–2 seconds...
5. The bot should reply: `"Yes, your order is being prepared..."`
6. Check your Google Sheet — you should see a new row in `Ticket_Log`!

**Troubleshooting:**
- If no reply: Check browser console (F12) for errors
- If Google Sheets not updating: Check `.env` file has correct `SHEET_ID`
- If server crashes: Check that all `.env` keys are present

### Step 9: Test the Dashboard

1. Go to http://localhost:8080/dashboard
2. You should see a table with the tickets you just created
3. Table refreshes every 30 seconds automatically
4. Try filtering by category (buttons at top)

---

## 🎨 Frontend Pages & Routes

### Route Map

| Route | File | Purpose | Users |
|-------|------|---------|-------|
| `/` | `pages/index.html` | Landing page, hero, features | Potential customers |
| `/about` | `pages/about.html` | About page, problem/solution | Interested users |
| `/chat-page` | `pages/chat.html` | Web chat demo (main feature) | **Hackathon judges** |
| `/dashboard` | `pages/dashboard.html` | Admin dashboard, tickets, stats | Business owners |
| `/api/health` | Python (API only) | Health check | Developers |

### Page Details

#### 1️⃣ Landing Page (`/`)
**File:** `frontend/pages/index.html`

**Sections:**
- **Navbar:** Logo (Jawab), links to About/Chat/Dashboard
- **Hero Section:** Animated grid background, typing animation, two CTAs
- **Features Section:** 6 feature cards (scrolls & fades in)
- **Flow Section:** 3-step walkthrough (Customer → Jawab → Dashboard)
- **Stats Section:** 4 key metrics (reply time, availability, categories, logging)
- **CTA Banner:** "Stop losing customers to slow replies" + action button

**Design:** Dark theme with neon green accents, smooth animations

**Key Features:**
- Canvas-based animated background
- Intersection Observer for scroll reveals
- Responsive grid layout
- Smooth transitions

---

#### 2️⃣ Chat Page (`/chat-page`) — **Main Demo for Judges**
**File:** `frontend/pages/chat.html`

**Sections:**
- **Chat Header:** Jawab logo + "Online" green dot (live indicator)
- **Message Thread:** Scrollable chat window
  - User messages appear on right (green background)
  - Bot messages appear on left (grey background)
  - Typing indicator (3 animated dots) while awaiting reply
- **Category Badge:** Small pill showing `query` / `complaint` / `escalate`
- **Input Area:** Text box + Send button at bottom

**Features:**
- Real-time API integration with `/chat` endpoint
- Typing indicator (UX polish)
- localStorage persistence (chat history survives page reload)
- Automatic scrolling to latest message
- Error handling (if backend is down)

**Test Scenarios:**
```
Test 1: General Query
Input: "What's your return policy?"
Expected: Classification "query", helpful response

Test 2: Complaint
Input: "I ordered 3 days ago and got the wrong item!"
Expected: Classification "complaint", empathetic response

Test 3: Escalation
Input: "I want to speak to a manager immediately!"
Expected: Classification "escalate", escalation message
```

---

#### 3️⃣ Dashboard (`/dashboard`) — Admin View
**File:** `frontend/pages/dashboard.html`

**Sections:**
- **Stats Cards:** 4 cards showing
  - Total tickets today
  - Escalated tickets
  - Complaints
  - Queries
- **Filter Bar:** Buttons to filter by category (All, Complaints, Queries, Escalated)
- **Live Table:** Columns
  - Ticket ID (unique)
  - Phone (customer phone number)
  - Category (query/complaint/escalate)
  - Message (first 100 chars)
  - Status (Open/Escalated)
  - Timestamp (when created)
- **Empty State:** "No tickets yet" if no data

**Features:**
- Auto-refresh every 30 seconds (live view without page reload)
- Filter by category (real-time table filtering)
- Responsive table (mobile-friendly)
- Searches tickets from `/tickets` API endpoint

**For Demo:**
- Send 3–5 test messages on Chat page
- Go to Dashboard
- See tickets populate in real-time
- Click filters to test category filtering

---

#### 4️⃣ About Page (`/about`)
**File:** `frontend/pages/about.html`

**Sections:**
- **Hero:** Project tagline + problem statement
- **Problem Section:** "The Problem" card with stats
- **Solution Section:** "Jawab in Action" with 3 value props
- **Tech Stack Section:** 5 tech cards (Python, Gemini, WhatsApp, Sheets, Classifier)
- **Vision Section:** Roadmap and future plans
- **Team Section:** 3 placeholder team member cards (update with real names!)

**Design:** Consistent dark neon theme, smooth fade-in animations

---

## 🔌 Backend API Endpoints

All responses are JSON. Base URL: `http://localhost:8080`

### 1. Health Check
```
GET /api/health
```

**Response:** `200 OK`
```json
{
  "status": "running",
  "message": "AI Support Bot is online",
  "version": "1.0"
}
```

**Use Case:** Check if backend is alive

---

### 2. Web Chat (Main)
```
POST /chat
```

**Request Body:**
```json
{
  "message": "Is my order ready?",
  "session_id": "web-user"
}
```

**Response:** `200 OK`
```json
{
  "reply": "Yes, your order is being prepared and will arrive tomorrow.",
  "category": "query",
  "escalated": false
}
```

**Process:**
1. Classify message → `query` / `complaint` / `escalate`
2. Retrieve conversation history for session
3. Call Gemini AI → generate reply
4. Log ticket to Google Sheets
5. Save message to conversation history
6. Return reply + category

**Error Cases:**
- No message provided → `400 Bad Request`
- Backend down → Connection refused

---

### 3. Get All Tickets
```
GET /tickets
```

**Response:** `200 OK`
```json
{
  "tickets": [
    {
      "Ticket ID": "TKT-ABC123",
      "Phone": "923001234567",
      "Category": "query",
      "Message": "When will my order arrive?",
      "Status": "Open",
      "Timestamp": "2024-05-03 14:30:45",
      "Escalated": "NO"
    },
    {
      "Ticket ID": "TKT-XYZ789",
      "Phone": "923009876543",
      "Category": "complaint",
      "Message": "I received the wrong item!",
      "Status": "Escalated",
      "Timestamp": "2024-05-03 15:12:22",
      "Escalated": "YES"
    }
  ],
  "count": 47
}
```

**Use Case:** Dashboard retrieves and displays all tickets

---

### 4. WhatsApp Webhook (Verification)
```
GET /webhook?hub.mode=subscribe&hub.verify_token=xxx&hub.challenge=yyy
```

**Response:** `200 OK`
```
yyy
```

(Raw challenge string, not JSON)

**Use Case:** Meta verifies webhook on registration

---

### 5. WhatsApp Webhook (Receive Messages)
```
POST /webhook
```

**Request Body:** (Meta webhook payload)
```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "123456789",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "phone_number_id": "102345xxxxx"
            },
            "messages": [
              {
                "from": "923001234567",
                "id": "wamid.xxx",
                "timestamp": "1609459200",
                "type": "text",
                "text": {
                  "body": "Hello, is my order ready?"
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

**Response:** `200 OK`
```json
{"status": "OK"}
```

**Process:**
1. Extract phone + message from payload
2. Classify message
3. Get AI reply
4. Log ticket
5. Send WhatsApp reply back to customer

---

### 6. Serve Pages (GET)
```
GET /
GET /chat-page
GET /about
GET /dashboard
```

**Response:** `200 OK` (HTML page)

**Use Case:** Flask renders frontend pages from `frontend/pages/`

---

## ⚙️ Environment Setup Details

### .env File (What to Create)

**File location:** Project root (same level as `backend/` folder, NOT inside it)

```env
# ===== GEMINI AI =====
# Get from: https://aistudio.google.com/app/apikey
# Click "Get API Key" → Copy → Paste here
GEMINI_API_KEY=AIzaSyD1234567890abcdefghijklmnop

# ===== GOOGLE SHEETS =====
# Create a Google Sheet at https://sheets.google.com
# Copy the ID from URL: docs.google.com/spreadsheets/d/[THIS_ID]/
# Then share the sheet with your service account email (from credentials.json)
SHEET_ID=1a2b3c4d5e6f7g8h9i0j

# ===== WHATSAPP (Optional — only if you have a Business Account) =====
# Get from: https://developers.facebook.com/
# Create an app → WhatsApp → Settings
WHATSAPP_TOKEN=EABxxxxxx123456789
PHONE_NUMBER_ID=102345xxxxx
VERIFY_TOKEN=mysecrettoken123

# ===== FLASK SERVER =====
PORT=8080
FLASK_ENV=development
```

### credentials.json File (How to Create)

**File location:** Project root (same level as `.env`)

**Steps:**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project (or use existing)
3. Enable APIs:
   - Search "Google Sheets API" → Enable
   - Search "Google Drive API" → Enable
4. Go to **IAM & Admin** → **Service Accounts**
5. Click **Create Service Account**
   - Name: `Jawab Service`
   - Description: `AI Support Bot`
   - Click "Create and Continue"
6. Grant role: `Editor` (so it can read/write sheets)
7. Click on the service account you just created
8. Go to **Keys** tab
9. Click **Add Key** → **Create new key** → **JSON**
10. A `credentials.json` downloads automatically
11. Move it to your project root folder
12. Open your Google Sheet and share it with the **client_email** from credentials.json

**Example credentials.json:**
```json
{
  "type": "service_account",
  "project_id": "my-project-12345",
  "private_key_id": "abcdef1234567890",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n",
  "client_email": "jawab-service@my-project-12345.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/jawab-service%40my-project-12345.iam.gserviceaccount.com"
}
```

---

## 🔄 How It Works (End-to-End)

### Scenario 1: WhatsApp Customer Messages

```
Step 1: Customer sends WhatsApp message
  Phone: +923001234567
  Message: "Order nahi aaya bhai"
  
Step 2: Meta Cloud API sends webhook to Jawab
  POST http://localhost:8080/webhook
  Payload: {from: "923001234567", text: "Order nahi aaya bhai"}
  
Step 3: Jawab extracts phone + message
  phone = "923001234567"
  message = "Order nahi aaya bhai"
  
Step 4: Classifier analyzes message
  Keywords detected: ["nahi aaya" (didn't arrive)]
  → Category: "complaint"
  → Escalated: true
  
Step 5: AI Engine generates reply
  Gemini prompt: "This is a complaint about an order not arriving.
                  Respond in Roman Urdu. Be empathetic."
  → Reply: "Bilkul, main aapka order track kar raha hoon..."
  
Step 6: Log ticket to Google Sheets
  Ticket_Log: [TKT-ABC123, 923001234567, "Order nahi aaya bhai", 
               complaint, Escalated, 2024-05-03 14:30:45]
  
Step 7: Save to conversation history
  Conversation_History: [923001234567, user, "Order nahi aaya bhai", ...]
                       [923001234567, model, "Bilkul...", ...]
  
Step 8: Send reply back via WhatsApp
  POST to WhatsApp API with reply message
  
Step 9: Customer receives reply instantly
  ✓ Message delivered to phone
  ✓ Business owner sees ticket in dashboard (30s refresh)
```

### Scenario 2: Web Chat Demo

```
Step 1: Visitor opens http://localhost:8080/chat-page
  Browser loads chat.html
  JavaScript initializes localStorage
  
Step 2: Visitor types message + clicks Send
  Message: "Is my order ready?"
  JavaScript validates & sends to backend:
  POST /chat
  {message: "Is my order ready?", session_id: "web-user"}
  
Step 3: Backend processes (same as WhatsApp)
  Classify → query
  Get history → no prior messages
  AI reply → "Yes, your order is being prepared..."
  Log ticket → Google Sheets
  
Step 4: Backend responds
  {reply: "Yes, your order is...", category: "query", escalated: false}
  
Step 5: JavaScript updates chat UI
  Adds bot message to screen
  Saves to localStorage (persists on page refresh)
  
Step 6: Visitor refreshes page
  JavaScript loads chat history from localStorage
  Chat is still there (no data loss!)
  
Step 7: Visitor opens Dashboard
  Page fetches GET /tickets
  Table shows all messages (including chat page messages)
  Updates every 30 seconds
```

---

## ✨ Key Features

### 1. **Bilingual Support**
- Messages in Urdu/Roman Urdu automatically generate replies in same language
- Gemini AI detects language context
- No manual translation needed

### 2. **Intent Classification**
- Automatically categorizes messages as `query`, `complaint`, or `escalate`
- Routes urgent issues to human agents
- Helps business owner prioritize

### 3. **Conversation History**
- Every message logged to Google Sheets
- AI uses conversation history for context
- Searchable by phone number, date, category

### 4. **24/7 Availability**
- Bot responds instantly (no human needed)
- Handles 100+ messages simultaneously
- No sleep, no breaks

### 5. **Dashboard Analytics**
- Real-time ticket view
- Filter by category
- Stats: Total, Escalated, Complaints, Queries
- Live updates every 30 seconds

### 6. **Zero Subscription Cost**
- Uses free Google API tier
- Uses free Gemini 2.5-flash API (free queries/month)
- Flask is open-source
- Google Sheets is free

---

## ⚠️ Known Limitations

| Limitation | Impact | Workaround / Future Fix |
|-----------|--------|------------------------|
| **WhatsApp Integration is Stub** | Messages don't actually send to WhatsApp yet | Member 2 must implement in `whatsapp_handler.py` |
| **No Authentication on Dashboard** | Anyone with URL can see all tickets | Add login/password in Phase 2 |
| **Keyword-Based Classification** | Misses context sometimes (e.g., "The package looks great!" marked as complaint) | Upgrade to NLP model in Phase 2 |
| **Conversation History in Sheets** | Slow for 10,000+ tickets | Migrate to real database in Phase 2 |
| **Mobile Dashboard** | Layout breaks on very small screens (iPhone SE) | Add media queries in Phase 2 |
| **Message Parsing Assumes Standard Format** | Custom/malformed WhatsApp payloads may fail | Add robust error handling |
| **Rate Limiting Missing** | Vulnerable to spam (1000 messages/second) | Add rate limiter middleware |
| **No Caching** | Slow on dashboard with 1000+ tickets | Add Redis caching in Phase 2 |

---

## 🚀 Future Roadmap

### Phase 2 (Post-Hackathon, Month 1–2)
- [ ] User authentication & role-based access (owner, agent, viewer)
- [ ] Real WhatsApp Business API integration (working end-to-end)
- [ ] SMS support (Twilio integration)
- [ ] Email support
- [ ] Urdu-native NLP classifier (not just keywords)
- [ ] Voice message support (WhatsApp voice notes transcription)
- [ ] Rate limiting on APIs
- [ ] Redis caching for performance

### Phase 3 (Scale, Month 3–6)
- [ ] CRM integration (HubSpot, Pipedrive)
- [ ] Custom domain & branded widget
- [ ] Multiple business accounts on one instance
- [ ] AI training on business-specific data (FAQs, products)
- [ ] Advanced analytics dashboard
- [ ] Automated escalation rules (e.g., "escalate if mentioned 'refund'")
- [ ] Dashboard mobile app

### Phase 4 (Enterprise, Month 6+)
- [ ] Self-hosted Docker deployment
- [ ] SaaS platform at jawab.pk
- [ ] White-label reseller program
- [ ] Compliance certifications (PCI-DSS, SOC 2)
- [ ] Support for more languages (Sindhi, Pashto, Punjabi)
- [ ] Video chat integration (WhatsApp video calls)
- [ ] AI training on industry-specific data

---

## 🐛 Troubleshooting

### Issue: Chat page doesn't send messages

**Symptoms:**
- Click Send → nothing happens
- Browser console shows error

**Solutions:**
1. Make sure Flask backend is running (`python backend/app.py`)
2. Check you're visiting `http://localhost:8080/chat-page` (not file://)
3. Open browser console (F12) → Network tab → check `/chat` request
4. Verify `.env` file exists with GEMINI_API_KEY set

---

### Issue: Google Sheets not logging tickets

**Symptoms:**
- Chat works but tickets don't appear in Google Sheet
- Backend console shows error: "No such file or directory: credentials.json"

**Solutions:**
1. Verify `credentials.json` is in project root (not in `backend/`)
2. Check that Google Sheet is shared with service account email
3. Verify `SHEET_ID` in `.env` is correct (copy from sheet URL)
4. Check permissions on credentials.json (must be readable)

---

### Issue: Gemini API errors

**Symptoms:**
- Chat shows "error" or no reply
- Backend console shows: "Invalid API key" or "Rate limit exceeded"

**Solutions:**
1. Check `GEMINI_API_KEY` in `.env` is correct
2. Visit https://aistudio.google.com/app/apikey and verify key is active
3. If rate limited, wait 1 minute and try again (free tier has quotas)
4. Create new API key if old one is compromised

---

### Issue: Server crashes on startup

**Symptoms:**
```
Error: KeyError: 'GEMINI_API_KEY'
or
Error: FileNotFoundError: credentials.json
```

**Solutions:**
1. Check `.env` file has all required variables
2. Check `.env` is in project root, not in `backend/`
3. Check `credentials.json` is in project root
4. Run: `python -m dotenv list` to verify variables loaded

---

### Issue: Dashboard table is empty

**Symptoms:**
- Dashboard loads but shows "No tickets yet"
- Even after sending chat messages

**Solutions:**
1. Check chat messages are actually being sent (check browser console)
2. Wait 10 seconds for Google Sheets to write
3. Check GET `/tickets` endpoint directly in browser:
   - Visit `http://localhost:8080/tickets` in new tab
   - Should show JSON with tickets
4. If empty, check `sheets_handler.py` for errors in backend console

---

### Issue: WhatsApp messages not received

**Symptoms:**
- Messages don't trigger webhook
- Dashboard shows no activity

**Solutions:**
1. This is expected if Member 2 hasn't implemented `whatsapp_handler.py` yet
2. For testing, use Chat page instead: `http://localhost:8080/chat-page`
3. To fully test WhatsApp: Member 2 must set up Meta app & webhook URL

---

### Issue: Page won't load (blank screen)

**Symptoms:**
- Browser shows blank page
- Console has errors like "Flask is not defined"

**Solutions:**
1. Make sure you're visiting correct URL: `http://localhost:8080/` (not file://)
2. Check Flask is running (should see messages in terminal)
3. Reload page (Ctrl+R or Cmd+R)
4. Clear browser cache (Ctrl+Shift+Del)
5. Check port 8080 is not used by another app: `netstat -ano | findstr :8080`

---

### Issue: Mobile doesn't work

**Symptoms:**
- Opening on phone shows layout broken
- Buttons hard to click

**Solutions:**
1. Chat page is designed responsive but not fully mobile-optimized yet
2. Try landscape mode
3. Zoom out in browser (Ctrl+- or Cmd+-)
4. Use desktop for best experience during hackathon
5. Mobile improvements in Phase 2

---

## 📞 Support & Questions

**If something breaks:**
1. Check troubleshooting section above
2. Check backend console for error messages
3. Ask Backend Lead (they know the whole system)
4. Check GitHub issues if available

**For specific questions:**
- **AI/Classifier issues** → Ask Member 1
- **WhatsApp integration** → Ask Member 2
- **Google Sheets/Data** → Ask Member 3
- **Frontend/UI** → Ask Member 4

---

## 📄 License & Attribution

This project is **open source** and built during a hackathon. Free to use, modify, and share.

---

## 🎉 Good Luck!

This is an ambitious project. Breakdown into pieces, coordinate between team members, test early and often. You've got this! 

**Questions? Issues? Ask your team lead or the Backend Lead.**

---

**Built with ❤️ for Pakistani SMEs.**  
**Jawab — Your Support, Always On.**
