"""Static content used by the prototype."""

DOCUMENT_TITLE = "Overfitting và Underfitting trong Machine Learning"

DEFAULT_DOCUMENT = """Overfitting xảy ra khi một mô hình học quá chi tiết dữ liệu huấn luyện, bao gồm cả nhiễu và những đặc điểm ngẫu nhiên. Vì vậy, mô hình có thể đạt kết quả rất tốt trên dữ liệu huấn luyện nhưng hoạt động kém trên dữ liệu mới.

Underfitting xảy ra khi mô hình quá đơn giản hoặc chưa học đủ các quy luật trong dữ liệu. Khi đó, mô hình thường hoạt động kém trên cả dữ liệu huấn luyện và dữ liệu kiểm thử.

Một số phương pháp giảm overfitting gồm tăng dữ liệu huấn luyện, sử dụng regularization, giảm độ phức tạp của mô hình và áp dụng early stopping."""

DEFAULT_SELECTION = """Overfitting xảy ra khi một mô hình học quá chi tiết dữ liệu huấn luyện, bao gồm cả nhiễu và những đặc điểm ngẫu nhiên. Vì vậy, mô hình có thể đạt kết quả rất tốt trên dữ liệu huấn luyện nhưng hoạt động kém trên dữ liệu mới."""

MOCK_ANSWER = """Khi mô hình học quá kỹ dữ liệu huấn luyện, nó không chỉ học các quy luật chung mà còn ghi nhớ cả nhiễu và những chi tiết ngẫu nhiên. Những chi tiết này thường không xuất hiện trong dữ liệu mới. Vì vậy, mô hình có thể đạt kết quả cao trên tập huấn luyện nhưng dự đoán kém trên tập kiểm thử hoặc dữ liệu thực tế."""

MOCK_CONFIDENCE = 0.87

MOCK_EVIDENCE = """“…mô hình học quá chi tiết dữ liệu huấn luyện, bao gồm cả nhiễu và những đặc điểm ngẫu nhiên…”"""

QUIZ_QUESTION = (
    "Tại sao mô hình bị overfitting thường hoạt động kém trên dữ liệu mới?"
)

QUIZ_OPTIONS = [
    "A. Vì mô hình không học được dữ liệu huấn luyện.",
    "B. Vì mô hình học cả nhiễu và các chi tiết không mang tính tổng quát.",
    "C. Vì dữ liệu huấn luyện luôn nhỏ hơn dữ liệu kiểm thử.",
    "D. Vì mô hình sử dụng quá ít tham số.",
]

CORRECT_QUIZ_OPTION = QUIZ_OPTIONS[1]

CORRECT_EXPLANATION = (
    "Chính xác. Overfitting làm mô hình ghi nhớ cả nhiễu và những chi tiết riêng "
    "của tập huấn luyện, nên mô hình khó tổng quát hóa sang dữ liệu mới."
)

MISCONCEPTION_FEEDBACK = {
    QUIZ_OPTIONS[0]: (
        "Bạn đang nhầm overfitting với underfitting. Mô hình bị overfitting thường "
        "học rất tốt dữ liệu huấn luyện. Vấn đề là nó ghi nhớ cả nhiễu và các chi "
        "tiết riêng của tập huấn luyện nên không tổng quát tốt sang dữ liệu mới."
    ),
    QUIZ_OPTIONS[2]: (
        "Kích thước tương đối giữa tập huấn luyện và tập kiểm thử không phải nguyên "
        "nhân trực tiếp gây overfitting. Nguyên nhân chính là mô hình học các chi "
        "tiết không mang tính tổng quát trong dữ liệu huấn luyện."
    ),
    QUIZ_OPTIONS[3]: (
        "Quá ít tham số thường khiến mô hình dễ underfitting hơn. Overfitting thường "
        "liên quan đến mô hình quá phức tạp so với lượng và chất lượng dữ liệu."
    ),
}

RETRY_QUESTION = (
    "Một mô hình đạt 99% độ chính xác trên tập huấn luyện nhưng chỉ đạt 65% trên "
    "tập kiểm thử. Trường hợp này có nhiều khả năng là gì?"
)

RETRY_OPTIONS = ["A. Overfitting", "B. Underfitting"]
CORRECT_RETRY_OPTION = RETRY_OPTIONS[0]

