# CP1 — Canvas 7 dòng

> **Tên ý tưởng:** VLearn Check-for-Understanding  
> **Trạng thái:** Sẵn sàng trình TA sau khi điền tên người thử và tên thành viên ở dòng 7.

| # | Mục | Nội dung chốt |
|---:|---|---|
| 1 | **Chiến tuyến** | **Hướng A — VLearn AI Tutor:** tối ưu tutor hiện có bằng một bước kiểm tra hiểu ngắn sau khi giải thích khái niệm. |
| 2 | **Ai đang làm việc này — một vai cụ thể** | **Học viên vừa nhận lời giải thích một khái niệm từ VLearn Tutor trong buổi học** và muốn biết mình đã hiểu đúng trước khi học tiếp. |
| 3 | **Pain — ai, đang làm gì, vướng đâu, hậu quả gì** | Khi học viên vừa đọc lời giải thích của tutor và muốn xác nhận mình đã hiểu đúng, tutor thường kết thúc sau phần giải thích mà không kiểm tra lại; học viên vì vậy có thể tiếp tục học với một hiểu lầm chưa được phát hiện. |
| 4 | **1–2 bằng chứng đầu tiên** | **(1)** Trong 1.261 lượt hỏi–đáp, chỉ **3 lượt (0,24%)** có `asked_check_question=True`; chỉ **1 lượt (0,08%)** dùng move `validate_understanding`. **(2)** `misconceptions` và `follow_ups` đều trống ở **1.261/1.261 lượt tutor**; trong khi mining keyword sơ bộ cho thấy **560/1.261 câu hỏi (44,4%)** có nhu cầu giải thích/hiểu khái niệm. Phương pháp và ví dụ kiểm tra được ghi tại `evidence/cp1-mining.md`. |
| 5 | **Lát cắt MỘT CÂU** | **Với một học viên vừa nhận giải thích một khái niệm, AI đánh giá câu trả lời của học viên cho một câu kiểm tra ngắn là _hiểu đúng / hiểu một phần / có hiểu lầm_ và đưa một phản hồi hoặc gợi ý phù hợp để học viên biết chính xác phần cần sửa trước khi học tiếp.** |
| 6 | **AI tự làm đến đâu + lý do** | **Conditional automation / augment:** tutor mời học viên làm một câu kiểm tra ngắn; AI chỉ chẩn đoán sau khi học viên trả lời và luôn hiển thị căn cứ từ nội dung bài học. Không tự kết luận năng lực tổng thể, không chấm điểm và không lưu hồ sơ năng lực. Chọn mức này vì chẩn đoán sai có thể củng cố kiến thức sai; học viên phải thấy và có quyền sửa phản hồi. |
| 7 | **≥3 người sẽ thử + phân công có tên** | **Willing users ngoài nhóm:** `[Tên 1]`, `[Tên 2]`, `[Tên 3]`. **Phân công:** `[Tên A]` — evidence & khảo sát; `[Tên B]` — prompt & golden set; `[Tên C]` — prototype; `[Tên D]` — spec & validation; `[Tên E, nếu có]` — demo & QA. |

## Câu nói 30 giây với TA

“Nhóm chọn VLearn Check-for-Understanding cho học viên vừa được tutor giải thích một khái niệm. Trong 1.261 lượt hỏi–đáp, tutor chỉ hỏi kiểm tra hiểu 3 lần, move `validate_understanding` chỉ xuất hiện 1 lần, còn misconception và follow-up chưa từng được ghi nhận. Prototype của nhóm chỉ làm một quyết định AI: sau một câu kiểm tra ngắn, phân loại học viên hiểu đúng, hiểu một phần hay có hiểu lầm, rồi đưa hint có căn cứ. Nhóm chọn augment thay vì tự động chấm điểm vì chẩn đoán sai có thể làm học viên học sai.”

## Những gì nhóm không tuyên bố ở CP1

- Chưa tuyên bố rằng mọi học viên đều muốn bị kiểm tra sau mọi câu trả lời.
- Chưa suy ra “không có check question” đồng nghĩa với “học viên chắc chắn học sai”.
- Chưa tuyên bố hệ thống phát hiện misconception chính xác trước khi chạy golden set.

Ba nhận định này cần được xác nhận bằng khảo sát người dùng và evaluation sau CP1.
