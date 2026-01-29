from dataclasses import dataclass
from typing import List

@dataclass
class DocRecord:
    corpus: str
    doc_id: str
    path: str
    text: str
    word_tokens: List[str]
    sentences: List[str]

@dataclass
class ChunkRecord:
    corpus: str
    doc_id: str
    chunk_id: str
    text: str
    word_tokens: List[str]
    sentences: List[str]
