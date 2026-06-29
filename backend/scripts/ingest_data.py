import os
import json
import numpy as np
from google import genai
from dotenv import load_dotenv

load_dotenv()

# We need to ensure we run this from the backend root or adjust paths.
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "trusted_sources.json")
VECTOR_STORE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "vector_store.json")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str) -> list:
    """
    Mock embedding generator for MVP since AI Studio key lacks text-embedding-004.
    Generates a deterministic 128-dimensional vector using text hashing.
    """
    np.random.seed(abs(hash(text)) % (2**32))
    vec = np.random.rand(128)
    return (vec / np.linalg.norm(vec)).tolist()

def ingest_data():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    print(f"Loaded {len(documents)} documents. Starting embedding generation...")
    
    vector_store = []
    
    for idx, doc in enumerate(documents):
        # We can embed the concatenation of title and text for better context
        content_to_embed = f"Title: {doc.get('title', '')}\nContent: {doc.get('text', '')}"
        
        try:
            print(f"Embedding document {idx + 1}/{len(documents)}: {doc.get('title')}")
            embedding = get_embedding(content_to_embed)
            
            # Store the original document plus the embedding
            doc_record = doc.copy()
            doc_record["embedding"] = embedding
            vector_store.append(doc_record)
            
        except Exception as e:
            print(f"Failed to embed document '{doc.get('title')}': {e}")
            
    # Save the vector store
    os.makedirs(os.path.dirname(VECTOR_STORE_FILE), exist_ok=True)
    with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(vector_store, f, indent=2)
        
    print(f"Successfully saved {len(vector_store)} vectors to {VECTOR_STORE_FILE}")

if __name__ == "__main__":
    ingest_data()
