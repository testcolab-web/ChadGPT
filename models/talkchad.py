import requests
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def get_talkchad_response(query, api_key):
    logging.debug("Processing query with TalkChad.")
    endpoint = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": query}

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("generated_text", "No response generated.")
    except Exception as e:
        logging.error(f"TalkChad error: {e}")
        return f"Error: Unable to generate response. {e}"
