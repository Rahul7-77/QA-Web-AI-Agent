import pytest
import sys
import os

# Add root directory to sys.path so imports work from tests/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from data_processing.scrape_web import scrape_web
from vector_storage.embed_text import embed_text
from vector_storage.store_vectors import store_in_faiss
from retrieval.semantic_search import search_vectors
from llm.question_answer import generate_answer

def test_scrape_web():
    # Check if it scrapes something
    contents = scrape_web("https://python.langchain.com/docs", max_pages=1)
    assert len(contents) > 0 
    assert "https" in contents[0][1]  

def test_embed_text():
    # Check if embedding works
    embeddings = embed_text(["This is a test"])
    assert len(embeddings) == 1  
    assert len(embeddings[0]) == 384  

def test_search_and_answer():
    # Test completelt
    contents = scrape_web("https://python.langchain.com/docs", max_pages=1)
    texts, urls = zip(*contents)
    embeddings = embed_text(texts)
    index, metadata = store_in_faiss(embeddings, texts, urls)
    results = search_vectors("What is LangChain?", index, metadata)
    answer, url = generate_answer("What is LangChain?", results)
    assert "sorry" not in answer.lower() 
    assert "https" in url 