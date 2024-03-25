from board.aweleboard import AweleBoard

def play_awele_game():
    # Create an instance of the AweleBoard class
    board = AweleBoard()
    board.display_board()

    # Implement the game logic
    while not board.game_over():
        # Display the current state of the board
        print(board)

        #Le tour du joueur 1
        print("Player 1's turn")
        move = int(input("Enter your move: "))        
        board.make_move(move, 1)
        #Voir si le dernier mouvement est un coup gagnant
        board.check_last_piece(move, 1)
        #Afficher le tableau
        board.display_board()

        #Voir si le jeu est terminé
        if board.game_over():
            print("Game over!")
            print("Final scores:")
            print("Player 1:", board.get_player_score(1))
            print("Player 2:", board.get_player_score(2))
            break

        #Le tour du joueur 2
        print("Player 2's turn")
        move = int(input("Enter your move: "))
        board.make_move(move, 2)
        #Voir si le dernier mouvement est un coup gagnant
        board.check_last_piece(move, 2)
        #Afficher le tableau
        board.display_board()

        #Voir si le jeu est terminé
        if board.game_over():
            print("Game over!")
            print("Final scores:")
            print("Player 1:", board.get_player_score(1))
            print("Player 2:", board.get_player_score(2))
            break

# Start the game
play_awele_game()