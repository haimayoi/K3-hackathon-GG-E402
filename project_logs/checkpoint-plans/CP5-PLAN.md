# CP5 — Validation, changelog và dry run

- Thời điểm tạo: 2026-07-30 (Asia/Saigon)
- Mục tiêu: Chuẩn bị quy trình có thể chạy; không tuyên bố validation/dry run đã làm.
- Hiện trạng: Template đã tạo; feedback log chỉ có header; timing sheet chưa có lượt thật.
- File tạo: validation/README.md, validation/session-script.md,
  validation/feedback-log.csv, validation/feedback-summary-template.md,
  validation/consent-and-privacy-note.md, demo/dry-run-checklist.md,
  demo/timing-sheet.md, plan này.
- Command/test: kiểm tra CSV chỉ có header; tìm marker NOT YET RUN/CHƯA; git diff --check;
  git status --short.
- Kết quả artifact prep: PASS — feedback log đúng 1 header, marker chưa chạy và checklist unchecked; git diff --check PASS.
- Trạng thái checkpoint: PLAN_ONLY / BLOCKED_BY_HUMAN_VALIDATION.

## Timeline tuần tự

1. Freeze feature sau CP4; chỉ sửa bug/failure có evidence.
2. Chọn ít nhất 5 người ngoài nhóm, ưu tiên ít nhất 2 willing users đã khai; lấy consent.
3. Mỗi phiên 10 phút: giao task, im lặng quan sát, hỏi đúng 3 câu theo session script.
4. Log tên/vai khi consent, task, observation, quote nguyên văn và severity.
5. Tổng hợp pattern lặp; tách observation khỏi interpretation.
6. Chọn 1–2 thay đổi nhỏ có impact cao, trỏ về session/severity cụ thể.
7. Cập nhật spec.md §9 changelog; nếu giữ nguyên, ghi lý do từ evidence.
8. Chạy lại toàn bộ golden set sau thay đổi thành run-002.
9. So sánh run-001/run-002, không đổi quality bar 80% và hai điều kiện 100%.
10. Chuẩn bị slide final và dry run 5 phút có bấm giờ thật.
11. Kiểm tra ngẫu nhiên mỗi thành viên giải thích được phần có tên mình.

## Checklist rubric — để trống đến khi có evidence thật

- [ ] Ít nhất 5 feedback rows từ 5 người ngoài nhóm.
- [ ] Ít nhất 2 người là willing users đã khai.
- [ ] Có tên/vai và quote nguyên văn với consent.
- [ ] Có ít nhất một thay đổi từ feedback hoặc lý do giữ nguyên có căn cứ.
- [ ] spec.md §9 đã cập nhật từ feedback.
- [ ] run-002 chạy toàn bộ và so với run-001, bar không đổi.
- [ ] Slide final tồn tại.
- [ ] Dry run đã bấm giờ và timing-sheet có dòng thật.
- [ ] Mỗi thành viên giải thích được phần được phân công.

## Blockers cần con người

- Điền tên/mã thành viên và xác nhận willing users.
- Tuyển người thử, lấy consent, điều phối phiên và ghi quote thật.
- Cấu hình API key để hoàn tất run-001/run-002.
- Tạo slide và thực hiện dry run thật.

## Bước tiếp theo

Con người hoàn tất danh tính/willing users và API key trước; sau đó chạy timeline đúng thứ tự.
