# Chi phí khi dùng thật

> Điền từ kết quả chạy thật `python run.py simulate --rate-from eval/run-2.csv` (lượt `simulate-1@20261128-124358`, 50 phiên, không sửa số khung sinh).

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`, `seed: 42`, `sessions: 50`, tổng `share = 1.0`):
  - `nguoi_moi_ra_mot_lan` (`share: 0.50`, `1` phiên/tháng, `2` lượt/phiên) — `(tự ước tính)` dựa định tính từ P2 (rà 1 lần trước mua, 0 phút phát sinh).
  - `nguoi_chinh_sua_nhieu_lan` (`share: 0.35`, `2` phiên/tháng, `3` lượt/phiên) — `(tự ước tính)` dựa định tính từ P1 (3 lần/30 ngày) và P3 (đổi linh kiện do hết hàng); không dùng câu 9 khảo sát còn mâu thuẫn làm số chắc chắn.
  - `nguoi_hoi_nhieu_cau_hinh` (`share: 0.15`, `4` phiên/tháng, `4` lượt/phiên) — `(tự ước tính)`.
- **Số người dùng thật** 3 kịch bản: thấp `100` · cơ sở `300` · cao `800` — `(tự ước tính)` (chưa có thống kê công khai số sinh viên tự ráp PC lần đầu mỗi tháng).
- **Giá** 2 mức model (USD / 1 triệu token, kiểm tra ngày `28/11/2026`):
  - `openai/gpt-4.1-mini`: `$0.40` vào / `$1.60` ra ([OpenRouter](https://openrouter.ai/openai/gpt-4.1-mini))
  - `openai/gpt-4.1-nano`: `$0.10` vào / `$0.40` ra ([OpenRouter](https://openrouter.ai/openai/gpt-4.1-nano))
- **Tỷ giá quy đổi:** `1 USD = 25.400 ₫` (`(tự ước tính)` tham khảo ngày `28/11/2026`).
- **Tỉ lệ đạt** dùng để tính: `22/25 (88%)` — lượt 2 `run-2@20261128-123026` (`eval/run-2.csv`, model `openai/gpt-4.1-mini`).
- **Phạm vi đo:** Token được đo **thật** trên `openai/gpt-4.1-mini`; dòng `openai/gpt-4.1-nano` là **ước tính chi phí từ cùng lượng token**, **chưa đo chất lượng / tỷ lệ đạt của Nano** (không coi 88% của Mini là chất lượng của Nano).

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-124358` · `50` phiên · `seed 42` · phiên lỗi: `0/50`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| nguoi_moi_ra_mot_lan | 23 | 2 | 1082 | 271 | 2.0 | 16.0 |
| nguoi_chinh_sua_nhieu_lan | 16 | 3 | 1640 | 429 | 3.0 | 24.9 |
| nguoi_hoi_nhieu_cau_hinh | 11 | 4 | 2157 | 535 | 4.0 | 32.7 |

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (300 người) | Chi phí / tháng — cao (800 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `openai/gpt-4.1-mini` (đo thật; vào 0.4 · ra 1.6 $/1M) | $0.0012 (≈ 31 ₫) | $0.0014 (≈ 35 ₫) | $0.00050 (≈ 13 ₫) | $0.2404 (≈ 6.107 ₫) | $0.7213 (≈ 18.322 ₫) | $1.92 (≈ 48.859 ₫) | $0.0024 (≈ 61 ₫) |
| `openai/gpt-4.1-nano` (ước tính từ token Mini; vào 0.1 · ra 0.4 $/1M) | $0.00030 (≈ 8 ₫) | $0.00034 (≈ 9 ₫) | $0.00012 (≈ 3 ₫) | $0.0601 (≈ 1.527 ₫) | $0.1803 (≈ 4.581 ₫) | $0.4809 (≈ 12.215 ₫) | $0.00060 (≈ 15 ₫) |

- Công thức: `Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt (0.88)`; `Chi phí / tháng = Σ (số người dùng × share × số phiên/người/tháng × chi phí trung bình/phiên của persona)`.

## 3. So với impact

- **Impact / người / tháng (`spec.md` §2):** Trong 3 cuộc phỏng vấn, P1 báo khoảng `30 phút / 30 ngày` phát sinh do đổi mainboard (3 lần × ~10 phút), P2 báo `0 phút` phát sinh (`5 phút` rà thường lệ), P3 báo `10 phút` đổi linh kiện do hết hàng. §2 ghi rõ chưa đủ dữ liệu cùng định nghĩa để suy ra tần suất đại diện hoặc chứng minh ROI.
- **Chi phí / người / tháng (cơ sở 300 người, `openai/gpt-4.1-mini`):** `$0.0024` (`≈ 61 ₫` / người / tháng; tổng cả 300 người là `$0.7213 ≈ 18.322 ₫` / tháng).
- **Giới hạn ước tính:** (1) Số người dùng và tần suất ở `personas.yaml` là `(tự ước tính)`; (2) Ước tính của `openai/gpt-4.1-nano` chưa kiểm chất lượng thật; (3) Lượt 2 (`88%`) vẫn còn 1 câu bỏ sót xung đột (B22).
- **Kết luận — đáng làm không:** **Đáng tiếp tục thử nghiệm về mặt chi phí API** (chỉ ~`61 ₫` / người / tháng, rất nhỏ so với 30 phút phát sinh ở P1), nhưng **chưa thể kết luận ROI hay đưa vào dùng rộng ngay** do dữ liệu impact §2 còn mỏng và hệ thống chưa đạt điều kiện cứng `0` bỏ sót xung đột ở lượt 2.
