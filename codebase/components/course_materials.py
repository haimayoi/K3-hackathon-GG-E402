"""Deterministic lookup and adapters for bundled and uploaded course PDFs."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Mapping


ROOT = Path(__file__).resolve().parents[2]
SLIDES_DIR = ROOT / "data" / "vlearn-pack" / "slides"


@dataclass(frozen=True)
class CoursePage:
    document_id: str
    document_title: str
    page: int
    text: str
    selection_text: str = ""

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
    return re.sub(r'\s+', ' ', value).strip().casefold()


_PDF_PUNCTUATION = str.maketrans(
    {
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
        "ˮ": '"',
        "–": "-",
        "—": "-",
        "−": "-",
    }
)


def normalize_source_text(value: str) -> str:
    """Reconcile harmless glyph differences between pypdf and fitz layers."""
    canonical = unicodedata.normalize("NFKC", value).translate(_PDF_PUNCTUATION)
    return normalize_text(canonical)


@lru_cache(maxsize=2)
def load_document(document_id: str) -> tuple[CoursePage, ...]:
    """Preserved API: extract every page of one bundled course document."""
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
    """Preserved API: resolve one page from a bundled document."""
    pages = load_document(document_id)
    if page < 1 or page > len(pages):
        return None
    return pages[page - 1]


def validate_selection(page: CoursePage, selected_text: str) -> bool:
    """Confirm that normalized learner text occurs on this exact cited page."""
    selected = normalize_source_text(selected_text)
    page_texts = (page.text, page.selection_text)
    if not selected:
        return False
    return any(
        selected in normalize_source_text(candidate)
        for candidate in page_texts
        if candidate
    )


def relevant_context(page: CoursePage, selected_text: str, radius: int = 700) -> str:
    """Return only the selected passage and nearby text from its verified page."""
    page_text = re.sub(r'\s+', ' ', page.text).strip()
    selected = re.sub(r'\s+', ' ', selected_text).strip()
    if not selected:
        return ""
    offset = normalize_source_text(page_text).find(normalize_source_text(selected))
    if offset < 0:
        selected_tokens = re.findall(r'\w+', normalize_source_text(selected))
        if not selected_tokens:
            return ''
        offset = normalize_source_text(page_text).find(selected_tokens[0])
        if offset < 0:
            return ''
    start = max(0, offset - radius)
    end = min(len(page_text), offset + len(selected) + radius)
    return page_text[start:end].strip()


def course_page_from_document(
    document: Mapping[str, object], page_number: int
) -> CoursePage | None:
    """Adapt one normalized PDF document page to the preserved agent contract."""
    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        return None
    pages = document.get("pages")
    if not isinstance(pages, list) or page_number < 1 or page_number > len(pages):
        return None
    page_data = pages[page_number - 1]
    if not isinstance(page_data, Mapping):
        return None
    if int(page_data.get("page_number", page_number)) != page_number:
        return None
    document_id = str(document.get("id", "")).strip()
    document_name = str(document.get("name", "")).strip()
    if not document_id or not document_name:
        return None
    return CoursePage(
        document_id=document_id,
        document_title=document_name,
        page=page_number,
        text=str(page_data.get("text", "")),
        selection_text=str(page_data.get("selection_text", "")),
    )


def normalize_submission(
    submission: Mapping[str, object] | None,
    documents: Mapping[str, Mapping[str, object]],
    *,
    active_document_id: str,
    fallback_page: int,
) -> tuple[dict[str, object] | None, CoursePage | None]:
    """Resolve document/page once and normalize selector compatibility keys.

    Lookup is deliberately page-local and only the active document can resolve.
    The learning agent still performs selection validation, preserving its
    reason codes and state transitions.
    """
    if not submission:
        return None, None
    document_id = str(submission.get("document_id") or active_document_id).strip()
    if document_id != active_document_id:
        return None, None
    raw_page = submission.get("page_number", submission.get("page", fallback_page))
    try:
        page_number = int(raw_page)
    except (TypeError, ValueError):
        page_number = 0
    document = documents.get(document_id)
    page = course_page_from_document(document, page_number) if document else None
    normalized = dict(submission)
    normalized.update(
        {
            "document_id": document_id,
            "page_number": page_number,
            "page": page_number,
        }
    )
    return normalized, page
