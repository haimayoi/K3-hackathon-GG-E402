"""Run eval/golden_set.jsonl through the real AI call and record a results table.

Usage (from repo root, with GEMINI_API_KEY set in .env):
    python eval/run_golden_set.py

Writes:
    eval/run-01-<YYYYMMDD>.md     -- human-readable table, one row per case
    eval/run-01-<YYYYMMDD>.jsonl  -- full raw output per case, for the manual
                                      grounded/on-concept/domain-correct pass

Automates chiều 1 (đúng status) and chiều 4 (đúng định dạng schema) since those
are objectively checkable. Chiều 2/3/5 (có căn cứ / đúng phạm vi / đúng chuyên
môn) still need a human to read the raw output -- that's what the .jsonl is for.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from components.ai_client import generate_comprehension_quiz  # noqa: E402

GOLDEN_SET_PATH = Path(__file__).parent / "golden_set.jsonl"


def load_cases() -> list[dict]:
    cases = []
    with GOLDEN_SET_PATH.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def check_schema(result: dict) -> bool | None:
    """Chiều 4: đúng 4 options, correct_index hợp lệ, misconceptions phủ mọi option sai."""
    if result.get("status") != "ok":
        return None
    options = result.get("options") or []
    correct_index = result.get("correct_index")
    misconceptions = result.get("misconceptions") or []
    if len(options) != 4:
        return False
    if not isinstance(correct_index, int) or not (0 <= correct_index < 4):
        return False
    covered = {m.get("option_index") for m in misconceptions}
    wrong_indices = {i for i in range(4) if i != correct_index}
    return wrong_indices.issubset(covered)


def main() -> None:
    cases = load_cases()
    run_id = "run-01-" + date.today().strftime("%Y%m%d")
    md_path = Path(__file__).parent / f"{run_id}.md"
    jsonl_path = Path(__file__).parent / f"{run_id}.jsonl"

    rows = []
    status_matches = 0
    schema_checks = []

    for case in cases:
        result = generate_comprehension_quiz(case["selected_text"], case["tutor_answer"])
        status_match = result.get("status") == case["expected_status"]
        schema_valid = check_schema(result)
        if status_match:
            status_matches += 1
        if schema_valid is not None:
            schema_checks.append(schema_valid)

        rows.append(
            {
                "id": case["id"],
                "class": case["class"],
                "expected_status": case["expected_status"],
                "actual_status": result.get("status"),
                "status_match": status_match,
                "schema_valid": schema_valid,
                "question": result.get("question"),
                "reason": result.get("reason"),
                "raw_result": result,
            }
        )

    total = len(cases)
    schema_pass = sum(1 for v in schema_checks if v)
    schema_total = len(schema_checks)

    with jsonl_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    lines = [
        f"# {run_id} — golden set results ({total} case)",
        "",
        f"**Chiều 1 (đúng status): {status_matches}/{total} ({status_matches / total:.0%})**",
        (
            f"**Chiều 4 (đúng schema, chỉ tính case status=ok cả hai bên): "
            f"{schema_pass}/{schema_total}"
            + (f" ({schema_pass / schema_total:.0%})" if schema_total else " (n/a)")
            + "**"
        ),
        "",
        "Chiều 2 (có căn cứ) / 3 (đúng phạm vi) / 5 (đúng chuyên môn ở lớp ④) chưa tự động hoá được "
        f"— đọc `{jsonl_path.name}` và chấm tay theo `eval/golden_set.md`, 2 người chấm độc lập các case khó.",
        "",
        "| id | lớp | expected | actual | status khớp? | schema hợp lệ? | question (rút gọn) |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        q = (row["question"] or row["reason"] or "").replace("\n", " ")
        if len(q) > 70:
            q = q[:70] + "…"
        schema_cell = "–" if row["schema_valid"] is None else ("✓" if row["schema_valid"] else "✗")
        lines.append(
            f"| {row['id']} | {row['class']} | {row['expected_status']} | {row['actual_status']} | "
            f"{'✓' if row['status_match'] else '✗'} | {schema_cell} | {q} |"
        )

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Chiều 1 (status): {status_matches}/{total} ({status_matches / total:.0%})")
    if schema_total:
        print(f"Chiều 4 (schema): {schema_pass}/{schema_total} ({schema_pass / schema_total:.0%})")
    print(f"Wrote {md_path}")
    print(f"Wrote {jsonl_path}")


if __name__ == "__main__":
    main()
