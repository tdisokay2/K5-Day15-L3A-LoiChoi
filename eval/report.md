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

**Nguyên nhân gốc (đọc trace `traces/run-1.jsonl`, CP4 #22):** cả 9 câu trượt đều hỏng ở bước *trước* checker, checker không sai lần nào.
- Model trích `query` kèm chữ thừa, `lookup_components` chỉ khớp chính xác/alias nên trả `match_type: none`: "TUF GAMING B650-PLUS WIFI **BIOS 1409**" (B04, B16, B18, B22) · "**RAM** KF556C40BBK2-32" (B09, B18) · "Kingston FURY Beast **32GB**" (B08 — alias đúng nhưng không ra 2 ứng viên) · "**main** b650 tuf wifi", "**ram** kf432 **16gb**", "**card** 4060 ventus…", "**case** h5 flow 2024" (B15).
- Model chép nguyên câu người dùng vào `case_clearance_condition`, checker so chuỗi sau chuẩn hoá: "không radiator trước" ≠ "Không lắp radiator mặt trước" (B06) · cả câu "… Lắp vừa không?" (B19) · lời shop "lắp được card dài 322 mm" thay cho "có radiator 120 mm" (B22).
- Khi linh kiện bị mất, cặp liên quan thành "Thiếu thông tin" → kết luận chung bị hạ, và **xung đột thật bị che** (B15, B22).

## 3. Một lần cải tiến

### Kế hoạch (chốt ở #22, trước khi sửa code — chưa có kết quả lượt 2)

- **Nhắm vào nhóm lỗi:** *nhận diện linh kiện và ngữ cảnh làm mất thông tin kiểm* — gộp nhóm "dính tiền tố/hậu tố", "tên viết tắt" và "điều kiện vỏ so theo chuỗi" vì cùng một chỗ hỏng (bước trích + tra trước checker). Phủ cả 9 câu trượt: B04, B06, B08, B09, B15, B16, B18, B19, B22.
- **Vì sao đau nhất với người dùng:** đây là nhóm duy nhất gây **bỏ sót xung đột** (B15, B22) — người mua thấy "Thiếu thông tin", tưởng chỉ cần bổ sung mã, trong khi cấu hình có linh kiện không lắp được. Đúng pain gốc: người mới phải tra lại vì tên/mã dễ nhầm (`evidence/summary.md`). Các nhóm còn lại không làm sai kết luận.
- **Giả thuyết:** nếu tách được *đúng mã sản phẩm* và *đúng điều kiện lắp đặt* trước khi tra, checker (vốn đúng) sẽ nhận đủ linh kiện → cặp đúng trạng thái, xung đột đã biết không bị che. Không hứa tỷ lệ cải thiện khi chưa đo.
- **Phạm vi một lần cải tiến (Dương làm ở #24):**
  1. Trích `query` chỉ gồm tên/mã sản phẩm: bỏ từ chỉ loại ("main", "RAM", "card", "case", "vỏ"…), bỏ BIOS/dung lượng/bố trí khỏi tên và đưa BIOS vào `context.bios_version`.
  2. Tra cứu chịu được tên viết tắt / thiếu chữ: so theo token với `model`/`aliases` của catalog, **trả nhiều ứng viên khi chưa chắc** (giữ nguyên quy tắc hỏi lại, không chọn ngầm).
  3. Điều kiện vỏ: model chọn trong **danh sách điều kiện có trong catalog** hoặc `null` (chưa rõ / khác điều kiện), không chép nguyên câu; lời shop/người bán không phải điều kiện lắp đặt.
- **Không làm:** không sửa `tools.py` checker, catalog, benchmark `15183c9`, expected/pass_criterion, metric hay chuẩn §7; **không viết code/prompt so khớp nguyên văn input của bộ thử** (vd không thêm alias "b650 tuf wifi" chỉ vì có trong B15). Ví dụ kiểm thử của #24/#25 phải là câu khác bộ thử.
- **Cách kiểm hồi quy (Thắng ở #25, trước lượt 2):**
  - `python -m unittest discover -s tests -v` đạt; thêm ca hồi quy *ngoài bộ thử* cho: tên kèm BIOS/tiền tố loại/dung lượng, viết tắt, alias nhiều ứng viên, điều kiện vỏ diễn đạt khác, lời shop.
  - Không được tệ đi: 5 câu tu_choi (B12, B13, B14, B23, B24) và các câu hỏi lại đúng (B07, B11, B20, B21) — bước sửa không được làm model chọn ngầm hay bỏ qua injection.
  - `python run.py eval --try` (không tính lượt) để kiểm kết nối; sau đó mới chạy lượt 2.
- **Người review:** Thắng duyệt bản chạy lượt 2 (#25); Dương duyệt phạm vi sửa; Khánh chạy và chấm lượt 2 (#26), Thắng/Dương rà các câu đổi kết quả và điều kiện cứng.
- **Kết quả (điền ở #26 sau lượt 2):** nhóm lỗi đó 0/9 → __/9 · tổng 64% → __% · bỏ sót xung đột 2 → __
- **Câu nào tệ đi sau khi sửa:** __ (điền ở #26)

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
