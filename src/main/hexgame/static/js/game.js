window.onload = function() {
    let current_player = 1; // Player 1 starts the game
    let game_over = false;

    const reset_button = document.getElementById('reset_button');
    const undo_button = document.getElementById('undo_button');

    const game_history = []; // Store the game state before each move
    const cells = document.querySelectorAll('.hex'); // Get all hex cells

    


    cells.forEach(hex => {
        // Add initial hover class
        hex.classList.add('hex-player1-hover');

        // Add click event listener to each hex cell
        hex.onclick = function() {
            // Save the current game state before making a move
            game_history.push(Array.from(cells).map(cell => cell.style.backgroundColor));

            const hexid = this.id;
            // alert("Cellule " + hexid + " choisie !");

            // Make a POST request to /place_piece
            fetch('/place_piece', {
                    method: 'POST',
                    headers: {
                            'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                            'hexid': hexid,
                            'current_player': current_player
                    }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    // handle error
                    alert(data.error);
                } else {
                    // handle successful move
                    console.log('Success:', data);
                    // toggle the colour of the hex cell
                    toggle_colour(this);

                    // check if the game is over
                    if (data.game_over) {
                        game_over = true;
                    }

                    // toggle the hover class for the next player
                    cells.forEach(hex => {
                        if (current_player === 1) {
                            hex.classList.add('hex-player2-hover');
                            hex.classList.remove('hex-player1-hover');
                        } else {
                            hex.classList.add('hex-player1-hover');
                            hex.classList.remove('hex-player2-hover');
                        }
                        if (game_over) {
                            hex.classList.remove('hex-player1-hover');
                            hex.classList.remove('hex-player2-hover');
                        }
                    });

                    if (game_over) {
                        data.hexid.forEach(hexID =>{
                            hex = document.getElementById(hexID);
                            hex.style.backgroundColor = 'yellow';
                        });                       
                        return;
                    }
                    current_player = data.current_player; // Set current_player to the one in data.current_player
                }
            })
            .catch((error) => {
                    alert('Unknown error: ' + error); //
            })

        }; // end of hex.onclick
    }); // end of cells.forEach

    // Function to toggle the colour of the hex cell
    // also adds the hover class for the next player
    function toggle_colour(hex) {
        if (current_player === 1) {
            // change the colour of the hex cell
            hex.style.backgroundColor = '#29335C';
            // remove the hover class for player 1
            hex.classList.remove('hex-player1-hover');
        } else {
            // change the colour of the hex cell
            hex.style.backgroundColor = '#A51613';
            // remove the hover class for player 2
            hex.classList.remove('hex-player2-hover');
        }
    }

    window.reset_board = function() {
        // reset cells to initial state
        cells.forEach(hex => {
            // reset the colour of all hex cells
            hex.style.backgroundColor = '#B0BFB1';
            // reset the hover class for all hex cells
            hex.classList.add('hex-player1-hover');
            hex.classList.remove('hex-player2-hover');
        });
        game_over = false;
        current_player = 1;

        // Make a POST request to /load_game
        fetch('/reload_game', {
            method: 'POST',
            headers: {
                    'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                    'size': size,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Reloaded game:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    } // end of reset_board

    // Function to undo the last move
    window.undo_move = function() {
        if (game_history.length > 0) {
            const last_game_state = game_history.pop();
            cells.forEach((cell, index) => {
                cell.style.backgroundColor = last_game_state[index];
            });
        }
    } // end of undo_move

    reset_button.addEventListener('click', reset_board);
    undo_button.addEventListener('click', undo_move);
}

function back() {
    window.location.href = '/';
}
