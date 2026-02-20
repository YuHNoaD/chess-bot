"""
Chess.com Bot Configuration for ELO Farming
"""

# Chess.com Bot Credentials
CHESSCOM_BOT_USERNAME = "your_bot_username"  # Thay bằng username của bot
CHESSCOM_API_KEY = "your_api_key"  # Thay bằng API key từ chess.com

# ELO Farming Configuration
ELO_FARMING_DEPTH = 5  # Độ sâu tìm kiếm (3-10)
MIN_OPPONENT_RATING = 1000  # Rating tối thiểu của đối thủ
MAX_OPPONENT_RATING = 1500  # Rating tối đa của đối thủ

# Auto-play Configuration
MAX_GAMES = 100  # Số game tối đa chơi
CHECK_INTERVAL = 10  # Kiểm tra game mỗi X giây

# Search Configuration
SEARCH_DEPTH = 5  # Độ sâu tìm kiếm mặc định
SEARCH_TIME = 1.0  # Thời gian tìm kiếm (giây)

# Randomness (để tránh bị detect)
RANDOM_MOVE_CHANCE = 0.05  # 5% cơ hội đi nước ngẫu nhiên
RANDOM_DEPTH_VARIANCE = 1  # Biến thiên độ sâu ±1

# Logging
LOG_GAMES = True  # Log các game
LOG_FILE = "elo_farming.log"

# Safety
MAX_CONSECUTIVE_LOSSES = 5  # Dừng nếu thua 5 game liên tiếp
MIN_TIME_BETWEEN_GAMES = 60  # Thời gian tối thiểu giữa các game (giây)

# Strategy
PLAY_OPENING_BOOK = False  # Sử dụng opening book
PLAY_ENDGAME_TABLEBASE = False  # Sử dụng endgame tablebase

# Anti-detection
USE_HUMAN_LIKE_TIMING = True  # Giả lập thời gian đi như người
MIN_THINK_TIME = 1.0  # Thời gian suy nghĩ tối thiểu (giây)
MAX_THINK_TIME = 5.0  # Thời gian suy nghĩ tối đa (giây)