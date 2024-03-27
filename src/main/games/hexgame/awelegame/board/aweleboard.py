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
        print(" 0  1  2  3  4  5")
        print(self.board[0:6])
        print(self.board[11:5:-1])
        print("11  10  9  8  7  6")
        print("\nPlayer 1 Score:", self.score_1, "\n")

    def valid_move(self, move, player):
        if player == 1:
            return 0 <= move <= 5 and self.board[move] > 0
        else:
            return 6 <= move <= 11 and self.board[move] > 0


    def get_board(self):
        return self.board
        
    
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
        self.check_last_piece((move - (seeds)) % 12, player)  

        # Check if the game is over
        if self.game_over():
            # Determine the winner and return their number
            return self.check_winner()

        # If the game is not over, return None
        return None
    
    def check_last_piece(self, last_piece, player):
        print("last_piece",last_piece)
        print("player",player)
        last_value = self.board[last_piece]
        print("last_value",last_value)
        if last_value == 2 or last_value == 3:
            if player == 1 and 6<= last_piece <= 11: 
                self.score_1 += last_value
                self.board[last_piece] = 0
                #print("points player 1", self.score_1)
            elif player == 2 and 0 <= last_piece <= 5:
                self.score_2 += last_value
                self.board[last_piece] = 0
                #print("points player 2", self.score_2)
            

    def game_over(self):
        return 0;
        #return sum(self.board[0:5]) == 0 or sum(self.board[6:12]) == 0


    def check_winner(self,player):
        if player == 1:
            if self.board[0:6] == [0,0,0,0,0,0]:
                self.score_2  = 48
                return 2
        if player == 2:
            if self.board[5:11] == [0,0,0,0,0,0]:
                self.score_1  = 48
                return 1
        if sum(self.board) <= 3:
            if self.score_1 > self.score_2:
                return 1
            if self.score_2 > self.score_1:
                return 2
