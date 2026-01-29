import collections
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
from .models import DocRecord

def calculate_burrows_delta(docs: List[DocRecord], mfw_limit: int = 150) -> Tuple[pd.DataFrame, List[str]]:
    """
    Computes Burrows' Delta distance matrix between all unique corpora in the docs list.
    
    Algorithm:
    1. Identify Top N Most Frequent Words (MFW) across the entire dataset.
    2. Calculate the relative frequency (%) of each MFW in every document.
    3. Calculate the Mean and Standard Deviation for each MFW across all documents.
    4. Convert relative frequencies into Z-scores: (freq - mean) / std.
    5. Compute the Manhattan Distance (Delta) between the average Z-score vectors of each corpus.
    """
    if not docs or mfw_limit < 1:
        return pd.DataFrame(), []

    # 1. Build master MFW list
    all_tokens = []
    for d in docs:
        all_tokens.extend([t.lower() for t in d.word_tokens])
    
    if not all_tokens:
        return pd.DataFrame(), []
        
    counts = collections.Counter(all_tokens)
    mfw = [word for word, count in counts.most_common(mfw_limit)]
    
    # 2. Get relative frequencies per document
    doc_data = []
    for d in docs:
        d_total = len(d.word_tokens)
        if d_total == 0: continue
        d_counts = collections.Counter([t.lower() for t in d.word_tokens])
        row = {w: (d_counts[w] / d_total) for w in mfw}
        row['_corpus'] = d.corpus
        doc_data.append(row)
    
    if not doc_data:
        return pd.DataFrame(), mfw
        
    df_freqs = pd.DataFrame(doc_data)
    
    # 3 & 4. Standardize to Z-scores
    for w in mfw:
        mu = df_freqs[w].mean()
        sigma = df_freqs[w].std()
        if sigma == 0 or np.isnan(sigma): 
            df_freqs[w] = 0.0
        else:
            df_freqs[w] = (df_freqs[w] - mu) / sigma
            
    # 5. Calculate Corpus Centroids and Delta Matrix
    centroids = df_freqs.groupby('_corpus')[mfw].mean()
    labels = centroids.index.tolist()
    n = len(labels)
    delta_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            # Delta is the average absolute difference of Z-scores
            diff = np.abs(centroids.iloc[i] - centroids.iloc[j])
            delta_matrix[i, j] = diff.mean()
            
    delta_df = pd.DataFrame(delta_matrix, index=labels, columns=labels)
    return delta_df, mfw
