import json
import urllib.request
import urllib.error
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from .models import DocRecord

def get_embedding(text: str, api_base: str, model: str) -> Optional[np.ndarray]:
    """Retrieves a vector embedding for the given text from a local OpenAI-compatible API."""
    payload = {
        "model": model,
        "input": text
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{api_base.rstrip('/')}/embeddings", data=data)
    req.add_header("Content-Type", "application/json")
    
    try:
        # 120s timeout for large embeddings
        with urllib.request.urlopen(req, timeout=120) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return np.array(res_data["data"][0]["embedding"])
    except urllib.error.HTTPError as he:
        print(f"Embedding request failed (HTP {he.code}): {he.reason}. Check if '{model}' supports embeddings and if the server has them enabled.")
        return None
    except Exception as e:
        print(f"Embedding request failed: {e}")
        return None

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Calculates cosine similarity between two vectors."""
    dot = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(dot / (norm1 * norm2))

def calculate_semantic_similarity_matrix(docs: List[DocRecord], api_base: str, model: str) -> Tuple[pd.DataFrame, Dict[str, np.ndarray]]:
    """
    Computes a semantic similarity matrix across corpora by averaging document embeddings.
    """
    corpus_embeddings: Dict[str, List[np.ndarray]] = {}
    doc_embeddings: Dict[str, np.ndarray] = {}
    
    print(f"Fetching semantic embeddings for {len(docs)} documents...")
    for d in docs:
        # Use first 2000 words to avoid context window limits or slow API
        sample_text = " ".join(d.word_tokens[:2000])
        emb = get_embedding(sample_text, api_base, model)
        
        if emb is not None:
            doc_embeddings[d.doc_id] = emb
            if d.corpus not in corpus_embeddings:
                corpus_embeddings[d.corpus] = []
            corpus_embeddings[d.corpus].append(emb)
            
    if not corpus_embeddings:
        return pd.DataFrame(), {}
        
    # Calculate corpus centroids
    labels = sorted(corpus_embeddings.keys())
    centroids = {l: np.mean(corpus_embeddings[l], axis=0) for l in labels}
    
    # Build similarity matrix
    n = len(labels)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i, j] = cosine_similarity(centroids[labels[i]], centroids[labels[j]])
            
    df = pd.DataFrame(matrix, index=labels, columns=labels)
    return df, centroids
