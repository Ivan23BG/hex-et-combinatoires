from board.awaleboard import AwaleBoard


def play_awele_game():
    # Create an instance of the AweleBoard class
    player = 0
    board = AwaleBoard()

    # Implement the game logic
    while not board.game_over():
        print("-------------------")
        board.display_board()
        if player == 1:
            player = 2
        else:
            player = 1
        print(f"Player's {player} turn")

        move = int(input("Choose pit number: "))

        board.make_move(move, player)
        
        winner = None
        if winner:
            print(winner)



# Start the game
play_awele_game()