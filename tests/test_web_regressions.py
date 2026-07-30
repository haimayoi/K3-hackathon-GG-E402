from pathlib import Path
from urllib.error import HTTPError

import pytest

import services.ai_client as ai_client
from components.pdf_loader import COURSE_PDF_PATHS, load_pdf_path
from services.ai_client import (
    AIConfig,
    GeminiClient,
    LEARNING_RESPONSE_SCHEMA,
    ProviderError,
)


def test_course_slides_are_ordered_d1_then_d2():
    assert [path.name for path in COURSE_PDF_PATHS] == [
        'd1-slide-hackathon.pdf',
        'd2-slide-hackathon.pdf',
    ]
    documents = [load_pdf_path(path) for path in COURSE_PDF_PATHS]
    assert [document['page_count'] for document in documents] == [29, 29]


def test_retired_gemini_model_is_migrated(monkeypatch):
    monkeypatch.setenv('LLM_MODEL', 'gemini-2.5-flash')
    config = AIConfig.from_env()
    assert config.model == 'gemini-3.5-flash'


def test_google_api_key_is_supported_as_fallback(monkeypatch):
    monkeypatch.setenv('GEMINI_API_KEY', '')
    monkeypatch.setenv('GOOGLE_API_KEY', 'fallback-key')
    assert AIConfig.from_env().api_key == 'fallback-key'


def test_http_404_reports_model_unavailable(monkeypatch):
    config = AIConfig(
        provider='gemini', model='missing-model', use_mock=False,
        api_key='test-key', base_url='https://example.invalid',
        timeout_seconds=1,
    )

    def fail_request(*args, **kwargs):
        raise HTTPError('https://example.invalid', 404, 'missing', {}, None)

    monkeypatch.setattr(ai_client, 'urlopen', fail_request)
    with pytest.raises(ProviderError, match='model_unavailable'):
        GeminiClient(config).generate_json({'question': 'test'})


def test_provider_schema_locks_quiz_option_counts():
    quiz = LEARNING_RESPONSE_SCHEMA['properties']['quiz']
    assert quiz['properties']['options']['minItems'] == 4
    assert quiz['properties']['options']['maxItems'] == 4
    assert quiz['properties']['retry_options']['minItems'] == 2
    assert quiz['properties']['retry_options']['maxItems'] == 2


def test_document_viewer_keeps_scroll_on_outer_scroller():
    frontend = (
        Path(__file__).parents[1]
        / 'components'
        / 'document_selector_frontend'
        / 'index.html'
    ).read_text(encoding='utf-8')
    assert 'overscroll-behavior: contain;' in frontend
    assert 'touch-action: pan-y;' in frontend
    assert 'args.library_documents' in frontend
    slide_rule = frontend.split('.slide-canvas {', 1)[1].split('}', 1)[0]
    assert 'overflow: hidden;' in slide_rule
