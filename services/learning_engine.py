'''Shared learning engine used by Streamlit and the evaluation runner.'''

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import time
from typing import Any, Protocol
from uuid import uuid4

from components.mock_data import DEFAULT_TEST_CASE_ID, TEST_CASES
from models.learning_response import LearningResponse, ResponseValidationError
from services.ai_client import (
    AIConfig,
    GeminiClient,
    ProviderConfigurationError,
    ProviderError,
    ProviderResult,
)


class ProviderLike(Protocol):
    def generate_json(self, user_payload: dict[str, Any]) -> ProviderResult: ...


@dataclass(frozen=True)
class LearningTurn:
    response: LearningResponse
    provider: str
    model: str
    latency_ms: int
    trace_path: str | None


def parse_provider_json(raw_text: str) -> LearningResponse:
    text = raw_text.strip()
    fence = chr(96) * 3
    if text.startswith(fence + 'json') and text.endswith(fence):
        text = text[7:-3].strip()
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as error:
        raise ResponseValidationError('provider output không phải JSON') from error
    return LearningResponse.from_dict(payload)


def _write_trace(trace: dict[str, Any]) -> str:
    trace_dir = Path(__file__).parents[1] / 'eval' / 'traces'
    trace_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    path = trace_dir / f'{stamp}-{uuid4().hex[:8]}.json'
    path.write_text(
        json.dumps(trace, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    return str(path.relative_to(Path(__file__).parents[1]))


def _mock_response(selected_text: str, page_number: int, case_id: str) -> LearningResponse:
    scenario = TEST_CASES.get(case_id, TEST_CASES[DEFAULT_TEST_CASE_ID])
    options = list(scenario['quiz_options'])
    correct_text = str(scenario['correct_quiz_option'])
    correct = options.index(correct_text)
    feedback = {
        str(index): str(scenario['misconception_feedback'])
        for index in range(4) if index != correct
    }
    retry_options = list(scenario['retry_options'])
    retry_correct = retry_options.index(str(scenario['correct_retry_option']))
    quote = ' '.join(selected_text.split())[:180].strip()
    data = {
        'status': 'grounded',
        'answer': str(scenario['answer']),
        'citations': [{'page': page_number, 'quote': quote}],
        'reason': 'Mock demo được bật tường minh',
        'quiz': {
            'question': str(scenario['quiz_question']),
            'options': options,
            'correct_option_index': correct,
            'correct_explanation': str(scenario['correct_explanation']),
            'misconception_feedback': feedback,
            'retry_question': str(scenario['retry_question']),
            'retry_options': retry_options,
            'correct_retry_option_index': retry_correct,
            'retry_correct_explanation': str(scenario['retry_correct_explanation']),
            'retry_wrong_explanation': str(scenario['retry_wrong_explanation']),
        },
    }
    response = LearningResponse.from_dict(data)
    response.validate_citations(selected_text, page_number)
    return response


def run_learning_turn(
    selected_text: str,
    page_number: int,
    question: str,
    *,
    case_id: str | None = None,
    client: ProviderLike | None = None,
    config: AIConfig | None = None,
    write_trace: bool = True,
) -> LearningTurn:
    '''Run a turn and always return a graceful, structured response.'''
    selected_text = selected_text.strip()
    question = question.strip()
    event_id = case_id or uuid4().hex
    started = time.perf_counter()
    parse_result = 'not_started'
    citation_result = 'not_started'
    provider_name = 'unknown'
    model_name = 'unknown'
    error_code = None
    try:
        if not selected_text or not question or page_number < 1:
            raise ResponseValidationError('input không đầy đủ hoặc page_number sai')
        active_config = config or AIConfig.from_env()
        provider_name = active_config.provider
        model_name = active_config.model
        if active_config.use_mock and client is None:
            provider_name = 'mock'
            model_name = 'static-demo'
            response = _mock_response(
                selected_text, page_number, case_id or DEFAULT_TEST_CASE_ID
            )
            parse_result = 'valid'
            citation_result = 'valid'
        else:
            active_client = client or GeminiClient(active_config)
            result = active_client.generate_json({
                'case_id': event_id,
                'selected_text': selected_text,
                'page_number': page_number,
                'question': question,
            })
            provider_name = result.provider
            model_name = result.model
            response = parse_provider_json(result.text)
            parse_result = 'valid'
            response.validate_citations(selected_text, page_number)
            citation_result = 'valid'
    except ProviderConfigurationError as error:
        error_code = str(error)
        response = LearningResponse.error(
            'Chưa cấu hình dịch vụ trả lời. Bạn có thể thử lại sau khi thêm API key.',
            error_code,
        )
    except ProviderError as error:
        error_code = str(error)
        if 'authentication_failed' in error_code or 'permission_denied' in error_code:
            message = 'API key không hợp lệ hoặc chưa có quyền dùng Gemini.'
        elif 'model_unavailable' in error_code:
            message = 'Model AI không khả dụng. Hãy chọn model Gemini mới hơn.'
        elif 'quota_exceeded' in error_code:
            message = 'API key đã hết hạn mức tạm thời. Vui lòng thử lại sau.'
        else:
            message = 'Dịch vụ trả lời đang gián đoạn. Vui lòng thử lại.'
        response = LearningResponse.error(
            message,
            error_code,
        )
    except ResponseValidationError as error:
        error_code = type(error).__name__
        if parse_result == 'valid':
            citation_result = 'invalid'
        else:
            parse_result = 'invalid'
        response = LearningResponse.error(
            'Phản hồi chưa vượt qua kiểm tra an toàn. Vui lòng thử lại.',
            error_code,
        )
    except Exception as error:
        error_code = type(error).__name__
        response = LearningResponse.error(
            'Có lỗi không mong đợi. Vui lòng thử lại.',
            error_code,
        )
    latency_ms = round((time.perf_counter() - started) * 1000)
    trace = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'provider': provider_name,
        'model': model_name,
        'case_event_id': event_id,
        'page_number': page_number,
        'selected_text_sha256': sha256(selected_text.encode('utf-8')).hexdigest(),
        'question': question,
        'status': response.status,
        'latency_ms': latency_ms,
        'parse_validation': parse_result,
        'citation_validation': citation_result,
        'error': error_code,
    }
    trace_path = _write_trace(trace) if write_trace else None
    return LearningTurn(
        response, provider_name, model_name, latency_ms, trace_path
    )
