# VLearn Check-for-Understanding — CP2 Prototype

Prototype Streamlit mô phỏng giao diện VLearn và flow kiểm tra hiểu sau khi
AI Tutor giải thích một khái niệm.

## Chạy local

```powershell
py -3.11 -m pip install -r codebase/requirements.txt
py -3.11 -m streamlit run codebase/app.py
```

Nếu dùng virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r codebase/requirements.txt
streamlit run codebase/app.py
```

## Flow bấm được tại CP2

1. Mở một slide cụ thể trong tài liệu giả lập.
2. Bấm **Bôi đen đoạn “Context có thể hình dung…”** để mô phỏng chọn nội dung.
3. Thanh hành động xuất hiện với **Hỏi AI / Báo bối rối / Ghi chú**.
4. Bấm **Hỏi AI**, nhập câu hỏi và gửi cho Tutor.
5. Câu hỏi cùng phản hồi có căn cứ xuất hiện trong hội thoại bên phải.
6. Ngay sau phản hồi, hệ thống tự hiển thị **3 câu hỏi trắc nghiệm**; không hỏi học viên có muốn kiểm tra hay không.
7. Học viên chọn một đáp án cho từng câu và bấm **Nộp bài kiểm tra**.
8. Hệ thống hiển thị điểm `0–3/3`, giải thích từng câu và đáp án đúng cho câu làm sai.
9. Học viên có thể làm lại cả 3 câu hoặc báo lỗi kết quả chấm.
10. Có thể reset demo từ cột trái.

## Đáp án demo

Chọn các phương án sau để đạt `3/3`:

1. **Vì context chỉ chứa một lượng thông tin hữu hạn cho lượt xử lý hiện tại.**
2. **Một phần thông tin có thể bị bỏ sót hoặc không còn được nhìn thấy.**
3. **Context chỉ phục vụ lượt xử lý hiện tại, không mặc định là bộ nhớ vĩnh viễn.**

## Phần thật và phần mock

### Đã hoạt động thật

- Mô phỏng chọn/bôi đen nội dung trên một slide cụ thể.
- Thanh hành động **Hỏi AI / Báo bối rối / Ghi chú**.
- Nhập câu hỏi và đưa hội thoại sang panel Tutor bên phải.
- Tự hiển thị 3 câu trắc nghiệm sau phản hồi Tutor.
- Chặn nộp khi chưa trả lời đủ, chấm `0–3/3` và giải thích từng câu.
- Làm lại quiz và feedback/correction path.
- Guardrail: kết quả chỉ hỗ trợ tự học, không dùng làm điểm học tập.

### Đang mock ở CP2

- Slide và nội dung bài học.
- Ba câu hỏi, phương án và đáp án đúng.
- Giải thích đáp án và citation.

Tại CP3, AI call thật sẽ sinh quiz từ đoạn được chọn theo JSON có cấu trúc:

```json
{
  "source_segment_id": "T03-031",
  "questions": [
    {
      "question": "Câu hỏi",
      "options": ["A", "B", "C"],
      "correct_answer": "B",
      "explanation": "Giải thích dựa trên nguồn"
    }
  ]
}
```

## Checklist trình TA ở CP2

- [x] Flow chính bấm từ đầu đến cuối.
- [x] Có happy path.
- [x] Có partial/misconception path.
- [x] Có correction path.
- [x] Phần mock được ghi rõ.
- [ ] Repo có commit đầu tiên.
