import numpy as np
from vector_storage.embed_text import embed_text


def search_vectors(query, index, metadata, k=1):
    """ Search for top-k relevant content using cosine similarity """
    query_embedding = embed_text([query])
    if len(query_embedding.shape) == 1:
        query_embedding = query_embedding[np.newaxis, :]
    query_embedding = query_embedding/np.linalg.norm(query_embedding, axis=1, keepdims=True) # normalise query embedding for cosine similarity
    distances, indices = index.search(query_embedding, k)

    result_vectors = []
    for index, distance in zip(indices[0], distances[0]):
        if index!=-1 and distance >= 0.1:
            text, url = metadata[index]
            result_vectors.append((text, url, distance))

    return result_vectors if result_vectors else [(None, None, None)] 