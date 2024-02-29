
from collections import deque
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
            visited = set()
        row, col = position
        #visited.append(position)
        queue = deque()
        if player == 1:
            for r in range(len(self.board[0])):
                if self.board[r][0] == player:
                    queue.append((r,0))
                    visited.add((r,0))
            while queue:
                r, c = queue.popleft()
                if c == len(self.board) - 1:
                    print(visited)
                    return True
                for x, y in ((r-1,c), (r,c-1), (r+1,c), (r,c+1), (r-1,c+1), (r+1,c-1)):
                    if 0 <= x < len(self.board) and 0 <= y < len(self.board[0]) and self.board[x][y] == player and (x,y) not in visited:
                        queue.append((x,y))
                        visited.add((x,y))
            return False
        else:
            for c in range(len(self.board[0])):
                if self.board[0][c] == player:
                    queue.append((0,c))
                    visited.add((0,c))
            while queue:
                r, c = queue.popleft()
                if r == len(self.board) - 1:
                    print(visited)
                    return True
                for x, y in ((r-1,c), (r,c-1), (r+1,c), (r,c+1), (r-1,c+1), (r+1,c-1)):
                    if 0 <= x < len(self.board) and 0 <= y < len(self.board[0]) and self.board[x][y] == player and (x,y) not in visited:
                        queue.append((x,y))
                        visited.add((x,y))
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
