# 🤖 AI Chatbot Web App

A simple full-stack chatbot built with Flask and OpenAI, designed to run entirely from Google Colab. Supports a **$0 mock mode** that works without any API key.

---

## Features

- Chat interface with message history
- Four clickable sample prompts
- Flask backend wired to the OpenAI Chat Completions API
- **$0 mode** — falls back to local mock responses when no API key is set
- Public URL via ngrok (no server required)

---

## Project Structure

```
your_colab_project/
├── app.py                # Flask backend
├── mock_responses.json   # Local responses for $0 mode
└── templates/
    └── index.html        # Frontend (chat UI)
```

---

## Quickstart (Google Colab)

### 1. Install dependencies

```python
!pip install flask flask-cors openai pyngrok -q
```

### 2. Create the mock responses file

```python
%%writefile mock_responses.json
{
  "responses": [
    "I'm a mock chatbot response! Add your OpenAI API key to get real AI answers.",
    ...
  ]
}
```

### 3. Create the frontend and backend

Write `templates/index.html` and `app.py` (see source files).

### 4. Launch with ngrok

```python
from pyngrok import ngrok
import threading, subprocess, time

ngrok.set_auth_token("YOUR_NGROK_TOKEN")  # from dashboard.ngrok.com

def run_flask():
    subprocess.run(["python", "app.py"])

thread = threading.Thread(target=run_flask, daemon=True)
thread.start()
time.sleep(2)

ngrok.kill()  # clear any stale tunnels
public_url = ngrok.connect(5000)
print(f"🌐 Live at: {public_url}")
```

---

## Modes

### $0 Mode (default — no API key needed)

The app automatically runs in mock mode when no `OPENAI_API_KEY` environment variable is detected. Responses are served randomly from `mock_responses.json`.

```
⚠️  No OPENAI_API_KEY found — running in $0 mock mode.
```

### Live Mode (OpenAI API)

Set your API key before running the app:

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
```

Then restart the Flask app. The backend will use `gpt-3.5-turbo` and return real AI responses.

```
✅  OpenAI API key detected — running in live mode.
```

---

## API

### `POST /chat`

Sends the conversation history to the model and returns a reply.

**Request body:**
```json
{
  "messages": [
    { "role": "user", "content": "Hello!" }
  ]
}
```

**Response:**
```json
{
  "reply": "Hi! How can I help you today?"
}
```

---

## Requirements

| Package | Purpose |
|---|---|
| `flask` | Web server / backend |
| `flask-cors` | Allow frontend requests |
| `openai` | OpenAI API client |
| `pyngrok` | Expose localhost via public URL |

---

## Troubleshooting

**ngrok tunnel already online error (`ERR_NGROK_334`)**
Go to [dashboard.ngrok.com/endpoints](https://dashboard.ngrok.com/endpoints), delete the existing endpoint, then re-run the launch cell. Or call `ngrok.kill()` before `ngrok.connect()`.

**Authentication error (`ERR_NGROK_105`)**
Make sure you replaced `"YOUR_NGROK_TOKEN"` with your actual token from [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken).

**OpenAI API errors**
Verify your key is valid at [platform.openai.com/api-keys](https://platform.openai.com/api-keys) and that you have available credits.

---

## Resources

- [OpenAI API Docs](https://platform.openai.com/docs)
- [ngrok Dashboard](https://dashboard.ngrok.com)
- [Flask Docs](https://flask.palletsprojects.com)
