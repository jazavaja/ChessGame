import pygame
import sys
import chess

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
SQUARE_SIZE = WIDTH // 8
LIGHT_BROWN = (238, 238, 210)
DARK_BROWN = (0, 51, 0)
HIGHLIGHT_COLOR = (0, 255, 0, 100)

# Load and scale piece images
PIECES = {
    "P": pygame.image.load("images/w_chess_piyade.png"),
    "N": pygame.image.load("images/w_asb.png"),
    "B": pygame.image.load("images/w_fil.png"),
    "R": pygame.image.load("images/w_gale.png"),
    "Q": pygame.image.load("images/w_vazir.png"),
    "K": pygame.image.load("images/w_shah.png"),
    "p": pygame.image.load("images/b_piyade.png"),
    "n": pygame.image.load("images/b_asb.png"),
    "b": pygame.image.load("images/b_fil.png"),
    "r": pygame.image.load("images/b_gale.png"),
    "q": pygame.image.load("images/b_vazir.png"),
    "k": pygame.image.load("images/b_shah.png"),
}

for piece in PIECES:
    PIECES[piece] = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))


class Board:
    def __init__(self):
        self.board = chess.Board()

    def draw(self, screen):
        """Draw the chessboard and pieces."""
        for row in range(8):
            for col in range(8):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Draw pieces
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                piece_image = PIECES[piece.symbol()]
                screen.blit(piece_image, (chess.square_file(square) * SQUARE_SIZE, (7 - chess.square_rank(square)) * SQUARE_SIZE))

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
                        (target_col * SQUARE_SIZE + SQUARE_SIZE // 2, target_row * SQUARE_SIZE + SQUARE_SIZE // 2),
                        SQUARE_SIZE // 4
                    )

    def make_move(self, move):
        """Make a move on the board if it's legal."""
        if move in self.board.legal_moves:
            self.board.push(move)


class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("شطرنج")
        self.board = Board()
        self.selected_square = None

    def handle_events(self):
        """Handle user input (mouse clicks)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col = mouse_x // SQUARE_SIZE
                row = mouse_y // SQUARE_SIZE
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

            # Clear the screen
            self.screen.fill((0, 0, 0))

            # Draw the board and pieces
            self.board.draw(self.screen)

            # Highlight legal moves
            self.board.highlight_legal_moves(self.screen, self.selected_square)

            # Update the display
            pygame.display.flip()


if __name__ == "__main__":
    game = ChessGame()
    game.run()