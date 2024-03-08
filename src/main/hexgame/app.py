# app.py
# import flask
# trouver comment importer des images
from flask import Flask, render_template, request

# import the HexBoard class from hexboard.py
from board.hexboard import HexBoard
from flask import jsonify

app = Flask(__name__)

# create a global variable to store the game board
game_board = None
current_player = 1
size = 5
size_px = size


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home_hex')
def home_hex():
    return render_template('home_hex.html')

# handle the load game request
@app.route('/load_game', methods=['POST'])
def init_board():
    global game_board, current_player, size_px, size
    size = int(request.form['size'])
    size_px = 120 + (44 * size)  # update the size_px used in the play.html
    game_board = HexBoard(size)  # Create a new game board
    game_board.display_board()  # Display the game board in the console
    current_player = 1  # Set player 1 as the starting player
    return render_template('play.html', size=size, size_px=size_px, current_player=current_player)


# handle the reload game request
@app.route('/reload_game', methods=['POST'])
def reload_board():
    global game_board, current_player, size_px, size
    data = request.get_json()
    size = data['size']
    size_px = size  # update the size_px used in the play.html
    game_board = HexBoard(size)  # Create a new game board
    print("Game board reinitialized")
    game_board.display_board()
    current_player = 1  # Set player 1 as the starting player
    print("Current player: ", current_player)
    return jsonify({'size': size, 'size_px': size_px, 'current_player': current_player})


# handle the place piece request
@app.route('/place_piece', methods=['POST'])
def place_piece():
    global game_board, current_player
    data = request.get_json()
    hexid = data['hexid']
    current_player = data['current_player']
    

    # Remove the "hex" prefix and split into row and column
    row, col = map(int, hexid[3:].split('-'))

    # change the current player
    try:
        if game_board is not None:
            game_board.place_piece(current_player, (row, col))
            temp = current_player
            current_player = 1 if current_player == 2 else 2
            game_board.display_board()
            print("Current player: ", current_player)
            # check if the current player won
            winner = game_board.check_winner()
            if winner:
                short_path = game_board.shortest_path(temp)
                print("chemin le plus court :" ,short_path)
                return jsonify({'winner': current_player, 'game_over': True, 'current_player': current_player})
    except Exception as e:
        # Handle the exception here
        error_message = str(e)  # Get the error message
        return jsonify({'error': error_message}), 400

    return jsonify({'result': 'Success', 'current_player': current_player})


# necessary for to handle the error play return
@app.route('/place_piece', methods=['GET'])
def get_place_piece():
    return render_template('play.html', size=size, size_px=size_px, current_player=current_player)


if __name__ == '__main__':
    app.run(debug=True)
