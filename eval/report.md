# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-005643` | 16/25 | 64% | 5/9 | 6/11 | 5/5 | **chưa đạt** — dưới 80% và 2 câu bỏ sót xung đột (B15, B22) |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Nhận diện hỏng khi tên linh kiện dính tiền tố/hậu tố ("… BIOS 1409", "RAM KF556…", "… 32GB") → linh kiện bị coi là mã không có trong danh mục | 6 | B04, B08, B09, B16, B18, B22 |
| So khớp điều kiện lắp đặt vỏ theo chuỗi: cách diễn đạt khác hoặc cả câu bị lấy làm điều kiện → GPU–vỏ "Thiếu thông tin" sai | 3 | B06, B19, B22 |
| Không nhận diện tên viết tắt tự nhiên ("r5 5600", "b650 tuf", "kf432", "4060 ventus") | 1 | B15 |
| Thiếu thông tin trong câu hỏi lại (không nêu ứng viên / không nêu radiator trước làm giảm khoảng trống) | 2 | B08, B19 |

Một câu có thể thuộc nhiều nhóm (B22: nhận diện main + điều kiện vỏ). **Điều kiện cứng:** bỏ sót xung đột 2 câu (B15, B22) — vi phạm "0 câu bỏ sót"; tu_choi 5/5 đạt; không thấy thông số/URL ngoài catalog (output lấy facts và URL từ `tools.py`).

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B15 | "r5 5600 + main b650 tuf wifi + ram kf432 16gb + card 4060 ventus 2x black + case h5 flow 2024 ko lắp rad trước, ổn ko ạ" | "Kết quả: Thiếu thông tin." · chỉ nhận diện CPU; 4 mục "Không tìm thấy … trong danh mục" | Bỏ sót 2 xung đột thật (AM4/AM5, DDR5/DDR4) vì không nhận diện tên viết tắt; người dùng tưởng chỉ cần bổ sung mã, có thể mua nhầm |
| B22 | Shop nói Terra chứa card 322 mm; người dùng có radiator 120 mm; card PROART-RTX4080S-O16G | "GPU–vỏ máy: Thiếu thông tin. Bố trí vỏ máy ('vỏ Fractal Design Terra lắp được card dài 322 mm') chưa khớp điều kiện…" | Lời shop bị lấy làm điều kiện lắp đặt, bỏ qua "radiator 120 mm" → không báo xung đột 300 > 200 mm |
| B04 | "… TUF GAMING B650-PLUS WIFI BIOS 1409 …" | "Không tìm thấy 'TUF GAMING B650-PLUS WIFI BIOS 1409' trong danh mục" · CPU–main, main–RAM Thiếu thông tin | Phiên bản BIOS dính vào tên main nên main không được nhận diện; cùng lỗi ở B16, B18, B22 |
| B06 | "… vỏ H5 Flow 2024 không radiator trước" | "GPU–vỏ máy: Thiếu thông tin. Bố trí vỏ máy ('không radiator trước') chưa khớp điều kiện 'Không lắp radiator mặt trước'…" | Cùng nghĩa nhưng khác chữ; checker so chuỗi sau chuẩn hoá nên báo thiếu thông tin |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
