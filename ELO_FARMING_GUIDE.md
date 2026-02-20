# ELO Farming Guide

## 🎯 Cách ELO Farm trên Chess.com

### Bước 1: Đăng ký Bot Club

1. Vào: https://www.chess.com/club/chess-com-bots
2. Đăng ký bot với username và email
3. Chờ approval (có thể mất 1-3 ngày)
4. Lấy API key từ settings

### Bước 2: Cấu hình Bot

Edit `config_chesscom.py`:

```python
CHESSCOM_BOT_USERNAME = "your_bot_username"
CHESSCOM_API_KEY = "your_api_key"

# ELO Farming settings
ELO_FARMING_DEPTH = 5  # Độ sâu tìm kiếm
MIN_OPPONENT_RATING = 1000  # Rating tối thiểu
MAX_OPPONENT_RATING = 1500  # Rating tối đa
```

### Bước 3: Chạy ELO Farming

```bash
python elo_farming.py
```

### Bước 4: Theo dõi

Bot sẽ:
- ✅ Tự động chấp nhận challenges
- ✅ Chơi game liên tục
- ✅ Theo dõi win/loss/draw
- ✅ Dừng sau khi chơi đủ số game

---

## ⚙️ Cấu hình

### Độ mạnh của bot

```python
ELO_FARMING_DEPTH = 3  # Yếu (~1200 ELO)
ELO_FARMING_DEPTH = 5  # Trung bình (~1500 ELO)
ELO_FARMING_DEPTH = 7  # Mạnh (~1800 ELO)
ELO_FARMING_DEPTH = 10  # Rất mạnh (~2000+ ELO)
```

### Rating đối thủ

```python
MIN_OPPONENT_RATING = 1000  # Chỉ chơi với người >= 1000
MAX_OPPONENT_RATING = 1500  # Chỉ chơi với người <= 1500
```

### Số game

```python
MAX_GAMES = 100  # Chơi tối đa 100 game rồi dừng
```

---

## 📊 Kết quả mong đợi

### Với depth 5:
- **Win rate:** ~60-70%
- **ELO gain:** +10-20 ELO/100 games
- **Thời gian:** ~1-2 hours/100 games

### Với depth 7:
- **Win rate:** ~70-80%
- **ELO gain:** +20-30 ELO/100 games
- **Thời gian:** ~2-4 hours/100 games

---

## ⚠️ Lưu ý quan trọng

### 1. **Tuân thủ Terms of Service**
- ❌ Không spam challenges
- ❌ Không chơi quá nhanh
- ✅ Tôn trọng đối thủ
- ✅ Thời gian phản hồi hợp lý

### 2. **Tránh bị detect**
- ✅ Sử dụng human-like timing
- ✅ Thêm randomness vào nước đi
- ✅ Không chơi 24/7
- ✅ Đi một số nước ngẫu nhiên

### 3. **An toàn**
- ✅ Giới hạn số game liên tiếp
- ✅ Dừng nếu thua quá nhiều
- ✅ Theo dõi ELO thay đổi
- ✅ Backup game logs

---

## 🚀 Tối ưu hóa ELO gain

### Strategy 1: Farm rating thấp
```python
MIN_OPPONENT_RATING = 800
MAX_OPPONENT_RATING = 1200
ELO_FARMING_DEPTH = 7
```
- **Win rate:** ~80-90%
- **ELO gain:** +5-10 ELO/100 games

### Strategy 2: Farm rating trung bình
```python
MIN_OPPONENT_RATING = 1200
MAX_OPPONENT_RATING = 1600
ELO_FARMING_DEPTH = 5
```
- **Win rate:** ~60-70%
- **ELO gain:** +10-20 ELO/100 games

### Strategy 3: Farm rating cao
```python
MIN_OPPONENT_RATING = 1500
MAX_OPPONENT_RATING = 2000
ELO_FARMING_DEPTH = 7
```
- **Win rate:** ~50-60%
- **ELO gain:** +15-25 ELO/100 games

---

## 📈 Theo dõi tiến độ

Bot sẽ in ra:
```
============================================================
ELO FARMING BOT STARTED
Username: your_bot
Max games: 100
============================================================

Stats: 5W - 2D - 1L
Win rate: 62.5%
```

---

## 🔧 Troubleshooting

### Bot không có game?
- ✅ Check API key có đúng không
- ✅ Bot đã được approve chưa
- ✅ Bot đã có challenges chưa

### Bot thua liên tiếp?
- ✅ Giảm ELO_FARMING_DEPTH
- ✅ Giảm MAX_OPPONENT_RATING
- ✅ Tìm đối thủ yếu hơn

### Bot bị báo cáo?
- ✅ Tăng thời gian suy nghĩ
- ✅ Tambah randomness
- ✅ Giảm số game/ngày

---

## 💡 Tips

### 1. **Bắt đầu chậm**
- Đầu tiên chơi depth 3 để làm quen
- Tăng dần độ sau khi đã ổn định

### 2. **Theo dõi patterns**
- Lưu lại các game để phân tích
- Tìm ra điểm yếu của bot
- Điều chỉnh evaluation weights

### 3. **Dừng đúng lúc**
- Nếu đang thua nhiều, dừng lại
- Bot không phải là máy tính hoàn hảo
- Đôi khi nghỉ ngơi là tốt

---

## 🎯 Goal

### Mục tiêu thực tế:
- **Tuần 1:** Đạt 1200 ELO
- **Tuần 2:** Đạt 1500 ELO
- **Tuần 3:** Đạt 1800 ELO
- **Tuần 4:** Đạt 2000+ ELO

### Mục tiêu tối ưu:
- **Month 1:** 2000 ELO
- **Month 2:** 2200 ELO
- **Month 3:** 2500+ ELO

---

**Chúc bạn ELO farming thành công! 🎉**