"""Real OpenAI call for the prototype's central AI decision.

Lát cắt (canvas-cp1.md §5): after the tutor explains a concept, AI decides
whether/how to check the learner's understanding of THAT concept — this module
is that decision. Everything else in the flow (the tutor's own answer, the
retry follow-up question) stays mock and is labelled as such at the call site.

Class ① (nguồn sự thật) and ③ (ngoài phạm vi) are handled by instructing the
model to refuse (status="insufficient") instead of inventing a quiz when the
selected text has no clear academic content to check.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
_TRACE_PATH = Path(__file__).resolve().parent.parent / "eval" / "ai_call_log.jsonl"

_SYSTEM_INSTRUCTION = """Bạn là một tutor AI trong nền tảng học tập VLearn. Nhiệm vụ DUY NHẤT ở bước này:
sau khi đã giải thích một khái niệm cho học viên, soạn MỘT câu hỏi trắc nghiệm ngắn (đúng 4 lựa chọn,
đúng 1 đáp án đúng) để kiểm tra xem học viên có thực sự hiểu đúng khái niệm đó hay không.

Quy tắc bắt buộc:
- Câu hỏi PHẢI kiểm tra đúng khái niệm vừa giải thích, không hỏi lan man sang chủ đề khác.
- Chỉ dùng thông tin có trong đoạn văn được cung cấp — KHÔNG bịa thêm sự kiện, số liệu, hay khái niệm
  không có trong đoạn văn.
- Với mỗi lựa chọn SAI, giải thích rõ học viên đang hiểu nhầm điều gì — không chỉ nói "sai".
- Nếu đoạn văn KHÔNG đủ nội dung học thuật cụ thể để ra một câu hỏi kiểm tra hiểu có ý nghĩa
  (đoạn quá ngắn, là câu hỏi logistics, văn bản ngẫu nhiên, hoặc yêu cầu ngoài phạm vi giải thích
  khái niệm), trả về status="insufficient" kèm reason ngắn gọn bằng tiếng Việt — KHÔNG cố bịa câu hỏi.
- QUAN TRỌNG: "có một đáp án đúng-sai rõ ràng" KHÔNG đồng nghĩa với "đủ điều kiện ra quiz". Nếu đoạn văn
  không phải kiến thức của khoá học này (ví dụ: một phép tính số học đơn giản như "2 + 2 = ?", một câu đố
  vui, kiến thức phổ thông không liên quan bài giảng), PHẢI trả về status="insufficient" dù bản thân câu
  hỏi đó có đáp án đúng rõ ràng — vì nó không kiểm tra hiểu biết về nội dung khoá học.
- Khi status="ok": bắt buộc có đủ question, đúng 4 options, correct_index hợp lệ (0-3), và
  misconceptions cho từng option sai.
"""


class Misconception(BaseModel):
    option_index: int
    explanation: str


class QuizResult(BaseModel):
    status: str  # "ok" | "insufficient"
    reason: str | None = None
    question: str | None = None
    options: list[str] | None = None
    correct_index: int | None = None
    misconceptions: list[Misconception] = []


def _log_trace(record: dict[str, Any]) -> None:
    """Append one JSON line per call so CP3's 'AI thật, không hardcode' is auditable."""
    _TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _TRACE_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def generate_comprehension_quiz(selected_text: str, tutor_answer: str) -> dict[str, Any]:
    """Ask the model to produce (or refuse) a comprehension-check quiz.

    Returns a dict shaped like QuizResult, plus status="error" on any failure
    so the caller can render a graceful fallback instead of crashing.
    """
    call_id = uuid.uuid4().hex[:12]
    prompt = (
        "Đoạn tài liệu học viên đã bôi đen:\n"
        f'"""\n{selected_text}\n"""\n\n'
        "Câu trả lời tutor vừa đưa ra cho học viên:\n"
        f'"""\n{tutor_answer}\n"""\n\n'
        "Soạn quiz kiểm tra hiểu theo đúng quy tắc đã nêu."
    )

    started = time.time()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        result = {
            "status": "error",
            "reason": (
                "Thiếu OPENAI_API_KEY. Tạo file .env ở gốc repo (đã có trong .gitignore) "
                "với dòng OPENAI_API_KEY=<key của bạn>, xem .env.example."
            ),
        }
        _log_trace(
            {
                "call_id": call_id,
                "model": _MODEL,
                "selected_text": selected_text,
                "tutor_answer": tutor_answer,
                **result,
                "latency_s": round(time.time() - started, 2),
            }
        )
        return result

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.parse(
            model=_MODEL,
            input=[
                {"role": "system", "content": _SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt},
            ],
            text_format=QuizResult,
            temperature=0.3,
        )
        parsed: QuizResult = response.output_parsed
        result = parsed.model_dump()
    except Exception as exc:  # noqa: BLE001 - any failure must degrade gracefully in the UI
        result = {"status": "error", "reason": str(exc)}

    _log_trace(
        {
            "call_id": call_id,
            "model": _MODEL,
            "selected_text": selected_text,
            "tutor_answer": tutor_answer,
            **result,
            "latency_s": round(time.time() - started, 2),
        }
    )
    return result
