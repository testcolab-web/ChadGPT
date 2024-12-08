import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def get_surfchad_response(query, api_key):
    # Step 1: Perform search
    search_url = f"https://www.google.com/search?q=site:islamqa.info+{query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error during search: {e}")
        return f"Error: Unable to perform search. {e}", None

    soup = BeautifulSoup(response.text, "html.parser")
    link = None

    # Extract the first relevant link
    for result in soup.find_all("div", class_="g"):
        link_tag = result.find("a", href=True)
        if link_tag and "islamqa.info" in link_tag["href"]:
            link = link_tag["href"]
            break

    if not link:
        return "No relevant link found on islamqa.info.", None

    # Step 2: Scrape content
    try:
        content_response = requests.get(link, headers=headers)
        content_response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching content from {link}: {e}")
        return f"Error: Unable to fetch content. {e}", None

    content_soup = BeautifulSoup(content_response.text, "html.parser")
    content_div = content_soup.find("div", class_="content")

    if not content_div:
        return "Content not found on the page.", None

    content = content_div.get_text(strip=True)

    # Step 3: Summarize content
    summarization_endpoint = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    summarization_headers = {"Authorization": f"Bearer {api_key}"}
    summarization_payload = {"inputs": content[:4096]}  # Truncate if too long

    try:
        summarization_response = requests.post(
            summarization_endpoint, headers=summarization_headers, json=summarization_payload
        )
        summarization_response.raise_for_status()
        summary = summarization_response.json()[0]["summary_text"]
    except Exception as e:
        logging.error(f"Summarization error: {e}")
        return f"Error: Unable to summarize content. {e}", None

    return summary, link
