"""Historical CP2 mock fixtures; canonical app.py does not import this module."""

DOCUMENT_TITLE = "Overfitting và Underfitting trong Machine Learning"

DEFAULT_DOCUMENT = """Overfitting xảy ra khi một mô hình học quá chi tiết dữ liệu huấn luyện, bao gồm cả nhiễu và những đặc điểm ngẫu nhiên. Vì vậy, mô hình có thể đạt kết quả rất tốt trên dữ liệu huấn luyện nhưng hoạt động kém trên dữ liệu mới.

Underfitting xảy ra khi mô hình quá đơn giản hoặc chưa học đủ các quy luật trong dữ liệu. Khi đó, mô hình thường hoạt động kém trên cả dữ liệu huấn luyện và dữ liệu kiểm thử.

Một số phương pháp giảm overfitting gồm tăng dữ liệu huấn luyện, sử dụng regularization, giảm độ phức tạp của mô hình và áp dụng early stopping."""

DEFAULT_SELECTION = """Overfitting xảy ra khi một mô hình học quá chi tiết dữ liệu huấn luyện, bao gồm cả nhiễu và những đặc điểm ngẫu nhiên. Vì vậy, mô hình có thể đạt kết quả rất tốt trên dữ liệu huấn luyện nhưng hoạt động kém trên dữ liệu mới."""

MOCK_ANSWER = """Khi mô hình học quá kỹ dữ liệu huấn luyện, nó không chỉ học các quy luật chung mà còn ghi nhớ cả nhiễu và những chi tiết ngẫu nhiên. Những chi tiết này thường không xuất hiện trong dữ liệu mới. Vì vậy, mô hình có thể đạt kết quả cao trên tập huấn luyện nhưng dự đoán kém trên tập kiểm thử hoặc dữ liệu thực tế."""

MOCK_CONFIDENCE = 0.87

MOCK_EVIDENCE = """“…mô hình học quá chi tiết dữ liệu huấn luyện, bao gồm cả nhiễu và những đặc điểm ngẫu nhiên…”"""

# The comprehension-check quiz itself (question/options/misconceptions) is no
# longer static — it's generated per-turn by a real Gemini call in
# components/ai_client.py (see chatbot_panel._consume_submission). Only the
# retry follow-up below stays mock, out of CP3's scope.

RETRY_QUESTION = (
    "Một mô hình đạt 99% độ chính xác trên tập huấn luyện nhưng chỉ đạt 65% trên "
    "tập kiểm thử. Trường hợp này có nhiều khả năng là gì?"
)

RETRY_OPTIONS = ["A. Overfitting", "B. Underfitting"]
CORRECT_RETRY_OPTION = RETRY_OPTIONS[0]

