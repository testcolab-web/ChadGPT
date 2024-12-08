from flask import Flask, render_template, request, jsonify
import os
from models.surfchad import get_surfchad_response  # Updated model name
from models.finedchad import get_finedchad_response  # Updated model name
from models.talkchad import get_talkchad_response  # New conversational model

app = Flask(__name__)

# Environment variables for API keys
HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY")

# Default model to use
DEFAULT_MODEL = "WebChad"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    selected_model = request.json.get("model", DEFAULT_MODEL)

    if not user_message or len(user_message.strip()) == 0 or len(user_message) > 500:
        return jsonify({"error": "Invalid input. Please provide a valid message."}), 400

    try:
        if selected_model == "SurfChad":
            reply, source_url = get_surfchad_response(user_message, HUGGINGFACE_API_KEY)
            response = {"reply": reply, "source_url": source_url}
        elif selected_model == "FinedChad":
            reply = get_finedchad_response(user_message, HUGGINGFACE_API_KEY)
            response = {"reply": reply}
        elif selected_model == "BlenderChad":
            reply = get_blenderchad_response(user_message, HUGGINGFACE_API_KEY)
            response = {"reply": reply}
        else:
            response = {"error": "Invalid model selected."}
    except Exception as e:
        response = {"error": f"An error occurred: {str(e)}"}

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
