# Video demo CP3 (~30 giây) — LoiChoi

- **Model sử dụng:** `openai/gpt-4.1-mini` (qua OpenRouter, cùng model với lượt 1 `run-1@20261128-005643`)
- **Link video (YouTube Không công khai):** https://youtu.be/syBKNhpcIIE

## Kịch bản quay 30 giây (`python run.py` từ thư mục gốc repo)

> **Lưu ý an toàn trước khi quay:** Không mở `.env`, không để lộ `API_KEY`, không dán thông tin cá nhân (PII). Bỏ biến môi trường `MODEL_PROVIDER=fake` ở terminal nếu có.

1. **0–5s — Mở terminal tại thư mục gốc repo, chạy:**
   ```powershell
   python run.py
   ```
2. **5–18s — Dán ca thường có xung đột kèm nguồn (B01):**
   ```text
   Mình định ráp máy: CPU Ryzen 5 5600, main ASUS TUF GAMING B650-PLUS WIFI, RAM Kingston KF556C40BBK2-32, card MSI RTX 4060 VENTUS 2X BLACK 8G OC, vỏ NZXT H5 Flow (2024), không lắp radiator mặt trước. Kiểm giúp mình.
   ```
   - Chỉ ra trên màn hình: kết luận `Có xung đột` (CPU AM4 vs main AM5), hai cặp còn lại `Chưa phát hiện xung đột trong phạm vi đã kiểm`, có **Nguồn** (AMD/ASUS/Kingston/MSI/NZXT), mục **Chưa kiểm** và token thật > 0 từ `openai/gpt-4.1-mini`.
3. **18–30s — Dán ca giới hạn / mơ hồ cần hỏi lại (B07):**
   ```text
   Main ASUS B760M với RAM Kingston KF432C16BBK2/16 có dùng cùng nhau được không?
   ```
   - Chỉ ra trên màn hình: hệ thống trả `Thiếu thông tin`, liệt kê đủ 2 biến thể `TUF GAMING B760M-PLUS WIFI D4` (DDR4) và `TUF GAMING B760M-PLUS WIFI` (DDR5) để hỏi lại người dùng, không tự chọn ngầm.
