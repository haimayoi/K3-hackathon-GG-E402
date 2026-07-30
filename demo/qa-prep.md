# Q&A preparation

## Vì sao Conditional, không automate toàn bộ?

Quiz sai có thể củng cố kiến thức sai. Chỉ grounded output có page/quote hợp lệ mới được tạo
quiz; thiếu context, mơ hồ và ngoài phạm vi đi đường lui.

## Failure nguy hiểm nhất?

Citation hoặc correct answer trông chắc chắn nhưng sai. Đây là hard failure vì learner có
thể tin nguồn và học sai; parser/page/quote/quiz checks chặn render.

## Confidence xác định thế nào?

Không dùng self-reported confidence hay threshold. Hệ thống dùng status có lý do, strict
schema, citation substring/page match và eval hard conditions. Đây là kiểm tra điều kiện,
không phải xác suất model tự khai.

## Golden set lấy từ đâu?

24 case: 13 phát triển từ chatlog có turn_id, 10 từ slide có page, 1 synthetic; 9 normal,
12 hard và 3 rare. Context được rút tối thiểu, không copy raw pack.

## Có data leakage không?

Golden cases có thể cùng miền với prompt nhưng expected facts không được gửi riêng cho
provider. Eval gửi selected_text/page/question như app. Raw chatlog không gửi hàng loạt;
trace chỉ lưu hash. Cần tiếp tục kiểm soát người sửa prompt không tối ưu riêng theo case ID.

## Vì sao quiz chứng minh hiểu hơn chỉ đọc answer?

Quiz tạo một signal hành vi về việc áp dụng ý vừa giải thích; tốt hơn không có signal,
nhưng chưa chứng minh learning gain. Cần validation/pre-post measurement để kết luận mạnh.

## Nếu quiz do AI sinh sai?

Schema reject cấu trúc sai; grounding và eval kiểm fact/citation; run dưới bar thì HOLD.
Prototype không dùng quiz làm điểm chính thức và cần human review cho case khó.

## Phần nào real, phần nào mock?

Viewer, selection, page propagation, validation, provider adapter, trace và runner là code
thật. Gemini call/run 001 chưa chạy do thiếu key. TEST_CASES là mock fallback chỉ khi bật
USE_MOCK_LLM=true và có nhãn.

## Nếu kết quả dưới quality bar?

HOLD claim ship. Phân tích failure lớn nhất, sửa nhỏ, chạy lại toàn bộ thành run-002 và giữ
bar 80% cùng hai điều kiện 100% không đổi. Chỉ Limited nếu hard conditions đạt và phạm vi
giới hạn được công bố rõ.
