from __future__ import annotations

import sys
import unittest
from pathlib import Path

import fitz


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codebase"))

from components.chatbot_panel import _is_duplicate_submission
from components.course_materials import (
    course_page_from_document,
    normalize_submission,
    validate_selection,
)
from components.pdf_loader import (
    clear_pdf_cache,
    document_id_for_bytes,
    extract_pdf_document,
)


def make_pdf(page_texts: list[str | None]) -> bytes:
    document = fitz.open()
    for page_text in page_texts:
        page = document.new_page(width=420, height=300)
        if page_text:
            page.insert_text((40, 70), page_text, fontsize=12)
        else:
            page.draw_rect(fitz.Rect(40, 40, 180, 130), color=(0, 0, 0), fill=(0.8, 0.8, 0.8))
    data = document.tobytes()
    document.close()
    return data


class PdfExtractionTests(unittest.TestCase):
    def tearDown(self):
        clear_pdf_cache()

    def test_reads_multiple_pages_and_keeps_page_text_separate(self):
        data = make_pdf(["Alpha concept appears only here.", "Beta concept is on page two."])
        result = extract_pdf_document(data, "lesson.pdf")

        self.assertEqual(result["page_count"], 2)
        self.assertEqual(result["text_page_count"], 2)
        self.assertIn("Alpha concept", result["pages"][0]["text"])
        self.assertNotIn("Beta concept", result["pages"][0]["text"])
        self.assertIn("Beta concept", result["pages"][1]["text"])
        self.assertTrue(str(result["pages"][0]["image"]).startswith("data:image/jpeg;base64,"))
        self.assertGreater(len(result["pages"][0]["words"]), 0)

    def test_document_id_is_stable_for_identical_bytes(self):
        data = make_pdf(["Stable content"])
        first = extract_pdf_document(data, "first-name.pdf")
        second = extract_pdf_document(data, "renamed.pdf")

        self.assertEqual(first["id"], second["id"])
        self.assertEqual(first["id"], document_id_for_bytes(data))
        self.assertTrue(str(first["id"]).startswith("upload-"))

    def test_empty_and_corrupt_pdf_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "trống"):
            extract_pdf_document(b"", "empty.pdf")
        with self.assertRaisesRegex(ValueError, "hỏng"):
            extract_pdf_document(b"%PDF-1.7 broken", "broken.pdf")

    def test_image_only_pdf_remains_renderable_without_selectable_text(self):
        result = extract_pdf_document(make_pdf([None]), "scan.pdf")

        self.assertEqual(result["page_count"], 1)
        self.assertEqual(result["text_page_count"], 0)
        self.assertEqual(result["pages"][0]["text"], "")
        self.assertEqual(result["pages"][0]["words"], [])
        self.assertTrue(str(result["pages"][0]["image"]).startswith("data:image/jpeg;base64,"))


class DocumentAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = extract_pdf_document(
            make_pdf(
                [
                    "Alpha topic has enough explanatory context on the first page.",
                    "Beta topic belongs exclusively to the second page.",
                ]
            ),
            "uploaded-course.pdf",
        )

    @classmethod
    def tearDownClass(cls):
        clear_pdf_cache()

    def test_page_number_out_of_range_returns_none(self):
        self.assertIsNone(course_page_from_document(self.document, 0))
        self.assertIsNone(course_page_from_document(self.document, 3))

    def test_selection_on_exact_page_is_accepted_with_whitespace_normalization(self):
        page = course_page_from_document(self.document, 1)
        self.assertIsNotNone(page)
        self.assertTrue(validate_selection(page, "Alpha   topic has enough\nexplanatory context"))

    def test_selection_from_another_page_is_rejected(self):
        first_page = course_page_from_document(self.document, 1)
        self.assertIsNotNone(first_page)
        self.assertFalse(validate_selection(first_page, "Beta topic belongs exclusively"))

    def test_selection_from_rendered_word_layer_is_exactly_accepted(self):
        document = dict(self.document)
        first_page_data = dict(self.document['pages'][0])
        first_page_data['selection_text'] = 'Layer-only phrase from rendered words'
        document['pages'] = [first_page_data, self.document['pages'][1]]
        page = course_page_from_document(document, 1)
        self.assertTrue(validate_selection(page, 'Layer-only phrase from rendered words'))
        self.assertFalse(validate_selection(page, 'Layer-only invented phrase'))

    def test_upload_source_id_cannot_collide_with_bundled_id(self):
        page = course_page_from_document(self.document, 1)
        self.assertIsNotNone(page)
        self.assertTrue(page.source_id.startswith("upload-"))
        self.assertNotEqual(page.source_id, "d1:p01")
        self.assertNotEqual(page.source_id, "d2:p01")

    def test_normalize_submission_resolves_only_active_document_and_page(self):
        document_id = str(self.document["id"])
        registry = {document_id: self.document}
        submission = {
            "event_id": "evt-1",
            "document_id": document_id,
            "page_number": 2,
            "selected_text": "Beta topic",
            "question": "Explain this",
        }
        normalized, page = normalize_submission(
            submission,
            registry,
            active_document_id=document_id,
            fallback_page=1,
        )
        self.assertEqual(normalized["page"], 2)
        self.assertEqual(page.page, 2)

        stale_normalized, stale_page = normalize_submission(
            submission,
            registry,
            active_document_id="d1",
            fallback_page=1,
        )
        self.assertIsNone(stale_normalized)
        self.assertIsNone(stale_page)

    def test_repeated_event_id_is_detected(self):
        self.assertTrue(_is_duplicate_submission("evt-1", "evt-1"))
        self.assertFalse(_is_duplicate_submission("evt-2", "evt-1"))
        self.assertFalse(_is_duplicate_submission("", ""))


if __name__ == "__main__":
    unittest.main()
