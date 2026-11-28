# Reflection — Bùi Nguyên Dũng

**1. Vai trò + phần mình làm (trỏ tới file / commit):**

- Đảm nhiệm vai trò Leader và AI Core Engineer, phân công công việc, điều phối tiến độ và tổng hợp kết quả nộp các checkpoint.
- Thiết kế kiến trúc Hybrid Agent kết hợp LLM, Rulebase, Policy Engine, Guardrails và Tools.
- Xây dựng AI Core, tích hợp OpenAI API, Data Pipeline và cơ chế quản lý hội thoại nhiều lượt.
- Thực hiện kiểm thử AI Core và Data Pipeline với kết quả 120/120 test đạt.
- File phụ trách: `codebase/agent.py`, `ai.py`, `policy.py`, `rulebase.py`, `guardrails.py`, `tools.py`, `data_adapter.py`. Commit tiêu biểu: `6e0f60a`.

**2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**

- Sử dụng ChatGPT để hỗ trợ thiết kế kiến trúc, xây dựng code AI Core, thiết kế prompt và viết các bài kiểm thử.
- AI hỗ trợ phân tích lỗi, đề xuất phương án tích hợp dữ liệu và kết nối model qua API.
- kiểm tra và sửa lại một số output AI liên quan đến xử lý Unicode tiếng Việt, quản lý trạng thái hội thoại và nội dung phản hồi của Agent.
- Mình trực tiếp chạy test, kiểm thử các tình huống thực tế và đối chiếu kết quả với yêu cầu nghiệp vụ trước khi commit.

**3. Một câu thử trượt của nhóm và mình học được gì từ nó:**

- Câu thử B08 liên quan đến việc nhận diện sai dấu hiệu `VERIFICATION_BLOCKED`.
- LLM có thể nhầm việc giao dịch bị hệ thống ví tạm chặn với việc đối tượng lừa đảo ngăn cản người dùng xác minh độc lập.
- Sai sót trong quá trình trích xuất thông tin có thể khiến Rulebase và Policy Engine đưa ra quyết định không phù hợp, dù logic nghiệp vụ đã được lập trình đúng.
- Qua đó, tôi học được rằng không thể chỉ dựa vào kết quả phân loại của LLM mà cần định nghĩa rõ các dấu hiệu nghiệp vụ, kiểm thử trường hợp biên và phân tích trace.
- Việc xây dựng AI Agent an toàn đòi hỏi sự kết hợp giữa khả năng hiểu ngôn ngữ của AI, logic kiểm soát bằng code và quá trình đánh giá liên tục.