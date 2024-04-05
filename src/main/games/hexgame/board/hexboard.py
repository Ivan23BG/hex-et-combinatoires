
from collections import deque
import heapq
import random
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

    def dijkstra(self, player, start):
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

    def get_neighbors(self, node, rows, cols):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]
        for dir in directions:
            neighbor_row, neighbor_col = node[0] + dir[0], node[1] + dir[1]
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
        return neighbors

    def reconstruct_path(self, end, previous):
        path = []
        current_node = end
        while current_node:
            path.append(current_node)
            current_node = previous[current_node[0]][current_node[1]]
        if len(path[::-1]) == 1:
            return []
        return path[::-1]

    def shortest_path(self, player):
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
    
    def find_chains(self, player):
        """
        Find all the chains of the current player on the board.

        Args:
            player (int): The player value (1 or 2).

        Returns:
            list: The list of chains, where each chain is a list of positions.
        """
        chains = []
        visited = set()
        for row in range(self.size):
            for col in range(self.size):
                position = (row, col)
                if self.board[row][col] == player and position not in visited:
                    chain = self.dfs(position, player, visited)
                    chains.append(chain)
        return chains

    def dfs(self, position, player, visited):
        """
        Depth-first search to find a chain of the current player.

        Args:
            position (tuple): The starting position.
            player (int): The player value (1 or 2).
            visited (set): The set of visited positions.

        Returns:
            list: The chain of positions.
        """
        chain = []
        stack = [position]
        while stack:
            current_position = stack.pop()
            chain.append(current_position)
            visited.add(current_position)
            neighbors = self.get_neighbors((current_position[0], current_position[1]), self.size, self.size)
            for neighbor in neighbors:
                if self.board[neighbor[0]][neighbor[1]] == player and neighbor not in visited:
                    stack.append(neighbor)
        return chain 
    
    def is_winning_path(self, path, player):
        # Check if the path is empty
        if not path:
            return False

        # Check if the path belongs to the player
        for i, j in path:
            if self.board[i][j] != player:
                return False

        # Check if the path connects the two sides of the board
        if player == 1:
            # Player 1 wins by connecting the top and bottom sides
            cols = [j for i, j in path]
            return min(cols) == 0 and max(cols) == self.size - 1
        else:
            # Player 2 wins by connecting the left and right sides
            rows = [i for i, j in path]
            return min(rows) == 0 and max(rows) == self.size - 1
        
    def is_potential_winner(self, player, position):
        """
        Check if placing a piece at the given position could potentially lead to a win for the player.

        Args:
            player (int): The player value (1 or 2).
            position (tuple): The position to check.

        Returns:
            bool: True if the position could lead to a win, False otherwise.
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
    
    def evaluate_voisins(self):

        """
        Elle prend en compte la connectivité des pieces:
            - si une piece est connectée à une autre piece de la meme couleur, on augmente le score
            - on fait la difference des scores des deux joueurs
        """

        # Initialize scores
        player_1_score = 0
        player_2_score = 0
        # Evaluate the board for both players
        for i in range(self.size):
            for j in range(self.size):
                voisins = self.get_neighbors((i,j), self.size, self.size)
                if self.board[i][j] == 1: 
                    for v in voisins:
                        if self.board[v[0]][v[1]] == 1:
                            player_1_score += 1
                elif self.board[i][j] == 2:
                    for v in voisins:
                        if self.board[v[0]][v[1]] == 2:
                            player_2_score += 1

        # Calculate the difference in scores
        score_difference = player_1_score - player_2_score
        return score_difference
    
    def evaluate_proxi_edge(self, player):
        """
        Une fonction d'évaluation qui prend en compte la proximité des pieces par rapport aux bords du plateau.
        """
        player_1_score = 0
        player_2_score = 0

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    player_1_score += (self.size - j)
                elif self.board[i][j] == 2:
                    player_2_score += (self.size - i)

        score_difference = player_1_score - player_2_score

        return score_difference if player == 1 else -score_difference
    
    def evaluate_1(self, player):
        """
        J'essaide mettre en consideration les 2 arguments precedents
        """
        player_1_score = 0
        player_2_score = 0

        # Evaluate the board for both players
        for i in range(self.size):
            for j in range(self.size):
                voisins = self.get_neighbors((i,j), self.size, self.size)
                if self.board[i][j] == 1: 
                    # Increase score based on the number of neighboring pieces for player 1
                    for v in voisins:
                        if self.board[v[0]][v[1]] == 1:
                            player_1_score += 1
                    # Increase score based on proximity to the right edge for player 1
                    player_1_score += (self.size - j)
                elif self.board[i][j] == 2:
                    # Increase score based on the number of neighboring pieces for player 2
                    for v in voisins:
                        if self.board[v[0]][v[1]] == 2:
                            player_2_score += 1
                    # Increase score based on proximity to the bottom edge for player 2
                    player_2_score += (self.size - i)

        # Calculate the difference in scores
        score_difference = (player_1_score - player_2_score)/max(player_2_score, player)

        # Return the score difference from the perspective of the current player
        return score_difference if player == 1 else -score_difference
        
    def evaluate_2(self, player):
        player_1_score = 0
        player_2_score = 0

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    # Increase score based on the number of neighboring pieces for player 1
                    voisins = self.get_neighbors((i, j), self.size, self.size)
                    connected_pieces = 0
                    for v in voisins:
                        if self.board[v[0]][v[1]] == 1:
                            player_1_score += 1
                            connected_pieces += 1
                    # Increase score based on proximity to the borders for player 1
                    player_1_score += min(i, j, self.size - i, self.size - j)
                    # Increase score based on the connectivity of the chains for player 1
                    player_1_score += connected_pieces ** 2  # or some other function of connected_pieces
                elif self.board[i][j] == 2:
                    # Increase score based on the number of neighboring pieces for player 2
                    voisins = self.get_neighbors((i, j), self.size, self.size)
                    connected_pieces = 0
                    for v in voisins:
                        if self.board[v[0]][v[1]] == 2:
                            player_2_score += 1
                            connected_pieces += 1
                    # Increase score based on proximity to the borders for player 2
                    player_2_score += min(i, j, self.size - i, self.size - j)
                    # Increase score based on the connectivity of the chains for player 2
                    player_2_score += connected_pieces ** 2  # or some other function of connected_pieces

        score_difference = (player_1_score - player_2_score) 
        # Return the score difference from the perspective of the current player
        return score_difference if player == 1 else -score_difference
    
    def evaluate_3(self, player):
        # Use the same criteria as evaluate_2
        # Mon probleme avec cette fonction est que il bloque pas mal l'adversaire 
        # mais il sait pas gangner.
        player_1_score = 0
        player_2_score = 0

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

        # Add points if the shortest path of the opposite player is longer
        if player == 1:
            shortest_path_2 = self.shortest_path(2)
            if shortest_path_2 != "error":
                player_1_score += len(shortest_path_2)
            else:
                player_1_score += 0  # or some other value
        else:
            shortest_path_1 = self.shortest_path(1)
            if shortest_path_1 != "error":
                player_2_score += len(shortest_path_1)
            else:
                player_2_score += 0  # or some other value

        score_difference = (player_1_score - player_2_score)/max(player_2_score, player_1_score)
        return score_difference if player == 1 else -score_difference
    
    def evaluate_hex(self, player):
        player_1_score = 0
        player_2_score = 0

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
            shortest_path_2 = self.shortest_path(2)
            if shortest_path_2 != "error":
                player_1_score += len(shortest_path_2)
            else:
                player_1_score += 0  # or some other value
        else:
            shortest_path_1 = self.shortest_path(1)
            if shortest_path_1 != "error":
                player_2_score += len(shortest_path_1)
            else:
                player_2_score += 0  # or some other value

        score_difference = (player_1_score - player_2_score) 
        return score_difference if player == 1 else -score_difference
    
    def get_dijkstra_score(self, player, start):
        ends = []
        if player == 1:
            for k in range(self.size):
                if self.board[k][self.size-1] == player:
                    ends.append((k,self.size-1))
        else:
            for k in range(self.size):
                if self.board[self.size-1][k] == player:
                    ends.append((self.size-1,k))

        if not ends:  # Check if ends list is empty
            return float('inf') if player == 1 else float('-inf')  # Return infinity for player 1, negative infinity for player 2

        rows, cols = self.size, self.size
        visited = [[False] * cols for _ in range(rows)]
        distance = [[float('inf')] * cols for _ in range(rows)]

        distance[start[0]][start[1]] = 0
        heap = [(0, start)]

        while heap:
            current_dist, current_node = heapq.heappop(heap)

            if visited[current_node[0]][current_node[1]]:
                continue

            visited[current_node[0]][current_node[1]] = True

            neighbors = self.get_neighbors(current_node, rows, cols)
            for neighbor in neighbors:
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:  # Check board boundaries
                    if not visited[neighbor[0]][neighbor[1]] and self.board[neighbor[0]][neighbor[1]] == player:
                        new_dist = distance[current_node[0]][current_node[1]] + 1
                        if new_dist < distance[neighbor[0]][neighbor[1]]:
                            distance[neighbor[0]][neighbor[1]] = new_dist
                            heapq.heappush(heap, (new_dist, neighbor))

        min_distance = min(distance[end[0]][end[1]] for end in ends)
        
        return min_distance if min_distance != float('inf') else 0


    def evaluate_4(self, player):
        """
        Evaluate the current state of the board based on the minimum number of moves required to connect the two sides of the board.
        """
        # Calculate the dijkstra score for the current player
        start = (0, 0) if player == 1 else (self.size - 1, self.size - 1)
        dijkstra_score = self.get_dijkstra_score(player, start)
        
        # Calculate the dijkstra score for the opponent player
        opponent = 2 if player == 1 else 1
        opponent_start = (0, 0) if opponent == 1 else (self.size - 1, self.size - 1)
        opponent_dijkstra_score = self.get_dijkstra_score(opponent, opponent_start)
        
        # Calculate the score difference
        score_difference = dijkstra_score - opponent_dijkstra_score
        
        # Return the score difference from the perspective of the current player
        return score_difference if player == 1 else -score_difference
    

    def minimax(self, depth, player, alpha, beta):
        if depth == 0 or self.check_winner() is not None:
            return self.evaluate_4(player), None

        if player == 1:  # Maximizing player
            best_score = float('-inf')
            best_move = None
            possible_moves = self.get_possible_moves()
            for move in possible_moves:
                self.place_piece(player, move)
                score, _ = self.minimax(depth - 1, 2, alpha, beta)
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
                score, _ = self.minimax(depth - 1, 1, alpha, beta)
                self.undo_move(move)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
            return best_score, best_move
        
    def get_best_move(self, depth, player):
        best_score = float('-inf')
        best_move = None

        # iterate over all empty positions on the board
        for move in self.get_empty_cells():
            # simulate making the move
            self.place_piece(player, move)
            # calculate the score for this move using minimax with alpha-beta pruning
            score, _ = self.minimax(depth - 1, player, float('-inf'), float('inf'))
            # undo the move
            self.undo_move(move)
            # update the best move if this move has a higher score
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
    
    def get_empty_cells(self):
        """
        Get all the empty cells on the board.
        """
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells
