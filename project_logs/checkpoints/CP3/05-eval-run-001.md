# CP3.5 — Eval run 001

- Thời điểm: 2026-07-30 17:17 +07:00
- Mục tiêu: Chạy đủ 24 case qua cùng learning engine và so với quality bar đã khóa.
- Hiện trạng trước khi làm: Run cũ chỉ có `BLOCKED_BY_API_KEY.md`; model 2.5 trả 404.
- Thay đổi đã thực hiện: Chạy Gemini 3.5 thật; bổ sung resume/throttle; giữ mọi PASS/FAIL/ERROR; xóa blocker key sau khi có results.
- File thay đổi: `scripts/run_eval.py`, `eval/runs/run-001/*`, report này.
- Command/test đã chạy: `python scripts/run_eval.py --run-id run-001`; `python scripts/run_eval.py --run-id run-001 --resume --delay-seconds 6`; kiểm tra 24 dòng; `git diff --check`.
- Kết quả: 24/24 case; 10 PASS, 4 FAIL, 10 ERROR; pass rate 41.67%; 10 ERROR đều do `provider_http_429:quota_exceeded`; non-grounded quiz = 0; quality bar = NO.
- Bằng chứng/đường dẫn artifact: `eval/runs/run-001/results.jsonl`, `results.csv`, `summary.md`, `failures.md`, `config.json`.
- Vấn đề còn lại: Cần quota để resume 10 ERROR. Bốn FAIL cần review; không hạ quality bar và không bịa kết quả.
- Trạng thái: PARTIAL
- Bước tiếp theo: Chờ quota hồi phục rồi resume; summary cuối phải vẫn đủ 24 case.
