"""Interactive PDF.js slide viewer with a selectable text layer."""
import base64
from functools import lru_cache
from pathlib import Path
from typing import Any

import streamlit.components.v1 as st_components



_FRONTEND_PATH = Path(__file__).parent / "document_selector_frontend"
_document_selector = st_components.declare_component(
    "document_selector",
    path=str(_FRONTEND_PATH),
)


@lru_cache(maxsize=2)
def _pdf_as_base64(path: str) -> str:
    """Read each deck once for the local PDF.js viewer."""
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


def render_document_panel(
    title: str,
    pdf_path: Path,
    page: int,
    page_count: int,
    page_texts: list[str],
    component_key: str = "document-selector",
) -> dict[str, Any] | None:
    """Render the original slide with selectable PDF text."""
    value = _document_selector(
        title=title,
        pdf_base64=_pdf_as_base64(str(pdf_path.resolve())),
        page=page,
        page_count=page_count,
        page_texts=page_texts,
        default=None,
        key=component_key,
    )
    return value if isinstance(value, dict) else None
