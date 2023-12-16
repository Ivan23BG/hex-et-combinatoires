# HexGame/board/hex_board.py
class HexBoard:
    def __init__(self, size):
        # Initialisation du plateau de jeu
        self.size = size
        self.board = [[0] * size for _ in range(size)]

    def place_piece(self, player, position):
        # Logique pour placer une pièce sur le plateau
        row, col = position
        self.board[row][col] = player

    def check_winner(self):
        # Vérifie s'il y a un gagnant
        # On considère deux côtés opposés comme les côtés supérieur et inférieur pour le joueur 1,
        # et les côtés gauche et droit pour le joueur 2
        player_1_side = [(i, 0) for i in range(self.size)]  # Côté supérieur
        player_2_side = [(0, j) for j in range(self.size)]  # Côté gauche

        # On vérifie la connexion du côté supérieur au côté inférieur pour le joueur 1
        if any(self._dfs_connected(player_1_side, (i, 0), set()) for i in range(self.size)):
            return 1  # Le joueur 1 a gagné

        # On vérifie la connexion du côté gauche au côté droit pour le joueur 2
        if any(self._dfs_connected(player_2_side, (0, j), set()) for j in range(self.size)):
            return 2  # Le joueur 2 a gagné

        # Aucun gagnant n'a été trouvé
        return 0

    def _dfs_connected(self, side, current, visited):
        # Fonction DFS pour vérifier la connexion entre deux côtés
        i, j = current
        visited.add(current)

        if current in side:
            return True

        neighbors = self._get_neighbors(i, j)
        connected = any(neighbor not in visited and self.board[neighbor[0]][neighbor[1]] == self.board[i][j] and
                        self._dfs_connected(side, neighbor, visited)
                        for neighbor in neighbors)
        return connected

    def _get_neighbors(self, i, j):
        # Renvoie les voisins valides d'une cellule
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1), (i - 1, j + 1), (i + 1, j - 1)]
        return [(ni, nj) for ni, nj in neighbors if 0 <= ni < self.size and 0 <= nj < self.size]

    def display_board(self):
        # Display the board
        for i in range(self.size):
            print(" ---" * self.size)
            print("| ", end="")
            for j in range(self.size):
                if self.board[i][j] == 1:
                    print("X", end=" | ")
                elif self.board[i][j] == 2:
                    print("O", end=" | ")
                else:
                    print(" ", end=" | ")
            print()
        print(" ---" * self.size)
# Exemple d'utilisation
size = 4
game_board = HexBoard(size)
game_board.display_board()
game_board.place_piece(1, (0, 0))
game_board.place_piece(1, (1, 1))
game_board.place_piece(1, (2, 2))
game_board.place_piece(1, (3, 3))
game_board.display_board()
game_board.place_piece(2, (0, 1))
game_board.place_piece(2, (1, 2))
game_board.place_piece(2, (2, 3))
game_board.place_piece(2, (3, 0))
game_board.display_board()
winner = game_board.check_winner()
print("Le joueur", winner, "a gagné.")