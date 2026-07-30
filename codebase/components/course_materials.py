"""Deterministic lookup over the two supplied VLearn course PDFs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SLIDES_DIR = ROOT / "data" / "vlearn-pack" / "slides"


@dataclass(frozen=True)
class CoursePage:
    document_id: str
    document_title: str
    page: int
    text: str

    @property
    def source_id(self) -> str:
        return f"{self.document_id}:p{self.page:02d}"

    @property
    def source_label(self) -> str:
        return f"{self.document_title} · trang {self.page}"


DOCUMENTS = {
    "d1": ("AI & LLM Foundation", SLIDES_DIR / "d1-slide-hackathon.pdf"),
    "d2": ("Xác định bài toán cho AI", SLIDES_DIR / "d2-slide-hackathon.pdf"),
}


def normalize_text(value: str) -> str:
    """Normalize text for conservative exact/overlap checks."""
    return re.sub(r"\s+", " ", value).strip().casefold()


@lru_cache(maxsize=2)
def load_document(document_id: str) -> tuple[CoursePage, ...]:
    """Extract every page once; no embeddings or external retrieval required."""
    if document_id not in DOCUMENTS:
        return ()
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - exercised by startup smoke
        raise RuntimeError("Thiếu dependency pypdf; chạy pip install -r requirements.txt.") from exc

    title, path = DOCUMENTS[document_id]
    reader = PdfReader(str(path))
    return tuple(
        CoursePage(
            document_id=document_id,
            document_title=title,
            page=index,
            text=(pdf_page.extract_text() or "").strip(),
        )
        for index, pdf_page in enumerate(reader.pages, start=1)
    )


def get_page(document_id: str, page: int) -> CoursePage | None:
    pages = load_document(document_id)
    if page < 1 or page > len(pages):
        return None
    return pages[page - 1]


def validate_selection(page: CoursePage, selected_text: str) -> bool:
    """Confirm that the learner-selected text really occurs on the cited page."""
    selected = normalize_text(selected_text)
    page_text = normalize_text(page.text)
    if not selected or not page_text:
        return False
    if selected in page_text:
        return True
    selected_terms = {term for term in re.findall(r"\w+", selected) if len(term) > 2}
    page_terms = set(re.findall(r"\w+", page_text))
    return bool(selected_terms) and len(selected_terms & page_terms) / len(selected_terms) >= 0.85


def relevant_context(page: CoursePage, selected_text: str, radius: int = 700) -> str:
    """Return only the selected passage and nearby course text."""
    page_text = re.sub(r"\s+", " ", page.text).strip()
    selected = re.sub(r"\s+", " ", selected_text).strip()
    if not selected:
        return ""
    offset = normalize_text(page_text).find(normalize_text(selected))
    if offset < 0:
        return selected
    start = max(0, offset - radius)
    end = min(len(page_text), offset + len(selected) + radius)
    return page_text[start:end].strip()
