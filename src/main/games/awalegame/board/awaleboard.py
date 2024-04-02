#Implementation du jeu de Awele

class InvalidPositionError(Exception):
    pass

class AwaleBoard:
    def __init__(self):
        """
        Initialize the class
        """
        self.board = [4] * 12
        self.score_1 = 0
        self.score_2 = 0

    def spray_seeds(self, origin):
        """
        Distribute the seeds in the pits.
        """
        seeds = self.board[origin]
        self.board[origin] = 0
        for i in range(seeds):
            origin = (origin - 1) % 12
            self.board[origin] += 1
        return origin

    def capture(self, origin, player):
        """
        Check if the last seed lands in a pit with 2 or 3 seeds.
        """
        finished_capture = False
        while self.board[origin] in [2, 3] and player == 1 and 6 <= origin <= 11:
            self.score_1 += self.board[origin]
            self.board[origin] = 0
            origin += 1
            finished_capture = True
        if finished_capture:
            return
        while self.board[origin] in [2, 3] and player == 2 and 0 <= origin <= 5:
            self.score_2 += self.board[origin]
            self.board[origin] = 0
            origin += 1

    def game_over(self):
        """
        Check if the game is over.
        """
        return sum(self.board[:6]) == 0 or sum(self.board[6:]) == 0

    def display_board(self):
        """
        Display the board in the console.
        """
        print("0  1  2  3  4  5")
        print("----------------")
        print(f"{self.board[0]}  {self.board[1]}  {self.board[2]}  {self.board[3]}  {self.board[4]}  {self.board[5]}")
        print(f"{self.board[11]}  {self.board[10]}  {self.board[9]}  {self.board[8]}  {self.board[7]}  {self.board[6]}")
        print("----------------")
        print("11 10 9  8  7  6")
        print(f"Player 1: {self.score_1} Player 2: {self.score_2}\n")

    def valid_move(self, move, player):
        """
        Check if the move is valid.
        """
        if player == 1:
            return 0 <= move <= 5 and self.board[move] > 0
        else:
            return 6 <= move <= 11 and self.board[move] > 0

    def make_move(self, move, player):
        """
        Make a move on the board.
        """
        if not self.valid_move(move, player):
            raise InvalidPositionError("Invalid move")
        origin = move
        origin = self.spray_seeds(origin)
        self.capture(origin, player)
        return self.check_winner()

    def check_winner(self):
        """
        Determine the winner of the game.
        Right now this only checks if the total number of seeds in the pits is greater than 20.
        """
        if self.score_1 > 24:
            return 1
        elif self.score_2 > 24:
            return 2
        else:
            return None
