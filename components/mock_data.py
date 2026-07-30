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


# Three deterministic test routes grounded in day01-slide-blue-v0.pdf.
DEFAULT_TEST_CASE_ID = "expert_systems"

TEST_CASES = {
    "expert_systems": {
        "title": "Test 1 · Hệ chuyên gia và mùa đông AI",
        "slide_hint": "Trang 8–9",
        "focus_page": 8,
        "suggested_question": (
            "Vì sao hệ chuyên gia tạo ra giá trị nhưng vẫn dẫn đến mùa đông AI lần 2?"
        ),
        "answer": (
            "Hệ chuyên gia hoạt động tốt trong một miền hẹp bằng cách mã hóa tri thức "
            "chuyên gia thành luật. Tuy nhiên, khi mở rộng, tri thức phải được nhập thủ "
            "công, số lượng luật tăng nhanh, việc cập nhật trở nên khó khăn và hệ thống "
            "không xử lý tốt các ngoại lệ mới. Chính giới hạn về khả năng mở rộng và thích "
            "nghi này góp phần dẫn đến mùa đông AI lần 2."
        ),
        "evidence": (
            "“Tri thức phải nhập bằng tay, luật càng nhiều càng khó cập nhật, và hệ "
            "thống khó đứng vững trước ngoại lệ mới.”"
        ),
        "confidence": 0.91,
        "quiz_question": "Giới hạn cốt lõi của expert systems khi mở rộng là gì?",
        "quiz_options": [
            "A. Không thể giải bất kỳ bài toán chuyên môn hẹp nào.",
            "B. Phụ thuộc vào luật nhập tay, khó cập nhật và khó xử lý ngoại lệ mới.",
            "C. Chỉ hoạt động khi có GPU mạnh.",
            "D. Cần hàng triệu ván tự chơi để học.",
        ],
        "correct_quiz_option": (
            "B. Phụ thuộc vào luật nhập tay, khó cập nhật và khó xử lý ngoại lệ mới."
        ),
        "correct_explanation": (
            "Chính xác. Expert systems có thể hữu ích trong phạm vi hẹp, nhưng chi phí "
            "duy trì luật và khả năng ứng phó ngoại lệ khiến chúng khó mở rộng."
        ),
        "misconception_feedback": (
            "Điểm cần nhớ không phải là hệ chuyên gia hoàn toàn vô dụng. Chúng từng tạo "
            "ra giá trị thật, nhưng mô hình tri thức nhập tay trở thành nút thắt khi quy mô "
            "và số lượng ngoại lệ tăng lên."
        ),
        "retry_question": (
            "Một hệ thống cần chuyên gia sửa luật mỗi khi xuất hiện ngoại lệ mới. Đây có "
            "phải là dấu hiệu khó mở rộng của expert systems không?"
        ),
        "retry_options": ["A. Có", "B. Không"],
        "correct_retry_option": "A. Có",
        "retry_correct_explanation": (
            "Đúng. Phụ thuộc liên tục vào thao tác cập nhật luật thủ công là điểm nghẽn "
            "chính của hệ chuyên gia."
        ),
        "retry_wrong_explanation": (
            "Chưa đúng. Khi mỗi ngoại lệ đều cần sửa luật thủ công, chi phí vận hành sẽ "
            "tăng nhanh và hệ thống khó thích nghi ở quy mô lớn."
        ),
    },
    "alexnet": {
        "title": "Test 2 · Bước ngoặt AlexNet",
        "slide_hint": "Trang 12",
        "focus_page": 12,
        "suggested_question": (
            "Những yếu tố nào giúp AlexNet tạo ra bước ngoặt cho Deep Learning năm 2012?"
        ),
        "answer": (
            "AlexNet thành công nhờ sự kết hợp của ba yếu tố: ImageNet cung cấp lượng dữ "
            "liệu lớn, kiến trúc mạng sâu học đặc trưng theo nhiều tầng từ cạnh đến đối "
            "tượng, và GPU cung cấp đủ năng lực tính toán để huấn luyện khả thi. Kết quả "
            "này khiến ngành tin rằng năng lực mô hình có thể tiếp tục tăng khi dữ liệu và "
            "tính toán cùng mở rộng."
        ),
        "evidence": (
            "“ImageNet cho mô hình ăn một lượng dữ liệu chưa từng có… Kiến trúc sâu… "
            "GPU cung cấp đủ năng lực tính toán.”"
        ),
        "confidence": 0.89,
        "quiz_question": "Bộ ba nào mô tả đúng nền tảng thành công của AlexNet?",
        "quiz_options": [
            "A. Luật chuyên gia, suy luận symbolic và CPU.",
            "B. ImageNet, kiến trúc sâu và GPU.",
            "C. Transformer, attention và dữ liệu hội thoại.",
            "D. Tự chơi, reinforcement learning và tìm kiếm cây.",
        ],
        "correct_quiz_option": "B. ImageNet, kiến trúc sâu và GPU.",
        "correct_explanation": (
            "Chính xác. Dữ liệu, kiến trúc và năng lực tính toán cùng hội tụ đã tạo nên "
            "bước ngoặt AlexNet."
        ),
        "misconception_feedback": (
            "Hãy quay lại ba ý trên slide 12: dữ liệu ImageNet, kiến trúc đủ sâu để học "
            "đặc trưng phân cấp, và GPU giúp quá trình huấn luyện trở nên khả thi."
        ),
        "retry_question": "Nếu thiếu GPU, việc huấn luyện AlexNet thời điểm đó có dễ khả thi không?",
        "retry_options": ["A. Có", "B. Không"],
        "correct_retry_option": "B. Không",
        "retry_correct_explanation": (
            "Đúng. Slide nhấn mạnh GPU là yếu tố cung cấp đủ năng lực tính toán cho huấn luyện."
        ),
        "retry_wrong_explanation": (
            "Chưa đúng. Ở thời điểm đó, GPU là điều kiện quan trọng để khối lượng tính "
            "toán của mạng sâu trở nên khả thi."
        ),
    },
    "transformer": {
        "title": "Test 3 · Transformer và attention",
        "slide_hint": "Trang 14",
        "focus_page": 14,
        "suggested_question": (
            "Vì sao Transformer trở thành nền móng kỹ thuật cho GPT, BERT và làn sóng LLM?"
        ),
        "answer": (
            "Transformer tạo bước ngoặt vì cơ chế attention cho phép mỗi từ xem xét trực "
            "tiếp những từ quan trọng khác trong toàn câu, thay vì buộc phải xử lý ngữ "
            "cảnh tuần tự từng bước. Nhờ cách biểu diễn quan hệ ngôn ngữ linh hoạt này, "
            "Transformer trở thành nền tảng cho GPT, BERT và các LLM về sau."
        ),
        "evidence": (
            "“Mỗi từ có thể nhìn sang những từ quan trọng khác trong cả câu, thay vì chỉ "
            "đi tuần tự từng bước.”"
        ),
        "confidence": 0.90,
        "quiz_question": "Điểm khác biệt được slide nhấn mạnh ở Transformer là gì?",
        "quiz_options": [
            "A. Mỗi từ chỉ nhìn từ đứng ngay trước nó.",
            "B. Mỗi từ có thể chú ý đến các từ quan trọng khác trong toàn câu.",
            "C. Toàn bộ tri thức phải được viết thành luật thủ công.",
            "D. Mô hình chỉ học được từ hình ảnh ImageNet.",
        ],
        "correct_quiz_option": (
            "B. Mỗi từ có thể chú ý đến các từ quan trọng khác trong toàn câu."
        ),
        "correct_explanation": (
            "Chính xác. Attention giúp mô hình liên kết các phần quan trọng của ngữ cảnh "
            "một cách linh hoạt, tạo nền tảng cho các mô hình ngôn ngữ lớn."
        ),
        "misconception_feedback": (
            "Điểm chính trên slide là khả năng kết nối ngữ cảnh trong toàn câu. Transformer "
            "không bị giới hạn ở việc chỉ xử lý từng từ theo một chuỗi tuần tự cứng nhắc."
        ),
        "retry_question": "Attention có giúp một từ tham chiếu các từ quan trọng ở xa trong câu không?",
        "retry_options": ["A. Có", "B. Không"],
        "correct_retry_option": "A. Có",
        "retry_correct_explanation": (
            "Đúng. Đây chính là trực giác quan trọng được slide dùng để giải thích Transformer."
        ),
        "retry_wrong_explanation": (
            "Chưa đúng. Attention cho phép một từ liên hệ với những từ quan trọng khác, "
            "kể cả khi chúng không đứng cạnh nhau."
        ),
    },
}
