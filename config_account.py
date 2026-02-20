"""
Account Automation Configuration
"""

# Chess.com Account Credentials
CHESSCOM_USERNAME = "your_username"  # Tên đăng nhập chess.com của bạn
CHESSCOM_PASSWORD = "your_password"  # Mật khẩu chess.com của bạn

# Automation Settings
AUTO_ACCEPT_CHALLENGES = True  # Tự động chấp nhận challenges
AUTO_CHALLENGE_PLAYERS = True  # Tự động thách đấu người chơi
MAX_GAMES_PER_SESSION = 10  # Số game tối đa mỗi session
MIN_TIME_BETWEEN_MOVES = 1.0  # Thời gian tối thiểu giữa các nước đi (giây)
MAX_TIME_BETWEEN_MOVES = 5.0  # Thời gian tối đa giữa các nước đi (giây)

# Opponent Settings
MIN_OPPONENT_RATING = 1000  # Rating tối thiểu
MAX_OPPONENT_RATING = 1500  # Rating tối đa
AUTO_CHALLENGE_RANDOM = True  # Thách đấu ngẫu nhiên

# Browser Settings
HEADLESS = False  # Chạy ẩn danh (True = không hiển thị browser)
BROWSER = "chrome"  # chrome, firefox, edge
WINDOW_SIZE = (1920, 1080)

# Bot Settings
USE_BOT_MOVES = True  # Sử dụng bot để tính toán nước đi
BOT_DEPTH = 5  # Độ sâu tìm kiếm của bot
RANDOM_MOVE_CHANCE = 0.10  # 10% cơ hội đi nước ngẫu nhiên (để tránh detect)

# Safety
STOP_AFTER_LOSSES = 3  # Dừng sau khi thua X game liên tiếp
STOP_AFTER_WINS = 10  # Dừng sau khi thắng X game liên tiếp
SESSION_TIMEOUT = 3600  # Timeout session (giây) - 1 giờ

# Logging
LOG_MOVES = True  # Log các nước đi
LOG_FILE = "account_automation.log"

# Anti-detection
HUMAN_LIKE_BEHAVIOR = True  # Giả lập hành vi như người
RANDOM_CLICK_DELAY = True  # Thêm delay ngẫu nhiên khi click
RANDOM_SCROLL = True  # Scroll ngẫu nhiên
MOUSE_MOVEMENT = True  # Di chuột tự nhiên

# Time Control
PREFERRED_TIME_CONTROL = "10+0"  # 10 phút, 0 giây increment
ACCEPT_ANY_TIME_CONTROL = True  # Chấp nhận mọi time control