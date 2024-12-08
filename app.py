from flask import Flask, render_template, request, jsonify
import os
from models.surfchad import get_surfchad_response
from models.finedchad import get_finedchad_response
from models.talkchad import get_talkchad_response

app = Flask(__name__)

# Default model to use
DEFAULT_MODEL = "TalkChad"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    selected_model = request.json.get("model", DEFAULT_MODEL)

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    api_key = os.getenv("HF_API_KEY")
    if not api_key:
        return jsonify({"error": "API key is missing. Please set HF_API_KEY."}), 500

    # Route to appropriate model
    if selected_model == "SurfChad":
        reply, source_url = get_surfchad_response(user_message, api_key)
        response = {"reply": reply, "source_url": source_url}
    elif selected_model == "FinedChad":
        reply = get_finedchad_response(user_message, api_key)
        response = {"reply": reply, "source_url": None}
    elif selected_model == "TalkChad":
        reply = get_talkchad_response(user_message, api_key)
        response = {"reply": reply, "source_url": None}
    else:
        response = {"error": "Invalid model selected."}

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
