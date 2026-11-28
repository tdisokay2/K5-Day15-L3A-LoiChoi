# Dàn slide → lấy số từ file nào

> File PDF đã xuất: [`demo-slides.pdf`](../demo-slides.pdf) ở thư mục gốc repo. Nguồn HTML: [`slides/demo-slides.html`](demo-slides.html) (xuất lại: Chrome → In → Lưu PDF, hoặc `chrome --headless --print-to-pdf`). Bản 28/11 14:20 dựng lại từ PDF của Thắng (`65248e9`), chỉ sửa trang 4 (video CP4) và trang 7 (35 ₫/task, 61 ₫/người/tháng). Mọi số liệu, trích dẫn và run ID đều đối chiếu trực tiếp từ hồ sơ trong repo.

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Người dùng & pain | Sinh viên lần đầu tự ráp PC · 8/10 (80%) khảo sát có bước phát sinh · 1/3 phỏng vấn (P1) sai socket khi ráp thử + trích dẫn P1 | `evidence/summary.md` | ☑ |
| 2 | Vì sao chọn bài này | Bảng impact: chọn rà 3 cặp (P1 ~30 phút/30 ngày); hoãn so giá (6/10 chọn tốn thời gian nhưng thiếu giá/tồn kho) & hoãn rà toàn bộ máy | `spec.md` §2 | ☑ |
| 3 | Giải pháp | Lát cắt 1 câu · workflow cố định 1 lần gọi model (`AI trích → code tra & kiểm 3 cặp`) · AI gợi ý, người quyết | `spec.md` §4 | ☑ |
| 4 | Demo live | 1 ca thường (`B01`: AM4 vs AM5 `Có xung đột`) + 1 ca khó (`B07`: hỏi lại 2 biến thể `B760M`) + 1 câu lạ giám khảo; dự phòng video CP4 `https://youtu.be/CnhJdD9oC0c` (CP3: `https://youtu.be/syBKNhpcIIE`) | `eval/benchmark.csv`, `docs/cp3-demo.md` | ☑ |
| 5 | **Đánh giá thế nào** | 12 linh kiện `components.json` · 25 câu `15183c9` · 5 metric · Lượt 1 `run-1@20261128-005643` 16/25 (64%, sót B15/B22) → Lượt 2 `run-2@20261128-123026` 22/25 (88%, sót B22, B17 tệ đi) · chưa đạt điều kiện cứng | `eval/README.md`, `eval/report.md` | ☑ |
| 6 | **Chi phí khi dùng thật** | `simulate-1@20261128-124358` (50 phiên, `0/50` lỗi, tỉ lệ đạt 88%) · Mini đo thật `$0.0014`/task (`≈ 35 ₫`), 3 kịch bản `100/300/800` người (`$0.7213/tháng` cơ sở, `≈ 61 ₫`/người/tháng) · Nano ước tính từ token Mini (chưa đo chất lượng) · so impact §2 | `cost/cost-estimate.md`, `cost/simulate-1-summary.md` | ☑ |
| 7 | Kết luận | **ITERATE** (cải tiến trước khi dùng rộng): chi phí rất rẻ (`≈ 61 ₫`/người/tháng) và lượt 2 đạt `88%`, nhưng còn 1 ca sót xung đột (B22) và bằng chứng phỏng vấn mới 1/3 | Trang 1, 5, 6 | ☑ |
| 8 | Nếu có thêm 1 tuần | (1) Tách lời shop khỏi bố trí thật để xử lý B22; (2) Fallback tra ứng viên gần nhất khi model trích lệch 1 token (B17); (3) Mở rộng catalog có/không radiator và bổ sung câu `nguoi_dung` | `eval/report.md` mục 4 | ☑ |

## Kịch bản demo live & phân công trình bày (mỗi người ≥1 phần)

| Trang | Người nói | Nội dung chính |
|---|---|---|
| 1–2 | Hồ Văn Dũng | Người dùng sinh viên ráp PC lần đầu, bằng chứng khảo sát 8/10 & phỏng vấn 1/3 (P1), lý do chọn 3 cặp và hoãn giá/PSU |
| 3, 7 | Nguyễn Triều Dương | Workflow cố định AI trích + code kiểm, ranh giới an toàn và kết luận **Iterate** |
| 4, 6 | Kiều Văn Thắng | Chạy live `python run.py` (`openai/gpt-4.1-mini`) với B01, B07 + câu lạ; bảng chi phí 50 phiên & so impact |
| 5, 8 | Nguyễn Khắc Khánh | Hồ sơ 25 câu / 5 metric, tiến triển lượt 1 (64%) → lượt 2 (88%), lỗi B22/B17 và kế hoạch 1 tuần |

**Checklist trước khi lên demo:**
- [ ] Tải repo về thư mục/máy mới, chạy theo mục "Chạy trong 3 phút" của `README.md`.
- [ ] Máy demo có `.env` riêng (`MODEL_PROVIDER=openrouter`, `MODEL_NAME=openai/gpt-4.1-mini`), gọi thử 1 câu trong vòng 1 giờ trước giờ demo.
- [x] Video dự phòng CP4 `https://youtu.be/CnhJdD9oC0c` (code `443b6dc`, `openai/gpt-4.1-mini`, kịch bản `docs/cp4-demo.md`; kiểm xem được không đăng nhập 28/11). Video CP3 `https://youtu.be/syBKNhpcIIE` (model `openai/gpt-4.1-mini`, ca B01 & B07) đã mở công khai không cần đăng nhập; chuẩn bị thêm bản `demo-slides.pdf` và video ngoại tuyến phòng mất mạng.
- [ ] Tập chuyển người giữa Dũng → Dương → Thắng → Khánh và chuẩn bị xử lý 1 câu thử lạ của giám khảo (nếu ngoài phạm vi/thiếu thông tin, chỉ ra hệ thống trả `Thiếu thông tin` hoặc từ chối đúng giới hạn).
