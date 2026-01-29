import collections
from typing import List, Set
from .models import DocRecord

def find_boilerplate(docs: List[DocRecord], threshold: float = 0.5, min_len: int = 50) -> Set[int]:
    """
    Identifies paragraphs that appear in more than 'threshold' fraction of documents.
    Returns a set of hashes of boilerplate paragraphs.
    """
    if len(docs) < 3:
        return set()
        
    counts = collections.Counter()
    for d in docs:
        paragraphs = {p.strip() for p in d.text.split("\n") if len(p.strip()) >= min_len}
        for p in paragraphs:
            counts[p] += 1
            
    boilerplate_hashes = set()
    n_docs = len(docs)
    for p, count in counts.items():
        if count / n_docs >= threshold:
            boilerplate_hashes.add(hash(p))
            
    return boilerplate_hashes

def strip_boilerplate(docs: List[DocRecord], boilerplate_hashes: Set[int]):
    """Removes identified boilerplate paragraphs from documents in-place."""
    if not boilerplate_hashes:
        return
        
    for d in docs:
        lines = d.text.split("\n")
        new_lines = []
        for line in lines:
            if not line.strip():
                new_lines.append("")
                continue
            if hash(line.strip()) in boilerplate_hashes:
                continue
            new_lines.append(line)
        
        # Re-join and re-tokenize if changed
        new_text = "\n".join(new_lines).strip()
        if new_text != d.text.strip():
            d.text = new_text
            # We don't strictly HAVE to re-tokenize here if we're just about to chunk,
            # but it's cleaner. For performance in CLI, we might skip it until metrics.
            # However, word_tokens and sentences are used for metrics.
            # For now, let's just update d.text; the caller should re-process tokens.
