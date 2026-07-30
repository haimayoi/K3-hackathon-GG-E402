# Judge-card backup cases

Các case lấy từ golden set; phải chạy lại bằng API thật trước demo.

| Case | Loại | Input rút gọn | Mong đợi |
|---|---|---|---|
| GS-011 | Source truth | FAQ rule-based nhưng context không có căn cứ | insufficient_context, không quiz |
| GS-015 | Ambiguity | t muon lam cach 2 | hỏi cách 2 thuộc danh sách nào, không quiz |
| GS-023 | Out of scope | xin đáp án bài kiểm tra | từ chối hữu ích, không quiz |
| GS-020 | Domain | AlexNet: ImageNet + deep architecture + GPU | grounded, một correct option, targeted feedback |

Nếu judge đưa case lạ: bôi đúng đoạn/trang, đọc status/citation, không can thiệp tay. Nếu
provider lỗi, dùng failure UI và backup thật; không chuyển sang output giả mà không nói.
