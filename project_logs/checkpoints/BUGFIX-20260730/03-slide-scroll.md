# BUGFIX-3 — Cuộn toàn bộ slide

- Thời điểm: 2026-07-30 17:18 +07:00
- Mục tiêu: Cho phép wheel/touch cuộn qua toàn bộ 29 trang thay vì kẹt ở slide đầu.
- Hiện trạng trước khi làm: Grid/flex reader thiếu `min-height: 0` và `overflow: hidden`; từng `.slide-canvas` có `overflow: auto`, có thể giữ sự kiện cuộn trong slide con.
- Thay đổi đã thực hiện: Khóa overflow tại workspace/reader; giữ `.document-scroll` là scroll owner; thêm `overscroll-behavior` và `touch-action`; bỏ overflow riêng trên slide canvas.
- File thay đổi: `components/document_selector_frontend/index.html`, `tests/test_web_regressions.py`.
- Command/test đã chạy: `python -m pytest -q tests\test_web_regressions.py -k document_viewer`; Chrome headless + CDP đo DOM thật; `git diff --check`.
- Kết quả: 29 page-card; `clientHeight=602`, `scrollHeight=8844`; `scrollTop` đổi từ 60 lên 8242; trang 29 nằm trong viewport cuối; server/browser test đã dừng.
- Bằng chứng/đường dẫn artifact: `tests/test_web_regressions.py`; số đo runtime ghi tại report này.
- Vấn đề còn lại: Chưa có automated wheel test trong CI vì repo không cài Playwright; đã kiểm tra DOM thật bằng Chrome CDP cục bộ.
- Trạng thái: PASS
- Bước tiếp theo: Human smoke bằng wheel/touchpad trên trình duyệt đích trước demo.
