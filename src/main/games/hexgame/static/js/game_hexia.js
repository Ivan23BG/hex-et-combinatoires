function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_hex'
}


window.onload = function () {
    let current_player = 1; // Player 1 starts the game
    let game_over = false;
    let short_path = [];
    let winner = 0;

    const game_history = []; // stack to store game history
    const cells = document.querySelectorAll('.hex'); // Get all hex cells

    cells.forEach(hex => {
        // Add initial hover class
        hex.classList.add('hex-player1-hover');

        // Add click event listener to each hex cell
        hex.onclick = function () {

            if (this.getAttribute('disabled')) {
                return;
            }

            const hexid = this.id;

            // Check if the game is over
            if (game_over) {
                // remove all hovers
                cells.forEach(cell => {
                    cell.classList.remove('hex-player1-hover');
                    cell.classList.remove('hex-player2-hover');
                    cell.setAttribute('disabled', true);
                });
                // stop game immediately if game is over
                return;
            }

            // Try to play a piece
            fetch('/hex_place_piece_ia', {
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
                    let error = data.error
                    alert(error);
                    // briefly change the colour of the hex cell to indicate an invalid move
                    const original_colour = this.style.backgroundColor;
                    this.style.backgroundColor = '#FF0000';

                    // disable the click event on the hex cell
                    this.setAttribute('disabled', true);

                    setTimeout(() => {
                        this.style.backgroundColor = original_colour;

                        // re-enable the click event on the hex cell
                        this.removeAttribute('disabled');
                    }, 500);
                } else {
                    game_history.push(hexid);
                    toggle_colour(this);

                    // check if player 1 won
                    if (data.game_over_player === true) {
                        //save the winner
                        winner = 1;
                        //save shortest_parth
                        short_path = data.hexid;
                        // set game to over
                        game_over = true;
                    }
                    
                    //Place piece if player 1 doesn't win
                    if (!(game_over)){
                        let iamove = data.iamove;
                        var iahex = document.getElementById(iamove);
                        current_player=2;
                        game_history.push(iamove);
                        toggle_colour(iahex);
                    }

                    //check if IA won
                    if (data.game_over_IA === true){
                        //save the winner
                        winner = 2;
                        //save shortest_parth
                        short_path = data.hexid;
                        // set game to over
                        game_over = true;
                    }
                    
                    current_player = 1;

                    // toggle the hover class for all blank hex cells
                    cells.forEach(cell => {
                        toggle_hover(cell, current_player);
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
                        cells.forEach(cell => {
                            cell.classList.remove('hex-player1-hover');
                            cell.classList.remove('hex-player2-hover');
                            cell.setAttribute('disabled', true);
                        });
                        return;
                    }
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
        // check if the hex is disabled
        if (hex.getAttribute('disabled')) {
            return;
        }
        if (current_player === 1) {
            // change the colour of the hex cell
            hex.style.backgroundColor = '#29335C';
            // remove the hover class for the hex cell
            hex.classList.remove('hex-player1-hover');
            hex.classList.remove('hex-player2-hover');
            // deactive the hex
            // hex.setAttribute('disabled', true);
        } else {
            // change the colour of the hex cell
            hex.style.backgroundColor = '#A51613';
            // remove the hover class for the hex cell
            hex.classList.remove('hex-player1-hover');
            hex.classList.remove('hex-player2-hover');
            // deactive the hex
            // hex.setAttribute('disabled', true);
        }
    }

    function toggle_hover(hex, current_player) {
        if (hex.getAttribute('disabled')) {
            return;
        }
        if (current_player === 1) {
            hex.classList.add('hex-player1-hover');
            hex.classList.remove('hex-player2-hover');
        } else {
            hex.classList.add('hex-player2-hover');
            hex.classList.remove('hex-player1-hover');
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
            fetch('/undo_move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'hexid': lastMove,
                    'current_player': current_player
                }),
            })

            const hex = document.getElementById(lastMove);
            hex.style.backgroundColor = '#B0BFB1';

            if (game_over) {
                console.log(short_path);
                let index = short_path.indexOf(lastMove);
                short_path.splice(index, 1);
                if (winner===2){
                    let k=0;
                    let intervalId = setInterval(() => {
                        let hex = document.getElementById(short_path[short_path.length-k-1]);
                        hex.style.backgroundColor = '#A51613';
                        k++;
                        if (k === short_path.length) {
                            clearInterval(intervalId);
                        }
                    }, 100);
                    winner = 0;
                }
                if (winner===1){
                    let k=0;
                    let intervalId = setInterval(() => {
                        let hex = document.getElementById(short_path[short_path.length-k-1]);
                        hex.style.backgroundColor = '#29335C';
                        k++;
                        if (k === short_path.length) {
                            clearInterval(intervalId);
                        }
                    }, 100);
                    winner = 0;
                }
                
                game_over = false;
            }

            // toggle the current player
            current_player = current_player === 1 ? 2 : 1;

            
            // toggle the hover class for each hexagon
            cells.forEach(cell => {
                // remove the disabled attribute from the hex cell
                if (cell.getAttribute('disabled')) {
                    cell.removeAttribute('disabled');
                }
                toggle_hover(cell,current_player);
            });
        }
    } // end of undo_move

    window.undo_move2 = function () {
        undo_move();
        undo_move();
    }
}

