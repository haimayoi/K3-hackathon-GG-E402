# BUGFIX-1 — API key và Gemini provider

- Thời điểm: 2026-07-30 17:18 +07:00
- Mục tiêu: Khôi phục lời gọi Gemini thật mà không ghi hoặc hiển thị API key.
- Hiện trạng trước khi làm: Key trong `.env` được nạp, nhưng `gemini-2.5-flash` trả HTTP 404. UI chưa có cấu hình key theo session; output grounded có thể sai contract quiz.
- Thay đổi đã thực hiện: Migrate sang `gemini-3.5-flash`; hỗ trợ `GOOGLE_API_KEY`; phân loại HTTP; thêm password input chỉ lưu trong session; truyền `AIConfig` vào engine; khóa JSON schema và số option.
- File thay đổi: `services/ai_client.py`, `services/learning_engine.py`, `components/chatbot_panel.py`, `app.py`, `.env.example`, `README.md`, `tests/test_web_regressions.py`.
- Command/test đã chạy: `python -m pytest -q tests\test_env_config.py tests\test_web_regressions.py -k model`; real smoke `run_learning_turn(...)`; `git diff --check`.
- Kết quả: Unit subset PASS. Real smoke thiếu context trả `insufficient_context`, không quiz. Real grounded smoke trả `grounded`, 1 citation, quiz và retry hợp lệ bằng `gemini-3.5-flash`. Không in/ghi key.
- Bằng chứng/đường dẫn artifact: `tests/test_web_regressions.py`, `eval/runs/run-001/`.
- Vấn đề còn lại: Eval gặp quota HTTP 429 ở một số case; quality bar chưa đạt và không được hạ.
- Trạng thái: PASS
- Bước tiếp theo: Resume case lỗi quota; review FAIL tách biệt ERROR hạ tầng.
