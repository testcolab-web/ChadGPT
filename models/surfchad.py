import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def search_and_scrape(query):
    logging.debug("Starting search_and_scrape with query: %s", query)
    search_url = f"https://www.google.com/search?q=site:islamqa.info+{query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        logging.debug("Search request successful: %s", response.url)
    except requests.RequestException as e:
        logging.error("Error during Google search: %s", e)
        return f"Error: Unable to perform Google search. Exception: {e}", None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract the first link
    for g in soup.find_all("div", class_="g"):
        link = g.find("a", href=True)
        if link and "islamqa.info" in link['href']:
            logging.debug("Found matching link: %s", link['href'])
            return None, link['href']
    
    logging.warning("No results found on islamqa.info for the query.")
    return "Error: No results found on islamqa.info for the query.", None

def scrape_content(url):
    logging.debug("Starting scrape_content with URL: %s", url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logging.debug("Content fetch successful: %s", response.url)
    except requests.RequestException as e:
        logging.error("Error fetching page content: %s", e)
        return f"Error: Unable to fetch the page. Exception: {e}"
    
    soup = BeautifulSoup(response.text, "html.parser")
    content_div = soup.find("div", class_="content")
    if not content_div:
        logging.warning("Content div not found on the page.")
        return "Error: Content not found in the page."
    
    logging.debug("Successfully extracted content from page.")
    return content_div.get_text(strip=True)

def summarize_content(content, api_key):
    logging.debug("Starting summarize_content. Content length: %d", len(content))
    endpoint = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        payload = {"inputs": content[:4096]}  # Increased token limit support
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        logging.debug("Summarization successful. Summary length: %d", len(result[0].get("summary_text", "")))
        return result[0].get("summary_text", "Error: Summary not found in response.")
    except requests.RequestException as e:
        logging.error("Error during summarization: %s", e)
        return f"Error: Summarization failed. Exception: {e}"
    except KeyError:
        logging.error("Unexpected summarization response format.")
        return "Error: Unexpected summarization response format."

def generate_response(summary, query, api_key):
    logging.debug("Starting generate_response. Summary length: %d", len(summary))
    endpoint = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {api_key}"}

    input_text = f"""
    Based on the context, provide a concise and direct answer to the question:
    Context: {summary}
    Question: {query}
    Answer in one short sentence, without explanation.
    """

    try:
        payload = {"inputs": input_text}
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        logging.debug("Response generation successful.")
        return result[0].get("generated_text", "Error: Generated text not found in response.")
    except requests.RequestException as e:
        logging.error("Error during response generation: %s", e)
        return f"Error: Response generation failed. Exception: {e}"
    except KeyError:
        logging.error("Unexpected response generation response format.")
        return "Error: Unexpected response generation format."

def get_surfchad_response(query, api_key):
    logging.info("Starting main function.")  # Replace with your Hugging Face API key

    # Search and scrape content
    error, link = search_and_scrape(query)
    if error:
        logging.error(error)
        print(error)
        return
    
    content = scrape_content(link)
    if "Error" in content:
        logging.error(content)
        print(content)
        return
    
    # Summarize content
    summary = summarize_content(content, api_key)
    if "Error" in summary:
        logging.error(summary)
        print(summary)
        return

    # Generate response
    response = generate_response(summary, query, api_key)
    logging.info("Generated response: %s", response)
    return response, link
