# Decision log

## 2026-07-30 — Giữ nguyên UI CP2 cho đến khi đóng CP3

- Giữ `app.py`, custom document selector và bố cục hiện tại; chỉ thay đổi tối thiểu để truyền `page_number` và kết nối learning engine.
- Không dùng confidence tự báo làm cổng quyết định. Cổng trung tâm là trạng thái có thể kiểm tra: `grounded`, `insufficient_context`, `ambiguous`, `out_of_scope`, `error`.
- Prototype được khai là **Mock có AI thật ở lõi**. Mock chỉ được bật tường minh bằng `USE_MOCK_LLM=true`.
- Provider đầu tiên: Gemini REST để tránh thêm SDK provider; cấu hình hoàn toàn qua biến môi trường và không ghi key vào trace.
- Không suy đoán danh tính. Root workspace gợi ý `LeHaHaiVan`, trong khi branch là `2A202601465---Ha_Duyen_Hung`; giữ placeholder cho đến khi con người xác nhận.
- Quality bar sẽ được khóa ở 80% toàn bộ golden set, 0 citation bịa và 0 quiz ở case không grounded trước run 001.
