import os
import json
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- Detect mode ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
USE_MOCK = not OPENAI_API_KEY

if USE_MOCK:
    print("⚠️  No OPENAI_API_KEY found — running in $0 mock mode.")
    with open("mock_responses.json") as f:
        MOCK_DATA = json.load(f)
else:
    print("✅  OpenAI API key detected — running in live mode.")
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    if USE_MOCK:
        # $0 mode: return a random mock response
        reply = random.choice(MOCK_DATA["responses"])
    else:
        # Live mode: call OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = completion.choices[0].message.content

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=False)
