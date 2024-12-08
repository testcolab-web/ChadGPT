import requests
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def get_blenderchad_response(query, api_key):
    """Fetch a conversational response from BlenderBot-400M-distill."""
    endpoint = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": query}

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        logging.debug(f"BlenderBot response: {result}")
        # Extract generated response
        return result[0].get("generated_text", "Sorry, I couldn't generate a response.")
    except requests.exceptions.RequestException as e:
        logging.error(f"BlenderBot API error: {e}")
        return "An error occurred while processing your request."
