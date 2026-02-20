# Hướng dẫn sử dụng Chrome Profile

## 🚀 Sử dụng Chrome Profile đã có sẵn

Bot hiện tại đã được cập nhật để sử dụng Chrome profile đã có sẵn, giúp:
- ✅ Không cần login lại mỗi lần
- ✅ Lưu cookies và sessions
- ✅ Tự động login với tài khoản đã có

---

## 📋 Cấu hình Chrome Profile

### **Bước 1: Tìm đường dẫn Chrome Profile**

1. Mở Chrome
2. Gõ `chrome://version/` vào thanh địa chỉ
3. Xem mục **"Profile Path"**
4. Copy đường dẫn

**Ví dụ:**
```
Profile Path: C:\Users\dhuy8\AppData\Local\Google\Chrome\User Data\Default
```

Trong đó:
- `C:\Users\dhuy8\AppData\Local\Google\Chrome\User Data` là **User Data Directory**
- `Default` là **Profile Directory**

### **Bước 2: Cấu hình config_account.py**

Edit file `config_account.py`:

```python
# Chrome Profile Configuration
CHROME_USER_DATA_DIR = r"C:\Users\dhuy8\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_DIRECTORY = "Default"
```

### **Bước 3: Chọn Profile**

Có 3 lựa chọn:

#### **Option 1: Profile Default (Profile chính)**
```python
CHROME_USER_DATA_DIR = r"C:\Users\dhuy8\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_DIRECTORY = "Default"
```

#### **Option 2: Profile khác (Profile 1, Profile 2, v.v.)**
```python
CHROME_USER_DATA_DIR = r"C:\Users\dhuy8\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_DIRECTORY = "Profile 1"
```

#### **Option 3: Profile mới (không login)**
```python
CHROME_USER_DATA_DIR = ""
CHROME_PROFILE_DIRECTORY = ""
```

---

## 🎯 Cách sử dụng

### **Cách 1: Dùng profile đã có (không cần login)**

1. Login vào chess.com trên Chrome của bạn
2. Đăng nhập thành công
3. Đóng Chrome
4. Chạy bot:
   ```bash
   python play_on_account.py
   ```
5. Bot sẽ tự động sử dụng profile đã có và đã login

### **Cách 2: Dùng profile mới (cần login)**

1. Để trống cấu hình:
   ```python
   CHROME_USER_DATA_DIR = ""
   CHROME_PROFILE_DIRECTORY = ""
   ```
2. Chạy bot:
   ```bash
   python play_on_account.py
   ```
3. Bot sẽ login từ đầu

---

## ⚠️ Lưu ý quan trọng

### **Trước khi chạy bot:**
1. ✅ **Đóng Chrome** - Chrome không được mở khi chạy bot
2. ✅ **Đảm bảo đường dẫn đúng** - Kiểm tra lại Profile Path
3. ✅ **Đã login vào chess.com** - Nếu dùng profile đã có

### **Nếu gặp lỗi:**
1. ❌ "Chrome is being controlled by automated test software" - Normal, không cần lo
2. ❌ "Profile path not found" - Kiểm tra lại đường dẫn
3. ❌ "Cannot access profile" - Đóng Chrome và thử lại

---

## 🔍 Tìm Profile Path trên Windows

### **Cách 1: Dùng chrome://version/**
1. Mở Chrome
2. Gõ `chrome://version/`
3. Xem "Profile Path"

### **Cách 2: Dùng File Explorer**
1. Mở File Explorer
2. Đi đến: `C:\Users\<username>\AppData\Local\Google\Chrome\User Data`
3. Xem các thư mục: `Default`, `Profile 1`, `Profile 2`, v.v.

### **Cách 3: Dùng Command Prompt**
```cmd
echo %LOCALAPPDATA%\Google\Chrome\User Data
```

---

## 💡 Tips

### **Để tránh lỗi:**
1. Luôn đóng Chrome trước khi chạy bot
2. Dùng profile riêng cho bot (Profile 1, Profile 2)
3. Đừng dùng profile Default nếu bạn đang dùng Chrome

### **Để tối ưu:**
1. Tạo profile riêng cho bot
2. Login 1 lần và sử dụng nhiều lần
3. Dùng profile có ít extensions

---

## 📝 Ví dụ cấu hình hoàn chỉnh

### **Cấu hình 1: Dùng Profile Default**
```python
# config_account.py
CHESSCOM_USERNAME = "YuHNoaD"
CHESSCOM_PASSWORD = "YuHNoaD06@"

CHROME_USER_DATA_DIR = r"C:\Users\dhuy8\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_DIRECTORY = "Default"
```

### **Cấu hình 2: Dùng Profile 1**
```python
# config_account.py
CHESSCOM_USERNAME = "YuHNoaD"
CHESSCOM_PASSWORD = "YuHNoaD06@"

CHROME_USER_DATA_DIR = r"C:\Users\dhuy8\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_DIRECTORY = "Profile 1"
```

### **Cấu hình 3: Dùng profile mới**
```python
# config_account.py
CHESSCOM_USERNAME = "YuHNoaD"
CHESSCOM_PASSWORD = "YuHNoaD06@"

CHROME_USER_DATA_DIR = ""
CHROME_PROFILE_DIRECTORY = ""
```

---

## 🚀 Chạy bot

Sau khi cấu hình xong, chạy bot:

```bash
cd C:\Users\dhuy8\.openclaw\workspace-shared\code\chess-bot
python play_on_account.py
```

---

**Chúc bạn thành công! 🎉**