# Codex Task — Build Streamlit Learning Chatbot Flow Prototype

## 1. Mục tiêu

Xây dựng một ứng dụng **Streamlit prototype** mô phỏng luồng hoạt động của chatbot hỗ trợ học tập:

1. Người dùng xem tài liệu.
2. Người dùng chọn hoặc nhập đoạn nội dung cần giải thích.
3. Người dùng nhập câu hỏi liên quan đến đoạn đã chọn.
4. Chatbot hiển thị câu trả lời mẫu.
5. Hệ thống hiển thị điểm độ tin cậy của câu trả lời.
6. Nếu điểm tin cậy đạt ngưỡng, hệ thống đưa ra một câu hỏi trắc nghiệm ngắn.
7. Nếu người dùng trả lời sai, hệ thống giải thích lại đúng phần kiến thức bị hiểu sai.

Ở phiên bản hiện tại, chỉ cần xây dựng **giao diện cơ bản và luồng tương tác giả lập**. Không cần gọi API LLM, không cần RAG, không cần database và không cần xử lý tài liệu thật.

---

## 2. Công nghệ

- Python 3.10 trở lên
- Streamlit
- Không sử dụng framework frontend khác
- Không gọi API bên ngoài
- Dữ liệu mẫu được khai báo trực tiếp trong source code

---

## 3. Cấu trúc thư mục đề xuất

```text
learning-chatbot-demo/
├── app.py
├── requirements.txt
├── README.md
└── components/
    ├── __init__.py
    ├── document_panel.py
    ├── chatbot_panel.py
    └── quiz_panel.py
```

Có thể triển khai toàn bộ trong `app.py` nếu muốn giữ prototype đơn giản. Tuy nhiên, ưu tiên tách component để dễ cập nhật nội dung sau này.

---

## 4. Yêu cầu giao diện tổng thể

Trang web sử dụng layout rộng:

```python
st.set_page_config(
    page_title="Learning Assistant",
    page_icon="🎓",
    layout="wide"
)
```

Giao diện gồm ba khu vực chính:

### Sidebar

Hiển thị:

- Tên ứng dụng: `Learning Assistant`
- Tên tài liệu mẫu
- Thanh chọn ngưỡng confidence
- Nút reset phiên làm việc
- Phần mô tả ngắn về prototype

### Cột trái — Document Viewer

Hiển thị:

- Tiêu đề tài liệu
- Nội dung tài liệu mẫu
- Ô nhập đoạn văn được người dùng chọn
- Nút `Use selected text`

Do Streamlit mặc định chưa hỗ trợ lấy trực tiếp đoạn văn người dùng bôi đen trong Markdown, phiên bản prototype sử dụng `st.text_area` để giả lập phần nội dung đã được bôi đen.

### Cột phải — Learning Chatbot

Hiển thị:

- Đoạn nội dung đang được chọn
- Ô nhập câu hỏi
- Nút `Ask chatbot`
- Câu trả lời mẫu
- Điểm confidence
- Evidence hoặc phần nội dung được đối chiếu
- Câu hỏi trắc nghiệm nếu confidence đạt ngưỡng
- Phản hồi khi người dùng chọn đáp án

---

## 5. Nội dung tài liệu mẫu

Sử dụng nội dung mẫu sau:

```text
Overfitting xảy ra khi một mô hình học quá chi tiết dữ liệu huấn luyện, bao gồm cả nhiễu và những đặc điểm ngẫu nhiên. Vì vậy, mô hình có thể đạt kết quả rất tốt trên dữ liệu huấn luyện nhưng hoạt động kém trên dữ liệu mới.

Underfitting xảy ra khi mô hình quá đơn giản hoặc chưa học đủ các quy luật trong dữ liệu. Khi đó, mô hình thường hoạt động kém trên cả dữ liệu huấn luyện và dữ liệu kiểm thử.

Một số phương pháp giảm overfitting gồm tăng dữ liệu huấn luyện, sử dụng regularization, giảm độ phức tạp của mô hình và áp dụng early stopping.
```

Đoạn được chọn mặc định:

```text
Overfitting xảy ra khi một mô hình học quá chi tiết dữ liệu huấn luyện, bao gồm cả nhiễu và những đặc điểm ngẫu nhiên. Vì vậy, mô hình có thể đạt kết quả rất tốt trên dữ liệu huấn luyện nhưng hoạt động kém trên dữ liệu mới.
```

---

## 6. Luồng hoạt động của prototype

### State 1 — Chưa có câu hỏi

Giao diện hiển thị:

- Tài liệu mẫu
- Đoạn text đã chọn
- Ô nhập câu hỏi
- Chưa hiển thị answer hoặc quiz

### State 2 — Người dùng gửi câu hỏi

Khi nhấn `Ask chatbot`:

1. Kiểm tra đoạn selected text không rỗng.
2. Kiểm tra câu hỏi không rỗng.
3. Hiển thị spinner giả lập quá trình phân tích.
4. Hiển thị câu trả lời mẫu.
5. Hiển thị confidence score.
6. Nếu confidence lớn hơn hoặc bằng threshold, hiển thị quiz.
7. Nếu confidence thấp hơn threshold, hiển thị cảnh báo rằng chưa đủ độ tin cậy để tạo quiz.

### State 3 — Người dùng trả lời quiz

Khi người dùng chọn đáp án và nhấn `Submit answer`:

- Nếu đúng: hiển thị thông báo thành công và giải thích ngắn.
- Nếu sai: hiển thị thông báo chưa đúng, misconception tương ứng và phần giải thích lại.
- Sau khi trả lời sai, hiển thị thêm một câu kiểm tra lại đơn giản hơn.

---

## 7. Dữ liệu giả lập

### Câu trả lời mẫu

```text
Khi mô hình học quá kỹ dữ liệu huấn luyện, nó không chỉ học các quy luật chung mà còn ghi nhớ cả nhiễu và những chi tiết ngẫu nhiên. Những chi tiết này thường không xuất hiện trong dữ liệu mới. Vì vậy, mô hình có thể đạt kết quả cao trên tập huấn luyện nhưng dự đoán kém trên tập kiểm thử hoặc dữ liệu thực tế.
```

### Confidence mặc định

```python
mock_confidence = 0.87
```

### Evidence mẫu

```text
“...mô hình học quá chi tiết dữ liệu huấn luyện, bao gồm cả nhiễu và những đặc điểm ngẫu nhiên...”
```

### Quiz mẫu

Câu hỏi:

```text
Tại sao mô hình bị overfitting thường hoạt động kém trên dữ liệu mới?
```

Các lựa chọn:

```text
A. Vì mô hình không học được dữ liệu huấn luyện.
B. Vì mô hình học cả nhiễu và các chi tiết không mang tính tổng quát.
C. Vì dữ liệu huấn luyện luôn nhỏ hơn dữ liệu kiểm thử.
D. Vì mô hình sử dụng quá ít tham số.
```

Đáp án đúng:

```text
B. Vì mô hình học cả nhiễu và các chi tiết không mang tính tổng quát.
```

### Giải thích khi trả lời sai

Nếu người dùng chọn A:

```text
Bạn đang nhầm overfitting với underfitting. Mô hình bị overfitting thường học rất tốt dữ liệu huấn luyện. Vấn đề là nó ghi nhớ cả nhiễu và các chi tiết riêng của tập huấn luyện nên không tổng quát tốt sang dữ liệu mới.
```

Nếu người dùng chọn C:

```text
Kích thước tương đối giữa tập huấn luyện và tập kiểm thử không phải nguyên nhân trực tiếp gây overfitting. Nguyên nhân chính là mô hình học các chi tiết không mang tính tổng quát trong dữ liệu huấn luyện.
```

Nếu người dùng chọn D:

```text
Quá ít tham số thường khiến mô hình dễ underfitting hơn. Overfitting thường liên quan đến mô hình quá phức tạp so với lượng và chất lượng dữ liệu.
```

### Câu hỏi kiểm tra lại

```text
Một mô hình đạt 99% độ chính xác trên tập huấn luyện nhưng chỉ đạt 65% trên tập kiểm thử. Trường hợp này có nhiều khả năng là gì?
```

Các lựa chọn:

```text
A. Overfitting
B. Underfitting
```

Đáp án đúng:

```text
A. Overfitting
```

---

## 8. Quản lý trạng thái Streamlit

Sử dụng `st.session_state` với các biến sau:

```python
st.session_state.selected_text
st.session_state.user_question
st.session_state.answer_generated
st.session_state.mock_answer
st.session_state.confidence
st.session_state.quiz_visible
st.session_state.quiz_submitted
st.session_state.quiz_is_correct
st.session_state.selected_option
st.session_state.retry_quiz_visible
```

Khởi tạo các state khi ứng dụng chạy lần đầu.

Nút reset cần xóa hoặc khởi tạo lại toàn bộ session state.

---

## 9. Yêu cầu component

### `document_panel.py`

Tạo function:

```python
def render_document_panel(default_document: str, default_selection: str) -> str:
    ...
```

Chức năng:

- Hiển thị tài liệu mẫu.
- Hiển thị `st.text_area` chứa phần text được chọn.
- Trả về selected text hiện tại.

### `chatbot_panel.py`

Tạo function:

```python
def render_chatbot_panel(selected_text: str, confidence_threshold: float) -> None:
    ...
```

Chức năng:

- Hiển thị selected text.
- Nhận câu hỏi.
- Sinh phản hồi giả lập.
- Hiển thị confidence score.
- Quyết định có hiển thị quiz hay không.

### `quiz_panel.py`

Tạo function:

```python
def render_quiz_panel() -> None:
    ...
```

Chức năng:

- Hiển thị radio options.
- Chấm đáp án.
- Hiển thị feedback đúng hoặc sai.
- Khi sai, hiển thị targeted explanation.
- Hiển thị retry quiz.

---

## 10. Gợi ý bố cục Streamlit

```python
left_col, right_col = st.columns([1.1, 1])

with left_col:
    selected_text = render_document_panel(...)

with right_col:
    render_chatbot_panel(
        selected_text=selected_text,
        confidence_threshold=confidence_threshold
    )
```

Trong sidebar:

```python
with st.sidebar:
    st.title("🎓 Learning Assistant")
    confidence_threshold = st.slider(
        "Quiz confidence threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.80,
        step=0.05
    )
```

---

## 11. Cách hiển thị confidence

Hiển thị đồng thời:

- Giá trị phần trăm
- Progress bar
- Trạng thái bằng text

Ví dụ:

```python
st.metric("Answer confidence", "87%")
st.progress(0.87)
```

Phân loại:

```text
0.80–1.00: High confidence
0.60–0.79: Medium confidence
0.00–0.59: Low confidence
```

Không cần triển khai công thức tính confidence thật trong phiên bản này.

---

## 12. Yêu cầu trải nghiệm người dùng

- Giao diện sạch, dễ đọc.
- Có heading rõ ràng cho từng khu vực.
- Sử dụng `st.info`, `st.success`, `st.warning`, `st.error` hợp lý.
- Không hiển thị stack trace cho người dùng.
- Không cho gửi câu hỏi nếu selected text hoặc question rỗng.
- Có spinner khi giả lập chatbot đang xử lý.
- Quiz chỉ xuất hiện sau khi đã có câu trả lời và confidence đạt ngưỡng.
- Feedback sai phải chỉ ra đúng misconception tương ứng với đáp án người dùng chọn.
- Không tự động chuyển trang.
- Không cần đăng nhập.
- Không cần upload file ở phiên bản hiện tại.

---

## 13. `requirements.txt`

```text
streamlit>=1.36.0
```

---

## 14. Lệnh chạy ứng dụng

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Nếu PowerShell chặn script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

---

## 15. README cần có

README cần mô tả ngắn:

- Mục tiêu prototype
- Công nghệ sử dụng
- Cách cài đặt
- Cách chạy
- Luồng hoạt động
- Giới hạn hiện tại

Giới hạn hiện tại:

```text
- Chưa hỗ trợ bôi đen trực tiếp trên document viewer.
- Chưa tích hợp LLM.
- Chưa có RAG hoặc vector database.
- Confidence score đang được giả lập.
- Quiz và feedback đang sử dụng dữ liệu tĩnh.
- Chưa lưu tiến độ học tập.
```

---

## 16. Tiêu chí hoàn thành

Ứng dụng được xem là hoàn thành khi đáp ứng tất cả điều kiện sau:

- Chạy được bằng `streamlit run app.py`.
- Hiển thị document panel và chatbot panel trên cùng một trang.
- Người dùng có thể sửa đoạn selected text.
- Người dùng có thể nhập câu hỏi.
- Nhấn nút hỏi sẽ hiển thị câu trả lời giả lập.
- Hiển thị confidence score 87%.
- Thay đổi threshold trong sidebar có ảnh hưởng đến việc hiển thị quiz.
- Khi threshold nhỏ hơn hoặc bằng 0.87, quiz được hiển thị.
- Khi threshold lớn hơn 0.87, quiz không được hiển thị và có cảnh báo.
- Chọn đáp án đúng hiển thị trạng thái thành công.
- Chọn đáp án sai hiển thị misconception và giải thích lại.
- Sau câu trả lời sai có retry quiz.
- Nút reset đưa giao diện về trạng thái ban đầu.
- Source code rõ ràng, có comment ngắn tại các phần chính.

---

## 17. Không thực hiện trong phiên bản này

Không triển khai các chức năng sau:

- OpenAI API, Gemini API hoặc model LLM khác
- LangChain hoặc LlamaIndex
- Embedding
- Vector database
- OCR
- Upload PDF
- Authentication
- Database
- Theo dõi tiến độ học tập thật
- Phân tích misconception bằng AI
- Tính confidence thật
- Streaming token
- Deploy cloud

Các nội dung này sẽ được bổ sung ở phiên bản sau.

---

## 18. Yêu cầu cuối cùng dành cho Codex

Hãy thực hiện trực tiếp việc tạo source code hoàn chỉnh cho prototype theo đặc tả trên.

Ưu tiên:

1. Code chạy được ngay.
2. Luồng tương tác rõ ràng.
3. Giao diện cơ bản nhưng sạch và dễ mở rộng.
4. Không over-engineer.
5. Không thêm tính năng ngoài phạm vi.
6. Không gọi API thật.
7. Sử dụng dữ liệu mock để mô phỏng đầy đủ luồng học tập.

Sau khi hoàn thành, hãy kiểm tra syntax và cung cấp danh sách các file đã tạo hoặc chỉnh sửa.
