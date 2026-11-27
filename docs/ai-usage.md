# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
| :--- | :--- | :--- | :--- | :--- |
| Code bản chạy thử | ChatGPT | Hỗ trợ viết AI Core, tích hợp API và Data Pipeline, sửa lỗi | Kiểm tra code, chạy 120/120 test đạt, kiểm thử thực tế | Bùi Nguyên Dũng |
| Prompt / thiết kế lời gọi mô hình | ChatGPT | Hỗ trợ thiết kế prompt phân loại và giới hạn quyền Agent | Kiểm tra kết quả phân loại và hành vi an toàn | Bùi Nguyên Dũng |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay \_\_ dòng, khớp \_\_ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed \_\_ · kiểm tay \_\_ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công \_\_ câu thử, khớp **/** | |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
