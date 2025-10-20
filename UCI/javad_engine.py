#!/usr/bin/env python3
import sys
import chess
import random

# Print basic engine info (required by UCI protocol)
print("id name MyPythonEngine")
print("id author Javad")
print("uciok")

# Create a new chess board
board = chess.Board()

# Infinite loop to read commands from stdin
while True:
    try:
        line = input().strip()
    except EOFError:
        break  # Exit if input stream closes

    if not line:
        continue

    # === Handle 'uci' command ===
    # UCI GUI sends this first to identify the engine
    if line == "uci":
        print("id name MyPythonEngine")
        print("id author Javad")
        print("uciok")

    # === Handle 'isready' ===
    # GUI checks if the engine is ready to receive commands
    elif line == "isready":
        print("readyok")

    # === Handle 'ucinewgame' ===
    # Tells the engine that a new game is starting
    elif line == "ucinewgame":
        board.reset()

    # === Handle 'position' command ===
    # Example: "position startpos moves e2e4 e7e5"
    elif line.startswith("position"):
        parts = line.split("moves")
        if "startpos" in parts[0]:
            board.reset()
        elif "fen" in parts[0]:
            fen_part = parts[0].replace("position fen", "").strip()
            board.set_fen(fen_part)

        if len(parts) > 1:
            moves = parts[1].strip().split()
            for move in moves:
                try:
                    board.push_uci(move)
                except Exception:
                    pass  # Ignore illegal or invalid moves

    # === Handle 'go' command ===
    # Example: "go movetime 1000"
    elif line.startswith("go"):
        # Default move time
        movetime = 1000

        # Parse movetime if provided
        if "movetime" in line:
            try:
                movetime = int(line.split("movetime")[1].strip())
            except Exception:
                pass

        # Choose a random legal move (placeholder for real search)
        if board.is_game_over():
            print("bestmove 0000")  # No move if game is over
        else:
            move = random.choice(list(board.legal_moves))
            print(f"bestmove {move}")

    # === Handle 'quit' ===
    elif line == "quit":
        break

    # === Handle unknown commands (ignore) ===
    else:
        pass
