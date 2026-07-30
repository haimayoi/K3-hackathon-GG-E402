import json
from pathlib import Path

import pytest

from models.learning_response import LearningResponse, ResponseValidationError
from services.ai_client import ProviderError, ProviderResult
from services.learning_engine import parse_provider_json, run_learning_turn


def valid_payload(page: int = 8, quote: str = 'Tri thức phải nhập bằng tay'):
    return {
        'status': 'grounded',
        'answer': 'Luật nhập tay trở thành nút thắt khi mở rộng.',
        'citations': [{'page': page, 'quote': quote}],
        'reason': 'Context có căn cứ trực tiếp.',
        'quiz': {
            'question': 'Đâu là nút thắt khi mở rộng?',
            'options': ['Luật nhập tay', 'GPU', 'Ảnh', 'Mạng'],
            'correct_option_index': 0,
            'correct_explanation': 'Luật nhập tay khó duy trì.',
            'misconception_feedback': {
                '1': 'GPU không phải ý của đoạn.',
                '2': 'Ảnh không phải ý của đoạn.',
                '3': 'Mạng không phải ý của đoạn.',
            },
            'retry_question': 'Luật thủ công có khó mở rộng không?',
            'retry_options': ['Có', 'Không'],
            'correct_retry_option_index': 0,
            'retry_correct_explanation': 'Đúng.',
            'retry_wrong_explanation': 'Hãy xem lại nút thắt nhập luật.',
        },
    }


def test_parse_valid_json():
    response = parse_provider_json(json.dumps(valid_payload(), ensure_ascii=False))
    assert response.status == 'grounded'
    assert response.quiz is not None


def test_reject_quiz_when_not_grounded():
    payload = valid_payload()
    payload['status'] = 'ambiguous'
    with pytest.raises(ResponseValidationError):
        LearningResponse.from_dict(payload)


def test_reject_citation_absent_from_context():
    response = LearningResponse.from_dict(valid_payload())
    with pytest.raises(ResponseValidationError):
        response.validate_citations('Đoạn khác hoàn toàn', 8)


def test_exactly_one_correct_option_is_structurally_enforced():
    payload = valid_payload()
    payload['quiz']['correct_option_index'] = 5
    with pytest.raises(ResponseValidationError):
        LearningResponse.from_dict(payload)


class FailingProvider:
    def generate_json(self, user_payload):
        raise ProviderError('provider_failure:test')


def test_graceful_fallback_when_provider_fails():
    turn = run_learning_turn(
        'Tri thức phải nhập bằng tay', 8, 'Nút thắt là gì?',
        client=FailingProvider(), write_trace=False,
    )
    assert turn.response.status == 'error'
    assert turn.response.quiz is None


class CapturingProvider:
    def __init__(self):
        self.payload = None

    def generate_json(self, user_payload):
        self.payload = user_payload
        return ProviderResult(
            json.dumps(valid_payload(page=12), ensure_ascii=False),
            1,
            'fake',
            'fake-model',
        )


def test_page_number_reaches_learning_turn():
    provider = CapturingProvider()
    turn = run_learning_turn(
        'Tri thức phải nhập bằng tay', 12, 'Nút thắt là gì?',
        client=provider, write_trace=False,
    )
    assert provider.payload['page_number'] == 12
    assert turn.response.citations[0].page == 12


def test_frontend_submission_contains_page_number():
    frontend = (
        Path(__file__).parents[1]
        / 'components'
        / 'document_selector_frontend'
        / 'index.html'
    ).read_text(encoding='utf-8')
    assert 'page_number: selectedPageNumber' in frontend
    assert '.closest(\'.page-card\')' in frontend
