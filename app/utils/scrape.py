from bs4 import BeautifulSoup
import requests


# Given a url of a website, returns the text content of the article
def scrape_article(url: str):
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Find all <p> elements
    paragraphs = soup.find_all('p')

    # Extract the text from all <p> elements
    paragraphs = [p.get_text() for p in paragraphs]

    # Remove paragraphs with less than 20 words
    paragraphs = [p for p in paragraphs if len(p.split(" ")) > 20]

    # Join all paragraphs into a single string
    text_content = " ".join(paragraphs)

    return text_content
