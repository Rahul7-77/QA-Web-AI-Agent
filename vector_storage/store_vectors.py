import faiss
import numpy as np

def store_in_faiss(embeddings, texts, url):
    """ Stores embeddings in FAISS with text and URL metadata. Uses cosine similarity rule """
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension) # Inner product for cosine similarity
    index.add(embeddings)
    return index, list(zip(texts, url))