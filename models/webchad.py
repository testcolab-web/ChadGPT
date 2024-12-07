import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def search_and_scrape(query):
    search_url = f"https://www.google.com/search?q=site:islamqa.info+{query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error during Google search: {e}")
        return None, f"Error: Unable to search. {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    for result in soup.find_all("div", class_="g"):
        link = result.find("a", href=True)
        if link and "islamqa.info" in link["href"]:
            return link["href"], None

    return None, "No relevant link found on islamqa.info."

def scrape_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching page content: {e}")
        return None, f"Error: Unable to fetch content. {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", class_="content")
    if not content:
        return None, "Content not found on the page."

    return content.get_text(strip=True), None

def summarize_content(content, api_key):
    endpoint = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": content[:4096]}

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()[0]["summary_text"], None
    except Exception as e:
        logging.error(f"Summarization failed: {e}")
        return None, f"Error: Summarization failed. {e}"

def get_webchad_response(query, api_key):
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