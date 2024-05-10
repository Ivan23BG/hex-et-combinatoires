#Implementation du jeu de Awale
import copy
import random
from typing import List

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
    """
    A class to represent an Awale board for a game.

    Attributes
    ----------
    board : List[List[int]]
        The 2D list representing the board. Each element is an integer representing a player (0 means no player).
    player : int
        The current player (1 or 2).

    Methods
    -------
    display_board() -> None:
        Display the board in the console.
    is_legal_move(position: int, player: int) -> bool:
        Check if a move is legal.
    make_move(position: int, player: int) -> None:
        Make a move on the board.
    affamer(position: int, player: int) -> bool:
        Check if the move would starve the opponent.
    nourrir(position: int, player: int) -> None:
        Check if the player can feed the opponent.
    sow_seeds(position: int) -> int:
        Sow the seeds from a position.
    capture(origin: int, player: int) -> bool:
        Capture seeds if possible.
    get_scores() -> List[int]:
        Get the scores of the players.
    get_board() -> List[int]:
        Get the board.
    check_winner() -> int:
        Check if there is a winner.
    get_possible_moves(player: int) -> List[int]:
        Get the possible moves for a player.
    eval(player: int) -> int:
        Evaluate the board for a player.
    minimax(depth: int, player: int, alpha: int, beta: int) -> int:
        Minimax algorithm with alpha-beta pruning.
    get_best_move(depth: int, player: int) -> int:
        Get the best move for a player.
    set_board(board: List[int]) -> None:
        Set the board.
    set_scores(scores: List[int]) -> None:
        Set the scores of the players.
    undo_move(new_board: List[int], new_score_1: int, new_score_2: int) -> None:
        Undo a move.
    """
    def __init__(self):
        self.board: List[List[int]] = [4 for _ in range(12)]
        self.score_1: int = 0
        self.score_2: int = 0


    def display_board(self) -> None:
        """
        Display the board in the console.
        """
        print("|\t0\t1\t2\t3\t4\t5\t|")
        print(f"|\t{self.board[0]}\t{self.board[1]}\t{self.board[2]}\t{self.board[3]}\t{self.board[4]}\t{self.board[5]}\t|")
        print(f"|\t{self.board[11]}\t{self.board[10]}\t{self.board[9]}\t{self.board[8]}\t{self.board[7]}\t{self.board[6]}\t|\n")
        print("|\t11\t10\t9\t8\t7\t6\t|")
    
    
    def is_legal_move(self, position: int, player: int) -> bool:
        """
        Check if a move is legal.
        
        Args:
            position (int): The position of the move.
            player (int): The player making the move.
        
        Returns:
            bool: True if the move is legal, False otherwise.
        
        Raises:
            InvalidPositionError: If the position is invalid.
            PositionEmptyError: If the position is empty.
            AffamerError: If the move would starve the opponent.
            CanFeedError: If the player can feed the opponent.
            CannotFeedError: If the player cannot feed the opponent.
        """
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
    
    
    def make_move(self, position: int, player: int) -> None:
        """
        Make a move on the board.
        
        Args:
            position (int): The position of the move.
            player (int): The player making the move.
        
        Raises:
            InvalidPositionError: If the position is invalid.
            PositionEmptyError: If the position is empty.
            AffamerError: If the move would starve the opponent.
            CanFeedError: If the player can feed the opponent.
            CannotFeedError: If the player cannot feed the opponent.
        """
        self.is_legal_move(position, player)
        
        # Sow the seeds
        position = self.sow_seeds(position)
        
        # print("Position from sowing: ", position)
        
        # Check if any capture is possible
        self.capture(position, player)
    
    
    def affamer(self, position: int, player: int) -> bool:
        """
        Check if the move would starve the opponent.
        
        Args:
            position (int): The position of the move.
            player (int): The player making the move.
            
        Returns:
            bool: True if the move would starve the opponent, False otherwise.
        """
        game_copy = copy.deepcopy(self)
        game_copy.sow_seeds(position)
        
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
    
    
    def nourrir(self, position: int, player: int) -> None:
        """
        Check if the player can feed the opponent.
        
        Args:
            position (int): The position of the move.
            player (int): The player making the move.
        
        Returns:
            bool: True if the player can feed the opponent, False otherwise.
        
        Raises:
            CanFeedError: If the player can feed the opponent and did not.
            CannotFeedError: If the player cannot feed the opponent.
        """
        # Check if the opponent's side is empty
        if player == 1:
            if sum(self.board[6:12]) != 0:
                return True
        else:
            if sum(self.board[0:6]) != 0:
                return True
        
        # Check if the player's move will feed the opponent
        game_copy = copy.deepcopy(self)
        game_copy.sow_seeds(position)
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
                game_copy.sow_seeds(i)
                if sum(game_copy.board[6:12]) != 0:
                    raise CanFeedError("Player can feed the opponent")
        else:
            for i in range(6, 12):
                game_copy = copy.deepcopy(self)
                game_copy.sow_seeds(i)
                if sum(game_copy.board[0:6]) != 0:
                    raise CanFeedError("Player can feed the opponent")
        raise CannotFeedError("Player cannot feed the opponent")
    
    
    def sow_seeds(self, position: int) -> int:
        """
        Sow the seeds from a position.
        
        Args:
            position (int): The position of the move.
        
        Returns:
            int: The final position of the last seed sown.
        """
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
    
    
    def capture(self, origin: int, player: int) -> bool:
        """
        Capture seeds if possible.
        
        Args:
            origin (int): The position of the last seed sown.
            player (int): The player making the move.
        
        Returns:
            bool: True if a capture was made, False otherwise.
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
    
    
    def get_scores(self) -> List[int]:
        """
        Get the scores of the players.
        
        Returns:
            List[int]: The scores of the players.
        """
        return[self.score_1,self.score_2]
    
    
    def get_board(self) -> List[int]:
        """
        Get the board.
        
        Returns:
            List[int]: The board.
        """
        return self.board
    

    def check_winner(self) -> int:
        """
        Check if there is a winner.
        
        Returns:
            int: The winner (1 or 2) if there is one, None otherwise.
        """
    
        if self.board[0:5] == [0,0,0,0,0,0]:
            return 2
    
        if self.board[6:11] == [0,0,0,0,0,0]:
            return 1
        
        if self.score_1 > 24:
            return 1
        
        if self.score_2 > 24:
            return 2
        
        if sum(self.board) <= 3:
            return 2 - self.score_1 > self.score_2
        
        try:
            self.nourrir(0, 1)
        except CannotFeedError:
            return 1
        
        try:
            self.nourrir(6, 2)
        except CannotFeedError:
            return 2
        
        return None
    

    def get_possible_moves(self, player: int) -> List[int]:
        """
        Get the possible moves for a player.
        
        Args:
            player (int): The player.
        
        Returns:
            List[int]: The possible moves.
        """
        res = []
        game_copy = copy.deepcopy(self)
        
        if player == 1:
            for i in range(0, 6):
                try:
                    game_copy.is_legal_move(i, player)
                    res.append(i)
                except Exception:
                    pass
        else:
            for i in range(6, 12):
                try:
                    game_copy.is_legal_move(i, player)
                    res.append(i)
                except Exception:
                    pass
        return res
    
    
    def eval(self, player: int) -> int:
        """
        Evaluate the board for a player.

        Args:
            player (int): The player.

        Returns:
            int: The evaluation of the board for the player.
        """
        if player == 1:
            return self.score_1
        if player == 2:
            return -(self.score_2)
    
    def randomsaufpoints(self, player: int) -> int:
        """
        Evaluate the board for a player.
        
        Args:
            player (int): The player.
        
        Returns:
            int: The evaluation of the board for the player.
        """
        if player == 1 :
            return self.score_1
        else :
            return -(self.score_2)
    
    
    def minimax(self, depth: int, player: int, alpha: int, beta: int) -> int:
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            depth (int): The depth of the search.
            player (int): The player.
            alpha (int): The alpha value.
            beta (int): The beta value.
        
        Returns:
            int: The best score.
        """
        if depth == 0 :
            return self.eval(player)*((depth+1)*(depth+1)), None

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
                if score is not None and score > best_score:
                        best_score = score
                        best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
            #print("ici",best_score, best_move)
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
                if score is not None and score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
                #print(best_score,best_move)
            return best_score, best_move
    
    
    def get_best_move(self, depth: int, player: int) -> int:
        """
        Get the best move for a player.
        
        Args:
            depth (int): The depth of the search.
            player (int): The player.
        
        Returns:
            int: The best move.
        """
        a , best_move = self.minimax(depth, player, float('-inf'), float('inf'))
        #print("mov",a, best_move, player)
        return best_move
    
    
    def set_board(self, board: List[int]) -> None:
        """
        Set the board.
        
        Args:
            board (List[int]): The board.
        """
        self.board = board
    
    
    def set_scores(self, scores: List[int]) -> None:
        """
        Set the scores of the players.
        
        Args:
            scores (List[int]): The scores of the players.
        """
        self.score_1 = scores[0]
        self.score_2 = scores[1]
        
    
    def undo_move(self, new_board: List[int], new_score_1: int, new_score_2: int) -> None:
        """
        Undo a move.
        
        Args:
            new_board (List[int]): The new board.
            new_score_1 (int): The new score of player 1.
            new_score_2 (int): The new score of player 2.
        """
        self.board = new_board
        self.score_1 = new_score_1
        self.score_2 = new_score_2
