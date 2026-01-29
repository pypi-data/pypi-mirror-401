import statistics
import collections
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Sequence, Tuple, Optional
from stylo_metrix import StyloMetrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from .models import ChunkRecord
from .loaders import tokenize_words

DEFAULT_FUNCTION_WORDS = [
    "the","of","and","to","a","in","that","is","for","it","on","with","as","was","are",
    "be","at","by","this","from","or","an","which","but","not","have","has","had","they",
    "you","we","i","he","she","his","her","their","our","its","will","would","can","could",
    "should","may","might","do","does","did","so","if","than","then","there","here"
]

def mattr(tokens: Sequence[str], window: int = 500) -> float:
    n = len(tokens)
    if n == 0:
        return float("nan")
    if n <= window:
        return len(set(t.lower() for t in tokens)) / n
    ratios = []
    for i in range(0, n - window + 1):
        w = tokens[i:i+window]
        ratios.append(len(set(t.lower() for t in w)) / window)
    return float(sum(ratios) / len(ratios))

def yules_k(tokens: Sequence[str]) -> float:
    """Yule's Characteristic K (lexical diversity signal)."""
    if not tokens: return float("nan")
    tokens = [t.lower() for t in tokens]
    n = len(tokens)
    freqs = collections.Counter(tokens)
    # m1 = sum(f^1 * V_f), which is just N
    # m2 = sum(f^2 * V_f)
    m2 = sum(f**2 for f in freqs.values())
    if n <= 1: return float("nan")
    return 10000.0 * (m2 - n) / (n**2)

def hapax_legomena_rate(tokens: Sequence[str]) -> float:
    """Rate of words appearing only once."""
    if not tokens: return 0.0
    freqs = collections.Counter(tokens)
    hapax = sum(1 for f in freqs.values() if f == 1)
    return hapax / len(tokens)

def punctuation_counts(text: str) -> Dict[str, int]:
    return {
        "commas": text.count(","),
        "semicolons": text.count(";"),
        "colons": text.count(":"),
        "question_marks": text.count("?"),
        "exclamation_marks": text.count("!"),
        "hyphens": text.count("-"),
        "em_dashes": text.count("—") + text.count("--"),
        "ellipses": text.count("...") + text.count("…"),
        "quotes_double": text.count('"'),
        "quotes_single": text.count("'"),
        "parentheses": text.count("(") + text.count(")"),
    }

def compute_metrics_for_text(word_tokens: List[str], sentences: List[str], raw_text_for_punct: str,
                             function_words: Sequence[str], mattr_window: int) -> Dict[str, float]:
    n_words = len(word_tokens)
    n_sents = len(sentences) if sentences else 0

    if n_words == 0:
        return {
            "word_count": 0,
            "unique_word_count": 0,
            "avg_word_len": float("nan"),
            "mattr": float("nan"),
            "yules_k": float("nan"),
            "hapax_rate": 0.0,
            "sentence_count": n_sents,
            "avg_sentence_len": float("nan"),
            "sentence_len_sd": float("nan"),
            "commas_per_sentence": float("nan"),
            "semicolons_per_sentence": float("nan"),
            "commas_per_1000w": float("nan"),
            "semicolons_per_1000w": float("nan"),
            **{f"fw_{fw}": float("nan") for fw in function_words},
        }

    lower_tokens = [t.lower() for t in word_tokens]
    unique = len(set(lower_tokens))
    avg_word_len = sum(len(t) for t in word_tokens) / n_words
    
    m = mattr(lower_tokens, window=mattr_window)
    yk = yules_k(lower_tokens)
    hapax = hapax_legomena_rate(lower_tokens)

    sent_lens = []
    if n_sents > 0:
        for s in sentences:
            st = tokenize_words(s)
            if st:
                sent_lens.append(len(st))
    avg_sent_len = float(sum(sent_lens) / len(sent_lens)) if sent_lens else float("nan")
    sent_sd = float(statistics.pstdev(sent_lens)) if len(sent_lens) >= 2 else float("nan")

    p = punctuation_counts(raw_text_for_punct)
    commas = p["commas"]
    semis = p["semicolons"]

    out = {
        "word_count": n_words,
        "unique_word_count": unique,
        "avg_word_len": avg_word_len,
        "mattr": m,
        "yules_k": yk,
        "hapax_rate": hapax,
        "sentence_count": n_sents,
        "avg_sentence_len": avg_sent_len,
        "sentence_len_sd": sent_sd,
        "commas_per_sentence": commas / n_sents if n_sents > 0 else float("nan"),
        "semicolons_per_sentence": semis / n_sents if n_sents > 0 else float("nan"),
        "commas_per_1000w": commas / n_words * 1000.0,
        "semicolons_per_1000w": semis / n_words * 1000.0,
        "sent_lens": sent_lens
    }
    
    fw_counts = collections.Counter(lower_tokens)
    for fw in function_words:
        out[f"fw_{fw}"] = fw_counts[fw] / n_words

    for k, v in p.items():
        out[f"punct_{k}_per_1000w"] = v / n_words * 1000.0

    return out

_SM_INSTANCE: Optional[StyloMetrix] = None

def get_sm_instance(lang: str = "en") -> StyloMetrix:
    global _SM_INSTANCE
    if _SM_INSTANCE is None:
        try:
            _SM_INSTANCE = StyloMetrix(lang)
        except Exception as e:
            logging.warning(f"Failed to initialize StyloMetrix: {e}")
            raise
    return _SM_INSTANCE

def compute_sm_vectors(texts: List[str]) -> List[Dict[str, float]]:
    """Computes StyloMetrix feature vectors for a list of texts."""
    if not texts:
        return []
    
    try:
        sm = get_sm_instance()
        # StyloMetrix get_metrics can take a list of strings
        df = sm.get_metrics(texts)
        # Convert df to list of dicts
        return df.to_dict(orient="records")
    except Exception as e:
        logging.error(f"StyloMetrix extraction failed: {e}")
        return [{} for _ in texts]

def _mp_compute_metrics(payload):
    """Wrapper for multiprocessing pickling."""
    tokens, sents, text, fw, window = payload
    return compute_metrics_for_text(tokens, sents, text, fw, window)

def build_char_ngram_similarity(chunks: List[ChunkRecord], 
                                ngram_min: int = 3, ngram_max: int = 5,
                                lowercase: bool = True, analyzer: str = "char_wb",
                                max_features: int = 50000, min_df: int = 2,
                                random_seed: int = 1337) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if not chunks:
        return pd.DataFrame(), pd.DataFrame()

    texts = [c.text for c in chunks]
    corpora = [c.corpus for c in chunks]

    vectorizer = TfidfVectorizer(
        analyzer=analyzer,
        ngram_range=(ngram_min, ngram_max),
        lowercase=lowercase,
        min_df=min_df,
        max_features=max_features,
    )
    X = vectorizer.fit_transform(texts)

    corpus_labels = sorted(set(corpora))
    centroids = []
    for cl in corpus_labels:
        idx = [i for i, c in enumerate(corpora) if c == cl]
        if not idx:
            centroids.append(np.zeros((1, X.shape[1]), dtype=np.float32))
            continue
        centroid = X[idx].mean(axis=0)
        centroids.append(np.asarray(centroid))
    C = np.vstack([c.reshape(1, -1) for c in centroids])

    sim = cosine_similarity(C)
    corpus_similarity_df = pd.DataFrame(sim, index=corpus_labels, columns=corpus_labels)

    chunk_sims = cosine_similarity(X, C)
    best_idx = chunk_sims.argmax(axis=1)
    best_score = chunk_sims.max(axis=1)

    chunk_assignment_df = pd.DataFrame({
        "corpus": corpora,
        "doc_id": [c.doc_id for c in chunks],
        "chunk_id": [c.chunk_id for c in chunks],
        "assigned_corpus": [corpus_labels[i] for i in best_idx],
        "assignment_score": best_score
    })

    return corpus_similarity_df, chunk_assignment_df

def compute_stylistic_pca(chunks: List[ChunkRecord], chunk_metrics: List[Dict[str, float]]) -> pd.DataFrame:
    """Computes a 2D PCA mapping of chunks based on stylistic features."""
    if not chunks or not chunk_metrics:
        return pd.DataFrame()

    # Select features that are most indicative of style
    exclude = ["word_count", "sentence_count", "unique_word_count", "corpus", "doc_id", "path", "chunk_id", "sent_lens", "chunk_text", "assigned_corpus"]
    feature_keys = [k for k in chunk_metrics[0].keys() if k not in exclude and isinstance(chunk_metrics[0][k], (int, float))]
    
    data = []
    for m in chunk_metrics:
        data.append([m.get(k, 0) for k in feature_keys])
    
    X = np.array(data)
    # Replace any NaNs with 0
    X = np.nan_to_num(X)
    
    # Scale for PCA
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # PCA to 2D
    pca = PCA(n_components=2, random_state=1337)
    X_pca = pca.fit_transform(X_scaled)
    
    df = pd.DataFrame({
        "pc1": X_pca[:, 0],
        "pc2": X_pca[:, 1],
        "corpus": [c.corpus for c in chunks],
        "doc_id": [c.doc_id for c in chunks],
        "chunk_id": [c.chunk_id for c in chunks]
    })
    
    return df
