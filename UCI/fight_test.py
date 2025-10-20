import chess
import chess.engine

board = chess.Board()

engine1 = chess.engine.SimpleEngine.popen_uci([
    r"C:\PythonProject\ChessGame\.venv\Scripts\python.exe",
    r"C:\PythonProject\ChessGame\UCI\javad_engine.py"
])

engine2 = chess.engine.SimpleEngine.popen_uci(r"C:\Users\Lenovo.ws\Desktop\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe")



limit = chess.engine.Limit(time=0.5)

while not board.is_game_over():
    if board.turn == chess.WHITE:
        result = engine1.play(board, limit)
    else:
        result = engine2.play(board, limit)
    board.push(result.move)

print("Result:", board.result())

engine1.quit()
engine2.quit()
