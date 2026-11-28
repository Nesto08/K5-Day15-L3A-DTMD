# Tóm tắt mô phỏng simulate-1@20261128-113402

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 31 | 1 | 877 | 118 | 0.9 | 2.0 |
| dung_vua | 15 | 3 | 2749 | 436 | 2.9 | 6.5 |
| dung_nhieu | 4 | 2 | 1640 | 286 | 1.8 | 4.0 |

Tỉ lệ đạt dùng để tính: 13/20 (65%) — lượt run-2@20261128-103822

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (5.000 người) | Chi phí / tháng — cơ sở (10.000 người) | Chi phí / tháng — cao (20.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.4-nano-2026-03-17 (vào 0.2 · ra 1.25 $/1M) | $0.00058 | $0.00090 | $0.00053 | $4.12 | $8.24 | $16.47 | $0.00082 |
| gpt-5.4 (vào 2.5 · ra 15.0 $/1M) | $0.0072 | $0.0110 | $0.0066 | $50.46 | $100.93 | $201.86 | $0.0101 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.7) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-5.4-nano-2026-03-17. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
