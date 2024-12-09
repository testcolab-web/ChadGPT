import requests
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def get_talkchad_response(query, api_key):
    logging.debug("Processing query with TalkChad.")
    endpoint = "https://api-inference.huggingface.co/models/12sciencejnv/TalkGPT"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": query}

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "No response generated.")
            else:
                logging.error("Unexpected response format.")
                return "Error: Unexpected response format."
        else:
            logging.error(f"TalkChad API error: {response.status_code} - {response.text}")
            return f"Error: TalkChad API returned {response.status_code}. {response.text}"
    except Exception as e:
        logging.error(f"TalkChad mechanism failed: {e}")
        return f"Error: Unable to generate response due to {e}"
