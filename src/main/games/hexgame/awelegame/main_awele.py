from board.aweleboard import AweleBoard

def play_awele_game():
    # Create an instance of the AweleBoard class
    board = AweleBoard()
    board.display_board()

    # Implement the game logic
    while not board.game_over():
        #Le tour du joueur 1
        print("Player 1's turn")
        move = int(input("Enter your move: "))        
        if not board.make_move(move, 1):
            board.display_board()
            # show scores
            print("Player 1:", board.score_1)
            print("Player 2:", board.score_2)
        else:
            print("Game over!")
            print("Final scores:")
            print("Player 1:", board.get_player_score(1))
            print("Player 2:", board.get_player_score(2))
            break
        
        #Le tour du joueur 2
        print("Player 2's turn")
        move = int(input("Enter your move: "))        
        if not board.make_move(move, 2):
            board.display_board()
            # show scores
            print("Player 1:", board.score_1)
            print("Player 2:", board.score_2)
        else:
            print("Game over!")
            print("Final scores:")
            print("Player 1:", board.get_player_score(1))
            print("Player 2:", board.get_player_score(2))
            break

# Start the game
play_awele_game()