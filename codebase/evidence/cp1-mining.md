# CP1 — Mining evidence ban đầu cho Check-for-Understanding

## 1. Phạm vi dữ liệu

- File nguồn cục bộ: `data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv`
- 2.522 message = 1.261 cặp student–tutor.
- 369 user, 585 conversation, toàn bộ ở chế độ `in_class`.
- Chỉ ghi mã lượt (`turn_id`) và trích dẫn ngắn; không sao chép data pack vào repo nộp bài.

## 2. Phương pháp đếm có thể kiểm lại

### Chỉ số hành vi tutor

Lọc `role = tutor`, sau đó:

1. Đếm `asked_check_question = True`.
2. Đếm `move_used = validate_understanding`.
3. Đếm `misconceptions != []`.
4. Đếm `follow_ups != []`.

Kết quả:

| Chỉ số | Số lượt | Tỷ lệ trên 1.261 lượt tutor |
|---|---:|---:|
| `asked_check_question=True` | 3 | 0,24% |
| `move_used=validate_understanding` | 1 | 0,08% |
| `misconceptions` khác `[]` | 0 | 0% |
| `follow_ups` khác `[]` | 0 | 0% |

### Nhu cầu giải thích — tín hiệu bổ trợ

Lọc `role = student`; không phân biệt hoa thường; đếm message chứa ít nhất một trong các cụm:

- `giải thích`
- `là gì`
- `hiểu ... thế nào`

Kết quả sơ bộ: **560/1.261 lượt (44,4%)**.

Đây là keyword mining có thể trùng nghĩa hoặc bỏ sót cách diễn đạt khác. Trước CP4 cần kiểm tra tay một mẫu ngẫu nhiên để ước lượng precision và điều chỉnh định nghĩa.

## 3. Năm ví dụ tutor giải thích rồi kết thúc, không kiểm tra hiểu

Các ví dụ dưới đây đều có `asked_check_question=False`; trích ngắn để minh họa pattern.

| Turn | Yêu cầu học viên | Kết thúc hành vi tutor | Move |
|---|---|---|---|
| `T0959` | “giải thích 4 chiến lược” | Giải thích Write / Select / Compress / Isolate rồi kết thúc. | `review_concept` |
| `T0020` | “Giải thích ... instruction” | Định nghĩa instruction và đưa ví dụ, không hỏi lại. | `review_concept` |
| `T1053` | “Format: Output trông như thế nào?” | Giải thích các dạng format, không kiểm tra áp dụng. | `review_concept` |
| `T0780` | “Sinh văn bản = đoán → nối vào câu → đoán tiếp” | Diễn giải vòng lặp sinh token rồi kết thúc. | `review_concept` |
| `T0990` | “Context là gì” | Dùng ẩn dụ “bàn làm việc”, không kiểm tra học viên hiểu giới hạn context. | `review_concept` |

Các ví dụ này chứng minh **pattern hành vi hiện tại**, chưa tự chứng minh rằng từng học viên đã hiểu sai.

## 4. Pain hypothesis cần xác nhận bằng khảo sát

> Khi tutor chỉ giải thích rồi kết thúc, một số học viên không biết mình đã hiểu đúng hay mới chỉ thấy câu trả lời “có vẻ hợp lý”; họ có thể tiếp tục học với hiểu lầm chưa được phát hiện.

### Khảo sát nhanh đề xuất — tối thiểu 20 người ngoài nhóm

Không hỏi dẫn dắt “Bạn có thích feature này không?”. Hỏi theo trải nghiệm gần nhất:

1. “Lần gần nhất bạn hỏi VLearn Tutor để hiểu một khái niệm, sau câu trả lời bạn làm gì để biết mình đã hiểu đúng?”
2. “Đã có lần nào bạn tưởng mình hiểu nhưng sau đó làm bài hoặc nghe giảng mới biết mình hiểu sai không? Hãy kể lại lần gần nhất.”
3. “Nếu tutor mời bạn trả lời một câu kiểm tra 20–30 giây sau phần giải thích, trong tình huống nào bạn sẽ dùng hoặc bỏ qua?”
4. “Bạn muốn nhận đáp án ngay, một gợi ý, hay được thử sửa một lần? Vì sao?”

Ghi nguyên văn từng câu trả lời, tên/vai người tham gia và đánh dấu pain được xác nhận chỉ khi có trải nghiệm cụ thể, không chỉ trả lời “có/không”.

## 5. Điều kiện để tiếp tục hoặc đổi hướng

- **Tiếp tục:** ít nhất 10/20 người mô tả từng không chắc mình hiểu đúng, từng phát hiện hiểu lầm muộn, hoặc sẵn sàng dùng check ngắn trong một tình huống cụ thể.
- **Điều chỉnh:** người dùng chỉ muốn check khi họ chủ động bật → thiết kế opt-in, không tự hiện sau mọi câu trả lời.
- **Đổi hướng:** dưới 10/20 người xác nhận pain và không có segment cụ thể có nhu cầu mạnh.
