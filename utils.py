# utils.py

import pygame
from constants import PIECE_IMAGES, SQUARE_SIZE

def load_pieces():
    """Load and scale piece images."""
    pieces = {}
    for piece, path in PIECE_IMAGES.items():
        image = pygame.image.load(path)
        pieces[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
    return pieces