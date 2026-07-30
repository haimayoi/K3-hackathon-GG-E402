import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class CanonicalAppSmokeTest(unittest.TestCase):
    def test_app_starts_without_exception(self):
        app = AppTest.from_file("app.py", default_timeout=20)
        app.run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.selectbox), 2)
        self.assertGreaterEqual(len(app.button), 1)
        self.assertEqual(app.selectbox[1].value, 29)

    def test_slide_viewer_has_scroll_navigation_contract(self):
        frontend = Path(
            "components/document_selector_frontend/index.html"
        ).read_text(encoding="utf-8")
        self.assertIn('addEventListener("wheel"', frontend)
        self.assertIn("page: currentPage", frontend)
        self.assertIn("pageTexts[currentPage - 1]", frontend)
        self.assertIn('id="page-status"', frontend)
        self.assertIn('tabindex="0"', frontend)
        self.assertIn('id="document"', frontend)
        self.assertIn("article.replaceChildren()", frontend)
        self.assertNotIn("base64ToBlobUrl", frontend)
        self.assertNotIn("slide-image", frontend)


if __name__ == "__main__":
    unittest.main()