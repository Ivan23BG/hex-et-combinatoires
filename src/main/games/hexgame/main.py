# main.py
#vous etes sur la branche de timothée
# import the HexBoard class from hexboard.py
from hexgame.board.hexboard import HexBoard

# ask player for board size
size = int(input("Enter the size of the board: "))
game_board = HexBoard(size)
game_board.display_board()

# ask player for game mode
mode = input("Choose game mode (1 for 2 players, 2 for player vs PC): ")


# start the game
if mode == "1":
        # 2 players mode
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

elif mode == "2":
        # player vs PC mode
        while True:
            # player's turn
            print("Player's turn")
            row = int(input("Enter the row: "))
            col = int(input("Enter the column: "))

            # decrease row and col by 1 to match the index
            row -= 1
            col -= 1 

            # place the piece on the board
            game_board.place_piece(1, (row, col))
            game_board.display_board()

            # check if player won
            winner = game_board.check_winner()
            if winner:
                print("Player", winner, "won!")
                break

            # PC's turn
            print("PC's turn")

            # make a move using minimax algorithm and get_best_move method
            move = game_board.get_best_move(3,2)    
            game_board.place_piece(2, move)
            game_board.display_board()

            # check if PC won
            winner = game_board.check_winner()
            if winner:
                print("PC", winner, "won!")
                break

else:
        print("Invalid game mode. Please choose either 1 or 2.")