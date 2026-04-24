# MindEase — AI Mental Health Assessment

A simple AI-powered mental health assessment web app using voice and text input, built with Flask and Claude AI.

---

## Project Structure

```
mental-health-app/
├── app.py               ← Flask backend (API routes)
├── requirements.txt     ← Python dependencies
├── .env                 ← Your API key (never commit this)
└── templates/
    └── index.html       ← Full frontend UI
```

---

## Setup & Run in VS Code

### Step 1 — Prerequisites
- Python 3.9+ installed
- pip installed
- VS Code installed

### Step 2 — VS Code Extensions (install from Extensions panel)
- **Python** (by Microsoft) — ms-python.python
- **Pylance** (by Microsoft) — ms-python.vscode-pylance
- **REST Client** (optional, for API testing) — humao.rest-client

### Step 3 — Clone / Open Project
Open the `mental-health-app` folder in VS Code:
```
File → Open Folder → select mental-health-app
```

### Step 4 — Create Virtual Environment
Open VS Code Terminal (Ctrl + `) and run:
```bash
python -m venv venv
```

Activate it:
- Windows:  `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### Step 5 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 6 — Add Your API Key
Edit the `.env` file and replace with your real key:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
```
Get your key from: https://console.anthropic.com

### Step 7 — Load .env (update app.py if needed)
Add this at the top of app.py if not already there:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Step 8 — Run the App
```bash
python app.py
```

You'll see:
```
* Running on http://127.0.0.1:5000
```

### Step 9 — Open in Browser
Go to: **http://localhost:5000**

---

## Features
- 💬 Text chat with AI mental health assistant
- 🎙️ Voice input (uses browser Web Speech API)
- 📊 Full assessment report with wellbeing score
- 🔄 Reset and start a new session anytime

## Notes
* Voice input functionality works best in modern browsers such as Chrome or Edge.
* The chatbot uses an external AI language model via API to generate conversational responses and perform mental health assessment.
* This application is developed for educational and awareness purposes only.
* This system is not a substitute for professional mental health care, diagnosis, or treatment.

