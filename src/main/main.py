# main.py

# import the HexBoard class from hexboard.py through relative path
from hexgame.board.hexboard import HexBoard

# ask player for board size
size = int(input("Enter the size of the board: "))
game_board = HexBoard(size)
game_board.display_board()
# start the game
while True:
    # player 1
    print("Player 1's turn")
    row = int(input("Enter the row: "))
    col = int(input("Enter the column: "))

    # decrease row and col by 1 to match the index
    row -= 1
    col -= 1

    # place the piece on the board
    game_board.place_piece(1, (row, col))
    game_board.display_board()

    # check if player 1 won
    winner = game_board.check_winner()
    if winner:
        print("Player", winner, "won!")
        break

    # player 2
    print("Player 2's turn")
    row = int(input("Enter the row: "))
    col = int(input("Enter the column: "))

    # decrease row and col by 1 to match the index
    row -= 1
    col -= 1

    # place the piece on the board
    game_board.place_piece(2, (row, col))
    game_board.display_board()

    # check if player 2 won
    winner = game_board.check_winner()
    if winner:
        print("Player", winner, "won!")
        break