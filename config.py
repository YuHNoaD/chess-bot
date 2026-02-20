"""
Chess Bot Configuration
"""

# Search Configuration
SEARCH_DEPTH = 10  # Default search depth
SEARCH_TIME = 1.0  # Default search time (seconds)

# Transposition Table
TRANSPOSITION_TABLE_SIZE = 1024 * 1024  # 1M entries

# Evaluation Weights
MATERIAL_WEIGHT = 1.0
POSITION_WEIGHT = 1.0
MOBILITY_WEIGHT = 0.1
KING_SAFETY_WEIGHT = 0.5
PAWN_STRUCTURE_WEIGHT = 0.3

# Piece Values (in centipawns)
PAWN_VALUE = 100
KNIGHT_VALUE = 320
BISHOP_VALUE = 330
ROOK_VALUE = 500
QUEEN_VALUE = 900
KING_VALUE = 20000

# Chess.com API Configuration
CHESSCOM_API_URL = "https://api.chess.com"
CHESSCOM_BOT_USERNAME = "your_bot_username"
CHESSCOM_API_KEY = "your_api_key"

# UCI Options
UCI_HASH = 128  # Hash table size in MB
UCI_THREADS = 4  # Number of threads
UCI_SKILL_LEVEL = 10  # 0-20

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "bot.log"

# Performance
MAX_NODES = 10000000  # Maximum nodes to search
TIME_BUFFER = 0.1  # Time buffer (seconds)

# Debug
DEBUG_MODE = False
DEBUG_DEPTH = 5
DEBUG_POSITIONS = []