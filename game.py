# game.py
import sys

import chess
import pygame

import constants
from boards import Board
from constants import WIDTH, HEIGHT, WHITE, RED, YELLOW, INFO_HEIGHT


class ChessGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.board = Board()
        self.selected_square = None
        self.font = pygame.font.SysFont("Arial", 20)

    def draw_game_info(self):
        """Draw game information (turn, status, timers)."""
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, WIDTH, INFO_HEIGHT))

        turn_text = self.font.render(f"Turn: {'White' if self.board.board.turn else 'Black'}", True, WHITE)
        self.screen.blit(turn_text, (10, 10))

        if self.board.game_over:
            status_text = self.font.render("Game Over!", True, RED)
        elif self.board.board.is_checkmate():
            status_text = self.font.render("Checkmate!", True, RED)
        elif self.board.board.is_check():
            status_text = self.font.render("Check!", True, RED)
        elif self.board.board.is_stalemate():
            status_text = self.font.render("Stalemate!", True, YELLOW)
        else:
            status_text = self.font.render("Game in progress...", True, WHITE)
        self.screen.blit(status_text, (10, 40))

        white_time, black_time = self.board.get_time_remaining()
        white_timer = self.font.render(f"White: {white_time // 60}:{white_time % 60:02}", True, WHITE)
        black_timer = self.font.render(f"Black: {black_time // 60}:{black_time % 60:02}", True, WHITE)
        self.screen.blit(white_timer, (WIDTH - 150, 10))
        self.screen.blit(black_timer, (WIDTH - 150, 40))

    def handle_events(self):
        """Handle user input (mouse clicks)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not self.board.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col = mouse_x // constants.SQUARE_SIZE
                row = (mouse_y - INFO_HEIGHT) // constants.SQUARE_SIZE

                if 0 <= row < 8 and 0 <= col < 8:
                    square = chess.square(col, 7 - row)
                    if self.selected_square is None:
                        if self.board.board.piece_at(square):
                            self.selected_square = square
                    else:
                        move = chess.Move(self.selected_square, square)
                        self.board.make_move(move)
                        self.selected_square = None

    def run(self):
        """Main game loop."""
        while True:
            self.handle_events()
            self.board.update_timer()
            self.screen.fill((0, 0, 0))
            self.draw_game_info()
            self.board.draw(self.screen)
            self.board.highlight_legal_moves(self.screen, self.selected_square)
            pygame.display.flip()
