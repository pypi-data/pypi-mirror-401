import re
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
from .models import DocRecord

_STAGE_WORDS = {
    "applause", "laughter", "cheers", "cheering", "booing", "boos", "chuckles",
    "crosstalk", "cross talk", "inaudible", "music", "chanting", "audience",
    "silence", "pause", "standing ovation", "ovation"
}

_EXCLUDE_LABEL_PREFIXES = {"SECTION", "ARTICLE", "TITLE", "CHAPTER", "PART", "SUBTITLE", "SUBCHAPTER"}

@dataclass
class NormalizerConfig:
    remove_stage_directions: bool = True
    remove_quote_blocks: bool = False
    min_quote_block_lines: int = 2
    remove_speaker_labels: bool = False
    strip_urls: bool = False
    dedupe_paragraphs: bool = True
    boilerplate_threshold: float = 0.0

def _is_stage_direction_line(line: str) -> bool:
    content = line.strip()
    if not content:
        return False
    # Cases like [APPLAUSE] or (LAUGHTER) or **CHUCKLING**
    if (content.startswith("[") and content.endswith("]")) or \
       (content.startswith("(") and content.endswith(")")) or \
       (content.startswith("*") and content.endswith("*")):
        inner = re.sub(r"[^a-z ]", "", content.lower()).strip()
        if not inner: return True
        # If any stage word is in there, or if it's very short
        if any(w in inner for w in _STAGE_WORDS): return True
        if len(inner.split()) <= 3: return True
    return False

def _remove_speaker_labels(text: str) -> str:
    lines = text.split("\n")
    out = []
    for line in lines:
        # Match "NAME:" or "NAME (CONT'D):"
        match = re.match(r"^([A-Z][A-Z\s\.\-]{2,30}):\s*(.*)", line.strip())
        if match:
            label, remainder = match.groups()
            # Heuristic: if label is all caps, it's likely a speaker
            if label.isupper() and label not in _EXCLUDE_LABEL_PREFIXES:
                out.append(remainder)
                continue
        out.append(line)
    return "\n".join(out)

def _strip_urls(text: str) -> str:
    return re.sub(r"https?://\S+", "", text)

def _remove_quote_blocks(text: str, min_lines: int) -> str:
    """Removes blocks where every line starts with > and the block is at least min_lines long."""
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith(">"):
            start = i
            while i < len(lines) and lines[i].strip().startswith(">"):
                i += 1
            if (i - start) < min_lines:
                out.extend(lines[start:i])
            else:
                # Block removed
                pass
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out)

def normalize_text_advanced(text: str, cfg: NormalizerConfig) -> str:
    if cfg.strip_urls:
        text = _strip_urls(text)
    
    if cfg.remove_speaker_labels:
        text = _remove_speaker_labels(text)
        
    if cfg.remove_quote_blocks:
        text = _remove_quote_blocks(text, cfg.min_quote_block_lines)

    lines = text.split("\n")
    clean_lines = []
    
    for line in lines:
        if cfg.remove_stage_directions and _is_stage_direction_line(line):
            continue
        clean_lines.append(line)
        
    text = "\n".join(clean_lines)
    
    # Basic cleanup (re-using part of the original logic but enhanced)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(re.sub(r"[ \t]+", " ", l).strip() for l in text.split("\n"))
    
    if cfg.dedupe_paragraphs:
        seen = set()
        par_out = []
        for p in text.split("\n"):
            if not p.strip():
                par_out.append("")
                continue
            h = hash(p.strip())
            if h not in seen:
                par_out.append(p)
                seen.add(h)
        text = "\n".join(par_out)
        
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text
