# Account Automation Guide

## ⚠️ CẢNH BÁO QUAN TRỌNG

### **RỦI RO BAN TÀI KHOẢN**
- Chess.com có thể **BAN TÀI KHOẢN** của bạn
- Bot được detect là không tự nhiên
- Có thể mất tất cả ELO, achievements, và premium membership

### **LƯU Ý AN TOÀN**
✅ Sử dụng account phụ (nếu có)
✅ Giới hạn số game/ngày (max 20-30)
✅ Không chơi 24/7
✅ Thêm randomness để tránh detect
✅ Dừng nếu bị cảnh báo

❌ Không nên dùng tài khoản chính
❌ Không nên chơi quá nhanh
❌ Không nên spam challenges
❌ Không nên bỏ giữa game

---

## 🚀 CÁCH SỬ DỤNG

### Bước 1: Cài đặt Selenium

```bash
pip install selenium webdriver-manager
```

### Bước 2: Cài đặt Browser Driver

Selenium sẽ tự động tải driver với `webdriver-manager`

### Bước 3: Cấu hình

Edit `config_account.py`:

```python
CHESSCOM_USERNAME = "your_username"
CHESSCOM_PASSWORD = "your_password"

# Cấu hình bot
BOT_DEPTH = 5  # Độ sâu tìm kiếm
RANDOM_MOVE_CHANCE = 0.10  # 10% đi ngẫu nhiên

# Safety
MAX_GAMES_PER_SESSION = 10  # Max 10 game mỗi session
STOP_AFTER_LOSSES = 3  # Dừng sau 3 thua liên tiếp
```

### Bước 4: Chạy

```bash
python play_on_account.py
```

---

## 🎮 CÁCH HOẠT ĐỘNG

### **Tự động:**
1. Login vào chess.com
2. Kiểm tra pending challenges
3. Chấp nhận challenges phù hợp
4. Tính toán nước đi bằng bot
5. Đi nước đi trên web
6. Lặp lại cho đến khi xong game
7. Kiểm tra game mới
8. Dừng khi đạt giới hạn

### **Anti-detection:**
- ✅ Random think time (1-5s)
- ✅ Random mouse movement
- ✅ Random move chance (10%)
- ✅ Human-like behavior
- ✅ Random delays

---

## 📊 KẾT QUẢ MONG ĐỢI

### **Với depth 5:**
- **Win rate:** ~60-70%
- **ELO gain:** +10-20 ELO/10 games
- **Thời gian:** ~10-20 minutes/10 games

### **Với depth 7:**
- **Win rate:** ~70-80%
- **ELO gain:** +15-25 ELO/10 games
- **Thời gian:** ~15-30 minutes/10 games

---

## ⚙️ CẤU HÌNH AN TOÀN

### **Cách 1: Chơi chậm (an toàn nhất)**
```python
MAX_GAMES_PER_SESSION = 5
BOT_DEPTH = 3
RANDOM_MOVE_CHANCE = 0.20
MIN_TIME_BETWEEN_MOVES = 2.0
MAX_TIME_BETWEEN_MOVES = 8.0
```
- Win rate: ~50-60%
- ELO gain: +5-10 ELO/5 games
- Rủi ro: Rất thấp

### **Cách 2: Chơi trung bình (cân bằng)**
```python
MAX_GAMES_PER_SESSION = 10
BOT_DEPTH = 5
RANDOM_MOVE_CHANCE = 0.10
MIN_TIME_BETWEEN_MOVES = 1.0
MAX_TIME_BETWEEN_MOVES = 5.0
```
- Win rate: ~60-70%
- ELO gain: +10-20 ELO/10 games
- Rủi ro: Thấp

### **Cách 3: Chơi nhanh (rủi ro cao)**
```python
MAX_GAMES_PER_SESSION = 20
BOT_DEPTH = 7
RANDOM_MOVE_CHANCE = 0.05
MIN_TIME_BETWEEN_MOVES = 0.5
MAX_TIME_BETWEEN_MOVES = 3.0
```
- Win rate: ~70-80%
- ELO gain: +20-30 ELO/20 games
- Rủi ro: Cao ⚠️

---

## 🔒 ANTI-DETECTION

### **Bot đã có:**
✅ Random think time
✅ Random mouse movement
✅ Random move chance
✅ Human-like timing
✅ Random delays

### **Cần bạn làm:**
✅ Không chơi 24/7
✅ Dừng nếu bị cảnh báo
✅ Giới hạn số game/ngày
✅ Thỉnh thoảng chơi thủ công
✅ Không spam challenges

---

## 📈 ELO FARMING STRATEGY

### **Strategy 1: Farm rating thấp (an toàn)**
```python
MIN_OPPONENT_RATING = 800
MAX_OPPONENT_RATING = 1200
BOT_DEPTH = 5
MAX_GAMES_PER_SESSION = 10
```
- Win rate: ~80-90%
- ELO gain: +5-10 ELO/10 games
- Rủi ro: Rất thấp

### **Strategy 2: Farm rating trung bình (khuyên dùng)**
```python
MIN_OPPONENT_RATING = 1200
MAX_OPPONENT_RATING = 1600
BOT_DEPTH = 5
MAX_GAMES_PER_SESSION = 10
```
- Win rate: ~60-70%
- ELO gain: +10-20 ELO/10 games
- Rủi ro: Thấp

### **Strategy 3: Farm rating cao (rủi ro)**
```python
MIN_OPPONENT_RATING = 1500
MAX_OPPONENT_RATING = 2000
BOT_DEPTH = 7
MAX_GAMES_PER_SESSION = 10
```
- Win rate: ~50-60%
- ELO gain: +15-25 ELO/10 games
- Rủi ro: Trung bình

---

## 🛡️ SAFETY MEASURES

### **Auto-stop khi:**
- ✅ Thua 3 game liên tiếp
- ✅ Thắng 10 game liên tiếp
- ✅ Đã chơi 10 games
- ✅ Session timeout (1 giờ)
- ✅ Detect lỗi

### **Manual stop:**
- ✅ Nhấn Ctrl+C để dừng
- ✅ Đóng browser để dừng
- ✅ Logout để dừng

---

## 📝 LOGGING

Bot sẽ log:
```
[INFO] Logged in as your_username
[INFO] Found 1 pending challenge
[INFO] Accepted challenge from opponent (rating: 1200)
[INFO] Game started
[INFO] Calculating move... (depth 5)
[INFO] Best move: e2e4
[INFO] Made move e2e4
[INFO] Game over! Result: 1-0 (win)
[INFO] Stats: 1W - 0D - 0L
```

---

## 🔧 TROUBLESHOOTING

### **Không login được?**
- ✅ Check username/password
- ✅ Check internet connection
- ✅ Thử chạy với HEADLESS = False

### **Bot không đi nước?**
- ✅ Check element selectors
- ✅ Check browser console
- ✅ Tăng thời gian chờ

### **Bị detect?**
- ✅ Tăng RANDOM_MOVE_CHANCE
- ✅ Giảm số game
- ✅ Dừng vài ngày
- ✅ Chơi thủ công một thời gian

---

## 💡 TIPS

### **1. Bắt đầu chậm**
- Đầu tiên chơi depth 3
- Tăng dần độ sâu
- Theo dõi phản ứng của chess.com

### **2. Theo dõi patterns**
- Lưu lại các game
- Tìm ra điểm yếu
- Điều chỉnh cấu hình

### **3. Dừng đúng lúc**
- Nếu đang thua nhiều, dừng
- Nếu bị cảnh báo, dừng ngay
- Nếu có lỗi, dừng và kiểm tra

### **4. Chơi thủ công thỉnh thoảng**
- Đôi khi chơi thủ công
- Để account trừu nhiên hơn
- Tránh bị detect

---

## 🎯 GOAL

### **Mục tiêu an toàn:**
- **Tuần 1:** +50 ELO (5 sessions)
- **Tuần 2:** +100 ELO (10 sessions)
- **Tuần 3:** +150 ELO (15 sessions)
- **Tuần 4:** +200 ELO (20 sessions)

### **Mục tiêu tối ưu:**
- **Month 1:** +300 ELO
- **Month 2:** +500 ELO
- **Month 3:** +800 ELO

---

## ⚠️ FINAL WARNING

**Tôi không chịu trách nhiệm nếu:**
❌ Tài khoản của bạn bị BAN
❌ Mất ELO và achievements
❌ Mất premium membership
❌ Bị chess.com cảnh báo

**Sử dụng tại rủi ro của bạn!**

---

**Chúc bạn ELO farming an toàn! 🎉**

**Nhớ: AN TOÀN LÀ SỐ 1!**