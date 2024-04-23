#Implementation du jeu de Awale
import copy
import random

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
    
    def is_legal_move(self, position, player):
        # Check if the position is valid
        if position < 0 or position > 11:
            raise InvalidPositionError("Invalid position, position must be between 0 and 11")
        
        # Check if the position is empty
        if self.board[position] == 0:
            raise PositionEmptyError("Position is empty")
        
        # Check if the position is on the opponent's side
        if player == 1 and position > 5:
            raise InvalidPositionError("Invalid position, position must be on player 1's side")
        if player == 2 and position <= 5:
            raise InvalidPositionError("Invalid position, position must be on player 2's side")
        
        # Check rule "affamer"
        if self.affamer(position, player):
            raise AffamerError("Player would starve the opponent")
        
        # Check rule "nourrir"
        try:
            self.nourrir(position, player)
        except CanFeedError:
            raise CanFeedError("Player can feed the opponent")
        except CannotFeedError:
            raise CannotFeedError("Game should be over after this move")
        
        return True
    
    
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
            raise AffamerError("Player cannot play this move, it will starve the opponent")
        
        
        # Check rule "nourrir"
        if not self.nourrir(position, player):
            raise NourrirError("Player can feed the opponent")
        
        # Sow the seeds
        position = self.sow_seeds(position, player)
        
        # print("Position from sowing: ", position)
        
        # Check if any capture is possible
        self.capture(position, player)
        
        # Check if the game is over
        return self.check_winner()
    
    
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
        # Check if the opponent's side is empty
        if player == 1:
            if sum(self.board[6:12]) != 0:
                return True
        else:
            if sum(self.board[0:6]) != 0:
                return True
        
        # Check if the player's move will feed the opponent
        game_copy = copy.deepcopy(self)
        game_copy.sow_seeds(position, player)
        if player == 1:
            if sum(game_copy.board[6:12]) != 0:
                return True
        else:
            if sum(game_copy.board[0:6]) != 0:
                return True
        
        
        # Check if the player can feed the opponent
        if player == 1:
            for i in range(0, 6):
                game_copy = copy.deepcopy(self)
                game_copy.sow_seeds(i, player)
                if sum(game_copy.board[6:12]) != 0:
                    raise CanFeedError("Player can feed the opponent")
        else:
            for i in range(6, 12):
                game_copy = copy.deepcopy(self)
                game_copy.sow_seeds(i, player)
                if sum(game_copy.board[0:6]) != 0:
                    raise CanFeedError("Player can feed the opponent")
        raise CannotFeedError("Player cannot feed the opponent")
    
    
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
    
    
    def get_scores(self):
        return[self.score_1,self.score_2]
    
    
    def get_board(self):
        return self.board
    

    def check_winner(self):
        
        if self.board[0:5] == [0,0,0,0,0,0]:
            self.score_2  = 48
            return 2
    
        if self.board[6:11] == [0,0,0,0,0,0]:
            self.score_1  = 48
            return 1
        if self.score_1 > 24:
            return 1
        if self.score_2 > 24:
            return 2
        
        if sum(self.board) <= 3:
            if self.score_1 > self.score_2:
                return 1
            if self.score_2 > self.score_1:
                return 2
        #return 0
    

    def get_possible_moves(self,player):
        res = []
        game_copy = copy.deepcopy(self)
        
        if player == 1:
            for i in range(0, 6):
                try:
                    game_copy.is_legal_move(i, player)
                    res.append(i)
                except Exception as e:
                    pass
        else:
            for i in range(6, 12):
                try:
                    game_copy.is_legal_move(i, player)
                    res.append(i)
                except Exception as e:
                    pass
        return res
    
    
    def randomsaufpoints(self,player):
        if player == 1 :
            return self.score_1
        else :
            return -(self.score_2)
    
    
    def minimax(self, depth, player, alpha, beta):
        if depth == 0 or self.check_winner() is not None:
            return self.randomsaufpoints(player)*((depth+1)*(depth+1)), None

        if player == 1:  # Maximizing player
            best_score = float('-inf')
            best_move = None
            possible_moves = self.get_possible_moves(player)
            #print(possible_moves)
            for move in possible_moves:
                #print("m", move)
                game_copy = copy.deepcopy(self) #copy pour undo move
                game_copy.make_move(move, player)
                score, _ = game_copy.minimax(depth - 1, 1, alpha, beta)
                if score > best_score:
                        best_score = score
                        best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
            return best_score, best_move
        
        else:  # Minimizing player
            best_score = float('inf')
            best_move = None
            possible_moves = self.get_possible_moves(player)
            for move in possible_moves:
                game_copy = copy.deepcopy(self) #copy pour undo move
                game_copy.make_move( move, player)
                score, _ = game_copy.minimax(depth - 1, 1, alpha, beta)
                #self = game_copy #undo move
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
                print(best_score,best_move)
            return best_score, best_move
    
    
    def get_best_move(self, depth, player):
        a , best_move = self.minimax(depth, player, float('-inf'), float('inf'))
        print("mov",a, best_move, player)
        return best_move
    
    
    def set_board(self, board):
        self.board = board
    
    
    def set_scores(self, scores):
        self.score_1 = scores[0]
        self.score_2 = scores[1]
        
    
    def undo_move(self, new_board, new_score_1, new_score_2):
        self.board = new_board
        self.score_1 = new_score_1
        self.score_2 = new_score_2
