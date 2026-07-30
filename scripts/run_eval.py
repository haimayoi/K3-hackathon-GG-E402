'''Run the complete golden set through the same engine used by Streamlit.'''

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
from typing import Any

ROOT = Path(__file__).parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.learning_response import normalize_text
from services.ai_client import AIConfig
from services.learning_engine import run_learning_turn

GOLDEN = ROOT / 'eval' / 'golden-set.jsonl'
QUALITY_BAR = 0.80
NON_GROUNDED = {'insufficient_context', 'ambiguous', 'out_of_scope'}


def load_cases() -> list[dict[str, Any]]:
    cases = [
        json.loads(line) for line in GOLDEN.read_text(encoding='utf-8').splitlines()
        if line.strip()
    ]
    if not cases:
        raise RuntimeError('Golden set rỗng')
    return cases


def load_existing_results(run_dir: Path) -> dict[str, dict[str, Any]]:
    path = run_dir / 'results.jsonl'
    if not path.is_file():
        return {}
    return {
        item['case_id']: item
        for item in (
            json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()
            if line.strip()
        )
    }


def write_blocker(run_dir: Path, reason: str) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    text = '''# BLOCKED_BY_API_KEY

Run 001 chưa chạy và không có result giả.

- Lý do: {}
- Golden set: eval/golden-set.jsonl
- Quality bar giữ nguyên: 80%, không citation bịa, không quiz khi non-grounded.
- Cấu hình rồi chạy:

    $env:LLM_PROVIDER='openai'
    $env:OPENAI_MODEL='gpt-5.6-luna'
    $env:OPENAI_API_KEY='YOUR_KEY'
    $env:USE_MOCK_LLM='false'
    python scripts/run_eval.py --run-id run-001
'''.format(reason)
    (run_dir / 'BLOCKED_BY_API_KEY.md').write_text(text, encoding='utf-8')


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    turn = run_learning_turn(
        str(case['selected_text']), int(case['page_number']),
        str(case['question']), case_id=str(case['case_id'])
    )
    response = turn.response
    checks: dict[str, bool] = {
        'status_match': response.status == case['expected_status'],
        'answer_present': bool(response.answer.strip()),
        'answer_size': len(response.answer) <= 900,
        'must_not_contain': all(
            item.casefold() not in response.answer.casefold()
            for item in case['must_not_contain']
        ),
        'quiz_gate': (response.quiz is not None) == (response.status == 'grounded'),
    }
    answer_normalized = normalize_text(response.answer).casefold()
    checks['expected_facts'] = all(
        normalize_text(fact).casefold() in answer_normalized
        for fact in case['expected_facts']
    )
    expected_page = case['expected_citation_page']
    checks['citation_page'] = (
        expected_page is None
        or bool(response.citations)
        and all(item.page == expected_page for item in response.citations)
    )
    context = normalize_text(str(case['selected_text'])).casefold()
    checks['citation_quotes'] = all(
        normalize_text(item.quote).casefold() in context
        for item in response.citations
    )
    if response.quiz is not None:
        quiz = response.quiz
        checks['quiz_structure'] = (
            len(quiz.options) == 4
            and len(set(quiz.options)) == 4
            and quiz.correct_option_index in range(4)
            and len(quiz.misconception_feedback) == 3
            and all(len(item) >= 20 for item in quiz.misconception_feedback.values())
        )
    else:
        checks['quiz_structure'] = response.status != 'grounded'
    hard_failure = (
        not checks['citation_quotes']
        or not checks['citation_page']
        or response.status in NON_GROUNDED and response.quiz is not None
        or not checks['quiz_structure']
    )
    outcome = 'ERROR' if response.status == 'error' else (
        'PASS' if all(checks.values()) and not hard_failure else 'FAIL'
    )
    return {
        'case_id': case['case_id'], 'outcome': outcome,
        'expected_status': case['expected_status'], 'actual_status': response.status,
        'checks': checks, 'hard_failure': hard_failure,
        'latency_ms': turn.latency_ms, 'provider': turn.provider,
        'model': turn.model, 'trace_path': turn.trace_path,
        'response': response.to_dict(),
    }


def write_results(run_dir: Path, results: list[dict[str, Any]], config: AIConfig) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / 'results.jsonl').write_text(
        ''.join(json.dumps(item, ensure_ascii=False) + '\n' for item in results),
        encoding='utf-8',
    )
    with (run_dir / 'results.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            'case_id', 'outcome', 'expected_status', 'actual_status',
            'hard_failure', 'latency_ms', 'provider', 'model', 'trace_path',
        ])
        writer.writeheader()
        for result in results:
            writer.writerow({key: result[key] for key in writer.fieldnames})
    total = len(results)
    passed = sum(item['outcome'] == 'PASS' for item in results)
    failed = sum(item['outcome'] == 'FAIL' for item in results)
    errors = sum(item['outcome'] == 'ERROR' for item in results)
    fabricated_citations = sum(
        not item['checks']['citation_quotes'] or not item['checks']['citation_page']
        for item in results
    )
    non_grounded_quiz = sum(
        item['actual_status'] in NON_GROUNDED
        and item['response']['quiz'] is not None for item in results
    )
    pass_rate = passed / total
    bar_met = (
        pass_rate >= QUALITY_BAR
        and fabricated_citations == 0
        and non_grounded_quiz == 0
    )
    summary = '''# Eval summary

- Run time UTC: {}
- Total: {}
- PASS / FAIL / ERROR: {} / {} / {}
- Pass rate: {:.2%}
- Quality bar: 80% + zero fabricated citation + zero non-grounded quiz
- Fabricated citation/page: {}
- Non-grounded quiz: {}
- Bar met: {}
- Provider/model: {} / {}
'''.format(
        datetime.now(timezone.utc).isoformat(), total, passed, failed, errors,
        pass_rate, fabricated_citations, non_grounded_quiz,
        'YES' if bar_met else 'NO', config.provider, config.model,
    )
    (run_dir / 'summary.md').write_text(summary, encoding='utf-8')
    failure_lines = ['# Failures', '']
    for item in results:
        if item['outcome'] == 'PASS':
            continue
        failed_checks = [key for key, ok in item['checks'].items() if not ok]
        failure_lines.append(
            '- {}: {} — {}'.format(
                item['case_id'], item['outcome'], ', '.join(failed_checks)
            )
        )
    if len(failure_lines) == 2:
        failure_lines.append('- Không có failure.')
    (run_dir / 'failures.md').write_text(
        '\n'.join(failure_lines) + '\n', encoding='utf-8'
    )
    safe_config = {
        'provider': config.provider, 'model': config.model,
        'quality_bar': QUALITY_BAR, 'case_count': total,
        'use_mock': config.use_mock,
    }
    (run_dir / 'config.json').write_text(
        json.dumps(safe_config, indent=2) + '\n', encoding='utf-8'
    )
    (run_dir / 'BLOCKED_BY_API_KEY.md').unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-id', default='run-001')
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--delay-seconds', type=float, default=0.0)
    args = parser.parse_args()
    run_dir = ROOT / 'eval' / 'runs' / args.run_id
    config = AIConfig.from_env()
    if config.use_mock:
        write_blocker(run_dir, 'USE_MOCK_LLM phải là false cho eval thật')
        print('BLOCKED_BY_API_KEY: mock mode is not allowed for official eval')
        return 2
    if not config.api_key:
        write_blocker(run_dir, 'OPENAI_API_KEY chưa được cấu hình')
        print('BLOCKED_BY_API_KEY: missing OPENAI_API_KEY')
        return 2
    cases = load_cases()
    existing = load_existing_results(run_dir) if args.resume else {}
    results = []
    calls_made = 0
    for case in cases:
        previous = existing.get(str(case['case_id']))
        if previous is not None and previous.get('outcome') != 'ERROR':
            results.append(previous)
            continue
        if calls_made and args.delay_seconds > 0:
            time.sleep(args.delay_seconds)
        results.append(evaluate_case(case))
        calls_made += 1
    if len(results) != len(cases):
        raise RuntimeError('Runner đã skip case')
    write_results(run_dir, results, config)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
