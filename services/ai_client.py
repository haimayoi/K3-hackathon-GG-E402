'''OpenAI Responses API adapter configured only through environment values.'''

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_OPENAI_MODEL = 'gpt-5.6-luna'

LEARNING_RESPONSE_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'status': {
            'type': 'string',
            'enum': [
                'grounded', 'insufficient_context', 'ambiguous', 'out_of_scope'
            ],
        },
        'answer': {'type': 'string'},
        'citations': {
            'type': 'array',
            'items': {
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    'page': {'type': 'integer'},
                    'quote': {'type': 'string'},
                },
                'required': ['page', 'quote'],
            },
        },
        'reason': {'type': 'string'},
        'quiz': {
            'type': ['object', 'null'],
            'additionalProperties': False,
            'properties': {
                'question': {'type': 'string'},
                'options': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'minItems': 4,
                    'maxItems': 4,
                },
                'correct_option_index': {
                    'type': 'integer', 'minimum': 0, 'maximum': 3,
                },
                'correct_explanation': {'type': 'string'},
                'misconception_feedback': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'minItems': 4,
                    'maxItems': 4,
                },
                'retry_question': {'type': 'string'},
                'retry_options': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'minItems': 2,
                    'maxItems': 2,
                },
                'correct_retry_option_index': {
                    'type': 'integer', 'minimum': 0, 'maximum': 1,
                },
                'retry_correct_explanation': {'type': 'string'},
                'retry_wrong_explanation': {'type': 'string'},
            },
            'required': [
                'question', 'options', 'correct_option_index',
                'correct_explanation', 'misconception_feedback',
                'retry_question', 'retry_options',
                'correct_retry_option_index', 'retry_correct_explanation',
                'retry_wrong_explanation',
            ],
        },
    },
    'required': ['status', 'answer', 'citations', 'reason', 'quiz'],
}


def _load_dotenv_file() -> dict[str, str]:
    """Read a local .env file into memory without mutating the process env."""
    values: dict[str, str] = {}
    candidates = [Path.cwd(), Path(__file__).resolve().parents[1]]
    for base_dir in candidates:
        env_path = base_dir / '.env'
        if not env_path.is_file():
            continue
        for raw_line in env_path.read_text(encoding='utf-8').splitlines():
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                values[key] = value
        break
    return values


class ProviderError(RuntimeError):
    '''Provider request or response failed without exposing credentials.'''


class ProviderConfigurationError(ProviderError):
    '''Required provider configuration is absent or unsupported.'''


@dataclass(frozen=True)
class AIConfig:
    provider: str
    model: str
    use_mock: bool
    api_key: str | None
    base_url: str
    timeout_seconds: float

    def __post_init__(self) -> None:
        '''Normalize the single supported provider and its configured model.'''
        object.__setattr__(self, 'provider', 'openai')
        object.__setattr__(
            self, 'model', str(self.model or '').strip() or DEFAULT_OPENAI_MODEL,
        )

    @classmethod
    def from_env(cls) -> 'AIConfig':
        dotenv_values = _load_dotenv_file()
        use_mock = (
            os.getenv('USE_MOCK_LLM')
            or dotenv_values.get('USE_MOCK_LLM', 'false')
        ).strip().lower() == 'true'
        model = (
            os.getenv('OPENAI_MODEL')
            or dotenv_values.get('OPENAI_MODEL')
            or os.getenv('LLM_MODEL')
            or dotenv_values.get('LLM_MODEL')
            or DEFAULT_OPENAI_MODEL
        ).strip()
        api_key = (
            os.getenv('OPENAI_API_KEY')
            or dotenv_values.get('OPENAI_API_KEY')
            or None
        )
        base_url = (
            os.getenv('OPENAI_BASE_URL')
            or dotenv_values.get('OPENAI_BASE_URL')
            or 'https://api.openai.com/v1'
        ).rstrip('/')
        timeout = (
            os.getenv('LLM_TIMEOUT_SECONDS')
            or dotenv_values.get('LLM_TIMEOUT_SECONDS')
            or '45'
        )

        return cls(
            provider='openai',
            model=model,
            use_mock=use_mock,
            api_key=api_key,
            base_url=base_url,
            timeout_seconds=float(timeout),
        )


@dataclass(frozen=True)
class ProviderResult:
    text: str
    latency_ms: int
    provider: str
    model: str


class OpenAIClient:
    def __init__(self, config: AIConfig | None = None) -> None:
        self.config = config or AIConfig.from_env()

    def generate_json(self, user_payload: dict[str, Any]) -> ProviderResult:
        if self.config.provider != 'openai':
            raise ProviderConfigurationError('LLM_PROVIDER chưa được hỗ trợ')
        if not self.config.api_key:
            raise ProviderConfigurationError('BLOCKED_BY_API_KEY')
        prompt_path = Path(__file__).parents[1] / 'prompts' / 'learning_assistant.md'
        instructions = prompt_path.read_text(encoding='utf-8')
        body = {
            'model': self.config.model,
            'instructions': instructions,
            'input': json.dumps(user_payload, ensure_ascii=False),
            'store': False,
            'text': {
                'format': {
                    'type': 'json_schema',
                    'name': 'learning_response',
                    'schema': LEARNING_RESPONSE_SCHEMA,
                    'strict': True,
                },
            },
        }
        endpoint = f'{self.config.base_url}/responses'
        request = Request(
            endpoint,
            data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.config.api_key}',
            },
            method='POST',
        )
        started = time.perf_counter()
        try:
            with urlopen(request, timeout=self.config.timeout_seconds) as response:
                payload = json.loads(response.read().decode('utf-8'))
            text = _extract_response_text(payload)
            if not isinstance(text, str) or not text.strip():
                raise ProviderError('Provider trả output rỗng')
            return ProviderResult(
                text.strip(), round((time.perf_counter() - started) * 1000),
                self.config.provider, self.config.model,
            )
        except ProviderError:
            raise
        except HTTPError as error:
            error_kind = {
                400: 'invalid_request',
                401: 'authentication_failed',
                403: 'permission_denied',
                404: 'model_unavailable',
                429: 'quota_exceeded',
            }.get(error.code, 'provider_error')
            raise ProviderError(
                f'provider_http_{error.code}:{error_kind}'
            ) from error
        except (URLError, TimeoutError, KeyError, ValueError) as error:
            raise ProviderError(f'provider_failure:{type(error).__name__}') from error


def _extract_response_text(payload: dict[str, Any]) -> str:
    '''Extract assistant text from a raw Responses API response.'''
    direct = payload.get('output_text')
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    for output_item in payload.get('output', []):
        if not isinstance(output_item, dict) or output_item.get('type') != 'message':
            continue
        for content_item in output_item.get('content', []):
            if not isinstance(content_item, dict):
                continue
            if content_item.get('type') == 'refusal':
                raise ProviderError('provider_refusal')
            text = content_item.get('text')
            if content_item.get('type') == 'output_text' and isinstance(text, str):
                return text.strip()
    raise ProviderError('Provider trả output rỗng')
