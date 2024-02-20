from app.search import search
from app.analysis import analyze_articles
from app.summary import generate_summary
from app.schemas import *

from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

import json

from pydantic import BaseModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://searchengineapp-production.up.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello World"}


# For sending search results given query parameters query and language.
@app.get("/search", response_model=SearchResponse)
def get_search_results(query: Annotated[str, Query()], language: Annotated[str, Query()] = "en"):
    search_results = [rslt.url for rslt in search(query, language)]
    response = SearchResponse(results=search_results)
    return response


# For sending analysis of results given urls and query parameter language
@app.post("/analysis", response_model=AnalysisResponse)
def get_analysis(request: AnalysisRequest, language: Annotated[str, Query()] = "en"):
    named_entities = analyze_articles(request.urls, language)
    response = AnalysisResponse(named_entities=named_entities)
    print(response)
    return response


# For sending summary of given headlines and query parameter language
@app.post("/summary", response_model=SummaryResponse)
def get_summary(request: SummaryRequest, language: Annotated[str, Query()] = "en"):
    summary = generate_summary(request.headlines, request.topic, language)
    response = SummaryResponse(summary=summary)
    return response
