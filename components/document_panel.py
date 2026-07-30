"""Interactive document viewer with an anchored question popover."""

from pathlib import Path
from typing import Any

import streamlit.components.v1 as st_components

from components.mock_data import DOCUMENT_TITLE


_FRONTEND_PATH = Path(__file__).parent / "document_selector_frontend"
_document_selector = st_components.declare_component(
    "document_selector",
    path=str(_FRONTEND_PATH),
)


def render_document_panel(
    document: str,
    component_key: str = "document-selector",
    document_title: str = DOCUMENT_TITLE,
    question_placeholder: str = "Nhập câu hỏi của bạn…",
    focus_page: int | None = None,
    pages: list[dict[str, object]] | None = None,
    library_documents: list[dict[str, object]] | None = None,
    active_document_id: str | None = None,
) -> dict[str, Any] | None:
    """Render the document and return a question submitted from its popover."""
    value = _document_selector(
        title=document_title,
        document=document,
        question_placeholder=question_placeholder,
        focus_page=focus_page,
        pages=pages or [],
        library_documents=library_documents or [],
        active_document_id=active_document_id,
        default=None,
        key=component_key,
    )
    return value if isinstance(value, dict) else None
