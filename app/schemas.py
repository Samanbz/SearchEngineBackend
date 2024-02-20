from pydantic import BaseModel
from typing import List, Optional


# Schema for articles included in search results response
class Article(BaseModel):
    title: str
    author: Optional[str]  # To allow for incomplete data
    source: Optional[str]  # To allow for incomplete data
    published_at: str  # Isoformat


# Schema for a single search result
class SearchResult(BaseModel):
    article: Article
    url: str
    image_url: Optional[str]  # To allow for incomplete data


# Schema for search response
class SearchResponse(BaseModel):
    results: list[SearchResult]


# Schema for an Analysis request
class AnalysisRequest(BaseModel):
    # List of urls to scrape and analyze
    urls: List[str]


# Schema for a single Named Entity
class NamedEntity(BaseModel):
    name: str
    label: str
    frequency: int


# Schema for an Analysis response
class AnalysisResponse(BaseModel):
    named_entities: List[NamedEntity]


# Schema for a Summary request
class SummaryRequest(BaseModel):
    # List of headlines to summarize
    headlines: List[str]
    # Topic in relation to which the summary is generated (search query)
    topic: str


# Schema for a Summary response
class SummaryResponse(BaseModel):
    summary: str
