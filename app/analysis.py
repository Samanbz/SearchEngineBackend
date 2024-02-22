import numpy as np
import pandas as pd

from .utils.scrape import scrape_article
from .schemas import NamedEntity
import spacy

# Words that appear most frequently in the language and should be ignored
common_words = {
    "en": [
        'below', 'could', 'by', 'been', 'such', 'own', 'not', 'more', 'or', 'two',
        'was', 'don', 'no', 'use', 'both', 'these', 'will', 'a', 'she', 'over', 'like',
        'until', 'I', 'we', 'so', 'as', 'now', 'work', 'know', 'me', 'against', 'again',
        'think', 'one', 'if', 'further', 'who', 's', 'other', 'were', 'here', 'first',
        'above', 'should', 'up', 'where', 'they', 'off', 'are', 'our', 'had', 'same',
        'too', 'any', 'it', 'there', 'down', 'see', 'is', 'then', 'during', 'the',
        'come', 'while', 'between', 'few', 'of', 't', 'back', 'would', 'how', 'what',
        'just', 'to', 'him', 'day', 'give', 'which', 'once', 'has', 'be', 'us', 'some',
        'for', 'about', 'year', 'my', 'way', 'why', 'also', 'does', 'each', 'an',
        'but', 'when', 'because', 'say', 'make', 'nor', 'good', 'into', 'than', 'did',
        'their', 'in', 'look', 'get', 'that', 'all', 'this', 'and', 'from', 'people',
        'through', 'out', 'under', 'with', 'well', 'on', 'after', 'you', 'his', 'at',
        'most', 'do', 'want', 'he', 'can', 'very', 'even', 'before', 'new', 'go',
        'her', 'them', 'your', 'only', 'its', 'take', 'have', 'time', 'said', '-', 'mr',
        'i', 'told', 'says', 'read', 'among', 'may', '–', 'including', 'used', '—',
        'found', 'it’s', 'wired', 'dont', 'isnt', 'many', 'per', 'going', 'every', 'being',
        'still', 'really', 'much', 'those', 'that', 'thats', 'last', 'something', 'nothing',
        'things', 'thing', 'best', 'top', 'bbc', 'york', 'times', '--', 'next'],
    "de": [
        'das', 'sind', 'du', 'hat', 'nicht', 'in', 'mehr', 'einen', 'wir', 'auf',
        'es', 'über', 'sich', 'sehr', 'ja', 'nach', 'ist', 'ein', 'haben'
        'wenn', 'an', 'war', 'uns', 'von', 'den', 'würde', 'kann', 'sein', 'alle',
        'der', 'und', 'dass', 'mal', 'er', 'wird', 'man', 'bei', 'zum', 'ihr', 'noch',
        'eine', 'hier', 'gut', 'dann', 'ich', 'die', 'so', 'oder', 'habe', 'wie', 'Sie',
        'zu', 'werden', 'auch', 'mit', 'nur', 'aber', 'jetzt', 'um', 'für', 'aus', 'im',
        'des', 'sie', 'dem', '', 'am', 'sagte', '+++', 'sei', 'zwei', 'vor', 'gegen',
        'einem', 'als', 'worden', 'einer', 'seien', 'zur', 'durch', 'ihre', 'ihren',
        'ihrem', 'ihren', 'ihres', 'können'
    ]
}


# Given a list of urls of the search results, return a list of the accumulitive text content of all articles
def get_total_text_content(urls: list[str]) -> str:
    return " ".join([scrape_article(url) for url in urls])


# Spacy models according to the given language
spacy_model = {
    "en": "en_core_web_sm",
    "de": "de_core_news_sm",
}


# Given a large text, returns a list of all named entities using natural language processing
def get_named_entities(text_content: str, language: str):
    nlp = spacy.load(spacy_model[language])
    doc = nlp(text_content)
    named_entities = doc.ents

    return named_entities


# Given a list of named entities, sorts them by frequency and returns them with labels
def process_named_entities(named_entities: list[spacy.tokens.Span], language: str) -> list[NamedEntity]:

    labeled_named_entities = pd.Series(
        [(ent.text, ent.label_) for ent in named_entities])
    #
    named_entity_frequencies = labeled_named_entities.value_counts().to_dict()
    print(named_entity_frequencies)

    # Filters out all named entities that are common words
    filtered_named_entities = {
        k: v for k, v in named_entity_frequencies.items() if k[0] not in common_words[language]}

    # Filters out all named entities that showed up less than 5 times (no particular reason for the choice of the value of this condition, could be any number)
    relevant_named_entities = {k: v for k,
                               v in filtered_named_entities.items() if v > 2}

    # Parses the named entity dictionary into a list of NamedEntity objects
    object_named_entities = np.array([
        NamedEntity(name=k[0], label=k[1], frequency=v) for k, v in relevant_named_entities.items()])

    # Computes the sorted indices based on frequency
    sorted_indices = np.argsort(
        [ne.frequency for ne in object_named_entities])

    # Sorts the named entities by frequency in reverse order
    sorted_named_entities = object_named_entities[sorted_indices][::-1]

    return sorted_named_entities


# Given a list of urls of articles, returns a sorted list of named entities mentioned in them.
def analyze_articles(urls: list[str], language: str = "en") -> list[NamedEntity]:
    text_content = get_total_text_content(urls)
    named_entities = get_named_entities(text_content, language)
    processed_named_entities = process_named_entities(named_entities, language)
    return processed_named_entities
