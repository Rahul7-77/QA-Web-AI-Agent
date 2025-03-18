from data_processing.scrape_web import scrape_web
from vector_storage.embed_text import embed_text
from vector_storage.store_vectors import store_in_faiss
from retrieval.semantic_search import search_vectors
from llm.question_answer import setup_llm, generate_answer
from utils.helper import is_valid_url, normalize_url
from dotenv import load_dotenv
import os
import time

load_dotenv()

def main():
    if not os.getenv("HF_TOKEN") or not os.getenv("GROQ_API_KEY"):
        print("Please set HF_TOKEN and GROQ_API_KEY in your .env file.")
        return
    
    url = input("Enter website URL (e.g, https://www.pulsegen.io/)\n").strip()
    
    if not is_valid_url(url):
        print("Invalid URL format. please use https://example.com")
    
    start_time = time.time()
    print("Scrapping and indexing web content....(This may take a while)")
    contents = scrape_web(url)
    print(f"Scraped {len(contents)} pages in {time.time() - start_time:.2f} seconds:")
    
    if not contents or contents[0][0] == "No content found in URL.":
        print(f"Failed tp scrape {url}. Check URL or try another")
    
    texts, urls = zip(*contents)
    print("Generating embeddings...")
    embeddings = embed_text(texts)
    print(f"Embeddings generated in {time.time() - start_time:.2f} seconds.")

    print("Indexing in FAISS...")
    index, metadata = store_in_faiss(embeddings, texts, urls)
    print(f"Indexed in {time.time() - start_time:.2f} seconds.")

    #Starts queries
    print("\nReady for your questions. (type 'exit' to quit)...")
    while True:
        query = input("> ").strip()
        if query.lower() == "exit":
            break
        if not query:
            print("Please enter a question")
            continue

        query_start = time.time()
        results = search_vectors(query, index, metadata)
        answer, source_url = generate_answer(query, results)
        print(f"Answer : {answer}")
        if source_url:
            print(f"Source URL : {source_url}")
        print(f"Query processed in {time.time() - query_start:.2f} seconds\n")
        print()
    

if __name__ == "__main__":
    main()