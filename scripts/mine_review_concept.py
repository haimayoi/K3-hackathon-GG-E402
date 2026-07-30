'''Mine anonymized review_concept tutor turns without exporting raw chatlog.'''

from __future__ import annotations

import csv
import json
from pathlib import Path
import re
from statistics import median, quantiles

ROOT = Path(__file__).parents[1]
CSV_PATH = ROOT / 'data' / 'vlearn-pack' / 'chatlog' / 'chat_history_anonymized_for_hackathon.csv'
DICTIONARY_PATH = CSV_PATH.parent / 'DATA_DICTIONARY.md'
EVIDENCE_DIR = ROOT / 'evidence'


def _json_list(value: str) -> list[object]:
    if not value or not value.strip():
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    return parsed if isinstance(parsed, list) else []


def _is_true(value: str) -> bool:
    return value.strip().lower() in {'true', '1', 'yes'}


def _short(value: str, limit: int = 180) -> str:
    clean = re.sub(r'\s+', ' ', value).strip()
    return clean if len(clean) <= limit else clean[: limit - 1].rstrip() + '…'


def mine() -> dict[str, object]:
    with CSV_PATH.open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    tutor = [row for row in rows if row['role'].strip().lower() == 'tutor']
    review = [row for row in tutor if row['move_used'] == 'review_concept']
    checked = sum(_is_true(row['asked_check_question']) for row in review)
    empty_citations = sum(not _json_list(row['citations']) for row in review)
    empty_citation_rows = [row for row in review if not _json_list(row['citations'])]
    context_markers = (
        'không tìm thấy', 'không có thông tin', 'cung cấp thêm',
        'chưa tìm thấy', 'không thể truy cập',
    )
    insufficient_rows = [
        row for row in review
        if any(marker in row['content'].casefold() for marker in context_markers)
    ]
    misconceptions = sum(len(_json_list(row['misconceptions'])) for row in review)
    follow_ups = sum(len(_json_list(row['follow_ups'])) for row in review)
    ratings = [row['rating'].strip().lower() for row in review if row['rating'].strip()]
    latencies = sorted(
        int(float(row['avg_latency_ms']))
        for row in review if row['avg_latency_ms'].strip()
    )
    p90 = quantiles(latencies, n=10, method='inclusive')[8] if latencies else 0
    return {
        'all_rows': len(rows),
        'tutor_turns': len(tutor),
        'review_rows': review,
        'review_count': len(review),
        'review_users': len({row['user_id'] for row in review}),
        'review_conversations': len({row['conversation_id'] for row in review}),
        'checked_count': checked,
        'empty_citation_count': empty_citations,
        'empty_citation_users': len({row['user_id'] for row in empty_citation_rows}),
        'empty_citation_conversations': len({
            row['conversation_id'] for row in empty_citation_rows
        }),
        'insufficient_proxy_count': len(insufficient_rows),
        'insufficient_proxy_users': len({row['user_id'] for row in insufficient_rows}),
        'insufficient_proxy_conversations': len({
            row['conversation_id'] for row in insufficient_rows
        }),
        'misconceptions_count': misconceptions,
        'follow_ups_count': follow_ups,
        'rated_count': len(ratings),
        'rating_up': ratings.count('up'),
        'rating_down': ratings.count('down'),
        'latency_count': len(latencies),
        'latency_median': median(latencies) if latencies else 0,
        'latency_p90': p90,
        'latency_max': max(latencies, default=0),
        'latency_over_10s': sum(value >= 10000 for value in latencies),
    }


def write_counts(data: dict[str, object]) -> None:
    review_count = int(data['review_count'])
    rows = [
        ('all_csv_rows', data['all_rows'], '', ''),
        ('tutor_turns', data['tutor_turns'], '', ''),
        ('review_concept_turns', review_count, '', ''),
        ('unique_users_with_review', data['review_users'], '', ''),
        ('unique_conversations_with_review', data['review_conversations'], '', ''),
        ('asked_check_question_rate', data['checked_count'] / review_count, data['checked_count'], review_count),
        ('empty_citation_rate', data['empty_citation_count'] / review_count, data['empty_citation_count'], review_count),
        ('empty_citation_users', data['empty_citation_users'], '', ''),
        ('empty_citation_conversations', data['empty_citation_conversations'], '', ''),
        ('insufficient_context_proxy_turns', data['insufficient_proxy_count'], '', ''),
        ('insufficient_context_proxy_users', data['insufficient_proxy_users'], '', ''),
        ('insufficient_context_proxy_conversations', data['insufficient_proxy_conversations'], '', ''),
        ('recorded_misconceptions', data['misconceptions_count'], '', ''),
        ('recorded_follow_ups', data['follow_ups_count'], '', ''),
        ('rated_review_responses', data['rated_count'], '', ''),
        ('rating_up', data['rating_up'], data['rating_up'], data['rated_count']),
        ('rating_down', data['rating_down'], data['rating_down'], data['rated_count']),
        ('latency_median_ms', data['latency_median'], '', data['latency_count']),
        ('latency_p90_ms', data['latency_p90'], '', data['latency_count']),
        ('latency_max_ms', data['latency_max'], '', data['latency_count']),
        ('latency_ge_10000ms', data['latency_over_10s'], '', data['latency_count']),
    ]
    path = EVIDENCE_DIR / 'review-concept-counts.csv'
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['metric', 'value', 'numerator', 'denominator'])
        writer.writerows(rows)


def write_method() -> None:
    text = '''# Mining method — review_concept

- Nguồn duy nhất: data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv.
- Đọc bằng csv.DictReader với UTF-8 BOM, đối chiếu tổng số dòng trước khi lọc.
- Tutor turn: role sau trim/lower bằng tutor.
- Pattern: move_used bằng chính xác review_concept trên tutor rows.
- Citation/misconception/follow-up rỗng khi JSON parse thành list rỗng.
- asked_check_question nhận true, 1 hoặc yes; rating chỉ tính dòng không rỗng.
- Latency tính trên avg_latency_ms của review rows; p90 dùng quantile inclusive.
- Outlier báo cáo minh bạch bằng max và proxy đếm latency từ 10.000 ms.
- Proxy thiếu context đếm tutor content có ít nhất một marker: không tìm thấy,
  không có thông tin, cung cấp thêm, chưa tìm thấy, không thể truy cập.
- Artifact chỉ chứa aggregate, ID ẩn danh và excerpt tối đa 180 ký tự; không sao chép raw pack.

Chạy lại:

    python scripts/mine_review_concept.py

Hạn chế: log chỉ gồm turn completed trong một tuần, rating rất thưa, và cờ
asked_check_question không chứng minh người học hiểu. Không suy diễn causal impact hay
thời gian tiết kiệm từ các proxy này.
'''
    (EVIDENCE_DIR / 'mining-method.md').write_text(text, encoding='utf-8')


def write_summary(data: dict[str, object]) -> None:
    review = int(data['review_count'])
    check_rate = int(data['checked_count']) / review
    empty_rate = int(data['empty_citation_count']) / review
    dictionary = DICTIONARY_PATH.read_text(encoding='utf-8')
    expected_review_match = re.search(
        r'review_concept[^0-9]{0,20}(\d+)', dictionary
    )
    expected_review = int(expected_review_match.group(1)) if expected_review_match else None
    comparison = (
        'KHỚP' if expected_review == review
        else f'KHÁC: dictionary={expected_review}, script={review}'
    )
    text = f'''# Mining summary — review_concept

- Toàn bộ CSV: {data['all_rows']} dòng.
- Tutor turn: {data['tutor_turns']}.
- review_concept: {review}; {data['review_users']} user; {data['review_conversations']} conversation.
- Có check question: {data['checked_count']}/{review} ({check_rate:.2%}).
- Citation rỗng: {data['empty_citation_count']}/{review} ({empty_rate:.2%}).
- Citation rỗng ảnh hưởng {data['empty_citation_users']} user và {data['empty_citation_conversations']} conversation.
- Proxy thiếu context: {data['insufficient_proxy_count']} turn,
  {data['insufficient_proxy_users']} user, {data['insufficient_proxy_conversations']} conversation.
- Misconception/follow-up ghi nhận: {data['misconceptions_count']}/{data['follow_ups_count']}.
- Rating trong review: up={data['rating_up']}, down={data['rating_down']}, rated={data['rated_count']}.
- Latency: median={data['latency_median']:.0f}ms, p90={data['latency_p90']:.0f}ms,
  max={data['latency_max']}ms, >=10s={data['latency_over_10s']}.
- Đối chiếu review_concept với DATA_DICTIONARY: {comparison}.

Các số này chứng minh pattern và khoảng trống đo lường, không chứng minh user đã hiểu.
'''
    (EVIDENCE_DIR / 'mining-summary.md').write_text(text, encoding='utf-8')


def write_examples(data: dict[str, object]) -> None:
    review = list(data['review_rows'])
    if len(review) < 5:
        raise RuntimeError('Không đủ 5 review_concept examples')
    step = max(1, len(review) // 5)
    chosen = [review[min(index * step, len(review) - 1)] for index in range(5)]
    lines = [
        '# Review concept examples',
        '',
        'Excerpt tối đa 180 ký tự, ID đã ẩn danh; không dùng để nhận diện người học.',
        '',
    ]
    for index, row in enumerate(chosen, start=1):
        excerpt = _short(row['content']).replace('|', '¦')
        lines.extend([
            f'## Ví dụ {index}',
            '- turn_id: {}'.format(row['turn_id']),
            '- conversation_id: {}'.format(row['conversation_id']),
            f'- excerpt: {excerpt}',
            '',
        ])
    (EVIDENCE_DIR / 'review-concept-examples.md').write_text(
        '\n'.join(lines), encoding='utf-8'
    )


def main() -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    data = mine()
    write_counts(data)
    write_method()
    write_summary(data)
    write_examples(data)
    print(
        'review_concept={} users={} conversations={}'.format(
            data['review_count'], data['review_users'], data['review_conversations']
        )
    )


if __name__ == '__main__':
    main()
