"""PDF ingestion helpers for local paths and Streamlit uploads."""

from __future__ import annotations

import base64
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import re

import fitz
from pypdf import PdfReader


COURSE_PDF_PATHS = (
    Path(__file__).parents[1] / 'data' / 'vlearn-pack' / 'slides' / 'd1-slide-hackathon.pdf',
    Path(__file__).parents[1] / 'data' / 'vlearn-pack' / 'slides' / 'd2-slide-hackathon.pdf',
)

DEFAULT_PDF_PATHS = [
    COURSE_PDF_PATHS[0],
    Path(__file__).parents[1] / "data" / "vlearn-pack" / "slides" / "d2-slide-hackathon.pdf",
    Path(__file__).parents[1] / "data" / "uploads" / "day01-slide-blue-v0.pdf",
]
DEFAULT_PDF_PATH = next((path for path in DEFAULT_PDF_PATHS if path.is_file()), DEFAULT_PDF_PATHS[0])


def _normalize_page_text(text: str) -> str:
    """Remove extraction noise while keeping readable line boundaries."""
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def _render_pdf_pages(data: bytes) -> list[dict[str, object]]:
    """Render original slide images and their selectable word coordinates."""
    rendered_pages: list[dict[str, object]] = []
    with fitz.open(stream=data, filetype="pdf") as document:
        for page in document:
            pixmap = page.get_pixmap(matrix=fitz.Matrix(1.15, 1.15), alpha=False)
            image_bytes = pixmap.tobytes("jpeg", jpg_quality=72)
            words = [
                {
                    "text": str(word[4]),
                    "x0": round(float(word[0]), 2),
                    "y0": round(float(word[1]), 2),
                    "x1": round(float(word[2]), 2),
                    "y1": round(float(word[3]), 2),
                }
                for word in page.get_text("words", sort=True)
            ]
            rendered_pages.append(
                {
                    "image": (
                        "data:image/jpeg;base64,"
                        + base64.b64encode(image_bytes).decode("ascii")
                    ),
                    "width": round(float(page.rect.width), 2),
                    "height": round(float(page.rect.height), 2),
                    "words": words,
                }
            )
    return rendered_pages


def extract_pdf_document(data: bytes, filename: str, source: str) -> dict[str, object]:
    """Extract selectable text from a PDF byte stream."""
    if not data:
        raise ValueError("File PDF đang trống.")

    reader = PdfReader(BytesIO(data))
    page_sections: list[str] = []
    pages: list[dict[str, object]] = []
    extracted_pages = 0
    for page_number, page in enumerate(reader.pages, start=1):
        page_text = _normalize_page_text(page.extract_text() or "")
        pages.append({"page_number": page_number, "text": page_text})
        if not page_text:
            continue
        extracted_pages += 1
        page_sections.append(f"TRANG {page_number}\n{page_text}")

    if not page_sections:
        raise ValueError(
            "Không tìm thấy text trong PDF. File có thể chỉ chứa ảnh và cần OCR."
        )

    rendered_pages = _render_pdf_pages(data)
    for index, rendered_page in enumerate(rendered_pages):
        if index < len(pages):
            pages[index].update(rendered_page)

    digest = sha256(data).hexdigest()
    return {
        "id": digest[:16],
        "name": filename,
        "source": source,
        "page_count": len(reader.pages),
        "text_page_count": extracted_pages,
        "text": "\n\n".join(page_sections),
        "pages": pages,
    }


def load_pdf_path(path_value: str | Path) -> dict[str, object]:
    """Read and extract a PDF from an explicit local path."""
    path = Path(path_value).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Chỉ hỗ trợ PDF ở bước này: {path.name}")
    return extract_pdf_document(path.read_bytes(), path.name, str(path))
