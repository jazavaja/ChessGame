import chess

# ایجاد یک صفحه شطرنج جدید
board = chess.Board()

while not board.is_game_over():
    print("\nوضعیت فعلی صفحه:")
    print(board)

    # حرکت سفید
    white_move = input("حرکت سفید (مثال: e4): ")
    try:
        board.push_uci(white_move)
    except ValueError:
        print("حرکت نامعتبر است. دوباره تلاش کنید.")
        continue

    print("\nوضعیت جدید صفحه:")
    print(board)

    # حرکت سیاه
    black_move = input("حرکت سیاه (مثال: e5): ")
    try:
        board.push_uci(black_move)
    except ValueError:
        print("حرکت نامعتبر است. دوباره تلاش کنید.")
        continue