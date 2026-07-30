"""Compatibility adapter for the preserved golden set.

The canonical app uses components.learning_agent. This module keeps the original
`generate_comprehension_quiz(selected_text, tutor_answer)` evaluation contract,
while adding strict validation, one repair attempt, sanitized failures, and
privacy-minimized trace metadata.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
_TRACE_PATH = Path(__file__).resolve().parents[2] / "eval" / "live_call_traces.jsonl"
_PROMPT_VERSION = "golden-set-quiz-2026-07-30-v2"
_MAX_ATTEMPTS = 2

_SYSTEM_INSTRUCTION = """Bạn là VLearn Learning Check Agent. Chỉ dựa trên hai đoạn context được cấp.
Quyết định xem interaction có chứa một khái niệm thật sự của khoá học và đủ căn cứ để tạo quiz không.
Nếu không đủ, ngoài phạm vi, logistics, câu chào, phép tính hoặc kiến thức phổ thông không thuộc khoá,
trả status='insufficient' với reason ngắn. Nếu đủ, tạo đúng MỘT quiz với đúng 4 options, đúng một
correct_index, và đúng một misconception có mục tiêu cho từng option sai. Không tiết lộ chain-of-thought.
"""


class Misconception(BaseModel):
    option_index: int
    explanation: str


class QuizResult(BaseModel):
    status: Literal["ok", "insufficient"]
    reason: str | None = None
    question: str | None = None
    options: list[str] | None = None
    correct_index: int | None = None
    misconceptions: list[Misconception] = Field(default_factory=list)


def _valid(result: dict[str, Any]) -> tuple[bool, str]:
    if result.get("status") == "insufficient":
        return bool(str(result.get("reason") or "").strip()), "insufficient requires a reason"
    options = result.get("options") or []
    correct_index = result.get("correct_index")
    misconceptions = result.get("misconceptions") or []
    if not str(result.get("question") or "").strip() or len(options) != 4:
        return False, "exactly one question with four options is required"
    if len({str(option).strip().casefold() for option in options}) != 4:
        return False, "options must be unique"
    if not isinstance(correct_index, int) or not 0 <= correct_index < 4:
        return False, "correct_index must be 0..3"
    covered = sorted(item.get("option_index") for item in misconceptions)
    expected = [index for index in range(4) if index != correct_index]
    if covered != expected:
        return False, "misconceptions must cover every wrong option exactly once"
    return True, ""


def _trace(record: dict[str, Any]) -> None:
    _TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _TRACE_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def generate_comprehension_quiz(
    selected_text: str,
    tutor_answer: str,
    source_id: str | None = None,
) -> dict[str, Any]:
    """Generate or abstain, preserving the original golden-set return shape."""
    call_id = str(uuid.uuid4())
    started = time.perf_counter()
    prompt_hash = hashlib.sha256((_PROMPT_VERSION + _SYSTEM_INSTRUCTION).encode()).hexdigest()[:16]
    api_key = os.environ.get("OPENAI_API_KEY")
    base_trace = {
        "call_id": call_id,
        "model": _MODEL,
        "prompt_version": _PROMPT_VERSION,
        "prompt_hash": prompt_hash,
        "source_id": source_id,
        "selected_text_chars": len(selected_text),
        "tutor_answer_chars": len(tutor_answer),
        "selected_text_hash": hashlib.sha256(selected_text.encode()).hexdigest()[:12],
    }
    if not api_key:
        result = {"status": "error", "reason_code": "provider_error", "reason": "Model provider chưa được cấu hình."}
        _trace(base_trace | result | {"latency_ms": 0, "attempts": 0})
        return result

    client = OpenAI(api_key=api_key)
    feedback: str | None = None
    last_reason = "schema_invalid"
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        repair = f"\nVALIDATION_FEEDBACK: {feedback}" if feedback else ""
        prompt = (
            f"SOURCE_ID: {source_id or 'legacy-eval-context'}\n"
            f"SELECTED_TEXT:\n---\n{selected_text}\n---\n"
            f"TUTOR_ANSWER:\n---\n{tutor_answer}\n---{repair}"
        )
        try:
            response = client.responses.parse(
                model=_MODEL,
                input=[
                    {"role": "system", "content": _SYSTEM_INSTRUCTION},
                    {"role": "user", "content": prompt},
                ],
                text_format=QuizResult,
                temperature=0.2,
            )
            parsed = response.output_parsed
            if parsed is None:
                feedback = "empty structured output"
                continue
            result = parsed.model_dump()
            valid, feedback = _valid(result)
            if valid:
                _trace(
                    base_trace
                    | {
                        "status": result["status"],
                        "reason_code": "eligible" if result["status"] == "ok" else "insufficient_context",
                        "latency_ms": round((time.perf_counter() - started) * 1000),
                        "attempts": attempt,
                        "validation_outcome": "pass",
                    }
                )
                return result
            last_reason = "schema_invalid"
        except Exception:
            result = {
                "status": "error",
                "reason_code": "provider_error",
                "reason": "Model provider tạm thời không khả dụng.",
            }
            _trace(
                base_trace
                | result
                | {
                    "latency_ms": round((time.perf_counter() - started) * 1000),
                    "attempts": attempt,
                    "validation_outcome": "provider_error",
                    "error_category": "provider_unavailable",
                }
            )
            return result

    result = {
        "status": "insufficient",
        "reason_code": last_reason,
        "reason": "Output không hợp lệ sau giới hạn hai lần tạo; hệ thống đã abstain.",
    }
    _trace(
        base_trace
        | result
        | {
            "latency_ms": round((time.perf_counter() - started) * 1000),
            "attempts": _MAX_ATTEMPTS,
            "validation_outcome": "fail",
        }
    )
    return result