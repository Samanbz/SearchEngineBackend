---
title: News Search Engine
description: FastAPI server that given a query, returns a list of related news articles including a summary and analysis. 
tags:
  - FastAPI
  - Spacy (NER)
  - OpenAI (Text Generation)
  - BS4 (Web Scraping)
---

# What it does 

### Search
- Given a search query, using the NEWS API from https://newsapi.org/, returns a list of News articles from various sources.
- The received JSON is then parsed into Pydantic schemas for simple data validation.

### Analysis
- Given a list of URLs of articles:
  - All relevant paragraphs in each article are scraped from the web using BeautifulSoup, then joined together. (For now, due to the server being very basic, not all articles are scraped, but the first few, any more articles and the server would crash every time, this nevertheless establishes a sufficient list of keyword relevant to the topic)
  - The total text content of all articles is then anlayzed using Named Entity Recognition Models provided by Spacy, and a list of all named entities and their label is computed.
  - This list is then further processed into a list of unique named entities and their number of occurences (frequency).
  - The process takes relatively long (mostly because of the web-scraping), which is why the named entities are not computed using the search query, but using the URLs. The client sends a request for the search results (this is responded to pretty fast) and displays it, it then extracts the URLs of the articles it received and sends another request for their analysis.
 
### Summary
- Given a list of headlines of articles, using the OpenAI API and their LLMs, a brief summary of the headlines is generated.
- Again for optimization reasons, this is not computed using the query, but using the headlines, which also allows for more modularity and simpler error handling and testing.

# How it can be improved
- Both the NEWS API and the OpenAI API allow for only a limited amount of requests made per account (Yes, I'm using the free tier). This is why I would suggest not making a lot of requests per day (NEWS API allows for 100 requests per day, OpenAI allows only some per account regardless of time).
- All functions of the server are made to work with English and German search queries (this must always be specified as a query parameter as "en" or "de"), but the client has not yet been adapted to accomodate this feature.
- It would be a good idea to add unit tests, It would have saved a lot of headaches during production.
- I did not add a rate limiter to the API endpoints, only added a feature to disable the seach input on the client while requests where still being processed on the server. Rate limiters would also be a useful addition.
- Most of the error handling is done on the client, so some rigid error handling on this app might not be a terrible idea either.  


## Reference to what I used
- FastAPI: https://fastapi.tiangolo.com/
- Uvicorn ASGI server: https://www.uvicorn.org/
- NEWS API: https://newsapi.org/
- OpenAI API: https://platform.openai.com/docs/api-reference
- Spacy NER Models: https://spacy.io/universe/project/video-spacys-ner-mode
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
- other: pandas, numPy
