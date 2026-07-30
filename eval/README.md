# Evaluation protocol

Runner dùng cùng services.learning_engine.run_learning_turn với Streamlit. Mỗi case phải
có output PASS, FAIL hoặc ERROR; không được silently skip.

## Chiều chất lượng

1. Grounded correctness: PASS khi expected_facts đều xuất hiện trong answer sau normalize
   chữ thường/khoảng trắng; case không grounded không bị đoán thành grounded.
2. Citation validity: PASS khi citation page bằng expected_citation_page và mọi quote là
   substring của selected_text. Quote/page bịa là hard failure.
3. Relevance and size: PASS khi answer không rỗng, không chứa must_not_contain và không
   vượt 900 ký tự. Đây là rule proxy, cần người chấm đọc case khó.
4. Quiz validity: grounded phải có quiz, đúng 4 option khác nhau, một correct index hợp lệ,
   feedback cho đúng ba option sai; non-grounded phải không có quiz.
5. Graceful handling: expected insufficient_context, ambiguous hoặc out_of_scope phải đúng
   status và không quiz.
6. Misconception repair: mọi feedback đáp án sai phải có ít nhất 20 ký tự và không chỉ nói
   chưa đúng; retry có đúng 2 option và explanation cho cả đúng/sai.

## Hard failures

- Citation quote không có trong selected_text hoặc page sai.
- Answer chứa fact bắt buộc sai/thiếu nhưng thể hiện như chắc chắn.
- Quiz xuất hiện khi status không grounded.
- Correct index ngoài miền, option trùng hoặc thiếu feedback cho đáp án sai.

## Chấm PASS

Một case PASS khi status đúng, toàn bộ structural checks PASS, không hard failure, và với
case grounded thì expected facts/citation/quiz đều PASS. Rule-based score không thay thế
đọc tay: failures.md liệt kê case cần review. Không có evaluator LLM trong run 001 để tránh
giả vờ có đánh giá khi chưa cấu hình thêm model.

## Quality bar đã khóa trước run 001

Đạt khi ít nhất 80% toàn bộ golden set PASS, đồng thời:

- 100% case không có citation bịa;
- 100% case insufficient_context, ambiguous và out_of_scope không sinh quiz.

Không hạ bar sau khi thấy kết quả.

## Lệnh

    python scripts/run_eval.py --run-id run-001

Nếu thiếu key, runner dừng trước khi gọi case và tạo
eval/runs/run-001/BLOCKED_BY_API_KEY.md, không tạo results giả.
