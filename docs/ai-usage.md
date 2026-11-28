# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc                                   | Công cụ AI            | AI làm gì                                                                                                     | Người kiểm/sửa gì                                                                              | Ai phụ trách               |
| :------------------------------------- | :-------------------- | :------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------- | :------------------------- |
| Code bản chạy thử                      | ChatGPT               | Hỗ trợ viết AI Core, tích hợp API và Data Pipeline, sửa lỗi                                                   | Kiểm tra code, chạy 120/120 test đạt, kiểm thử thực tế                                         | Bùi Nguyên Dũng            |
| Prompt / thiết kế lời gọi mô hình      | ChatGPT               | Hỗ trợ thiết kế prompt phân loại và giới hạn quyền Agent                                                      | Kiểm tra kết quả phân loại và hành vi an toàn                                                  | Bùi Nguyên Dũng            |
| Đào data (viết script đếm, gợi ý nhãn) |                       |                                                                                                               | Kiểm tay \_\_ dòng, khớp \_\_                                                                  |                            |
| Rà câu hỏi phỏng vấn / khảo sát        | ChatGPT / Antigravity | Chỉ rà câu dẫn dắt, cấu trúc bảng hỏi hành vi và tổng hợp thống kê từ `results.csv`                           | Tự thiết kế nội dung 14 câu khảo sát & trực tiếp phỏng vấn P1–P3; kiểm tay 21/21 dòng khảo sát | Nguyễn Khánh Duy           |
| Viết câu thử (benchmark)               | ChatGPT               | Hỗ trợ phân loại các câu hỏi benchmark                                                                        | Kiểm tra phân loại câu hỏi trong `benchmark` cho từng câu                                      | Nguyễn Hoàng Văn Tiến Mạnh |
| Sinh data `synthetic` (nếu có)         | ChatGPT               | Hỗ trợ sinh data `synthetic`                                                                                  | Seed 42                                                                                        | Nguyễn Đức Trọng           |
| Chấm cột `pass` bằng LLM               | Codex                 | Đối chiếu phản hồi và trace với `pass_criterion` và điều kiện an toàn. Điền `pass` và `ghi_chu` cho hai lượt  | Review kết quả đánh giá dựa theo tiêu chí chấm trong `run-1.csv` và `run-2.csv`                | Nguyễn Hoàng Văn Tiến Mạnh |
| Slide, văn bản                         | ChatGPT / Antigravity | Hỗ trợ chuẩn hóa định dạng Markdown `canvas.md`, `spec.md` (nghiệp vụ), `slides/outline.md` theo khung rubric | Kiểm tra chéo mọi con số, trích dẫn nguyên văn và quyết định nghiệp vụ E3                      | Nguyễn Khánh Duy           |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
