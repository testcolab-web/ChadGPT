import requests
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def get_finedchad_response(query, api_key):
    logging.debug("Processing query with FinedChad.")
    endpoint = "https://api-inference.huggingface.co/models/12sciencejnv/ChadGPT"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": query}

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get("generated_text", "No response generated.")
        else:
            logging.error(f"FinedChad API error: {response.status_code} - {response.text}")
            return f"Error: FinedChad API returned {response.status_code}. {response.text}"
    except Exception as e:
        logging.error(f"FinedChad mechanism failed: {e}")
        return f"Error: Unable to generate response due to {e}"
