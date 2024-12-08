from flask import Flask, render_template, request, jsonify
import os
from models.webchad import get_webchad_response
from models.refinedchad import get_refinedchad_response
from models.blenderchad import get_blenderchad_response
import logging

# Flask application setup
app = Flask(__name__)

# Environment variables for API keys
HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY")

# Default model to use
DEFAULT_MODEL = "SurfChad"

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    selected_model = request.json.get("model", DEFAULT_MODEL)

    # Validate input
    if not user_message:
        return jsonify({"error": "Message is empty or invalid."}), 400

    logging.debug(f"Received message: {user_message}")
    logging.debug(f"Selected model: {selected_model}")

    # Route to the appropriate model
    try:
        if selected_model == "SurfChad":
            reply, source_url = get_webchad_response(user_message, HUGGINGFACE_API_KEY)
        elif selected_model == "FinedChad":
            reply = get_refinedchad_response(user_message, HUGGINGFACE_API_KEY)
            source_url = None
        elif selected_model == "TalkChad":
            reply = get_blenderchad_response(user_message, HUGGINGFACE_API_KEY)
            source_url = None
        else:
            return jsonify({"error": "Invalid model selected."}), 400

        # Provide feedback for no response or error
        if not reply:
            reply = "No response generated. Please try again."
        return jsonify({"reply": reply, "source_url": source_url})
    except Exception as e:
        logging.error(f"Error processing the request: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
