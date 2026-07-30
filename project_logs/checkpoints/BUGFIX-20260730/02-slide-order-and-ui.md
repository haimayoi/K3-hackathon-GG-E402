# BUGFIX-2 — Sắp xếp D1/D2 và giao diện

- Thời điểm: 2026-07-30 17:18 +07:00
- Mục tiêu: Hiển thị đủ slide theo thứ tự D1 rồi D2 và sửa nhãn sai.
- Hiện trạng trước khi làm: App chỉ nạp D2 mặc định; D1 không có trong luồng chọn; UI ghi cứng Day 1 · 23 trang trong khi mỗi PDF hiện có 29 trang.
- Thay đổi đã thực hiện: Tạo catalog `COURSE_PDF_PATHS` theo D1 → D2; thêm selectbox tài liệu; remount viewer khi đổi file; sidebar custom component render động hai day-card và đánh dấu tài liệu active; tách selector tài liệu khỏi kịch bản kiểm thử.
- File thay đổi: `components/pdf_loader.py`, `components/document_panel.py`, `components/document_selector_frontend/index.html`, `app.py`, `tests/test_web_regressions.py`.
- Command/test đã chạy: `python -m pytest -q tests\test_web_regressions.py -k course_slides`; Streamlit AppTest đổi `d1` sang `d2`; browser CDP smoke.
- Kết quả: D1 và D2 đều tải 29/29 trang; AppTest chuyển sang `d2` không exception; browser thấy sidebar theo đúng `Day 1`, `Day 2` và 29 page-card của tài liệu active.
- Bằng chứng/đường dẫn artifact: `tests/test_web_regressions.py`, `components/document_selector_frontend/index.html`.
- Vấn đề còn lại: Topic shortcut vẫn là nhóm điều hướng chung, chưa ánh xạ mục lục riêng theo từng PDF.
- Trạng thái: PASS
- Bước tiếp theo: Chỉ bổ sung mục lục riêng nếu có yêu cầu nội dung xác thực.
