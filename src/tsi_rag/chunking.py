from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .models import Chunk


SUPPORTED_SUFFIXES = {".md", ".txt"}


def _clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    """Simple, deterministic character-based chunking for teaching purposes."""
    text = _clean_text(text)
    if not text:
        return []
    if overlap >= chunk_size:
        raise ValueError("chunk_overlap debe ser menor que chunk_size")

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            chunks.append(current)
            tail = current[-overlap:] if overlap else ""
            current = f"{tail}\n\n{paragraph}".strip()
        else:
            start = 0
            step = max(1, chunk_size - overlap)
            while start < len(paragraph):
                chunks.append(paragraph[start : start + chunk_size].strip())
                start += step
            current = ""

        while len(current) > chunk_size:
            chunks.append(current[:chunk_size].strip())
            current = current[chunk_size - overlap :].strip() if overlap else current[chunk_size:]

    if current:
        chunks.append(current)
    return [c for c in chunks if c]


def load_corpus(corpus_dir: Path, chunk_size: int, overlap: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(corpus_dir.glob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        title = path.stem.replace("_", " ").replace("-", " ").title()
        for i, content in enumerate(chunk_text(text, chunk_size, overlap)):
            digest = hashlib.sha1(f"{path.name}:{i}:{content}".encode()).hexdigest()[:16]
            chunks.append(
                Chunk(
                    id=digest,
                    title=title,
                    source=path.name,
                    chunk_id=i,
                    content=content,
                )
            )
    return chunks
