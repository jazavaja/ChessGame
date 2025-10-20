# my_engine.py
import sys
import chess
import random

print("id name MyPythonEngine")
print("id author Javad")
print("uciok")

board = chess.Board()

while True:
    line = input()
    if line == "isready":
        print("readyok")

    elif line.startswith("position startpos"):
        moves = line.split("moves")
        board.reset()
        if len(moves) > 1:
            for move in moves[1].strip().split():
                board.push_uci(move)

    elif line.startswith("go"):
        move = random.choice(list(board.legal_moves))
        print(f"bestmove {move}")

    elif line == "quit":
        break
