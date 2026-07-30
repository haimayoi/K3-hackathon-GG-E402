# CP6 — Demo 5 phút và Q&A

- Thời điểm tạo: 2026-07-30 (Asia/Saigon)
- Mục tiêu: Chuẩn bị outline/script/cases/Q&A/backup; không tuyên bố demo đã thực hiện.
- Hiện trạng: Không có slide PDF, video/screenshot backup, user quotes, run result hay dry-run row thật.
- Artifact: demo/slide-outline-6-pages.md, demo/demo-script-5-minutes.md,
  demo/live-cases.md, demo/judge-card-backup-cases.md, demo/qa-prep.md,
  demo/backup-plan.md, reflection/TEMPLATE.md.
- Command/test: kiểm tra đủ 6 slide, script tối đa 5 phút, 2 loại live case, 9 Q&A,
  marker placeholder/unchecked; git diff --check; git status --short.
- Kết quả artifact prep: PASS — 6 slide sections, 9 Q&A, grounded + hard case, script 4:30 + 0:30 buffer, checklist chưa chạy; git diff --check PASS.
- Trạng thái checkpoint: PLAN_ONLY / BLOCKED_BY_HUMAN_DEMO_AND_VALIDATION.

## Trình tự hoàn tất

1. Hoàn tất run 001 thật và user validation; không thay quality bar.
2. Điền slide 4 bằng kết quả thật và failure lớn nhất.
3. Điền slide 5 bằng ít nhất 2 quote thật có tên/vai/consent và thay đổi đã làm.
4. Chạy lại live candidates; thay case nếu failure evidence cho thấy không ổn định.
5. Tạo slide PDF 6 trang và media backup thật.
6. Điền tên người nói; bảo đảm mỗi thành viên nói ít nhất một phần.
7. Dry run có bấm giờ; tổng tối đa 5 phút; cập nhật timing sheet.
8. Thử judge-card case lạ, provider/network failure và Q&A.
9. Mỗi thành viên viết reflection riêng từ case fail thật.

## Checklist — chưa đạt cho đến khi có artifact thật

- [ ] demo-slides.pdf 6 trang tồn tại.
- [ ] Slide 4 có % thật so bar không đổi.
- [ ] Slide 5 có ít nhất 2 quote thật có consent.
- [ ] Happy + hard live cases đã verified bằng API thật.
- [ ] Media backup thật tồn tại và đã scan privacy.
- [ ] Dry run tối đa 5 phút có timing row thật.
- [ ] Mỗi thành viên có phần nói và reflection riêng.
- [ ] Judge-card case lạ đã thử.
- [ ] Q&A answers được cập nhật theo kết quả/feedback thật.

## Blockers cần con người

API key/run thật; validation ≥5 người; tên/phân công; slide production; screenshot/video;
dry run; thuyết trình và reflection cá nhân.
