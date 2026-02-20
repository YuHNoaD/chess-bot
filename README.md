# Chess Bot - Complete Guide

## 🎮 CÁCH CHƠI VỚI CHESS BOT

---

## 📊 TỔNG QUAN

Bot chess đã hoàn thành với nhiều mode chơi khác nhau!

---

## 🎯 CÁCH CHƠI

### **1. Local Play - Chơi trên máy tính**

#### **Cách 1a: Chơi với bot (bạn vs bot)**
```bash
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\chess-bot
python play.py
```
**Commands:**
- Nhập nước đi: `e2e4`, `e7e5`, v.v.
- `quit` - Thoát
- `undo` - Hoàn tác nước đi

#### **Cách 1b: Bot tự chơi (bot vs bot)**
```bash
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\chess-bot
python auto_play.py
```
Bot sẽ tự chơi cả hai bên và hiển thị bàn cờ.

#### **Cách 1c: Run tests**
```bash
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\chess-bot
python test_bot.py
```
Chạy 7 tests để verify bot hoạt động.

#### **Cách 1d: UCI mode**
```bash
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\chess-bot
python main.py uci
```
UCI protocol để tích hợp với GUI (Arena, ChessBase).

---

### **2. Chess.com - Chơi trên chess.com**

#### **Cách 2a: ELO Farming (Cần Bot Club)**
```bash
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\chess-bot
python chess_com_bot.py
```

**Yêu cầu:**
1. Đăng ký Bot Club: https://www.chess.com/club/chess-com-bots
2. Lấy API key từ chess.com
3. Cấu hình `config_chesscom.py`:
```python
CHESSCOM_BOT_USERNAME = "your_bot_username"
CHESSCOM_API_KEY = "your_api_key"
```

**Bot sẽ:**
- ✅ Tự động chấp nhận challenges
- ✅ Chơi game liên tục
- ✅ Theo dõi win/loss/draw
- ✅ Dừng sau khi chơi đủ số game

#### **Cách 2b: Account Automation (Sử dụng Chrome Profile)**
```bash
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\chess-bot
python play_on_account.py
```

**Yêu cầu:**
1. Login vào chess.com trên Chrome của bạn
2. Đóng Chrome
3. Cấu hình `config_account.py` với Chrome profile:
```python
CHROME_USER_DATA_DIR = r"C:\Users\dhuy8\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_DIRECTORY = "Default"
```

**Bot sẽ:**
- ✅ Sử dụng Chrome profile đã có
- ✅ Không cần login lại
- ✅ Tự động chơi game
- ✅ Theo dõi win/loss/draw

**📖 Xem chi tiết:** `CHROME_PROFILE_GUIDE.md`

---

## 📈 KẾT QUẢ MONG ĐỢI

### **Local Play:**
- **Win rate:** ~60-70% (depth 5)
- **ELO gain:** Không áp dụng (local)
- **Thời gian:** ~1-2 seconds/move

### **ELO Farming:**
- **Win rate:** ~60-70% (depth 5)
- **ELO gain:** +10-20 ELO/10 games
- **Thời gian:** ~10-20 minutes/10 games

### **Account Automation:**
- **Win rate:** ~60-70% (depth 5)
- **ELO gain:** +10-20 ELO/10 games
- **Thời gian:** ~10-20 minutes/10 games
- ⚠️ **Rủi ro cao** - có thể bị BAN

---

## 🛠️ CẤU HÌNH

### **Bot Depth (Độ mạnh):**
```python
# config_chesscom.py
ELO_FARMING_DEPTH = 3  # Yếu (~1200 ELO)
ELO_FARMING_DEPTH = 5  # Trung bình (~1500 ELO)
ELO_FARMING_DEPTH = 7  # Mạnh (~1800 ELO)
ELO_FARMING_DEPTH = 10  # Rất mạnh (~2000+ ELO)
```

### **Opponent Rating:**
```python
# config_chesscom.py
MIN_OPPONENT_RATING = 1000  # Rating tối thiểu
MAX_OPPONENT_RATING = 1500  # Rating tối đa
```

### **Max Games:**
```python
# config_chesscom.py
MAX_GAMES = 100  # Số game tối đa
```

### **Chrome Profile:**
```python
# config_account.py
CHROME_USER_DATA_DIR = r"C:\Users\dhuy8\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_DIRECTORY = "Default"
```

---

## 🔗 GitHub Repository

**URL:** https://github.com/YuHNoaD/chess-bot

---

## 📝 Files

### **Core Files:**
- `main.py` - Entry point
- `config.py` - Configuration
- `config_chesscom.py` - Chess.com config
- `config_account.py` - Account config

### **Play Modes:**
- `play.py` - Chơi với bot
- `auto_play.py` - Bot tự chơi
- `test_bot.py` - Test bot
- `chess_com_bot.py` - Chess.com bot
- `play_on_account.py` - Account automation

### **API:**
- `chess_com_api.py` - Chess.com API client

### **Source:**
- `src/type_defs/` - Type definitions
- `src/position/` - Position/board
- `src/movegen/` - Move generation
- `src/evaluation/` - Evaluation
- `src/search/` - Search
- `src/uci/` - UCI protocol

### **Documentation:**
- `README.md` - Project README
- `HOW_TO_PLAY.md` - Complete play guide
- `ELO_FARMING_GUIDE.md` - ELO farming guide
- `ACCOUNT_AUTOMATION_GUIDE.md` - Account automation guide
- `CHROME_PROFILE_GUIDE.md` - Chrome profile guide

---

## 🐛 Bugs Fixed

1. ✅ **Circular import** - `src/types` → `src/type_defs`
2. ✅ **Hash position** - Dict → individual hashing
3. ✅ **Double pawn push** - Rank check fix
4. ✅ **evaluate_mobility** - Restore original turn
5. ✅ **Chrome profile** - Use existing Chrome profile

---

## 💡 Tips

### **Để bắt đầu:**
1. ✅ Chạy `python play.py` để chơi với bot
2. ✅ Chạy `python auto_play.py` để xem bot chơi
3. ✅ Chạy `python test_bot.py` để test

### **Để ELO farming:**
1. ✅ Đăng ký Bot Club
2. ✅ Lấy API key
3. ✅ Cấu hình `config_chesscom.py`
4. ✅ Chạy `python chess_com_bot.py`

### **Để chơi trên chess.com account:**
1. ✅ Login vào chess.com trên Chrome
2. ✅ Đóng Chrome
3. ✅ Cấu hình `config_account.py` với Chrome profile
4. ✅ Chạy `python play_on_account.py`
5. ✅ Bot sẽ sử dụng profile đã có và tự động chơi

---

## ⚠️ Lưu ý quan trọng

### **Trước khi chạy play_on_account.py:**
1. ✅ **Đóng Chrome** - Chrome không được mở khi chạy bot
2. ✅ **Đảm bảo đường dẫn đúng** - Kiểm tra lại Profile Path
3. ✅ **Đã login vào chess.com** - Nếu dùng profile đã có

### **Nếu gặp lỗi:**
1. ❌ "Chrome is being controlled by automated test software" - Normal, không cần lo
2. ❌ "Profile path not found" - Kiểm tra lại đường dẫn
3. ❌ "Cannot access profile" - Đóng Chrome và thử lại

---

**Chúc bạn chơi vui! 🎉**