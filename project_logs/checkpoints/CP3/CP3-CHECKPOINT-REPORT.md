# CP3.6 — Checkpoint 3 report

- Thời điểm: 2026-07-30 17:18 +07:00
- Mục tiêu: Đối chiếu CP3 sau real smoke và run 001.
- Hiện trạng trước khi làm: Contract/provider/golden/runner có sẵn nhưng bị chặn bởi key/model.
- Thay đổi đã thực hiện: Sửa model và structured output; real smoke hai nhánh; chạy đủ 24 case; thêm resume/throttle; lưu kết quả thật.
- File thay đổi: `services/`, `scripts/run_eval.py`, `eval/runs/run-001/`, report này.
- Command/test đã chạy: `python -m pytest -q`; compileall; real smoke; eval run + resume; Chrome CDP; `git diff --check`.
- Kết quả: AI thật PASS ở smoke. Run 001 có 24/24 dòng nhưng chỉ 41.67% PASS, 10 ERROR quota; quality bar NO.
- Bằng chứng/đường dẫn artifact: `models/learning_response.py`, `services/ai_client.py`, `eval/golden-set.jsonl`, `eval/runs/run-001/`, `project_logs/checkpoints/BUGFIX-20260730/`.
- Vấn đề còn lại: `BLOCKED_BY_API_QUOTA` cho 10 case; 4 FAIL cần review; chưa được khai Working.
- Trạng thái: PARTIAL
- Bước tiếp theo: Resume error khi quota hồi phục, sửa failure có bằng chứng và chạy run mới mà không đổi bar.

## Rubric checklist

- [x] Lời gọi AI thật, không hardcode; grounded và insufficient-context smoke PASS.
- [x] Trace/log sanitize; không key/header/full selected text.
- [x] Golden set 24 case, gồm 13 nguồn chatlog.
- [x] Bảng kết quả đủ 24 case, kể cả ERROR.
- [x] Có phần trăm và so bar; 41.67%, bar NO.
- [x] Mock chỉ bật tường minh.
- [x] App graceful ở provider/quota failure.
- [ ] Chưa đạt quality bar; CP3 tổng thể vẫn PARTIAL.

## Lệnh resume

    $env:LLM_PROVIDER='gemini'
    $env:LLM_MODEL='gemini-3.5-flash'
    $env:USE_MOCK_LLM='false'
    python scripts/run_eval.py --run-id run-001 --resume --delay-seconds 6
