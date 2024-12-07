import requests
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def get_refinedchad_response(query, api_key):
    endpoint = "https://api-inference.huggingface.co/models/12sciencejnv/ChadGPT"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": query}

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result[0].get("generated_text", "No response generated.")
    except Exception as e:
        logging.error(f"Error generating response from RefinedChad: {e}")
        return f"Error: Unable to generate response. {e}"
