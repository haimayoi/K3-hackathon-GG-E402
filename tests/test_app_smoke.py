import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class CanonicalAppSmokeTest(unittest.TestCase):
    def test_root_app_starts_without_exception(self):
        app = AppTest.from_file("app.py", default_timeout=90)
        app.run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.file_uploader), 0)
        self.assertGreaterEqual(len(app.button), 1)
        self.assertEqual(len(app.selectbox), 0)

    def test_rendered_pdf_viewer_selection_contract(self):
        frontend = Path(
            "codebase/components/document_selector_frontend/index.html"
        ).read_text(encoding="utf-8")
        self.assertIn('id="previous-page"', frontend)
        self.assertIn('id="next-page"', frontend)
        self.assertIn('id="page-status"', frontend)
        self.assertIn('className = "slide-image"', frontend)
        self.assertIn('className = "text-layer"', frontend)
        self.assertIn('action: "switch_document"', frontend)
        self.assertIn("startCard !== endCard", frontend)
        self.assertIn("document_id: activeDocumentId", frontend)
        self.assertIn("page_number: selectedPageNumber", frontend)
        self.assertIn("page: selectedPageNumber", frontend)
        self.assertIn("selected_text: selectedText", frontend)
        self.assertIn("question: text", frontend)
        self.assertIn("question.placeholder = suggestedQuestion", frontend)
        self.assertIn("question.value.trim() || suggestedQuestion", frontend)
        self.assertIn("event.target.closest?.(\".text-layer span\")", frontend)
        self.assertIn("selection.isCollapsed", frontend)
        self.assertIn("clearActiveSelection();", frontend)
        self.assertNotIn("OPENAI_API_KEY", frontend)
        self.assertNotIn("confidence", frontend.casefold())


if __name__ == "__main__":
    unittest.main()
