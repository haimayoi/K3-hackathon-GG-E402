import json
from pathlib import Path
from urllib.error import HTTPError

import pytest

import services.ai_client as ai_client
from components.pdf_loader import COURSE_PDF_PATHS, load_pdf_path
from services.ai_client import (
    AIConfig,
    LEARNING_RESPONSE_SCHEMA,
    OpenAIClient,
    ProviderError,
)


def test_course_slides_are_ordered_d1_then_d2():
    assert [path.name for path in COURSE_PDF_PATHS] == [
        'd1-slide-hackathon.pdf',
        'd2-slide-hackathon.pdf',
    ]
    documents = [load_pdf_path(path) for path in COURSE_PDF_PATHS]
    assert [document['page_count'] for document in documents] == [29, 29]


def test_openai_model_can_be_configured_from_env(monkeypatch):
    monkeypatch.setenv('OPENAI_MODEL', 'gpt-5.6-terra')
    config = AIConfig.from_env()
    assert config.provider == 'openai'
    assert config.model == 'gpt-5.6-terra'


def test_gemini_key_is_not_used_for_openai(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', '')
    monkeypatch.setenv('GEMINI_API_KEY', 'legacy-key')
    monkeypatch.setenv('GOOGLE_API_KEY', 'legacy-key')
    assert AIConfig.from_env().api_key is None


def test_http_404_reports_model_unavailable(monkeypatch):
    config = AIConfig(
        provider='openai', model='missing-model', use_mock=False,
        api_key='test-key', base_url='https://example.invalid',
        timeout_seconds=1,
    )
    assert config.model == 'missing-model'

    def fail_request(*args, **kwargs):
        raise HTTPError('https://example.invalid', 404, 'missing', {}, None)

    monkeypatch.setattr(ai_client, 'urlopen', fail_request)
    with pytest.raises(ProviderError, match='model_unavailable'):
        OpenAIClient(config).generate_json({'question': 'test'})


def test_openai_client_uses_responses_api_and_strict_schema(monkeypatch):
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return json.dumps({
                'output': [{
                    'type': 'message',
                    'content': [{'type': 'output_text', 'text': '{}'}],
                }],
            }).encode('utf-8')

    def fake_request(request, **kwargs):
        captured['url'] = request.full_url
        captured['body'] = json.loads(request.data.decode('utf-8'))
        return FakeResponse()

    monkeypatch.setattr(ai_client, 'urlopen', fake_request)
    config = AIConfig(
        provider='openai', model='gpt-5.6-luna', use_mock=False,
        api_key='test-key', base_url='https://api.openai.test/v1',
        timeout_seconds=1,
    )
    result = OpenAIClient(config).generate_json({'question': 'test'})

    assert captured['url'] == 'https://api.openai.test/v1/responses'
    assert captured['body']['text']['format']['strict'] is True
    assert captured['body']['store'] is False
    assert result.text == '{}'


def test_provider_schema_locks_quiz_option_counts():
    quiz = LEARNING_RESPONSE_SCHEMA['properties']['quiz']
    assert LEARNING_RESPONSE_SCHEMA['additionalProperties'] is False
    assert quiz['additionalProperties'] is False
    assert quiz['properties']['options']['minItems'] == 4
    assert quiz['properties']['options']['maxItems'] == 4
    assert quiz['properties']['retry_options']['minItems'] == 2
    assert quiz['properties']['retry_options']['maxItems'] == 2
    assert quiz['properties']['misconception_feedback']['minItems'] == 4
    assert quiz['properties']['misconception_feedback']['maxItems'] == 4


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
    assert 'document.createElement(\'button\')' in frontend
    assert 'action: \'switch_document\'' in frontend
    assert 'document_id: documentId' in frontend
    slide_rule = frontend.split('.slide-canvas {', 1)[1].split('}', 1)[0]
    assert 'overflow: hidden;' in slide_rule


def test_document_viewer_highlight_is_translucent_and_click_clears_it():
    frontend = (
        Path(__file__).parents[1]
        / 'components'
        / 'document_selector_frontend'
        / 'index.html'
    ).read_text(encoding='utf-8')
    assert '--selection: rgba(' in frontend
    assert 'background: var(--selection);' in frontend
    assert 'function clearActiveSelection()' in frontend
    assert 'window.CSS?.highlights?.delete("active-passage");' in frontend
    assert 'article.addEventListener("click", (event) =>' in frontend
    assert 'if (selection && !selection.isCollapsed) return;' in frontend


def test_selection_prefills_explanation_question():
    frontend = (
        Path(__file__).parents[1]
        / 'components'
        / 'document_selector_frontend'
        / 'index.html'
    ).read_text(encoding='utf-8')
    assert 'question.value = `Giải thích //${text}//`;' in frontend
    assert 'suggestedQuestion' not in frontend


def test_app_does_not_render_api_key_or_model_inputs():
    app_source = (Path(__file__).parents[1] / 'app.py').read_text(encoding='utf-8')
    assert 'render_ai_settings' not in app_source
    assert 'runtime_api_key' not in app_source
    assert 'Cấu hình AI' not in app_source
    assert 'handle_document_switch' in app_source
    assert 'render_scenario_control' not in app_source
    assert 'render_test_case_control' not in app_source
    assert 'TEST_CASES' not in app_source
    assert 'active_test_case' not in app_source
