"""
Main entry point for ChessBot
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.uci.uci import UCIEngine
import config


def main():
    """Main function"""
    print("ChessBot 1.0 - Stockfish-like Architecture")
    print(f"Debug mode: {config.DEBUG_MODE}")
    print(f"Search depth: {config.SEARCH_DEPTH}")
    print(f"Search time: {config.SEARCH_TIME}s")
    print("Type 'uci' to start UCI mode")
    print("Type 'help' for commands")
    print()

    engine = UCIEngine()

    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        if command == "uci":
            engine.run()
        else:
            engine.handle_command(command)
    else:
        # Interactive mode
        print("ChessBot Interactive Mode")
        print("Enter 'uci' to start UCI mode")
        print("Enter 'quit' to exit")
        print()

        while True:
            try:
                line = input("> ").strip()

                if not line:
                    continue

                if line == "quit":
                    break
                elif line == "uci":
                    engine.run()
                    break
                elif line == "help":
                    print_help()
                else:
                    engine.handle_command(line)

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break


def print_help():
    """Print help"""
    print("""
ChessBot Commands:
  uci              Start UCI mode
  isready          Check if engine is ready
  ucinewgame       Start new game
  position <fen>   Set position from FEN
  position startpos moves <move1> <move2> ...
  go depth <d>     Search to depth d
  go movetime <ms> Search for ms milliseconds
  stop             Stop search
  quit             Exit engine
  debug on/off     Enable/disable debug mode
  setoption name <name> value <value>

Examples:
  uci
  isready
  ucinewgame
  position startpos moves e2e4 e7e5
  go depth 10
  quit
    """)


if __name__ == "__main__":
    main()