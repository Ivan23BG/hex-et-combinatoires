# app.py
# Imports
from flask import Flask, render_template, request, jsonify
from game_logic.hexgame.board.hexboard import HexBoard
from game_logic.awalegame.board.awaleboard import AwaleBoard


# Global variables
app = Flask(__name__, template_folder='game_ui/templates', static_folder='game_ui/static')
game_board = None
current_player = 1
size = 5
size_px = size

# Player vs IA variables
player = 0
IA = 0

# IA vs IA variables
IA1 = 1
IA2 = 2
current_IA = 1


@app.route('/') # Home page
def index():
    return render_template('home.html')


@app.route('/home_hex') # Hex options page
def home_hex():
    return render_template('home_hex.html')


@app.route('/home_awale') # Hex options page
def home_awale():
    return render_template('home_awale.html')


@app.route('/game_hex', methods=['POST']) # Hex play page
def game_hex():
    global game_board, current_player, size_px, size
    size = int(request.form['size'])
    size_px = 120 + (44 * size)  # update the size_px used in the play.html
    game_board = HexBoard(size)  # Create a new game board
    game_board.display_board()  # Display the game board in the console
    current_player = 1  # Set player 1 as the starting player
    return render_template('game_hex.html', size=size, size_px=size_px, current_player=current_player)


@app.route('/game_hexia', methods=['POST']) # Hex play page
def game_hexia():
    global game_board, current_player, size_px, size, player, IA
    player = int(request.form['player'])
    IA = 3 - player
    print(player)
    print(IA)   
    size = int(request.form['size'])
    size_px = 120 + (44 * size)  # update the size_px used in the play.html
    game_board = HexBoard(size)  # Create a new game board
    game_board.display_board()  # Display the game board in the console
    
    return render_template('game_hexia.html', size=size, size_px=size_px)


@app.route('/game_hexiaia', methods=['POST']) # Hex play page
def game_hexiaia():
    global game_board, size_px, size
    size = int(request.form['size'])
    size_px = 120 + (44 * size)  # update the size_px used in the play.html
    game_board = HexBoard(size)  # Create a new game board
    game_board.display_board()  # Display the game board in the console
    return render_template('game_hexiaia.html', size=size, size_px=size_px)


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
        game_board.display_board() # Display the game board in the console
        print("error: ",error_message)
        return jsonify({'error': "An error has occured"}), 400

    return jsonify({'result': 'Success', 'current_player': current_player})


# @app.route('/hex_place_piece_ia', methods=['POST']) # Place a piece on the board
# def hex_place_piece_ia():
#     global game_board, player, IA 
    
#     data = request.get_json()
#     hexid = data['hexid']
    
#     # Remove the "hex" prefix and split into row and column
#     row, col = map(int, hexid[3:].split('-'))

    
#     try:
#         if game_board is not None:
#             game_board.place_piece(player, (row, col)) # Try to place the piece
            
#             # check if the current player won
#             winner = game_board.check_winner()
#             if winner:
#                 short_path = game_board.shortest_path(player)
#                 print(f"Shortest path for player {player}: {short_path}")
#                 hexid = [f"hex{i[0]}-{i[1]}" for i in short_path]
#                 return jsonify({'winner': player, 'game_over_player': True,'hexid':hexid})
            

#             #IA's turn
#             IA = 3 - player
#             # make a move using minimax algorithm and get_best_move method (actualy random move)
#             move = game_board.get_best_move(2,IA)
#             game_board.place_piece(IA, move)
            
            
#             iamove = "hex" + str(move[0]) + "-" + str(move[1])

#             # check if IA won
#             winner = game_board.check_winner()
#             if winner:
#                 short_path = game_board.shortest_path(IA)
#                 print(f"Shortest path for player {IA}: {short_path}")
#                 hexid = [f"hex{i[0]}-{i[1]}" for i in short_path]
#                 return jsonify({'winner': IA, 'game_over_IA': True,'hexid':hexid,'iamove':iamove})
            
#     except Exception as e:
#         # Handle the exception here
#         error_message = str(e)  # Get the error message
#         game_board.display_board()
#         print("error: ",error_message)
#         return jsonify({'error': "An error has occured"}), 400
        

#     return jsonify({'result': 'Success','iamove': iamove})


@app.route('/hexiaia_place_piece', methods=['POST']) # Place a unique piece on the board
def hexiaia_place_piece():
    global game_board, current_IA

    data = request.get_json()
    current_IA = data['current_IA']

    try:
        if game_board is not None:

            move_IA = game_board.get_best_move(2,current_IA)
            game_board.place_piece(current_IA, move_IA) # Try to place the piece
            iamove = "hex" + str(move_IA[0]) + "-" + str(move_IA[1])
            
            # check if current_IA won
            winner = game_board.check_winner()
            if winner:
                short_path = game_board.shortest_path(current_IA)
                print(f"Shortest path for player {current_IA}: {short_path}")
                hexid = [f"hex{i[0]}-{i[1]}" for i in short_path]
                return jsonify({'winner': current_IA, 'game_over': True,'hexid':hexid,'iamove':iamove})
            
    except Exception as e:
        # Handle the exception here
        error_message = str(e)  # Get the error message
        game_board.display_board()
        print("error: ",error_message)
        return jsonify({'error': "An error has occured"}), 400
        

    return jsonify({'result': 'Success','iamove': iamove,'game_over': False})


@app.route('/players_hexia', methods=['POST']) # Return player's and IA's values
def players_hexia():
    global player, IA
    return jsonify({'result': 'Success','player': player,'IA':IA})


@app.route('/first_move_IA',methods=['POST']) #Return IA's first move if player=2
def first_move_IA():
    global game_board, IA 
    move = game_board.get_best_move(3,IA)    
    game_board.place_piece(IA, move)
    iamove = "hex" + str(move[0]) + "-" + str(move[1])
    return jsonify({'result': 'Success','iamove':iamove})


@app.route('/undo_move', methods=['POST']) # Undo last move on the board
def undo_move():
    global game_board
    
    data = request.get_json()
    hexid = data['hexid']
    
    
    # Remove the "hex" prefix and split into row and column
    row, col = map(int, hexid[3:].split('-'))

    # Remove the hex in board
    try:
        if game_board is not None:
            game_board.undo_move((row,col))


    except Exception as e:
        # Handle the exception here
        error_message = str(e)  # Get the error message
        game_board.display_board()

        print("error: ",error_message)
        return jsonify({'error': "An error has occured"}), 400

    return jsonify({'result': 'Success'})


@app.route('/game_awale', methods=['POST']) # Hex play page
def game_awale():
    global game_board, current_player
    game_board = AwaleBoard()  # Create a new game board
    game_board.display_board()  # Display the game board in the console
    current_player = 1  # Set player 1 as the starting player
    return render_template('game_awale.html',current_player=current_player)


@app.route('/awale_place_piece', methods=['POST']) # Place a piece on the board
def awale_place_piece():
    global game_board, current_player
    
    data = request.get_json()
    pitid = data['pitid']
    current_player = data['current_player']
    id = int(pitid)
    
    if game_board is not None:
        try:
            game_board.make_move(id, current_player) # Try to place the piece
            scores = game_board.get_scores()
            game_board.display_board() # Display the game board in the console
            values = game_board.get_board()
            #print("values",values)
            winner = game_board.game_over()
            if winner:
                winner = 2 - (game_board.score_1 > game_board.score_2)
                return jsonify({'winner': current_player, 'game_over': True, 'current_player': current_player,'pitid':pitid})
            current_player = 1 if current_player == 2 else 2
        except Exception as e:
            # Handle the exception here
            error_message = str(e)  # Get the error message
            print("error: ",error_message)
            return jsonify({'error': "An error has occured"}), 400
    return jsonify({'result': 'Success', 'current_player': current_player,'values':values,'score_1':scores[0],'score_2':scores[1]})


if __name__ == '__main__':
    app.run(debug=True)
