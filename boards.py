# boards.py

import time
import chess
import pygame
import requests
import threading

from constants import LIGHT_BROWN, DARK_BROWN, HIGHLIGHT_COLOR, INFO_HEIGHT, SQUARE_SIZE
from utils import load_pieces


class Board:
    def __init__(self, difficulty=8):
        self.board = chess.Board()
        self.start_time = time.time()
        self.white_time = 600  # 10 minutes for white (player)
        self.black_time = 600  # 10 minutes for black (bot)
        self.last_move_time = self.start_time
        self.game_over = False
        self.pieces = load_pieces()
        self.difficulty = difficulty  # 1-8, where 8 is strongest
        self.bot_thinking = False

    def draw(self, screen):
        """Draw the chessboard and pieces."""
        for row in range(8):
            for col in range(8):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(
                    screen, color,
                    (col * SQUARE_SIZE, INFO_HEIGHT + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )

        # Draw pieces
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_image = self.pieces[piece.symbol()]
                screen.blit(
                    piece_image,
                    (chess.square_file(square) * SQUARE_SIZE,
                     INFO_HEIGHT + (7 - chess.square_rank(square)) * SQUARE_SIZE)
                )

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
                        (target_col * SQUARE_SIZE + SQUARE_SIZE // 2,
                         INFO_HEIGHT + target_row * SQUARE_SIZE + SQUARE_SIZE // 2),
                        SQUARE_SIZE // 4
                    )

    def make_move(self, move):
        """Make a move on the board if it's legal."""
        if move in self.board.legal_moves:
            self.board.push(move)
            self.last_move_time = time.time()
            return True
        return False

    def get_bot_move_from_lichess(self):
        """Get a move from Lichess API."""
        try:
            # Lichess API endpoint for analysis
            url = "https://lichess.org/api/cloud-eval"

            # Prepare the FEN position
            fen = self.board.fen()

            params = {
                'fen': fen,
                'multiPv': 1
            }

            response = requests.get(url, params=params, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if 'pvs' in data and len(data['pvs']) > 0:
                    # Get the best move from the primary variation
                    best_move = data['pvs'][0]['moves'].split()[0]
                    return chess.Move.from_uci(best_move)

            # Fallback: use simple local evaluation if API fails
            return self.get_simple_bot_move()

        except Exception as e:
            print(f"Error getting bot move from Lichess: {e}")
            return self.get_simple_bot_move()

    def get_simple_bot_move(self):
        """Simple fallback bot that picks a random legal move with basic evaluation."""
        import random

        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            return None

        # Simple scoring: prioritize captures and checks
        scored_moves = []
        for move in legal_moves:
            score = 0
            # Check if it's a capture
            if self.board.is_capture(move):
                score += 10
            # Check if it gives check
            self.board.push(move)
            if self.board.is_check():
                score += 5
            self.board.pop()
            scored_moves.append((move, score))

        # Sort by score and add some randomness
        scored_moves.sort(key=lambda x: x[1] + random.random() * 2, reverse=True)
        return scored_moves[0][0]

    def bot_move(self):
        """Make the bot move (called when it's black's turn)."""
        if self.bot_thinking or self.game_over:
            return

        self.bot_thinking = True

        # Add a small delay to make it feel more natural
        pygame.time.wait(500)

        move = self.get_bot_move_from_lichess()

        if move and move in self.board.legal_moves:
            self.board.push(move)
            self.last_move_time = time.time()

        self.bot_thinking = False

    def update_timer(self):
        """Update the timer for both players."""
        if self.game_over or self.bot_thinking:
            return

        current_time = time.time()
        elapsed_time = current_time - self.last_move_time

        if self.board.turn:  # White's turn (player)
            self.white_time -= elapsed_time
        else:  # Black's turn (bot)
            self.black_time -= elapsed_time

        self.last_move_time = current_time

        if self.white_time <= 0:
            self.game_over = True
            print("Your time is up! Bot wins!")
        elif self.black_time <= 0:
            self.game_over = True
            print("Bot's time is up! You win!")

        # Check for game over conditions
        if self.board.is_checkmate() or self.board.is_stalemate():
            self.game_over = True

    def get_time_remaining(self):
        """Return the remaining time for both players."""
        return max(0, int(self.white_time)), max(0, int(self.black_time))
