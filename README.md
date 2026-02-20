# Chess Bot - Stockfish-like Architecture

A chess bot with architecture similar to Stockfish, written in Python.

## 📋 Overview

This chess bot implements a Stockfish-like architecture with:
- ✅ Type definitions (Piece, Square, Move, etc.)
- ✅ Position/Board representation
- ✅ Move generation
- ✅ Position evaluation
- ✅ Alpha-Beta search algorithm
- ✅ UCI protocol support
- ✅ Integration with chess.com API

## 🏗️ Architecture

```
chess-bot/
├── README.md
├── requirements.txt
├── main.py
├── config.py
└── src/
    ├── types/
    │   ├── __init__.py
    │   ├── types.py
    │   ├── piece.py
    │   ├── square.py
    │   ├── move.py
    │   └── color.py
    ├── position/
    │   ├── __init__.py
    │   ├── position.py
    │   ├── bitboard.py
    │   └── fen.py
    ├── movegen/
    │   ├── __init__.py
    │   ├── movegen.py
    │   ├── legal.py
    │   └── pseudo.py
    ├── search/
    │   ├── __init__.py
    │   ├── search.py
    │   ├── alphabeta.py
    │   ├── transposition.py
    │   └── quiescence.py
    ├── evaluation/
    │   ├── __init__.py
    │   ├── evaluation.py
    │   ├── material.py
    │   ├── position.py
    │   └── piece_square.py
    └── uci/
        ├── __init__.py
        ├── uci.py
        └── commands.py
```

## 🚀 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

## 🎮 Usage

### UCI Mode (Default)
```bash
python main.py
```

### Chess.com Integration
```python
from src.uci.uci import UCIEngine

# Create engine
engine = UCIEngine()

# Connect to chess.com
engine.connect_to_chesscom(username="your_bot", api_key="your_key")

# Start playing
engine.play_loop()
```

## 📊 Features

- **Alpha-Beta Pruning:** Efficient search algorithm
- **Transposition Table:** Cache positions to avoid recomputation
- **Quiescence Search:** Extend search in tactical positions
- **Material Evaluation:** Basic piece values
- **Position Evaluation:** Piece-square tables
- **UCI Protocol:** Compatible with UCI chess engines
- **Chess.com API:** Play automatically on chess.com

## ⚙️ Configuration

Edit `config.py` to adjust:
- Search depth
- Time control
- Evaluation weights
- Transposition table size

## 📈 Performance

- **Depth:** 10-15 ply (depending on time)
- **Nodes per second:** ~100k-1M (depending on hardware)
- **ELO:** ~1500-2000 (basic evaluation)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Stockfish:** Inspiration for architecture
- **python-chess:** Chess library for Python
- **chess.com:** Platform for playing

---

**Made with ❤️ by YuHNoaD**