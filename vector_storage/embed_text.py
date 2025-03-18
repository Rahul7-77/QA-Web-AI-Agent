from huggingface_hub import InferenceClient
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

def embed_text(texts):
    """Embed texts into vector embeddings"""
    if not HF_TOKEN:
        raise ValueError("Hugging Face API token not found in .env")
    client = InferenceClient(token=HF_TOKEN)

    # Use feature-extraction task for embeddings
    response = client.feature_extraction(texts, model="sentence-transformers/all-MiniLM-L6-v2")
    embeddings = np.array(response)
    # Adjust shape
    if len(embeddings.shape) == 1:
        embeddings = embeddings[np.newaxis, :]
    return embeddings
