# main.py
from src.main.hexgame.board import hexboard


if __name__ == "__main__":
    size = 7
    game_board = HexBoard(size)
    print(game_board.board)  # Vérifiez que le plateau est correctement initialisé
