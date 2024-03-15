window.onload = function () {
    let current_player = 1; // Player 1 starts the game
    let game_over = false;

    const reset_button = document.getElementById('reset-form');
    const undo_button = document.getElementById('undo-form');

    const game_history = []; // stack to store game history
    const cells = document.querySelectorAll('.hex'); // Get all hex cells

    cells.forEach(hex => {
        // Add initial hover class
        hex.classList.add('hex-player1-hover');

        // Add click event listener to each hex cell
        hex.onclick = function () {
            const hexid = this.id;

            // Make a POST request to /place_piece
            if (game_over) {
                // stop game immediately if game is over
                return;
            }
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
                        // handle game over
                        if (data.game_over === true) {
                            // set game to over
                            game_over = true;
                        }

                        // add move to stack
                        game_history.push(hexid);

                        // toggle the colour of the hex cell
                        toggle_colour(this);
                        // toggle the hover class for the next player
                        cells.forEach(hex => {
                            toggle_hover(hex)
                        });

                        // display winning path
                        if (game_over) {
                            let k = 0;
                            let intervalId = setInterval(() => {
                                let hex = document.getElementById(data.hexid[k]);
                                hex.style.backgroundColor = '#FFD700';
                                k++;
                                if (k === data.hexid.length) {
                                    clearInterval(intervalId);
                                }
                            }, 100);
                            return;
                        }
                        current_player = data.current_player; // Set current_player to the one in data.current_player
                    }
                })
                .catch((error) => {
                    alert('Unknown error, should never happen, if you get this please warn your supervisor' + error);
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
            hex.style.backgroundColor = '#A51613';
            hex.classList.remove('hex-player2-hover');
        }
    }

    function toggle_hover(hex) {
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
    }

    window.reset_board = function () {
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


    } // end of reset_board

    // Function to undo the last move
    window.undo_move = function () {
        // pop last element in stack and set it to default colour
        if (game_history.length > 0) {
            const lastMove = game_history.pop();
            const hex = document.getElementById(lastMove);
            hex.style.backgroundColor = '#B0BFB1';

            // toggle the hover class for each hexagon
            cells.forEach(cell => {
                if (cell !== hex) {
                    toggle_hover(cell);
                } else {
                    cell.classList.add('hex-player1-hover');
                    cell.classList.add('hex-player2-hover');
                }
            });

            // toggle the current player
            current_player = current_player === 1 ? 2 : 1;
        }
    } // end of undo_move
}

function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_hex'
}
