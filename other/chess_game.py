import pygame
import sys
import chess
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 500  # Increased height for info area
BOARD_HEIGHT = 400
INFO_HEIGHT = 100
SQUARE_SIZE = BOARD_HEIGHT // 8

LIGHT_BROWN = (238, 238, 210)
DARK_BROWN = (0, 51, 0)
HIGHLIGHT_COLOR = (0, 255, 0, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Load and scale piece images
PIECES = {
    "P": pygame.image.load("../images/w_chess_piyade.png"),
    "N": pygame.image.load("../images/w_asb.png"),
    "B": pygame.image.load("../images/w_fil.png"),
    "R": pygame.image.load("../images/w_gale.png"),
    "Q": pygame.image.load("../images/w_vazir.png"),
    "K": pygame.image.load("../images/w_shah.png"),
    "p": pygame.image.load("../images/b_piyade.png"),
    "n": pygame.image.load("../images/b_asb.png"),
    "b": pygame.image.load("../images/b_fil.png"),
    "r": pygame.image.load("../images/b_gale.png"),
    "q": pygame.image.load("../images/b_vazir.png"),
    "k": pygame.image.load("../images/b_shah.png"),
}

for piece in PIECES:
    PIECES[piece] = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))


class Board:
    def __init__(self):
        self.board = chess.Board()
        self.start_time = time.time()  # Start time for the game
        self.white_time = 600  # 10 minutes for white
        self.black_time = 600  # 10 minutes for black
        self.last_move_time = self.start_time
        self.game_over = False  # Flag to indicate if the game is over

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
                piece_image = PIECES[piece.symbol()]
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
            self.last_move_time = time.time()  # Update last move time

    def update_timer(self):
        """Update the timer for both players."""
        if self.game_over:
            return  # Stop updating the timer if the game is over

        current_time = time.time()
        elapsed_time = current_time - self.last_move_time
        if self.board.turn:  # White's turn
            self.white_time -= elapsed_time
        else:  # Black's turn
            self.black_time -= elapsed_time
        self.last_move_time = current_time

        # Check if time has run out for either player
        if self.white_time <= 0:
            self.game_over = True
            print("White's time is up! Black wins!")
        elif self.black_time <= 0:
            self.game_over = True
            print("Black's time is up! White wins!")

    def get_time_remaining(self):
        """Return the remaining time for both players."""
        return max(0, int(self.white_time)), max(0, int(self.black_time))


class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("شطرنج")
        self.board = Board()
        self.selected_square = None
        self.font = pygame.font.SysFont("Arial", 20)

    def draw_game_info(self):
        """Draw game information (turn, status, timers)."""
        # Clear the info area
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, INFO_HEIGHT))

        # Display whose turn it is
        turn_text = self.font.render(f"Turn: {'White' if self.board.board.turn else 'Black'}", True, WHITE)
        self.screen.blit(turn_text, (10, 10))

        # Display game status
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

        # Display timers
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
                col = mouse_x // SQUARE_SIZE
                row = (mouse_y - INFO_HEIGHT) // SQUARE_SIZE

                # Ensure the click is within the chessboard boundaries
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

            # Update the timer
            self.board.update_timer()

            # Clear the screen
            self.screen.fill(BLACK)

            # Draw game information
            self.draw_game_info()

            # Draw the board and pieces
            self.board.draw(self.screen)

            # Highlight legal moves
            self.board.highlight_legal_moves(self.screen, self.selected_square)

            # Update the display
            pygame.display.flip()


if __name__ == "__main__":
    game = ChessGame()
    game.run()