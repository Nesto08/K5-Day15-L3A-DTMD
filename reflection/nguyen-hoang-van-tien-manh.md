# Reflection — Nguyễn Hoàng Văn Tiến Mạnh

1. Vai trò + phần mình làm (trỏ tới file / commit):

Đánh giá và chi phí AI, xây [bộ 20 câu thử](../eval/benchmark.csv) và [6 tiêu chí chấm](../eval/metric_spec.yaml). Commit [`b4c5122`](https://github.com/Nesto08/K5-L3A-DTMD-AI-Product-Hackathon/commit/b4c51228c737285b38c9f37a2120f974a836e36c).

Chạy [Run 1](../eval/run-1.csv), tinh chỉnh phân loại ngữ cảnh và chạy [Run 2](../eval/run-2.csv). Tỷ lệ đạt tăng từ 55% lên 65%. Commit [`2bfac69`](https://github.com/Nesto08/K5-L3A-DTMD-AI-Product-Hackathon/commit/2bfac69b0db6927bda6b219ab09359e5f1f04680) và [`cc41a07`](https://github.com/Nesto08/K5-L3A-DTMD-AI-Product-Hackathon/commit/cc41a07faf1e6c9b3f1a3f5aaae946e7fa73d655).

Tạo [mô phỏng 50 phiên](../cost/simulate-1.csv) và lập [báo cáo chi phí](../cost/cost-estimate.md) cho ba kịch bản. Commit [`38cb408`](https://github.com/Nesto08/K5-L3A-DTMD-AI-Product-Hackathon/commit/38cb408ea1c9b02136e070b04240f04c88565dc9).

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

Dùng ChatGPT hỗ trợ phân loại câu hỏi benchmark.

Dùng Codex để đọc trace, đề xuất chỉnh prompt và logic phân loại, rồi đối chiếu từng phản hồi với tiêu chí để điền `pass` và `ghi_chu`.

Sửa lỗi tiếng Việt trong `ghi_chu` bị lỗi mã hóa. Nhờ Codex khôi phục dấu cho 20 ghi chú và kiểm tra lại điểm. Commit [`92e8a1a`](https://github.com/Nesto08/K5-L3A-DTMD-AI-Product-Hackathon/commit/92e8a1a9b40909de1cf60f99d80f59544c88a462).

3. Một câu thử trượt của nhóm và mình học được gì từ nó:

Ở B08, người dùng tự báo cần đóng viện phí. Lượt 1 nhầm trạng thái ví tạm giữ với việc bị cản xác minh, nên cảnh báo lừa đảo và bỏ bước bàn giao ưu tiên.

Lượt 2 hết gán nhầm cờ nhưng vẫn chọn `unclear`, nên B08 vẫn trượt. Phải kiểm tra cả hành động cuối trong trace sau khi sửa phần trích xuất. [Báo cáo đánh giá](../eval/report.md)
