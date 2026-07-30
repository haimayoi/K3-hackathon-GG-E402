"""Interactive rendered-PDF viewer with selectable text and anchored questions."""

from pathlib import Path
from typing import Any

import streamlit.components.v1 as st_components

from components.pdf_loader import load_pdf_path


_FRONTEND_PATH = Path(__file__).parent / "document_selector_frontend"
_document_selector = st_components.declare_component(
    "document_selector",
    path=str(_FRONTEND_PATH),
)


def render_document_panel(
    title: str,
    pdf_path: Path | None = None,
    page: int = 1,
    page_count: int | None = None,
    page_texts: list[str] | None = None,
    component_key: str = "document-selector",
    *,
    pages: list[dict[str, object]] | None = None,
    library_documents: list[dict[str, object]] | None = None,
    active_document_id: str | None = None,
    focus_page: int | None = None,
) -> dict[str, Any] | None:
    """Render a document while preserving the former positional call shape.

    Legacy callers may still provide a PDF path and page texts. New callers
    pass normalized rendered pages plus the session document library.
    """
    if pages is None and pdf_path is not None:
        loaded = load_pdf_path(pdf_path)
        pages = list(loaded["pages"])
        if page_texts:
            for index, text in enumerate(page_texts):
                if index < len(pages):
                    pages[index]["text"] = text
        page_count = int(loaded["page_count"])
    value = _document_selector(
        title=title,
        pages=pages or [],
        page_count=page_count or len(pages or []),
        library_documents=library_documents or [],
        active_document_id=active_document_id,
        focus_page=focus_page if focus_page is not None else page,
        default=None,
        key=component_key,
    )
    return value if isinstance(value, dict) else None
