from .schemas import SearchResult, Article

from dotenv import load_dotenv
from datetime import datetime, timedelta

import os
import requests
import time
import numpy as np

load_dotenv()

API_KEY = os.environ.get('NEWS_API_KEY')
url = 'https://newsapi.org/v2/everything'


# Parses the response from the News API into the SearchResult schema
def parse_result(results: list[dict]):
    output = []
    for result in results:
        title = result['title']
        author = result['author']
        source = result['source']['name']
        published_at = result['publishedAt']
        url = result['url']
        image_url = result['urlToImage']

        article = Article(
            title=title,
            author=author,
            source=source,
            published_at=published_at
        )

        search_result = SearchResult(
            article=article,
            url=url,
            image_url=image_url
        )

        output.append(search_result)

    return output


# Fetches the results from the News API as JSON objects
def fetch_results(search_query: str, language: str) -> list[dict]:
    global url, API_KEY

    params = {
        'q': search_query,
        'apiKey': API_KEY,
        'from': datetime.now().date() - timedelta(weeks=4),
        'to': datetime.now().date(),
        'language': language,
        'pageSize': 5,
    }

    response = requests.get(url, params=params)
    print(response.status_code)
    results = np.array(response.json()['articles'])

    return results


# Given a query, returns a list of SearchResults objects
def search(search_query: str, language: str = "en") -> list[SearchResult]:
    results = fetch_results(search_query, language)
    return parse_result(results)
