# Slide outline — 6 trang

Status: OUTLINE ONLY. Chưa có slide PDF, user quote hay eval result thật.

## 1. User & Job — 35 giây

- Học viên đọc slide cần hiểu đúng khái niệm và tự kiểm tra trước khi học tiếp.
- Evidence: 1.074 review_concept/326 user; chỉ 1 lượt có check question.
- Nguồn: evidence/mining-summary.md.

## 2. Vì sao chọn — 35 giây

- Quiz: 1.073 lượt review không có check.
- Citation: 448 lượt rỗng/215 user — không chọn làm feature chính, giữ làm safety gate.
- Thiếu context: proxy 178 lượt/116 user — không chọn làm feature chính, giữ failure path.
- Nguồn: evidence/impact-analysis.md.

## 3. Giải pháp và live demo — 110 giây

- Lát cắt một câu và Conditional theo cost-of-error.
- Happy candidate: GS-006, trang 9, grounded answer + citation + quiz/retry.
- Hard candidate: GS-013, ambiguous, hỏi làm rõ và không quiz.
- Hai case phải chạy lại với API thật trước demo; hiện chưa gọi là ổn định.

## 4. Kết quả đo — 35 giây

- Golden set 24 case; quality bar khóa 80% + hai điều kiện 100%.
- Unit test: 7 passed.
- Run 001: BLOCKED_BY_API_KEY; không có phần trăm.
- Placeholder sau run thật: [PASS/FAIL/ERROR, %, failure lớn nhất].

## 5. User thật nói gì — 30 giây

- [QUOTE THẬT 1 + TÊN/VAI + CONSENT — CẦN ĐIỀN]
- [QUOTE THẬT 2 + TÊN/VAI + CONSENT — CẦN ĐIỀN]
- [THAY ĐỔI TỪ FEEDBACK — CẦN ĐIỀN]

## 6. Nếu thêm một tuần — 25 giây

1. Sửa failure lớn nhất từ run thật rồi chạy lại toàn bộ.
2. Đo learning outcome/quiz validity với người dùng thật, không dùng check-question flag làm kết luận.
3. Cải thiện extraction cho page không có text dựa trên case GS-022.

Tổng nội dung 4 phút 30 giây; giữ 30 giây buffer, tổng tối đa 5 phút.
