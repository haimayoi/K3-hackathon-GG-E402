"""Bounded PDF ingestion for bundled course files and session uploads."""

from __future__ import annotations

import base64
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import re

import fitz
from pypdf import PdfReader


MAX_PDF_SIZE_BYTES = 20 * 1024 * 1024
MAX_PDF_PAGES = 100
_RENDER_SCALE = 1.15
_SELECTABLE_CONTENT_BOTTOM_RATIO = 0.92


def _normalize_page_text(text: str) -> str:
    """Remove extraction noise while retaining useful line boundaries."""
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def document_id_for_bytes(data: bytes) -> str:
    """Return the stable, namespace-safe ID used for an uploaded PDF."""
    return f"upload-{sha256(data).hexdigest()[:16]}"


def _render_pdf_pages(data: bytes) -> list[dict[str, object]]:
    """Render page images and word boxes used by the selectable viewer layer."""
    rendered: list[dict[str, object]] = []
    try:
        with fitz.open(stream=data, filetype="pdf") as document:
            for page in document:
                pixmap = page.get_pixmap(
                    matrix=fitz.Matrix(_RENDER_SCALE, _RENDER_SCALE),
                    alpha=False,
                )
                image_bytes = pixmap.tobytes("jpeg", jpg_quality=70)
                words = [
                    {
                        "text": str(word[4]),
                        "x0": round(float(word[0]), 2),
                        "y0": round(float(word[1]), 2),
                        "x1": round(float(word[2]), 2),
                        "y1": round(float(word[3]), 2),
                    }
                    for word in page.get_text("words", sort=True)
                    # Repeated slide furniture/watermarks live in the bottom band.
                    # Keep them visible in the page image, but never selectable.
                    if float(word[1]) < float(page.rect.height) * _SELECTABLE_CONTENT_BOTTOM_RATIO
                ]
                selection_text = " ".join(str(word["text"]) for word in words)
                rendered.append(
                    {
                        "image": "data:image/jpeg;base64,"
                        + base64.b64encode(image_bytes).decode("ascii"),
                        "width": round(float(page.rect.width), 2),
                        "height": round(float(page.rect.height), 2),
                        "words": words,
                        "selection_text": selection_text,
                    }
                )
    except Exception as exc:
        raise ValueError("Không thể render file PDF. File có thể bị hỏng.") from exc
    return rendered


@lru_cache(maxsize=8)
def _extract_pdf_payload(data: bytes) -> dict[str, object]:
    """Extract immutable-by-convention content; callers receive a deep copy."""
    if not data:
        raise ValueError("File PDF đang trống.")
    if len(data) > MAX_PDF_SIZE_BYTES:
        raise ValueError("File PDF vượt quá giới hạn 20 MB.")

    try:
        reader = PdfReader(BytesIO(data), strict=False)
        page_count = len(reader.pages)
    except Exception as exc:
        raise ValueError("Không thể đọc file PDF. File có thể bị hỏng.") from exc

    if page_count < 1:
        raise ValueError("File PDF không có trang nào.")
    if page_count > MAX_PDF_PAGES:
        raise ValueError("File PDF vượt quá giới hạn 100 trang.")

    pages: list[dict[str, object]] = []
    page_sections: list[str] = []
    text_page_count = 0
    try:
        for page_number, pdf_page in enumerate(reader.pages, start=1):
            page_text = _normalize_page_text(pdf_page.extract_text() or "")
            pages.append({"page_number": page_number, "text": page_text})
            if page_text:
                text_page_count += 1
                page_sections.append(f"TRANG {page_number}\n{page_text}")
    except Exception as exc:
        raise ValueError("Không thể trích xuất text từ file PDF.") from exc

    rendered_pages = _render_pdf_pages(data)
    if len(rendered_pages) != page_count:
        raise ValueError("Số trang render không khớp với file PDF.")
    for page, rendered_page in zip(pages, rendered_pages, strict=True):
        page.update(rendered_page)

    return {
        "id": document_id_for_bytes(data),
        "page_count": page_count,
        "text_page_count": text_page_count,
        "text": "\n\n".join(page_sections),
        "pages": pages,
    }


def extract_pdf_document(data: bytes, filename: str, source: str = "upload") -> dict[str, object]:
    """Validate and extract a PDF without writing its bytes to disk.

    Image-only PDFs are valid display documents. They return zero text pages so
    the UI can explain that OCR is intentionally out of scope.
    """
    safe_name = Path(filename or "document.pdf").name
    if Path(safe_name).suffix.lower() != ".pdf":
        raise ValueError("Chỉ hỗ trợ file PDF.")
    payload = deepcopy(_extract_pdf_payload(bytes(data)))
    payload.update({"name": safe_name, "source": str(source)})
    return payload


def load_pdf_path(path_value: str | Path) -> dict[str, object]:
    """Read a trusted local course PDF through the same normalized contract."""
    path = Path(path_value).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Chỉ hỗ trợ PDF: {path.name}")
    return extract_pdf_document(path.read_bytes(), path.name, "bundled")


def clear_pdf_cache() -> None:
    """Clear extraction cache; intended for deterministic tests and maintenance."""
    _extract_pdf_payload.cache_clear()
