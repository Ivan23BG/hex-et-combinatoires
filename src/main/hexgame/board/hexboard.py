# HexGame/board/hex_board.py
class InvalidPositionError(Exception):
    pass


class InvalidPlayerError(Exception):
    pass


class PositionOccupiedError(Exception):
    pass


class HexBoard:
    def __init__(self, size):
        """
        Initialize the class with the given size.
    
        Args:
            size (int): The size of the board.
        """
        if size <= 0:
            raise ValueError("Size must be a positive integer")
        self.size = size
        self.board = None
        self.initialize_board()

    def initialize_board(self):
        """
        Initialize the board with zeros.
        """
        self.board = [[0] * self.size for _ in range(self.size)]

    def place_piece(self, player, position):
        """
        place a piece on the board.
        
        Args:
            player (int): The player value (1 or 2).
            position (tuple): The position on the board.
        """
        # Place a piece on the board
        row, col = position

        # Check if the position is valid
        if not self.is_valid_position(row, col):
            raise InvalidPositionError("Invalid position")

        # Check if the player value is valid
        if player not in [1, 2]:
            raise InvalidPlayerError("Invalid player value. Player must be 1 or 2.")

        # Check if the position is already occupied
        if self.is_position_occupied(position):
            raise PositionOccupiedError("Position already occupied")

        self.board[row][col] = player

    def is_valid_position(self, row, col):
        """
        check if the position is within the bounds of the board.

        Args:
            row (int): The row index.
            col (int): The column index.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        return 0 <= row < self.size and 0 <= col < self.size

    def is_position_occupied(self, position):
        """
        Check if the position is already occupied.

        Args:
            position (tuple): The position on the board.

        Returns:
            bool: True if the position is occupied, False otherwise.
        """
        row, col = position
        return self.board[row][col] != 0

    def check_winner(self):
        """
        Check if there is a winner.

        Returns:
            int: The player value (1 or 2) if there is a winner, None otherwise.
        """
        for i in range(self.size):
            if self.board[i][0] == 1:  # left side
                if self.check_winner_player(1, (i, 0)):
                    return 1
            if self.board[0][i] == 2:  # top side
                if self.check_winner_player(2, (0, i)):
                    return 2
        return None

    def check_winner_player(self, player, position, visited=None):
        """
        check if the player has won.

        Args:
            player (int): The player value (1 or 2).
            position (tuple): The position on the board.
            visited (list): The list of visited positions.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        if visited is None:
            visited = []
        row, col = position
        visited.append(position)
        if col == self.size - 1 and player == 1:  # we're on the right side
            print("Winning path:", visited)
            return True
        if row == self.size - 1 and player == 2:  # we're on the bottom side
            print("Winning path:", visited)
            return True

        if row > 0:
            if (row - 1, col) not in visited:
                if self.board[row - 1][col] == player:
                    return self.check_winner_player(player, (row - 1, col), visited)  # top left
        if row > 0 and col < self.size - 1:
            if (row - 1, col + 1) not in visited:
                if self.board[row - 1][col + 1] == player:
                    return self.check_winner_player(player, (row - 1, col + 1), visited)  # top right
        if row < self.size - 1 and col > 0:
            if (row + 1, col - 1) not in visited:
                if self.board[row + 1][col - 1] == player:
                    return self.check_winner_player(player, (row + 1, col - 1), visited)  # bottom left
        if row < self.size - 1:
            if (row + 1, col) not in visited:
                if self.board[row + 1][col] == player:
                    return self.check_winner_player(player, (row + 1, col), visited)  # bottom right
        if col < self.size - 1:
            if (row, col + 1) not in visited:
                if self.board[row][col + 1] == player:
                    return self.check_winner_player(player, (row, col + 1), visited)  # right
        if col > 0:
            if (row, col - 1) not in visited:
                if self.board[row][col - 1] == player:
                    return self.check_winner_player(player, (row, col - 1), visited)  # left
        return False

    def display_board(self):
        """
        Display the board.
        """
        # add an offset to the board to make it look like a hexagon

        board_string = ""
        separator = " | "
        symbol_1 = "X"
        symbol_2 = "O"
        horizontal_line = " ---" * self.size
        offset = ""
        for i in range(self.size):
            # Add offset to the line
            offset = " " * (i * 2)
            board_string += offset + horizontal_line + "\n"
            board_string += offset + "| "
            for j in range(self.size):
                if self.board[i][j] == 1:
                    board_string += symbol_1 + separator
                elif self.board[i][j] == 2:
                    board_string += symbol_2 + separator
                else:
                    board_string += "*" + separator
            board_string += "\n"
        board_string += offset + horizontal_line
        print(board_string)       

    def make_move(self, player, position):
        """
        Make a move on the board by placing a piece and checking for a winner.
        """
        self.place_piece(player, position)
        self.display_board()
        return self.check_winner()
    
    def get_possible_moves(self):
        """
        Get all the possible moves on the board.
        """
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    moves.append((row, col))
        return moves
    
    def undo_move(self, position):
        """
        Undo a move on the board by removing the piece from the given position.
        """
        row, col = position
        self.board[row][col] = 0 

    def evaluate_board(self):
        """
        Evaluate the current state of the board.

        Returns:
            int: The evaluation score.
        """
        # Define the evaluation scores for each player
        player_1_score = 0
        player_2_score = 0

        # Evaluate the board for player 1
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    player_1_score += 1

        # Evaluate the board for player 2
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 2:
                    player_2_score += 1

        # Calculate the difference in scores
        score_difference = player_1_score - player_2_score

        return score_difference
    
    def minimax(self, depth, player, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            depth (int): The depth of the search tree.
            player (int): The player value (1 or 2).
            alpha (int): The alpha value for pruning.
            beta (int): The beta value for pruning.

        Returns:
            int: The best score for the current player.
        """
        if depth == 0 or self.check_winner() is not None:
            return self.evaluate_board()

        if player == 1:
            best_score = float('-inf')
            possible_moves = self.get_possible_moves()
            for move in possible_moves:
                self.place_piece(player, move)
                score = self.minimax(depth - 1, 2, alpha, beta)
                self.undo_move(move)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            possible_moves = self.get_possible_moves()
            for move in possible_moves:
                self.place_piece(player, move)
                score = self.minimax(depth - 1, 1, alpha, beta)
                self.undo_move(move)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
        
    def get_best_move(self, depth, player):
        """
        Get the best move for the given player using the minimax algorithm.

        Args:
            depth (int): The depth of the search tree.
            player (int): The player value (1 or 2).

        Returns:
            tuple: The best move (row, col).
        """
        best_score = float('-inf') if player == 1 else float('inf')
        best_move = None
        possible_moves = self.get_possible_moves()
        for move in possible_moves:
            self.place_piece(player, move)
            score = self.minimax(depth - 1, 3 - player, float('-inf'), float('inf'))
            self.undo_move(move)
            if player == 1 and score > best_score:
                best_score = score
                best_move = move
            elif player == 2 and score < best_score:
                best_score = score
                best_move = move
        return best_move
    
    def get_played_moves(self):
        """
        Get all the moves that have been played in the game.

        Returns:
            list: The list of played moves in the order they were played.
        """
        played_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != 0:
                    played_moves.append((row, col))
        return played_moves
