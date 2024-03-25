# app.py
# Imports
from flask import Flask, render_template, request
from board.hexboard import HexBoard
#from awelegame.board.aweleboard import AweleBoard
from flask import jsonify


# Global variables
app = Flask(__name__)
game_board = None
current_player = 1
size = 5
size_px = size


@app.route('/') # Home page
def index():
    return render_template('home.html')

@app.route('/home_hex') # Hex options page
def home_hex():
    return render_template('home_hex.html')

@app.route('/home_awale') # Hex options page
def home_awale():
    return render_template('home_awale.html')

@app.route('/game_awale') # Hex options page
def game_awale():
    return render_template('game_awale.html')


@app.route('/game_hex', methods=['POST']) # Hex play page
def game_hex():
    global game_board, current_player, size_px, size
    size = int(request.form['size'])
    size_px = 120 + (44 * size)  # update the size_px used in the play.html
    game_board = HexBoard(size)  # Create a new game board
    game_board.display_board()  # Display the game board in the console
    current_player = 1  # Set player 1 as the starting player
    return render_template('game_hex.html', size=size, size_px=size_px, current_player=current_player)


@app.route('/hex_place_piece', methods=['POST']) # Place a piece on the board
def hex_place_piece():
    global game_board, current_player
    
    data = request.get_json()
    hexid = data['hexid']
    current_player = data['current_player']
    
    # Remove the "hex" prefix and split into row and column
    row, col = map(int, hexid[3:].split('-'))

    # change the current player
    try:
        if game_board is not None:
            game_board.place_piece(current_player, (row, col)) # Try to place the piece
            game_board.display_board() # Display the game board in the console
            
            # check if the current player won
            winner = game_board.check_winner()
            if winner:
                short_path = game_board.shortest_path(current_player)
                print(f"Shortest path for player {current_player}: {short_path}")
                hexid = [f"hex{i[0]}-{i[1]}" for i in short_path]
                return jsonify({'winner': current_player, 'game_over': True, 'current_player': current_player,'hexid':hexid})
            current_player = 1 if current_player == 2 else 2
    except Exception as e:
        # Handle the exception here
        error_message = str(e)  # Get the error message
        return jsonify({'error': error_message}), 400

    return jsonify({'result': 'Success', 'current_player': current_player})

@app.route('/undo_move', methods=['POST']) # Place a piece on the board
def undo_move():
    global game_board, current_player
    
    data = request.get_json()
    hexid = data['hexid']
    current_player = data['current_player']
    
    
    # Remove the "hex" prefix and split into row and column
    row, col = map(int, hexid[3:].split('-'))

    # change the current player
    try:
        if game_board is not None:
            game_board.undo_move(row,col)
            game_board.display_board()
            current_player = 1 if current_player == 2 else 2


    except Exception as e:
        # Handle the exception here
        error_message = str(e)  # Get the error message
        return jsonify({'error': error_message}), 400

    return jsonify({'result': 'Success', 'current_player': current_player})



if __name__ == '__main__':
    app.run(debug=True)
