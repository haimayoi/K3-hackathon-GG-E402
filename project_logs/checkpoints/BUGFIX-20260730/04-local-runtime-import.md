# BUGFIX-4 — Local runtime import và restart sạch

- Thời điểm: 2026-07-30 17:40 +07:00
- Mục tiêu: Sửa lỗi khi mở app thật trên localhost 8501.
- Hiện trạng trước khi làm: Browser báo `ImportError` cho `COURSE_PDF_PATHS`, sau hot-reload tiếp tục dùng signature cũ của `document_panel`.
- Thay đổi đã thực hiện: `app.py` tự khai báo catalog D1/D2 thay vì import constant mới từ module có thể bị cache; dừng đúng launcher + child Streamlit cũ và khởi động fresh bằng `.venv`.
- File thay đổi: `app.py`, report này.
- Command/test đã chạy: kiểm tra process tree; `.venv` import/signature smoke; Chrome CDP trên localhost 8501; compileall; `pytest -q`; `git diff --check`.
- Kết quả: localhost 8501 không exception; 29 page-card; Day 1/Day 2 đúng; compile PASS; 14 tests PASS; server giữ chạy trên 8501.
- Bằng chứng/đường dẫn artifact: `app.py`; runtime log tạm tại `%TEMP%\vlearn-local-fresh.stderr.log`.
- Vấn đề còn lại: Browser cũ có thể cần Ctrl+F5 để bỏ màn hình exception đã cache.
- Trạng thái: PASS
- Bước tiếp theo: Mở `http://localhost:8501`; khi sửa module Python trong lúc dev nên restart Streamlit sạch.
