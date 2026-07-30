"""Interactive text slide viewer with a page-grounded question popover."""
from pathlib import Path
from typing import Any

import streamlit.components.v1 as st_components



_FRONTEND_PATH = Path(__file__).parent / "document_selector_frontend"
_document_selector = st_components.declare_component(
    "document_selector",
    path=str(_FRONTEND_PATH),
)



def render_document_panel(
    title: str,
    page: int,
    page_count: int,
    page_texts: list[str],
    component_key: str = "document-selector",
) -> dict[str, Any] | None:
    """Render extracted slide text and return a page-grounded question."""
    value = _document_selector(
        title=title,
        page=page,
        page_count=page_count,
        page_texts=page_texts,
        default=None,
        key=component_key,
    )
    return value if isinstance(value, dict) else None
