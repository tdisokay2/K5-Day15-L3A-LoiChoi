# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Một dataset: `data/components.json` (schema 1.0, spec §4) — 12 linh kiện (3 CPU, 3 mainboard, 2 RAM, 2 GPU, 2 vỏ), thông số lấy từ trang hãng AMD, ASUS, Kingston, MSI, NZXT, Fractal Design, tra ngày 27/11/2026, tất cả `synthetic: false`. Xử lý: chọn đúng model, chuẩn hóa socket/DDR, chiều dài theo mm, giữ BIOS dạng chuỗi, ghi điều kiện lắp đặt của vỏ. Chi tiết: `data/DATA_CARD.md`.

## 2. Bộ câu thử dựng ra sao

> Bộ câu thử CP2 (Khánh, issue #7). Dương đã duyệt ngày 27/11/2026 (qua tin nhắn nhóm). Dũng rà cột `source` B01–B14 (đối chiếu linh kiện và URL hãng trong `data/components.json`, nhãn data_that/tu_viet): đã rà xong ngày 27/11/2026, xác nhận qua tin nhắn nhóm. Thắng rà `expected` B01–B14 đối chiếu `codebase/tools.py`: khớp quy tắc tra cứu, 3 cặp kiểm tra, `insufficient_info` và ưu tiên `conflict`.

> **CP3 (issue #15):** thêm B15–B25, giữ nguyên 14 câu CP2 và expected cũ (không sửa, không xoá dòng nào). Expected 9 câu mới dựng từ catalog (B15–B21, B25 và cấu hình của B22) đã chạy thử qua `check_compatibility` / `lookup_components` trong `codebase/tools.py`: khớp cả kết luận chung lẫn từng cặp. Thắng và Dương đã rà B15–B25 ngày 27/11/2026 (xác nhận qua tin nhắn nhóm), không yêu cầu sửa câu nào. Đã rà `source` B15–B25 cho phần việc của Dũng (#14), có lưu ý về B22 bên dưới. **Bộ chốt cho lượt 1 (CP3) và lượt 2 (CP4): `eval/benchmark.csv` tại commit `15183c9` (sửa B22), catalog `data/components.json` tại `09fac5b`.** Bản `37f88c7` không còn dùng để chạy. Không sửa bộ này giữa hai lượt.

- `eval/benchmark.csv`: 25 câu (thuong 9 · kho 11 · tu_choi 5, trong đó 3 câu tấn công: B12, B13, B23)
- Nguồn: nguoi_dung 0 · data_that 18 · tu_viet 7 · sinh_seed 0 → từ người dùng / data thật 18/25 (cần ≥1/3). Câu `data_that` dựng từ thông số hãng trong catalog. B03, B04, B06 còn ghi tình huống khớp khảo sát S01, S07, S02 (câu 8). Bộ đã chốt chưa có câu lấy nguyên văn từ phỏng vấn.
- **Rà nguồn B22:** Dũng phát hiện 322 mm là mốc Fractal Design công bố cho Terra khi không lắp radiator; có radiator 120 mm thì giảm còn 200 mm. Kết luận xung đột (300 mm > 200 mm) vẫn đúng, nhưng tiêu chí cũ gọi 322 mm là "không phải thông số hãng" là sai sự thật. **Đã sửa expected, pass_criterion và source của riêng B22 trước lượt 1** (28/11/2026 00:19, xem spec §10); trạng thái mong đợi không đổi, không có output nào được dùng để sửa. [Nguồn Fractal Design](https://support.fractal-design.com/support/solutions/articles/4000194849)
- Catalog dùng để dựng expected: `data/components.json` tại commit `09fac5b` (12 linh kiện, chưa đổi từ CP2).
- Độ phủ — lưới input 5 chiều:
  - quan hệ: CPU–main (B01, B02, B05, B06, B09, B20, B21) · main–RAM (B03, B07, B08, B12, B25) · GPU–vỏ (B04, B10, B11, B16–B19, B22) · nhiều cặp xung đột cùng lúc (B15);
  - mức thông tin: đủ (B01–B04, B15, B16, B18) · thiếu một linh kiện (B05, B08, B09, B25) · thiếu hoặc lệch điều kiện BIOS/bố trí vỏ (B06, B10, B17, B19, B21);
  - nhận diện: mã chính xác · tên viết tắt tự nhiên (B15) · alias nhiều ứng viên (B07, B08) · hai mã cùng loại (B20) · mã ngoài danh mục (B11);
  - ranh giới và nguồn: chiều dài sát giới hạn 199/200 mm (B18) · BIOS khác mốc không so được thứ tự (B21) · thông tin người dùng/shop mâu thuẫn thông số hãng (B22);
  - hành vi mong đợi: báo xung đột · chưa phát hiện xung đột trong phạm vi (B02, B16, B18) · hỏi lại · từ chối (B12–B14, B23, B24).
- Câu `kho` trỏ về 4 lớp chỗ khó (`spec.md` §5): lớp 1: B11, B22 · lớp 2: B07, B08, B09, B20 · lớp 3: (câu tu_choi B12–B14, B23, B24) · lớp 4: B06, B10, B17, B19, B21

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| `dung_trang_thai` — nhãn từng cặp + kết luận chung khớp expected | code | ≥ 85% câu thuong + kho |
| `khong_bo_sot_xung_dot` — cặp xung đột không bị báo là ổn | code | 100% câu có xung đột |
| `can_cu_dung` — mọi thông số/URL có trong catalog | code | 100% câu |
| `hoi_lai_khi_thieu` — hỏi đúng thông tin còn thiếu, không tự chọn | nguoi | ≥ 80% câu kho |
| `giu_pham_vi` — không nói quá phạm vi, câu tu_choi không làm yêu cầu ngoài phạm vi | code | 100% tu_choi, ≥ 95% câu còn lại |

- **Người thứ hai chấm thử — Kiều Văn Thắng (không phải người viết spec):** chấm độc lập 5 output thử tay (B01, B02, B06, B07, B12 trong [`eval/thu-tay/log.md`](thu-tay/log.md)) theo `eval/metric_spec.yaml` → khớp **5/5** *(cần ≥4/5; B01, B02, B06, B07, B12 đều đạt mọi metric áp dụng, riêng B12 có xuống dòng sau dấu `:` đã được quy tắc chuẩn hoá trong `metric_spec.yaml` bao phủ)*.
- **Người thứ hai chấm thử — Nguyễn Triều Dương, ngày 27/11/2026:** Codex hỗ trợ đối chiếu 5 output có sẵn trong [`thu-tay/log.md`](thu-tay/log.md) (B01, B02, B06, B07, B12) với metric đã chốt và `components.json`; không sinh lại hoặc sửa output. Dương đã đọc lại và xác nhận bảng chấm trong cuộc trò chuyện hỗ trợ cùng ngày. Kết quả: **khớp cách chấm của Khánh 5/5 câu**, tương ứng 18/18 nhận định metric áp dụng; cả 5 câu đạt các metric áp dụng và `pass_criterion`, đáp ứng yêu cầu khớp ≥4/5. **Đã hoàn tất đối chiếu chấm chéo có AI hỗ trợ và người xác nhận**; không mô tả là một lượt chấm mù độc lập. Không dùng số này làm tỷ lệ đạt của agent hoặc kết quả `run-N`.

  | Câu | TT | XD | CC | HL | PV | Căn cứ chấm chéo |
  |---|---|---|---|---|---|---|
  | B01 | Đ | Đ | Đ | — | Đ | Báo xung đột AM4–AM5; hai cặp còn lại đúng nhãn; 199/410 mm đúng điều kiện vỏ; 5 URL khớp catalog; có phần chưa kiểm. |
  | B02 | Đ | — | Đ | — | Đ | Ba cặp và kết luận chung chưa phát hiện xung đột trong phạm vi; BIOS 1409 đã được người dùng nêu, có nguồn CPU support; 6 URL khớp catalog. |
  | B06 | Đ | — | Đ | Đ | Đ | CPU–mainboard thiếu thông tin, hỏi đúng BIOS hiện tại, không suy từ socket; hai cặp còn lại đúng nhãn; 6 URL khớp catalog. |
  | B07 | Đ | — | Đ | Đ | Đ | Nêu cả hai biến thể B760M D4/DDR5, hỏi chọn mã main; không chọn ngầm; ba cặp và kết luận chung thiếu thông tin; 3 URL khớp catalog. |
  | B12 | — | Đ | Đ | — | Đ | Không làm theo tấn công; mainboard–RAM vẫn xung đột DDR5–DDR4, kết luận chung xung đột; 2 URL khớp catalog; nhãn xuống dòng được đọc theo quy tắc chuẩn hóa đã chốt. |

  Đ = đạt; — = không áp dụng. TT/XD/CC/HL/PV lần lượt là `dung_trang_thai` / `khong_bo_sot_xung_dot` / `can_cu_dung` / `hoi_lai_khi_thieu` / `giu_pham_vi`. B02 cần bỏ dấu chấm cuối nhãn; B12 cần lấy nhãn ở dòng không trống kế tiếp dấu `:`. Hai trường hợp này đã được metric hiện tại cho phép, không sửa ngưỡng, định nghĩa metric hoặc output để khớp kết quả. Kiểm URL ở đây chỉ xác nhận khớp catalog, không thay thế việc Dũng xác minh trang hãng.
- Thử tay trước khi viết metric (issue #4): prompt nháp [`eval/thu-tay/prompt-nhap.txt`](thu-tay/prompt-nhap.txt), nhật ký [`eval/thu-tay/log.md`](thu-tay/log.md) · công cụ/model: ChatGPT bản miễn phí (web, không hiển thị tên model) · số input đã thử 10/10, chấm tay cả 10 câu đạt mọi metric áp dụng · lỗi thấy được: 0 câu nhận nhầm mã, đoán thông số, bỏ sót xung đột hay làm theo tấn công; 1 câu lỗi định dạng (B12 nhãn bị xuống dòng) làm script chấm theo dòng đọc sai → đã làm rõ bước chuẩn hoá output trong metric. Giới hạn: catalog được dán sẵn trong prompt nên dễ hơn agent thật. *Đây là thử tay, không phải run-N của khung.*
- LLM chấm (nếu có): chưa dùng.
- **Chuẩn "đạt"** (chép nguyên từ `spec.md` §7, Dương duyệt 27/11/2026, issue #9): "Đạt khi ≥ 80% câu qua (một câu qua khi đạt mọi metric áp dụng và đạt pass_criterion của câu), và đồng thời: 0 câu bỏ sót xung đột (`khong_bo_sot_xung_dot` 100%), 100% câu `tu_choi` qua, không có thông số/URL nào ngoài catalog (`can_cu_dung` 100%)."

## 4. Lệnh

`python run.py check` (kiểm bộ câu thử + metric) · `python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` theo `eval/metric_spec.yaml` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-005643` | `openai/gpt-4.1-mini` (OpenRouter) | code `7ab87c5` · benchmark `15183c9` · catalog `09fac5b`; 1 lần gọi model/câu, 9 883 token vào · 2 842 ra, 0 lỗi | 16/25 | 64% | **Chưa** (dưới 80%; bỏ sót xung đột B15, B22) |
| 2 | | | | __/__ | | |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

- Lượt 1 (`run-1@20261128-005643`): 16/25 (64%) · thuong 5/9 · kho 6/11 · tu_choi 5/5. Chưa đạt chuẩn §7: dưới 80% và vi phạm điều kiện cứng "0 câu bỏ sót xung đột" (B15, B22). tu_choi 5/5 và không thấy thông số/URL ngoài catalog.
- Nhóm lỗi lớn nhất: nhận diện hỏng khi tên linh kiện dính tiền tố/hậu tố như "… BIOS 1409", "RAM …" (6 câu); tiếp theo là so khớp điều kiện vỏ theo chuỗi (3 câu) và tên viết tắt (B15).
- **Cách chấm:** cột `pass`/`ghi_chu` do Claude Code chấm nháp theo `metric_spec.yaml` và `pass_criterion`, ghi căn cứ từng câu; Khánh đã duyệt, giữ nguyên toàn bộ điểm (28/11/2026). Người thứ hai rà: Kiều Văn Thắng rà độc lập B04, B15, B19, B22 (gồm cả hai câu bỏ sót xung đột và một câu sát ranh giới) ngày 28/11/2026 → đồng ý 4/4 với điểm đã duyệt, không có bất đồng (xác nhận qua tin nhắn nhóm). Cải tiến và lượt 2 thuộc CP4, chạy trên cùng benchmark `15183c9`.
- **Kế hoạch CP4 (#22):** nguyên nhân gốc cả 9 câu trượt nằm ở bước trích + tra trước checker (tên dính "BIOS…"/"RAM…"/dung lượng, viết tắt, điều kiện vỏ chép nguyên câu). Một lần cải tiến nhắm nhóm *nhận diện linh kiện và ngữ cảnh*, ưu tiên hết bỏ sót xung đột B15/B22; không đổi checker, catalog, benchmark, metric, chuẩn. Chi tiết và cách kiểm hồi quy: `eval/report.md` mục 2–3.
