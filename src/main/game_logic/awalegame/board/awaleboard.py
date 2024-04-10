#Implementation du jeu de Awale
import copy


class InvalidPositionError(Exception):
    pass


class PositionEmptyError(Exception):
    pass


class AffamerError(Exception):
    pass


class CanFeedError(Exception):
    pass

class CannotFeedError(Exception):
    pass

class NourrirError(Exception):
    pass


class AwaleBoard:
    def __init__(self):
        self.board = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.score_1=0
        self.score_2=0

    def display_board(self):
        print("|\t0\t1\t2\t3\t4\t5\t|")
        print(f"|\t{self.board[0]}\t{self.board[1]}\t{self.board[2]}\t{self.board[3]}\t{self.board[4]}\t{self.board[5]}\t|")
        print(f"|\t{self.board[11]}\t{self.board[10]}\t{self.board[9]}\t{self.board[8]}\t{self.board[7]}\t{self.board[6]}\t|\n")
        print("|\t11\t10\t9\t8\t7\t6\t|")
        
        
    def make_move(self, position, player):
        # Check if the position is valid
        if position < 0 or position > 11:
            raise InvalidPositionError("Invalid position, position should be between 1 and 12")
        
        # Check if the position is empty
        if self.board[position] == 0:
            raise PositionEmptyError("Position is empty")
        
        # Check if the position is on the opponent's side
        if player == 1 and position > 5:
            raise InvalidPositionError("Invalid position, position is on the opponent's side")
        if player == 2 and position <= 5:
            raise InvalidPositionError("Invalid position, position is on the opponent's side")
        
        
        # Check rule "affamer"
        if self.affamer(position, player):
            return AffamerError("Player cannot play this move, it will starve the opponent")
        
        
        # Check rule "nourrir"
        try:
            self.nourrir(position, player)
        except CanFeedError:
            return NourrirError("Player can feed the opponent")
        except CannotFeedError:
            # add all the remaining seeds to the opponent's score
            # then end the game
            if player == 1:
                for i in range(12):
                    self.score_2 += self.board[i]
                    self.board[i] = 0
            else:
                for i in range(12):
                    self.score_1 += self.board[i]
                    self.board[i] = 0
            return NourrirError("Player can't feed the opponent")
        
        # Sow the seeds
        position = self.sow_seeds(position, player)
        
        # print("Position from sowing: ", position)
        
        # Check if any capture is possible
        self.capture(position, player)
        
        # Check if the game is over
        return self.game_over()
    
    
    def affamer(self, position, player):
        game_copy = copy.deepcopy(self)
        game_copy.sow_seeds(position, player)
        
        # Check if the other player has any seeds left
        if player == 1:
            for i in range(6, 12):
                if game_copy.board[i] > 0:
                    return False
        else:
            for i in range(6):
                if game_copy.board[i] > 0:
                    return False
        return True
    
    
    def nourrir(self, position, player):
        game_copy = copy.deepcopy(self)
        game_copy.sow_seeds(position, player)
        
        # Check if the other player can still play
        if player == 1:
            for i in range(6, 12):
                if game_copy.board[i] > 0:
                    return True
        else:
            for i in range(6):
                if game_copy.board[i] > 0:
                    return True
        
        # If the other player cannot play, check if the current player can feed the opponent
        game_copy = copy.deepcopy(self)
        if player == 1:
            for i in range(6):
                if game_copy.board[i] >= 6 - i:
                    return CanFeedError("Player can feed the opponent")
        else:
            for i in range(6, 12):
                if game_copy.board[i] >= 12 - i:
                    return CanFeedError("Player can feed the opponent")
        return CannotFeedError("Player can't feed the opponent")
    
    
    def sow_seeds(self, position, player):
        seeds = self.board[position]
        self.board[position] = 0
        current_position = position
        # print("Initial position: ", current_position)
        while seeds > 0:
            # print("Changing position")
            # Skip the original position if seeds > 12
            # This is to avoid sowing seeds in the original position
            # Sow a seed in anti-clockwise direction
            current_position = (current_position - 1) % 12
            if current_position == position:
                current_position = (current_position - 1) % 12
            self.board[current_position] += 1
            seeds -= 1
        # print("Final position: ", current_position)
        return current_position
    
    
    def capture(self, origin, player):
        """
        Check if the last seed lands in a pit with 2 or 3 seeds.
        """
        finished_capture = False
        while self.board[origin] in [2, 3] and player == 1 and 6 <= origin <= 11:
            self.score_1 += self.board[origin]
            self.board[origin] = 0
            origin = (origin + 1) % 12
            finished_capture = True
        if finished_capture:
            return True
        while self.board[origin] in [2, 3] and player == 2 and 0 <= origin <= 5:
            self.score_2 += self.board[origin]
            self.board[origin] = 0
            origin = (origin + 1) % 12
            finished_capture = True
        return finished_capture
    
    
    def game_over(self):
        # Check if any player has a score of 25 or more
        if self.score_1 >= 25 or self.score_2 >= 25:
            return True
        # Check if there are less than 6 seeds left on the board
        seeds_left = 0
        for i in range(12):
            seeds_left += self.board[i]
        if seeds_left < 6:
            return True
        return False
    
    def get_scores(self):
        return[self.score_1,self.score_2]
    
    def get_board(self):
        return self.board
    
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