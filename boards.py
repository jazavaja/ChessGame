# board.py

import time
import chess
import pygame

from constants import LIGHT_BROWN, DARK_BROWN, HIGHLIGHT_COLOR, INFO_HEIGHT, SQUARE_SIZE
from utils import load_pieces

class Board:
    def __init__(self):
        self.board = chess.Board()
        self.start_time = time.time()
        self.white_time = 600  # 10 minutes for white
        self.black_time = 600  # 10 minutes for black
        self.last_move_time = self.start_time
        self.game_over = False
        self.pieces = load_pieces()

    def draw(self, screen):
        """Draw the chessboard and pieces."""
        for row in range(8):
            for col in range(8):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, INFO_HEIGHT + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Draw pieces
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_image = self.pieces[piece.symbol()]
                screen.blit(piece_image, (chess.square_file(square) * SQUARE_SIZE, INFO_HEIGHT + (7 - chess.square_rank(square)) * SQUARE_SIZE))

    def highlight_legal_moves(self, screen, selected_square):
        """Highlight legal moves for the selected piece."""
        if selected_square is not None:
            legal_moves = list(self.board.legal_moves)
            for move in legal_moves:
                if move.from_square == selected_square:
                    target_col = chess.square_file(move.to_square)
                    target_row = 7 - chess.square_rank(move.to_square)
                    pygame.draw.circle(
                        screen,
                        HIGHLIGHT_COLOR,
                        (target_col * SQUARE_SIZE + SQUARE_SIZE // 2, INFO_HEIGHT + target_row * SQUARE_SIZE + SQUARE_SIZE // 2),
                        SQUARE_SIZE // 4
                    )

    def make_move(self, move):
        """Make a move on the board if it's legal."""
        if move in self.board.legal_moves:
            self.board.push(move)
            self.last_move_time = time.time()

    def update_timer(self):
        """Update the timer for both players."""
        if self.game_over:
            return

        current_time = time.time()
        elapsed_time = current_time - self.last_move_time
        if self.board.turn:  # White's turn
            self.white_time -= elapsed_time
        else:  # Black's turn
            self.black_time -= elapsed_time
        self.last_move_time = current_time

        if self.white_time <= 0:
            self.game_over = True
            print("White's time is up! Black wins!")
        elif self.black_time <= 0:
            self.game_over = True
            print("Black's time is up! White wins!")

    def get_time_remaining(self):
        """Return the remaining time for both players."""
        return max(0, int(self.white_time)), max(0, int(self.black_time))