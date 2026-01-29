import re
import shutil
import tempfile
import urllib.request
import io
from pypdf import PdfReader
from pathlib import Path
from typing import List, Optional, Sequence, Tuple
from .models import DocRecord, ChunkRecord
from .normalizer import normalize_text_advanced, NormalizerConfig

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", re.UNICODE)
SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

def safe_read_text(path: Path) -> str:
    """Read text robustly with a couple of encodings."""
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc, errors="strict")
        except Exception:
            continue
    # last resort: ignore errors
    return path.read_text(encoding="utf-8", errors="ignore")

def normalize_text(text: str) -> str:
    """Original basic normalizer."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", text).strip()

def tokenize_words(text: str) -> List[str]:
    return WORD_RE.findall(text)

def split_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    sents = SENT_SPLIT_RE.split(text)
    return [s.strip() for s in sents if s and s.strip()]

def iter_text_files(root: Path) -> List[Path]:
    exts = {".txt", ".md", ".text"}
    files = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts and not p.name.startswith("~"):
            files.append(p)
    return sorted(files)

def fetch_url_content(url: str) -> str:
    """Fetches content from a URL and strips HTML tags."""
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            raw_data = response.read().decode("utf-8", errors="ignore")
            
            # Very basic HTML stripping
            # Remove scripts and styles
            clean_text = re.sub(r'<(script|style).*?>.*?</\1>', '', raw_data, flags=re.DOTALL | re.IGNORECASE)
            # Remove all other tags
            clean_text = re.sub(r'<.*?>', '', clean_text, flags=re.DOTALL)
            # Unescape some common HTML entities
            clean_text = clean_text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            
            return clean_text
    except Exception as e:
        raise RuntimeError(f"Failed to fetch URL {url}: {e}")

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extracts text from PDF bytes using pypdf."""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")

def load_corpus(label: str, path_str: str, norm_cfg: Optional[NormalizerConfig] = None) -> Tuple[List[DocRecord], Optional[Path]]:
    temp_root = None
    
    # Check if path_str is a URL
    if path_str.startswith(("http://", "https://")):
        print(f"Fetching content from {path_str}...")
        
        req = urllib.request.Request(
            path_str, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            content_type = response.info().get_content_type()
            raw_data = response.read()
            
            if "pdf" in content_type or path_str.lower().endswith(".pdf"):
                web_text = extract_text_from_pdf_bytes(raw_data)
            else:
                html_text = raw_data.decode("utf-8", errors="ignore")
                # Very basic HTML stripping
                clean_text = re.sub(r'<(script|style).*?>.*?</\1>', '', html_text, flags=re.DOTALL | re.IGNORECASE)
                clean_text = re.sub(r'<.*?>', '', clean_text, flags=re.DOTALL)
                web_text = clean_text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        
        docs: List[DocRecord] = []
        doc_id = label.lower().replace(" ", "_")
        
        if norm_cfg:
            text = normalize_text_advanced(web_text, norm_cfg)
        else:
            text = normalize_text(web_text)
            
        tokens = tokenize_words(text)
        sents = split_sentences(text)
        docs.append(DocRecord(
            corpus=label,
            doc_id=doc_id,
            path=path_str,
            text=text,
            word_tokens=tokens,
            sentences=sents
        ))
        return docs, None

    path = Path(path_str).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")

    if path.is_file() and path.suffix.lower() == ".zip":
        temp_root = Path(tempfile.mkdtemp(prefix=f"stylocorpus_{label}_"))
        shutil.unpack_archive(str(path), str(temp_root))
        root = temp_root
    else:
        root = path

    docs: List[DocRecord] = []

    def _process_file(fp: Path, doc_id: str):
        raw = safe_read_text(fp)
        if norm_cfg:
            text = normalize_text_advanced(raw, norm_cfg)
        else:
            text = normalize_text(raw)
        
        tokens = tokenize_words(text)
        sents = split_sentences(text)
        docs.append(DocRecord(
            corpus=label,
            doc_id=doc_id,
            path=str(fp),
            text=text,
            word_tokens=tokens,
            sentences=sents
        ))

    if root.is_file():
        _process_file(root, root.stem)
        return docs, temp_root

    files = iter_text_files(root)
    if not files:
        raise ValueError(f"No .txt/.md files found under: {root}")

    for fp in files:
        rel = fp.relative_to(root)
        _process_file(fp, str(rel).replace("\\", "/"))
        
    return docs, temp_root

def chunk_doc(doc: DocRecord, chunk_words: int, overlap: int = 0) -> List[ChunkRecord]:
    tokens = doc.word_tokens
    if not tokens:
        return []
    
    if overlap >= chunk_words:
        overlap = chunk_words // 2
        
    chunks: List[ChunkRecord] = []
    step = chunk_words - overlap
    
    for i in range(0, len(tokens), step):
        w = tokens[i : i + chunk_words]
        if len(w) < max(50, chunk_words // 5):
            continue
            
        chunk_id = f"c{len(chunks):04d}"
        chunk_text = " ".join(w)
        sents = split_sentences(chunk_text)
        chunks.append(ChunkRecord(
            corpus=doc.corpus,
            doc_id=doc.doc_id,
            chunk_id=chunk_id,
            text=chunk_text,
            word_tokens=w,
            sentences=sents
        ))
        
        # Avoid creating a tiny final chunk if we've already covered almost everything
        if i + chunk_words >= len(tokens):
            break
            
    return chunks
