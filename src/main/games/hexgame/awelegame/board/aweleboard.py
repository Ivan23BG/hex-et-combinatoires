#Implementation du jeu de Awele

class InvalidPositionError(Exception):
    pass

class AweleBoard:
    def __init__(self):
        self.board = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.score_1=0
        self.score_2=0

    def display_board(self):
        print("\nPlayer 2 Score:", self.score_2, "\n")
        print(self.board[0:6])
        print(self.board[11:5:-1])
        print("\nPlayer 1 Score:", self.score_1, "\n")

    def valid_move(self, move, player):
        if player == 1:
            return 0 <= move <= 5 and self.board[move] > 0
        else:
            return 6 <= move <= 11 and self.board[move] > 0

    def make_move(self, move, player):
        # Check if the move is valid
        if not self.valid_move(move, player):
            raise InvalidPositionError("Invalid move")

        # Get the number of seeds in the selected pit
        seeds = self.board[move]

        # Empty the selected pit
        self.board[move] = 0

        # Distribute the seeds
        for i in range(1, seeds + 1):
            index = (move - i) % 12  
            self.board[index] += 1

        # Check if the last piece landed in a valid pit and can be captured
        self.check_last_piece((move + seeds) % 12, player)  

        # Check if the game is over
        if self.game_over():
            # Determine the winner and return their number
            return self.check_winner()

        # If the game is not over, return None
        return None
    
    def check_last_piece(self, move, player):
        last_piece = self.board[move]
        if last_piece == 2 or last_piece == 3:
            if player == 1 and 6<= move <= 11: 
                self.score_1 += last_piece
                self.board[move] = 0
            elif player == 2 and 0 <= move <= 5:
                self.score_2 += last_piece
                self.board[move] = 0
            

    def game_over(self):
        return sum(self.board[0:5]) == 0 or sum(self.board[6:12]) == 0

    def check_winner(self):
        player1_score = self.score_1
        player2_score = self.score_2
        if player1_score > player2_score:
            return 1
        elif player2_score > player1_score:
            return 2
        else:
            return None
