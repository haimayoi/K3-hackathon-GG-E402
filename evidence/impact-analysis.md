# Impact candidates from review_concept mining

Nguồn số: evidence/review-concept-counts.csv, sinh bởi
scripts/mine_review_concept.py. Không có số thời gian tiết kiệm vì chưa đo.

| Ứng viên | User/turn bị chạm | Tần suất proxy | Hậu quả quan sát/proxy | Quyết định |
|---|---:|---:|---|---|
| Quiz kiểm tra hiểu sau review_concept | 1.074 turn trên 326 user; 1.073/1.074 turn không có check question | 2,05 review turn mỗi conversation có review | Tutor trả lời nhưng không có signal kiểm tra hiểu; không được suy ra là user chưa hiểu | Chọn |
| Cải thiện grounding/citation | 448 turn citation rỗng, 215 user, 276 conversation | 1,62 turn citation rỗng mỗi affected conversation | Người học thiếu đường kiểm lại nguồn; chưa đo citation sai | Không chọn làm feature chính; giữ làm cổng an toàn |
| Phát hiện thiếu context và hỏi lại | 178 turn proxy, 116 user, 135 conversation | 1,32 turn mỗi affected conversation | Tutor phải nói không tìm thấy/yêu cầu thêm context; heuristic có thể false positive | Không chọn làm feature chính; triển khai failure path |

## Lý do chọn và loại

Quiz được chọn vì khoảng trống check question xuất hiện ở 1.073 lượt, lớn hơn proxy citation
rỗng 448 lượt và proxy thiếu context 178 lượt, đồng thời nối trực tiếp vào flow quiz/retry đã
có ở CP2. Đây là số về opportunity, không phải bằng chứng quiz sẽ cải thiện điểm số.

Grounding/citation không bị bỏ khỏi thiết kế: nó là điều kiện cứng để cho phép answer/quiz.
Ứng viên thiếu context cũng được giữ như graceful failure. Hai ứng viên không được tuyên bố
là feature impact chính để giữ lát cắt một câu và demo được trong 5 phút.

## Hạn chế và bias

- Data chỉ gồm turn completed từ 22–29/07/2026 và conversation_mode in_class.
- 60/1.074 review response có rating; 30 up và 30 down không đại diện toàn bộ user.
- Marker thiếu context là heuristic lexical, không phải nhãn ground truth.
- asked_check_question chỉ là cờ hệ thống; có check question cũng chưa chứng minh hiểu.
- Không có pre/post learning score, completion rate hay time-on-task; impact học tập chưa đo.
