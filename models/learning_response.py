'''Strict contract for one learning-assistant response.'''

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any, Mapping

PROVIDER_STATUSES = {
    'grounded', 'insufficient_context', 'ambiguous', 'out_of_scope'
}


class ResponseValidationError(ValueError):
    '''Provider output violated the declared contract.'''


def _keys(value: Mapping[str, Any], expected: set[str], at: str) -> None:
    if set(value) != expected:
        raise ResponseValidationError(
            f'{at}: expected={sorted(expected)}, actual={sorted(value)}'
        )


def _text(value: Any, at: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ResponseValidationError(f'{at}: phải là chuỗi không rỗng')
    return value.strip()


def normalize_text(value: str) -> str:
    return re.sub(r'\s+', ' ', value.replace('“', '＂').replace('”', '＂')).strip()


@dataclass(frozen=True)
class Citation:
    page: int
    quote: str

    @classmethod
    def from_dict(cls, value: Any) -> 'Citation':
        if not isinstance(value, Mapping):
            raise ResponseValidationError('citation: phải là object')
        _keys(value, {'page', 'quote'}, 'citation')
        page = value['page']
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise ResponseValidationError('citation.page: phải là số nguyên dương')
        return cls(page, _text(value['quote'], 'citation.quote'))


@dataclass(frozen=True)
class Quiz:
    question: str
    options: list[str]
    correct_option_index: int
    correct_explanation: str
    misconception_feedback: dict[str, str]
    retry_question: str
    retry_options: list[str]
    correct_retry_option_index: int
    retry_correct_explanation: str
    retry_wrong_explanation: str

    @classmethod
    def from_dict(cls, value: Any) -> 'Quiz':
        if not isinstance(value, Mapping):
            raise ResponseValidationError('quiz: phải là object')
        _keys(value, set(cls.__dataclass_fields__), 'quiz')
        raw_options = value['options']
        if not isinstance(raw_options, list) or len(raw_options) != 4:
            raise ResponseValidationError('quiz.options: cần đúng 4 lựa chọn')
        options = [_text(item, f'options[{i}]') for i, item in enumerate(raw_options)]
        if len(set(options)) != 4:
            raise ResponseValidationError('quiz.options: lựa chọn phải khác nhau')
        correct = value['correct_option_index']
        if isinstance(correct, bool) or not isinstance(correct, int) or correct not in range(4):
            raise ResponseValidationError('correct_option_index: ngoài miền 0..3')
        raw_feedback = value['misconception_feedback']
        wrong_keys = {str(i) for i in range(4) if i != correct}
        if not isinstance(raw_feedback, Mapping) or set(raw_feedback) != wrong_keys:
            raise ResponseValidationError('misconception_feedback: sai tập đáp án')
        feedback = {str(k): _text(v, f'feedback[{k}]') for k, v in raw_feedback.items()}
        raw_retry = value['retry_options']
        if not isinstance(raw_retry, list) or len(raw_retry) != 2:
            raise ResponseValidationError('retry_options: cần đúng 2 lựa chọn')
        retry = [_text(item, f'retry[{i}]') for i, item in enumerate(raw_retry)]
        if len(set(retry)) != 2:
            raise ResponseValidationError('retry_options: lựa chọn phải khác nhau')
        retry_correct = value['correct_retry_option_index']
        if (
            isinstance(retry_correct, bool)
            or not isinstance(retry_correct, int)
            or retry_correct not in range(2)
        ):
            raise ResponseValidationError('correct_retry_option_index: ngoài miền 0..1')
        return cls(
            _text(value['question'], 'question'), options, correct,
            _text(value['correct_explanation'], 'correct_explanation'), feedback,
            _text(value['retry_question'], 'retry_question'), retry, retry_correct,
            _text(value['retry_correct_explanation'], 'retry_correct_explanation'),
            _text(value['retry_wrong_explanation'], 'retry_wrong_explanation'),
        )


@dataclass(frozen=True)
class LearningResponse:
    status: str
    answer: str
    citations: list[Citation]
    reason: str
    quiz: Quiz | None

    @classmethod
    def from_dict(cls, value: Any) -> 'LearningResponse':
        if not isinstance(value, Mapping):
            raise ResponseValidationError('response: phải là object')
        _keys(value, set(cls.__dataclass_fields__), 'response')
        status = value['status']
        if status not in PROVIDER_STATUSES:
            raise ResponseValidationError('response.status: không hợp lệ')
        raw_citations = value['citations']
        if not isinstance(raw_citations, list):
            raise ResponseValidationError('response.citations: phải là array')
        citations = [Citation.from_dict(item) for item in raw_citations]
        quiz = None if value['quiz'] is None else Quiz.from_dict(value['quiz'])
        if status == 'grounded' and (not citations or quiz is None):
            raise ResponseValidationError('grounded: bắt buộc citation và quiz')
        if status != 'grounded' and quiz is not None:
            raise ResponseValidationError(f'{status}: không được sinh quiz')
        return cls(
            status, _text(value['answer'], 'answer'), citations,
            _text(value['reason'], 'reason'), quiz
        )

    @classmethod
    def error(cls, message: str, reason: str) -> 'LearningResponse':
        return cls('error', message, [], reason, None)

    def validate_citations(self, context: str, page_number: int) -> None:
        normalized = normalize_text(context).casefold()
        for citation in self.citations:
            if citation.page != page_number:
                raise ResponseValidationError('citation.page không khớp page_number')
            if normalize_text(citation.quote).casefold() not in normalized:
                raise ResponseValidationError('citation.quote không có trong context')

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
