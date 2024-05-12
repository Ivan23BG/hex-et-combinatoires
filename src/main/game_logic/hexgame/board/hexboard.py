from math import *  # for math functions
from collections import deque  # for queue
import heapq  # for priority queue
import random  # for random number generation
from time import time  # for time functions
import numpy as np  # for numpy arrays
from typing import List, Tuple, Dict  # for type hints
LOSE=1000  # for infinity


# ----------------- EXCEPTIONS ----------------- #
class InvalidPositionError(Exception):
    pass


class InvalidPlayerError(Exception):
    pass


class PositionOccupiedError(Exception):
    pass


# ----------------- HEX BOARD ----------------- #
class HexBoard:
    """
    A class to represent a hexagonal board for a game.

    Attributes
    ----------
    size : int
        The size of the board (number of hexagons per side).
    board : List[List[int]]
        The 2D list representing the board. Each element is an integer representing a player (0 means no player).

    Methods
    -------
    initialize_board() -> None:
        Initialize the board with zeros, representing an empty board.
    place_piece(player: int, position: Tuple[int, int]) -> None:
        Place a piece on the board at the given position.
    is_valid_position(row: int, col: int) -> bool:
        Check if the position is valid.
    is_position_occupied(position: Tuple[int, int]) -> bool:
        Check if the position on the board is occupied.
    check_winner() -> int:
        Check if there is a winner.
    check_winner_player(player: int, position: Tuple[int, int], visited=None) -> bool:
        Check if the given player has won the game starting from the given position.
    """
    def __init__(self, size: int):
        """
        Initialize the HexBoard with the given size.

        Args:
            size (int): The size of the board. Must be a positive integer.

        Raises:
            ValueError: If size is not a positive integer.
        """
        if size <= 0:
            raise ValueError("Size must be a positive integer")
        self.size: int = size
        self.board: List[List[int]] = []
        self.initialize_board()


    def initialize_board(self) -> None:
        self.board = [[0] * self.size for _ in range(self.size)]


    def place_piece(self, player: int, position: Tuple[int, int]) -> None:
        """
        Place a piece on the board at the given position.
        
        Args:
            player (int): The player value (1 or 2).
            position (Tuple[int, int]): The position on the board to place the piece.
            
        Raises:
            InvalidPositionError: If the position is invalid.
            InvalidPlayerError: If the player value is invalid.
            PositionOccupiedError: If the position is already occupied.
        """
        # Place a piece on the board
        row, col = position

        # Check if the position is valid
        if not self.is_valid_position(row, col):
            raise InvalidPositionError(f"Invalid position, out of bounds: {position}")

        # Check if the player value is valid
        if player not in [1, 2]:
            raise InvalidPlayerError(f"Invalid player value. Player must be 1 or 2: {player}")

        # Check if the position is already occupied
        if self.is_position_occupied(position):
            raise PositionOccupiedError(f"Position already occupied: {position}")

        self.board[row][col] = player


    def is_valid_position(self, row: int, col: int) -> bool:
        """
        Check if the position is valid.
        
        Args:
            row (int): The row index.
            col (int): The column index.
            
        Returns:
            bool: True if the position is valid, False otherwise.
        """
        return 0 <= row < self.size and 0 <= col < self.size


    def is_position_occupied(self, position: Tuple[int, int]) -> bool:
        """
        Check if the position on the board is occupied.
        
        Args:
            position (Tuple[int, int]): The position on the board to check.
            
        Returns:
            bool: True if the position is occupied, False otherwise.
        """
        row, col = position
        return self.board[row][col] != 0


    def check_winner(self) -> int:
        """
        Check if there is a winner.
        
        Returns:
            Optional[int]: The player value if there is a winner, None otherwise.
        """
        for i in range(self.size):
            if self.board[i][0] == 1:  # start on left side
                if self.check_winner_player(1, (i, 0)):
                    # print("Found winner 1")
                    return 1
            if self.board[0][i] == 2:  # start on top side
                if self.check_winner_player(2, (0, i)):
                    # print("Found winner 2")
                    return 2
        return None


    def check_winner_player(self, player: int, position: Tuple[int, int], visited=None) -> bool:
        """
        Check if the given player has won the game starting from the given position.
        
        Args:
            player (int): The player value (1 or 2).
            position (Tuple[int, int]): The position on the board to start the check.
            visited (Optional[Set[Tuple[int, int]]]): The set of visited positions.

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
                    #print(visited)
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
                    #print(visited)
                    return True
                for x, y in ((r-1,c), (r,c-1), (r+1,c), (r,c+1), (r-1,c+1), (r+1,c-1)):
                    if 0 <= x < len(self.board) and 0 <= y < len(self.board[0]) and self.board[x][y] == player and (x,y) not in visited:
                        queue.append((x,y))
                        visited.add((x,y))
            return False


    def is_player(self, position: Tuple[int, int], player: int) -> bool:
        """
        Check if the given position is occupied by the given player.

        Args:
            player (int): The player value (1 or 2).
            position (Tuple[int, int]): The position on the board to check.

        Returns:
            bool: True if the position is occupied by the player, False otherwise.
        """
        row, col = position
        return self.board[row][col] == player


    def is_empty(self, position: Tuple[int, int]) -> bool:
        """
        Check if the given position is empty.

        Returns:
            bool: True if the position is empty, False otherwise.
        """
        row, col = position
        return self.board[row][col] == 0


    def display_board(self) -> None:
        """
        Display the current state of the board.
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


    def make_move(self, player: int, position: Tuple[int, int]) -> None:
        """
        Make a move for the given player at the given position.

        Args:
            player (int): The player making the move.
            position (Tuple[int, int]): The position to place the piece.
        """
        self.place_piece(player, position)
        self.display_board()
        return self.check_winner()


    def get_possible_moves(self) -> List[Tuple[int, int]]:
        """
        Get all possible moves.

        Returns:
            List[Tuple[int, int]]: The list of possible moves.
        """
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    moves.append((row, col))
        return moves


    def undo_move(self, position: Tuple[int, int]) -> None:
        """
        Undo the move at the given position.

        Args:
            position (Tuple[int, int]): The position to undo the move.
        """
        row, col = position
        self.board[row][col] = 0 


    def get_played_moves(self) -> List[Tuple[int, int]]:
        """
        Get all played moves.

        Returns:
            List[Tuple[int, int]]: The list of played moves.
        """
        played_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != 0:
                    played_moves.append((row, col))
        return played_moves


    def get_neighbors(self, node: Tuple[int, int], rows: int, cols: int) -> List[Tuple[int, int]]:
        """
        Get the neighbors of the given node.
        
        Args:
            node (Tuple[int, int]): The node to get the neighbors for.
            rows (int): The number of rows in the board.
            cols (int): The number of columns in the board.
            
        Returns:
            List[Tuple[int, int]]: The list of neighbors.
        """
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]
        for dir in directions:
            neighbor_row, neighbor_col = node[0] + dir[0], node[1] + dir[1]
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
        return neighbors


    def is_potential_winner(self, player: int, position: Tuple[int, int]) -> bool:
        """
        Check if the player is a potential winner starting from the given position.

        Args:
            player (int): The player to check.
            position (Tuple[int, int]): The position to check.

        Returns:
            bool: True if the player is a potential winner, False otherwise.
        """
        # Check if the position is already occupied
        if self.is_position_occupied(position):
            return False
        # Place a temporary piece at the position
        row, col = position
        self.board[row][col] = player
        # Check if the player has won
        is_winner = self.check_winner_player(player, position)
        # Undo the temporary placement
        self.board[row][col] = 0

        return is_winner


    def get_CC(self, tab: List[Tuple[int, int]], move: Tuple[int, int]) -> List[List[Tuple[int, int]]]:
        """
        Get the connected component for the given move.
        
        Args:
            tab (List[Tuple[int, int]]): The list of connected components.
            move (Tuple[int, int]): The move to get the connected component for.
            
        Returns:
            List[List[Tuple[int, int]]]: The connected component.
        """
        tab.append(move)
        voisin = self.get_neighbors(move, self.size, self.size)
        for v in voisin:
            if self.board[v[0]][v[1]] == self.board[move[0]][move[1]] and v not in tab:
                tab.append(v)
                return self.get_CC(tab,v)
        return tab


    def find_connected_components(self, player: int) -> List[List[Tuple[int, int]]]:
        """
        Find the connected components for the given player.

        Args:
            player (int): The player to find the connected components for.

        Returns:
            List[List[Tuple[int, int]]]: The list of connected components.
        """
        rows, cols = self.size, self.size
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]

        def dfs(r, c):
            stack = [(r, c)]
            component = []
            while stack:
                cr, cc = stack.pop()
                if 0 <= cr < rows and 0 <= cc < cols and not visited[cr][cc] and self.board[cr][cc] == player:
                    visited[cr][cc] = True
                    component.append((cr, cc))
                    for dr, dc in directions:
                        stack.append((cr + dr, cc + dc))
            return component

        visited = [[False] * cols for _ in range(rows)]
        components = []

        for r in range(rows):
            for c in range(cols):
                if self.board[r][c] == player and not visited[r][c]:
                    components.append(dfs(r, c))

        return components


    def dijkstra(self, player: int, start: Tuple[int, int]) -> Dict[Tuple[int, int], Tuple[float, Tuple[int, int]]]:
        """
        Perform the Dijkstra algorithm to find the shortest path for the given player.
        
        Args:
            player (int): The player to find the shortest path for.
            start (Tuple[int, int]): The start position.
            
        Returns:
            Dict[Tuple[int, int], Tuple[float, Tuple[int, int]]]: The dictionary of positions and their distances and predecessors.
        """
        ends = []
        if player == 1:
            for k in range(self.size):
                if self.board[k][self.size-1] == player:
                    ends.append((k,self.size-1))
        else:
            for k in range(self.size):
                if self.board[self.size-1][k] == player:
                    ends.append((self.size-1,k))

        rows, cols = self.size, self.size
        visited = [[False] * cols for _ in range(rows)]
        distance = [[float('inf')] * cols for _ in range(rows)]
        previous = [[None] * cols for _ in range(rows)]

        distance[start[0]][start[1]] = 0
        heap = [(0, start)]

        while heap:
            current_dist, current_node = heapq.heappop(heap)

            if visited[current_node[0]][current_node[1]]:
                continue

            visited[current_node[0]][current_node[1]] = True

            neighbors = self.get_neighbors(current_node, rows, cols)
            for neighbor in neighbors:
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:  # Vérifier les limites du plateau
                    if not visited[neighbor[0]][neighbor[1]] and self.board[neighbor[0]][neighbor[1]] == player:
                        new_dist = distance[current_node[0]][current_node[1]] + 1
                        if new_dist < distance[neighbor[0]][neighbor[1]]:
                            distance[neighbor[0]][neighbor[1]] = new_dist
                            previous[neighbor[0]][neighbor[1]] = current_node
                            heapq.heappush(heap, (new_dist, neighbor))
        path = []
        for end in ends:
            if path == []:
                path = self.reconstruct_path( end, previous)
            else:
                temp = self.reconstruct_path( end, previous)
                if len(path) > len(temp) and len(temp) != 0:
                    path = temp
        return path


    def reconstruct_path(self, end: Tuple[int, int], previous: Dict[Tuple[int, int], Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Reconstruct the path from the end position using the previous dictionary.
        
        Args:
            end (Tuple[int, int]): The end position.
            previous (Dict[Tuple[int, int], Tuple[int, int]]): The dictionary of positions and their predecessors.
        
        Returns:
            List[Tuple[int, int]]: The reconstructed path.
        """
        path = []
        current_node = end
        while current_node:
            path.append(current_node)
            current_node = previous[current_node[0]][current_node[1]]
        if len(path[::-1]) == 1:
            return []
        return path[::-1]


    def shortest_path(self, player: int) -> List[Tuple[int, int]]:
        """
        Find the shortest path for the given player.

        Args:
            player (int): The player to find the shortest path for.

        Returns:
            List[Tuple[int, int]]: The shortest path.
        """
        path = []
        start = (0, 0)
        if player == 1:
            for k in range(self.size):
                #print("k",k)
                if self.board[k][0] == player:
                    start = (k, 0)
                    temp = self.dijkstra(player, start)
                    if path == []:
                        path = temp
                        #print("1er cas",start,path)
                    else:
                        if len(path) > len(temp) and len(temp) != 0:
                            path = temp
                            #print("2eme cas",start,path)

        if player == 2:
            for k in range(self.size):
                if self.board[0][k] == player:
                    start = (0, k)
                    temp = self.dijkstra(player, start)
                    if path == []:
                        path = temp
                    else:
                        if len(path) >= len(temp) and len(temp) != 0:
                            path = temp

        if path == []:
            return "error"
        return path


    def dijkstra_update(self, player: int, scores: np.ndarray, updated: np.ndarray) -> np.ndarray:
        """
        Update the Dijkstra scores for the given player.
        
        Args:
            player (int): The player to update the scores for.
            scores (np.ndarray): The array of scores.
            updated (np.ndarray): The array of updated positions.
            
        Returns:
            np.ndarray: The updated scores.
        """
        updating = True
        while updating: 
            updating = False
            for i, row in enumerate(scores): #go over rows
                for j, point in enumerate(row): #go over points 
                    if not updated[i][j]: 
                        neighborcoords = self.get_neighbors((i,j), self.size, self.size)
                        for neighborcoord in neighborcoords:
                            target_coord = tuple(neighborcoord)
                            path_cost = LOSE #1 for no color, 0 for same color, INF for other color 
                            if self.is_empty(target_coord):
                                path_cost = 1
                            elif self.is_player(target_coord, player):
                                path_cost = 0
                            
                            if scores[target_coord] > scores[i][j] + path_cost: #if new best path to this neighbor
                                scores[target_coord] = scores[i][j] + path_cost #update score
                                updated[target_coord] = False #This neighbor should be updated
                                updating = True #make sure next loop is started
        return scores


    def get_dijkstra_score(self, player: int) -> float:
        """
        Get the Dijkstra score for the given player.

        Args:
            player (int): The player to get the Dijkstra score for.

        Returns:
            float: The Dijkstra score.
        """
        scores = np.array([[LOSE for _ in range(self.size)] for _ in range(self.size)])
        updated = np.array([[True for _ in range(self.size)] for _ in range(self.size)]) #Start updating at one side of the board 

        #alignment of player (1 = left->right so (1,0))
        alignment = (0, 1) if player == 1 else (1, 0)


        for i in range(self.size):
            newcoord = tuple([i * j for j in alignment]) #iterate over last row or column based on alignment of current color

            updated[newcoord] = False
            if self.is_player(newcoord, player): #if same color --> path starts at 0
                scores[newcoord] = 0
            elif self.is_empty(newcoord): #if empty --> costs 1 move to use this path 
                scores[newcoord] = 1
            else: #If other color --> can't use this path
                scores[newcoord] = LOSE

        scores = self.dijkstra_update(player, scores, updated)

        results = [scores[alignment[0] * i - 1 + alignment[0]][alignment[1]*i - 1 + alignment[1]] for i in range(self.size)] #take "other side" to get the list of distance from end-end on board
        best_result = min(results)
        return best_result

    #time_limit = 2
    def minimax(self, player: int, depth: int, alpha: float, beta: float) -> Tuple[float, Tuple[int, int]]:
        """
        Perform the Minimax algorithm with alpha-beta pruning for the given player.

        Args:
            player (int): The player to perform the Minimax algorithm for.
            depth (int): The depth to search to.
            alpha (float): The alpha value for alpha-beta pruning.
            beta (float): The beta value for alpha-beta pruning.

        Returns:
            Tuple[float, Tuple[int, int]]: The result of the Minimax algorithm.
        """
        #start_time = time()
        #while time()-start_time < self.time_limit:

        if depth == 0 or self.check_winner() is not None:
            return self.eval(player)*((depth+1)*(depth+1)), None

        if player == 1:  # Maximizing player
            best_score = float('-inf')
            best_move = None
            possible_moves = self.get_possible_moves()
            for move in possible_moves:
                self.place_piece(player, move)
                #print(self.check_winner())
                #print(player ,move, self.minimax(depth - 1, 2, alpha, beta))
                score, _ = self.minimax(2, depth - 1, alpha, beta)
                self.undo_move(move)
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
            possible_moves = self.get_possible_moves()
            for move in possible_moves:
                self.place_piece(player, move)
                score, _ = self.minimax(1, depth - 1, alpha, beta)
                self.undo_move(move)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
            #print("min",best_score,best_move)
            return best_score, best_move


    def get_best_move(self, player: int, depth: int) -> Tuple[int, int]:
        """
        Get the best move for the given player using the Minimax algorithm.

        Args:
            player (int): The player to get the best move for.
            depth (int): The depth to search to.

        Returns:
            Tuple[int, int]: The best move.
        """
        a , best_move = self.minimax(depth, player, float('-inf'), float('inf'))
        print(a, best_move, player)
        return best_move


    def random_move(self) -> Tuple[int, int]:
        """
        Get a random move.

        Returns:
            Tuple[int, int]: The random move.
        """
        Trouve = False
        while(not Trouve):
            x = random.randint(1,self.size-2)
            y = random.randint(1,self.size-2)
            if not(self.is_position_occupied((x,y))):
                Trouve = True
                return (x,y)


    def eval_dijkstra(self, player: int) -> float:
        """
        Evaluate the board for the given player using the Dijkstra algorithm.

        Args:
            player (int): The player to evaluate the board for.

        Returns:
            float: The evaluation score.
        """
        if self.check_winner() == 1 : #winning move
            return 1000
        if self.check_winner() == 2 :
            return -1000
        return self.get_dijkstra_score(3-player)- self.get_dijkstra_score(player)


    def eval_test(self, player: int) -> float:
        """
        Test the evaluation function for the given player.

        Args:
            player (int): The player to test the evaluation function for.

        Returns:
            float: The test score.
        """
        center = (self.size//2,self.size//2)
        cv = self.get_neighbors(center,self.size,self.size)
        cv.append(center)
        player_1_score = 0
        player_2_score = 0

        if self.check_winner() == 1 :
            return 1000
        if self.check_winner() == 2 :
            return -1000
        
        if player == 1:
                components1 = self.find_connected_components(1)
                cpt = 0
                for co in components1:
                    M1 = max(co, key=lambda x: x[1])
                    m1 = min(co, key=lambda x: x[1])
                    s1 =  M1[1] - m1[1]
                    cpt = cpt + s1*5
                    t = []
                    for d in co :
                        if d in cv:
                            cpt += 2
                        if d[1] not in t:
                            t.append(d[1])
                            cpt = cpt+1
                        if d[1] == M1[1] or d[1] == M1[1] and d[1] != 0 and d[1] != self.size:
                            cpt = cpt + 1
                player_1_score += (cpt)
                player_1_score = player_1_score//len(components1)
                player_1_score += self.get_dijkstra_score(2)- self.get_dijkstra_score(1)
                return (player_1_score)
        if player == 2:
                components2 = self.find_connected_components(2)
                cpt = 0
                for co in components2:
                    M2 = max(co, key=lambda x: x[0])
                    m2 = min(co, key=lambda x: x[0])
                    s2 =  M2[0] - m2[0]
                    cpt = cpt + s2*5
                    for d in co :
                        if d in cv:
                            cpt += 2
                        if d[0] == M2[0] or d[0] == M2[0]:
                            cpt = cpt + 1
                player_2_score += (cpt)
                player_2_score = player_2_score//len(components2)
                player_2_score += self.get_dijkstra_score(1)- self.get_dijkstra_score(2)
                return (-player_2_score)


    def eval(self, player: int) -> float:
        """
        Evaluate the board for the given player.

        Args:
            player (int): The player to evaluate the board for.

        Returns:
            float: The evaluation score.
        """
        center = (self.size//2,self.size//2)
        cv = self.get_neighbors(center,self.size,self.size)
        cv.append(center)
        player_1_score = 0
        player_2_score = 0
        
        if self.check_winner() == 1 : #winning move
            return 1000
        if self.check_winner() == 2 : #blocking losing move
            return -1000
        
        if player == 1:
            components1 = self.find_connected_components(1)
            #print(components1)
            if len(components1) == 1:
                    if len(components1[0]) == 1:
                        print(components1[0])

            cpt = 0
            for co in components1:

                M1 = max(co, key=lambda x: x[1])
                m1 = min(co, key=lambda x: x[1])
                s1 =  M1[1] - m1[1]
                cpt = cpt + s1*5
                t = []
                for d in co :
                    if d in cv:
                        cpt += 2
                    if d[1] not in t:
                        t.append(d[1])
                        cpt = cpt+1
                    if d[1] == M1[1] or d[1] == M1[1] and d[1] != 0 and d[1] != self.size:
                        cpt = cpt + 1
            player_1_score += (cpt)
            player_1_score = player_1_score//len(components1)
            return (player_1_score) 

        else:
            components2 = self.find_connected_components(2)
            cpt = 0
            for co in components2:
                M2 = max(co, key=lambda x: x[0])
                m2 = min(co, key=lambda x: x[0])
                s2 =  M2[0] - m2[0]
                cpt = cpt + s2*5
                for d in co :
                    if d in cv:
                        cpt += 2
                    if d[0] == M2[0] or d[0] == M2[0]:
                        cpt = cpt + 1
            player_2_score += (cpt)
            player_2_score = player_2_score//len(components2)
            return (-player_2_score)


    def naif(self, player: int) -> Tuple[int, int]:
        """
        Get a naive move for the given player.

        Args:
            player (int): The player to get a naive move for.

        Returns:
            Tuple[int, int]: The naive move.
        """
        if self.check_winner() == 1 : #winning move
                return 1000
        if self.check_winner() == 2 : #blocking losing move
            return -1000
        voisins1 = []
        voisins2 = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    vs = self.get_neighbors((i, j), self.size, self.size)
                    for v in vs :
                        if self.board[v[0]][v[1]] != 0:
                            vs.remove(v)
                    voisins1.append(vs)
                if self.board[i][j] == 2:
                    vs = self.get_neighbors((i, j), self.size, self.size)
                    for v in vs :
                        if self.board[v[0]][v[1]] != 0:
                            vs.remove(v)
                    voisins2.append(vs)
        count1 = 0
        count2 = 0
        for v1 in voisins1:
            count1 += voisins1.count(v1)
        
        for v2 in voisins2:
            count2 += voisins1.count(v2)
        print(voisins1, voisins2)
        player_1_score = count1
        player_2_score = count2
        if player == 1:
                return -(player_1_score - player_2_score) 
        if player == 2:
                return (player_1_score - player_2_score)
    
    #C'est une fonction d'evaluation utilisant le tattonement 
    def evaluate_1(self, player: int) -> float:
        """
        Evaluate the board for the given player using the first evaluation function.

        Args:
            player (int): The player to evaluate the board for.

        Returns:
            float: The evaluation score.
        """
        player_1_score = 0
        player_2_score = 0

        if self.check_winner() == 1:
            return 1000
        if self.check_winner() == 2:
            return -1000

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    voisins = self.get_neighbors((i, j), self.size, self.size)
                    connected_pieces = 0
                    for v in voisins:
                        if self.board[v[0]][v[1]] == 1:
                            player_1_score += 2 
                            connected_pieces += 1
                    player_1_score += min(i, j, self.size - i, self.size - j)
                    player_1_score += connected_pieces ** 2
                elif self.board[i][j] == 2:
                    voisins = self.get_neighbors((i, j), self.size, self.size)
                    connected_pieces = 0
                    for v in voisins:
                        if self.board[v[0]][v[1]] == 2:
                            player_2_score += 2
                            connected_pieces += 1
                    player_2_score += min(i, j, self.size - i, self.size - j)
                    player_2_score += connected_pieces ** 2

        # Check if there's a potential winning move
        if player == 1:
            if self.is_potential_winner(player, (0, 0)):  # Assuming player 1 starts from the top-left corner
                return 1000  # A high score to prioritize the winning move
        else:
            if self.is_potential_winner(player, (0, 0)):  # Assuming player 2 starts from the top-left corner
                return -1000  # A high negative score to prioritize blocking the opponent's winning move

        # Add points if the shortest path of the opposite player is longer
        if player == 1:
            player_1_score += self.get_dijkstra_score(1)  # or some other value
        else:
            player_2_score += self.get_dijkstra_score(2) # or some other value

        score_difference = (player_1_score - player_2_score) 
        return player_1_score if player == 1 else player_2_score


    def aleatoire(self) -> Tuple[int, int]:
        """
        Get a random move.

        Returns:
            Tuple[int, int]: The random move.
        """
        if self.check_winner() == 1 :
            return 1000
        if self.check_winner() == 2 :
            return -1000
        return random.randint(-100,100)


    def getWinFactor(self, player: int) -> float:
        """
        Get the win factor for the given player.

        Args:
            player (int): The player to get the win factor for.

        Returns:
            float: The win factor.
        """
        cnt=0
        winPath = self.get_winning_path(player)
        for i in range(self.size):
            for j in range(self.size):
                if (i,j) in winPath:
                    cnt+=1
        return cnt/len(winPath)*100


    def getPathFactor(self, player: int) -> float:
        """
        Get the path factor for the given player.

        Args:
            player (int): The player to get the path factor for.

        Returns:
            float: The path factor.
        """
        score=0
        path=[]
        if (player == 1):
            for i in range(self.size):
                for j in range (self.size):
                    if (self.board[i][j] == 1):
                        path = self.dijkstra(1, (i,j))
                        score += 1
        else:
            for i in range(self.size):
                for j in range (self.size):
                    if (self.board[j][i] == 2):
                        path = self.dijkstra(2, (j,i))
                        score += 1
        return score/(self.size*self.size)*100


    def getAdjFactor(self, player: int) -> float:
        """
        Get the adjacency factor for the given player.

        Args:
            player (int): The player to get the adjacency factor for.

        Returns:
            float: The adjacency factor.
        """
        score=0
        if (player == 1):
            for i in range(self.size):
                for j in range (self.size):
                    if (self.board[i][j] == 1):
                        voisins = self.get_neighbors((i,j), self.size, self.size)
                        for v in voisins:
                            if (self.board[v[0]][v[1]] == 1):
                                score += 1
        else:
            for i in range(self.size):
                for j in range (self.size):
                    if (self.board[j][i] == 2):
                        voisins = self.get_neighbors((j,i), self.size, self.size)
                        for v in voisins:
                            if (self.board[v[0]][v[1]] == 2):
                                score += 1
        return score/(self.size*self.size)*100


    def getScore(self, player: int) -> float:
        """
        Get the score for the given player.

        Args:
            player (int): The player to get the score for.

        Returns:
            float: The score.
        """
        if self.check_winner() == player:
            return 1000
        return max (self.getWinFactor(player), self.getPathFactor(player) ,self.getAdjFactor(player))