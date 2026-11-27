# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử (`agent.py`, `ai.py`, `tools.py`) | Coding agent (Codex / Antigravity / Claude Code) | Gợi ý và viết khung hàm theo hợp đồng `spec.md §4`, hỗ trợ viết ca kiểm thử cục bộ | Đọc từng dòng diff, chạy `python run.py` và bộ test kiểm tra ca thường/xung đột/thiếu thông tin/biên, sửa lỗi khớp với catalog | Nguyễn Triều Dương (`agent.py`, `ai.py`), Kiều Văn Thắng (`tools.py`) |
| Prompt / thiết kế lời gọi mô hình | Coding agent | Gợi ý `SYSTEM` prompt trích xuất JSON ở `agent.py` và rà soát kịch bản tấn công prompt | Kiểm tra rule không tự đoán thông số, không giữ lựa chọn ngầm, giữ đúng hợp đồng JSON | Nguyễn Triều Dương |
| Kết nối OpenRouter CP3 — issue #12 | Codex | Viết HTTP adapter trong `ai.py`, kiểm usage API, che thông tin nhạy cảm trong lỗi; thêm 9 kiểm thử HTTP giả lập và cập nhật trạng thái hồ sơ | Codex chạy 35/35 unittest đạt; đã thử Nano qua eval --try, Mini qua 3 lời gọi nhận diện và CLI thật, chọn Mini dựa trên kết quả trích xuất. Token lấy từ API; còn chờ Dương đọc diff, chưa chấm lượt chính thức | Nguyễn Triều Dương |
| Đào data (`data/components.json`, `DATA_CARD.md`) | Không dùng AI sinh thông số tự động | Chỉ hỗ trợ chuẩn hóa định dạng JSON theo schema `1.0` | Tự tra trang thông số & CPU support chính thức của hãng (AMD, ASUS, Kingston, MSI, NZXT, Fractal Design), kiểm đối chiếu link HTTPS | Hồ Văn Dũng |
| Rà câu hỏi phỏng vấn / khảo sát (`evidence/`) | Coding agent | Rà câu hỏi khảo sát tránh dẫn dắt | Tự thu thập và tổng hợp phản hồi thật, ghi rõ giới hạn mẫu chưa đủ tại CP2 | Hồ Văn Dũng |
| Viết câu thử (`eval/benchmark.csv`, `metric_spec.yaml`) | Coding agent | Gợi ý cấu trúc 5 metric và rà trùng lặp câu thử | Tự đối chiếu từng câu với `data/components.json` và `spec.md §5`, chạy `python run.py check` xác nhận đủ 14 câu CP2 | Nguyễn Khắc Khánh |
| Sinh data `synthetic` (nếu có) | Chưa sử dụng tại CP2 | — | Catalog CP2 dùng dữ liệu hãng thật (`synthetic: false`); chỉ test đơn vị logic gắn nhãn synthetic ở `tools.py` | Hồ Văn Dũng, Kiều Văn Thắng |
| Chấm cột `pass` bằng LLM (nếu có) | Chưa sử dụng tại CP2 | — | Chưa chạy lượt `eval` model thật ở CP2 | Nguyễn Khắc Khánh |
| Slide, văn bản (`spec.md`, `README.md`, `docs/ai-usage.md`) | Coding agent | Hỗ trợ tóm tắt, biên tập văn bản và cập nhật hướng dẫn chạy `README.md` | Đọc kiểm từng mục đối chiếu với code và kết quả chạy thực tế trên nhánh `CP2` | Kiều Văn Thắng, Nguyễn Triều Dương |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
