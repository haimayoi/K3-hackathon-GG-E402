# CP4.4 — Checkpoint 4 report
- Thời điểm: 2026-07-30 (Asia/Saigon)
- Mục tiêu: Soát rubric, test, Git hygiene và security trước khi lập kế hoạch CP5/CP6.
- Hiện trạng trước khi làm: Spec/evidence/runbook đã hoàn chỉnh; CP3 real run còn blocked.
- Thay đổi đã thực hiện: Chạy security/test suite và đối chiếu từng rubric checkbox.
- File thay đổi: report này.
- Command/test đã chạy: secret regex scan; staged/.env/raw-copy checks; pytest; compileall; git diff --check; git status --short.
- Kết quả:
  - Secret pattern: không tìm thấy.
  - Staged files: none; .env không tồn tại.
  - Raw chat CSV chỉ tồn tại tại data/vlearn-pack/chatlog nguồn gốc.
  - 7 pytest PASS; compileall PASS; git diff --check PASS.
- Bằng chứng/đường dẫn artifact: spec.md, evidence/, eval/, README.md, project_logs/checkpoints/CP4/.
- Vấn đề còn lại: API key/run 001, tên/mã/phân công, willing users, research tương tự, validation và dry run thật.
- Trạng thái: PASS
- Bước tiếp theo: Chỉ tạo plan/template CP5–CP6; không bịa execution.

## Rubric checklist

- [x] Evidence chuẩn B có log và script kiểm lại: evidence/, scripts/mine_review_concept.py.
- [x] Bảng impact ít nhất 3 ứng viên: evidence/impact-analysis.md.
- [x] Có ứng viên đã loại và lý do định lượng: spec.md §2.
- [x] Bốn lớp cụ thể: spec.md §5.
- [x] Ít nhất 8 kịch bản: 11 dòng trong spec.md §5.
- [x] Ít nhất 4 nguyên tắc có vị trí áp dụng: 6 dòng trong spec.md §4b.
- [x] Quality bar bằng số và khóa trước run: spec.md §7, eval/README.md.
- [x] Spec đủ §1–§9: spec.md.
- [x] Danh sách việc thiếu trước CP5: mục dưới.
- [x] git diff --check PASS.
- [x] Unit tests/compile PASS: 7 passed; compileall không lỗi.

## Việc bắt buộc trước/ở CP5

1. Con người xác nhận tên, mã học viên, phân công và naming mismatch.
2. Cấu hình GEMINI_API_KEY, chạy run 001 đủ 24 case và ghi kết quả thật.
3. Thành viên trực tiếp thử sản phẩm tương tự hoặc giữ TO VERIFY.
4. Xác nhận ít nhất 3 willing users có tên thật và consent phù hợp.
5. Test với ít nhất 5 người ngoài nhóm; ghi quote/observation thật.
6. Chỉ sửa 1–2 failure/feedback có evidence rồi chạy run 002 toàn bộ.
7. Tạo slide thật, backup thật và dry run 5 phút có bấm giờ.

## Security notes

- .gitignore chặn .env, .env.*, .venv, cache; giữ .env.example.
- Không stage file nào và không dùng git add dot.
- Trace chỉ chứa hash selected text và metadata; scan không thấy credential pattern.
- Không có bản copy mới của raw chat CSV ngoài data pack gốc.
