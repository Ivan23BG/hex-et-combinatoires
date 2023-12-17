# main.py
from src.main.hexgame.board.hexboard import HexBoard


# Example 1
size = 3
game_board = HexBoard(size)
game_board.place_piece(1, (2, 0))
game_board.place_piece(2, (0, 1))
game_board.place_piece(1, (0, 2))
game_board.place_piece(2, (1, 1))
game_board.place_piece(1, (1, 2))
game_board.place_piece(2, (2, 2))
game_board.place_piece(1, (2, 1))
game_board.display_board()
winner = game_board.check_winner()
if winner:
    print("Player", winner, "won!")
else:
    print("No one has won yet")