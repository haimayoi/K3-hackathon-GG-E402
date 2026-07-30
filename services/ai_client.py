'''Small Gemini REST adapter configured only through environment variables.'''

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_GEMINI_MODEL = 'gemini-3.5-flash'
MODEL_MIGRATIONS = {
    # Gemini returns HTTP 404 for this model on newly provisioned accounts.
    'gemini-2.5-flash': DEFAULT_GEMINI_MODEL,
}

LEARNING_RESPONSE_SCHEMA = {
    'type': 'object',
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
            'properties': {
                'question': {'type': 'string'},
                'options': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'minItems': 4,
                    'maxItems': 4,
                },
                'correct_option_index': {'type': 'integer'},
                'correct_explanation': {'type': 'string'},
                'misconception_feedback': {
                    'type': 'object',
                    'properties': {
                        '0': {'type': 'string'},
                        '1': {'type': 'string'},
                        '2': {'type': 'string'},
                        '3': {'type': 'string'},
                    },
                },
                'retry_question': {'type': 'string'},
                'retry_options': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'minItems': 2,
                    'maxItems': 2,
                },
                'correct_retry_option_index': {'type': 'integer'},
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


def _load_dotenv_file() -> None:
    """Populate os.environ from a local .env file if present."""
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
            if key and key not in os.environ:
                os.environ[key] = value
        break


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

    @classmethod
    def from_env(cls) -> 'AIConfig':
        _load_dotenv_file()
        provider = os.getenv('LLM_PROVIDER', 'gemini').strip().lower()
        use_mock = os.getenv('USE_MOCK_LLM', 'false').strip().lower() == 'true'
        configured_model = os.getenv('LLM_MODEL', DEFAULT_GEMINI_MODEL).strip()
        return cls(
            provider=provider,
            model=MODEL_MIGRATIONS.get(configured_model, configured_model),
            use_mock=use_mock,
            api_key=os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY'),
            base_url=os.getenv(
                'GEMINI_BASE_URL',
                'https://generativelanguage.googleapis.com/v1beta',
            ).rstrip('/'),
            timeout_seconds=float(os.getenv('LLM_TIMEOUT_SECONDS', '45')),
        )


@dataclass(frozen=True)
class ProviderResult:
    text: str
    latency_ms: int
    provider: str
    model: str


class GeminiClient:
    def __init__(self, config: AIConfig | None = None) -> None:
        self.config = config or AIConfig.from_env()

    def generate_json(self, user_payload: dict[str, Any]) -> ProviderResult:
        if self.config.provider != 'gemini':
            raise ProviderConfigurationError('LLM_PROVIDER chưa được hỗ trợ')
        if not self.config.api_key:
            raise ProviderConfigurationError('BLOCKED_BY_API_KEY')
        prompt_path = Path(__file__).parents[1] / 'prompts' / 'learning_assistant.md'
        body = {
            'system_instruction': {
                'parts': [{'text': prompt_path.read_text(encoding='utf-8')}]
            },
            'contents': [{
                'role': 'user',
                'parts': [{'text': json.dumps(user_payload, ensure_ascii=False)}],
            }],
            'generationConfig': {
                'temperature': 0.1,
                'responseMimeType': 'application/json',
                'responseJsonSchema': LEARNING_RESPONSE_SCHEMA,
            },
        }
        endpoint = (
            f'{self.config.base_url}/models/{self.config.model}:generateContent'
        )
        request = Request(
            endpoint,
            data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'x-goog-api-key': self.config.api_key,
            },
            method='POST',
        )
        started = time.perf_counter()
        try:
            with urlopen(request, timeout=self.config.timeout_seconds) as response:
                payload = json.loads(response.read().decode('utf-8'))
            text = payload['candidates'][0]['content']['parts'][0]['text']
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
