import pygame
import sys
import chess

# تنظیمات اولیه
pygame.init()

# ابعاد صفحه
WIDTH, HEIGHT = 400, 400
SQUARE_SIZE = WIDTH // 8

# رنگ‌ها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (220, 139, 71)
DARK_BROWN = (101, 67, 33)
HIGHLIGHT_COLOR = (0, 255, 0, 100)  # رنگ برای نمایش حرکات مجاز

# مهره‌ها
PIECES = {
    "P": pygame.image.load("images/w_chess_piyade.png"),  # پیاده سفید
    "N": pygame.image.load("images/w_asb.png"),  # اسب سفید
    "B": pygame.image.load("images/w_fil.png"),  # فیل سفید
    "R": pygame.image.load("images/w_gale.png"),  # رخ سفید
    "Q": pygame.image.load("images/w_vazir.png"),  # وزیر سفید
    "K": pygame.image.load("images/w_shah.png"),  # شاه سفید
    "p": pygame.image.load("images/b_piyade.png"),  # پیاده سیاه
    "n": pygame.image.load("images/b_asb.png"),  # اسب سیاه
    "b": pygame.image.load("images/b_fil.png"),  # فیل سیاه
    "r": pygame.image.load("images/b_gale.png"),  # رخ سیاه
    "q": pygame.image.load("images/b_vazir.png"),  # وزیر سیاه
    "k": pygame.image.load("images/b_shah.png"),  # شاه سیاه
}

# تبدیل تصاویر به اندازه خانه‌ها
for piece in PIECES:
    PIECES[piece] = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))

# ایجاد صفحه شطرنج با python-chess
board = chess.Board()

# تابع برای رسم صفحه شطرنج
def draw_board(screen):
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # نمایش مهره‌ها
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_image = PIECES[piece.symbol()]
            screen.blit(piece_image, (chess.square_file(square) * SQUARE_SIZE, (7 - chess.square_rank(square)) * SQUARE_SIZE))

# تابع برای نمایش حرکات مجاز
def highlight_legal_moves(screen, selected_square):
    legal_moves = list(board.legal_moves)
    for move in legal_moves:
        if move.from_square == selected_square:
            target_col = chess.square_file(move.to_square)
            target_row = 7 - chess.square_rank(move.to_square)
            pygame.draw.circle(
                screen,
                HIGHLIGHT_COLOR,
                (target_col * SQUARE_SIZE + SQUARE_SIZE // 2, target_row * SQUARE_SIZE + SQUARE_SIZE // 2),
                SQUARE_SIZE // 4
            )

# تابع اصلی
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("شطرنج")

    selected_square = None  # خانه انتخاب‌شده

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # کلیک ماوس
                mouse_x, mouse_y = event.pos
                col = mouse_x // SQUARE_SIZE
                row = mouse_y // SQUARE_SIZE
                square = chess.square(col, 7 - row)  # تبدیل ردیف و ستون به شماره خانه

                if selected_square is None:  # اگر هیچ خانه‌ای انتخاب نشده باشد
                    if board.piece_at(square):  # اگر خانه حاوی مهره باشد
                        selected_square = square
                else:  # اگر خانه‌ای انتخاب شده باشد
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:  # اگر حرکت مجاز باشد
                        board.push(move)  # اعمال حرکت
                    selected_square = None  # خانه انتخاب‌شده را پاک کن

        # رسم صفحه
        draw_board(screen)

        # نمایش حرکات مجاز
        if selected_square is not None:
            highlight_legal_moves(screen, selected_square)

        pygame.display.flip()

# اجرای برنامه
if __name__ == "__main__":
    main()