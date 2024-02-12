# app.py
# import flask
from flask import Flask, render_template, request, redirect

# import the HexBoard class from hexboard.py
from board.hexboard import HexBoard

app = Flask(__name__)

# create a global variable to store the game board
game_board = None
current_player = 1
size = 0

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/init_board', methods=['POST'])
def init_board():
    global game_board, current_player, size
    size = int(request.form['size'])
    game_board = HexBoard(size)
    game_board.display_board()
    current_player = 1  # Set player 1 as the starting player
    return render_template('play.html', size=size)


# handle the place piece request
@app.route('/place_piece', methods=['POST'])
def place_piece():
    global game_board, current_player
    row = int(request.form['row']) - 1
    col = int(request.form['col']) - 1
    # change the current player
    try:
        if game_board is not None:
            game_board.place_piece(current_player, (row, col))
            current_player = 1 if current_player == 2 else 2
            game_board.display_board()
            # check if the current player won
            winner = game_board.check_winner()
            if winner:
                return render_template('winner.html', winner=winner)
    except Exception as e:
        # Handle the exception here
        error_message = str(e)  # Get the error message
        return render_template('error.html', error_message=error_message)
    return render_template('play.html', size=size)


# necessary for to handle the error play return
@app.route('/place_piece', methods=['GET'])
def get_place_piece():
    return render_template('play.html', size=size)


if __name__ == '__main__':
    app.run(debug=True)

