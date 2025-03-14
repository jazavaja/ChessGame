# Chess Game with Pygame

This is a simple chess game built using Python's `pygame` library and the `python-chess` module. The game includes a graphical user interface (GUI) for playing chess, a timer for each player, and highlighting of legal moves.

---

## Features

- **Graphical Chessboard**: A visually appealing chessboard with pieces rendered using images.
- **Legal Move Highlighting**: Highlights all legal moves for the selected piece.
- **Timer System**: Each player has a 10-minute timer that counts down during their turn.
- **Game Status Display**: Shows whose turn it is, the remaining time for each player, and the game status (e.g., check, checkmate, stalemate).
- **Modular Code Structure**: The project is organized into multiple files for better readability and maintainability.

---

## Requirements

To run this project, you need the following dependencies:

- Python 3.8 or higher
- Required Python packages:
  - `pygame`: For rendering the GUI.
  - `python-chess`: For handling chess logic.

You can install the required packages using the following command:

```bash
pip install pygame python-chess
```

Additionally, ensure that the piece images are placed in the `images/` directory. The image filenames should match those specified in the `constants.py` file.

---

## File Structure

The project is organized into the following files:

```
chess-game/
│
├── constants.py       # Contains global constants like colors, dimensions, and piece image paths.
├── utils.py           # Utility functions for loading and scaling piece images.
├── boards.py          # Manages the chessboard, timers, and game logic.
├── game.py            # Handles the main game loop, user input, and rendering.
├── main.py            # Entry point of the program.
└── images/            # Directory containing chess piece images.
```

---

## How to Run the Game

1. Clone or download the project repository.
2. Ensure that all required dependencies are installed (`pygame` and `python-chess`).
3. Place the chess piece images in the `images/` directory. The filenames should match those specified in `constants.py`.
4. Run the game using the following command:

```bash
python main.py
```

---

## Gameplay Instructions

- **Selecting a Piece**: Click on a piece to select it. Legal moves for the selected piece will be highlighted.
- **Making a Move**: Click on a highlighted square to move the selected piece.
- **Timer**: Each player has 10 minutes. The timer counts down during their turn. If a player's time runs out, they lose the game.
- **Game Status**: The top bar displays whose turn it is, the remaining time for each player, and the current game status (e.g., check, checkmate, stalemate).

---

## Customization

- **Piece Images**: Replace the images in the `images/` directory with your own custom images. Ensure the filenames match those in `constants.py`.
- **Board Colors**: Modify the `LIGHT_BROWN` and `DARK_BROWN` colors in `constants.py` to change the board's appearance.
- **Timer Duration**: Adjust the initial timer values (`white_time` and `black_time`) in `boards.py` to change the game duration.

---

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Possible improvements include:

- Adding sound effects for moves, captures, and game events.
- Implementing different time controls (e.g., blitz, rapid).
- Enhancing the GUI with additional features like move history or a promotion dialog.

---

## License

This project is open-source and available under the MIT License. See the `LICENSE` file for more details.

---

## Acknowledgments

- [Pygame](https://www.pygame.org/) for providing the GUI framework.
- [python-chess](https://python-chess.readthedocs.io/) for handling chess logic.
- Icons made AI

---

Happy coding, and enjoy the game! 🎮♟️

