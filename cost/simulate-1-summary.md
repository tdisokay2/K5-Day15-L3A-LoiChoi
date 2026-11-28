# Tóm tắt mô phỏng simulate-1@20261128-124358

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| nguoi_moi_ra_mot_lan | 23 | 2 | 1082 | 271 | 2.0 | 16.0 |
| nguoi_chinh_sua_nhieu_lan | 16 | 3 | 1640 | 429 | 3.0 | 24.9 |
| nguoi_hoi_nhieu_cau_hinh | 11 | 4 | 2157 | 535 | 4.0 | 32.7 |

Tỉ lệ đạt dùng để tính: 22/25 (88%) — lượt run-2@20261128-123026

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from). ⚠️ Lượt này chạy bằng  Khánh duyệt] Đạt (lượt 1 trượt → sửa được): 'không radiator trước' khớp điều kiện 410 mm → GPU–vỏ chưa phát hiện xung đột; CPU–main Thiếu thông tin + hỏi BIOS 1409.,  Khánh duyệt] Đạt (lượt 1 trượt → sửa được): main nhận diện được; 3 cặp chưa phát hiện xung đột; GPU–vỏ 300/410 mm.,  Khánh duyệt] Đạt (lượt 1 trượt → sửa được): main và RAM nhận diện được; 3 cặp chưa phát hiện xung đột; ranh giới 199/200 mm đúng.,  Khánh duyệt] Đạt (lượt 1 trượt → sửa được): nhận diện 'RAM KF556C40BBK2-32'; main–RAM chưa phát hiện xung đột; CPU–main Thiếu thông tin (danh sách rút gọn); hỏi mã vỏ., openai/gpt-4.1-mini, mô phỏng đo trên openai/gpt-4.1-mini — khác model.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (300 người) | Chi phí / tháng — cao (800 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| openai/gpt-4.1-mini (vào 0.4 · ra 1.6 $/1M) | $0.0012 (≈ 31 ₫) | $0.0014 (≈ 35 ₫) | $0.00050 (≈ 13 ₫) | $0.2404 (≈ 6.107 ₫) | $0.7213 (≈ 18.322 ₫) | $1.92 (≈ 48.859 ₫) | $0.0024 (≈ 61 ₫) |
| openai/gpt-4.1-nano (vào 0.1 · ra 0.4 $/1M) | $0.00030 (≈ 8 ₫) | $0.00034 (≈ 9 ₫) | $0.00012 (≈ 3 ₫) | $0.0601 (≈ 1.527 ₫) | $0.1803 (≈ 4.581 ₫) | $0.4809 (≈ 12.215 ₫) | $0.00060 (≈ 15 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.8) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: openai/gpt-4.1-mini. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
- Tỷ giá: 1 USD = 25.400 ₫ ((tự ước tính) Tỷ giá tham khảo USD/VND tại 28/11/2026).
