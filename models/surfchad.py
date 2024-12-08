import requests
from bs4 import BeautifulSoup
import logging
from functools import lru_cache

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

@lru_cache(maxsize=50)
def search_and_scrape(query):
    logging.debug(f"Performing search for: {query}")
    search_url = f"https://www.google.com/search?q=site:islamqa.info+{query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Search error: {e}")
        return None, f"Error: Unable to search. {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    for result in soup.find_all("div", class_="g"):
        link = result.find("a", href=True)
        if link and "islamqa.info" in link["href"]:
            return link["href"], None

    return None, "No relevant link found."

def scrape_content(url):
    logging.debug(f"Fetching content from: {url}")
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Content fetch error: {e}")
        return None, f"Error: Unable to fetch content. {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", class_="content")
    if not content:
        return None, "Content not found."

    return content.get_text(strip=True), None

def summarize_content(content, api_key):
    logging.debug("Summarizing content...")
    endpoint = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": content[:4096]}

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()[0]["summary_text"], None
    except Exception as e:
        logging.error(f"Summarization error: {e}")
        return None, f"Error: Summarization failed. {e}"

def get_surfchad_response(query, api_key):
    url, error = search_and_scrape(query)
    if error:
        return error, None

    content, error = scrape_content(url)
    if error:
        return error, None

    summary, error = summarize_content(content, api_key)
    if error:
        return error, None

    return summary, url
