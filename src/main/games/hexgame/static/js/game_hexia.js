function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_hex'
}

async function fetchPlayersJSON() {
    const response = await fetch('/players_hexia',{method:'POST',headers:{'Content-Type': 'application/json'}});
    const data = response.json();
    return data;
}

window.onload = function () {
    let player = 0; // Player default value 
    let IA = 0; // IA default value 

    let game_over = false;
    let short_path = [];
    let winner = 0;
    let first = true;

    const game_history = []; // stack to store game history
    const cells = document.querySelectorAll('.hex'); // Get all hex cells
    
    cells.forEach(hex => {
        // Add correct hover class for each cell
        if (first){
             
            fetchPlayersJSON().then(data => {
                player = data.player;
                IA = data.IA;
                console.log(player,IA);
            });

            fetch('/players_hexia', { // get IA's and player's values
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                
            })
        }
        first = false;
        console.log("second");
        console.log("player",player);
        if (player===1){
            hex.classList.add('hex-player1-hover');
            console.log("oui1");
        }
        if (player===2){
            hex.classList.add('hex-player2-hover');
            console.log("oui2");

            fetch('/first_move_IA', { // Get first move when IA is Blue
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data =>{
                let iamove = data.iamove;
                var iahex = document.getElementById(iamove);
                game_history.push(iamove);
                toggle_colour(iahex,IA);
            })
        } // End of first move IA
        
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
                    'hexid': hexid
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
                    toggle_colour(this,player);

                    // check if player 1 won
                    if (data.game_over_player === true) {
                        //save the winner
                        winner = player;
                        //save shortest_parth
                        short_path = data.hexid;
                        // set game to over
                        game_over = true;
                    }
                    
                    //Place piece if player 1 doesn't win
                    if (!(game_over)){
                        let iamove = data.iamove;
                        var iahex = document.getElementById(iamove);
                        game_history.push(iamove);
                        toggle_colour(iahex,IA);
                    }

                    //check if IA won
                    if (data.game_over_IA === true){
                        //save the winner
                        winner = IA;
                        //save shortest_parth
                        short_path = data.hexid;
                        // set game to over
                        game_over = true;
                    }

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
    function toggle_colour(hex,current_player) {
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

    window.reset_board = function () {
        // reset cells to initial state
        cells.forEach(hex => {
            // reset the colour of all hex cells
            hex.style.backgroundColor = '#B0BFB1';
            // reset the hover class for all hex cells
            if (player===1){
                hex.classList.add('hex-player1-hover');
                hex.classList.remove('hex-player2-hover');
            }
            else{
                hex.classList.add('hex-player2-hover');
                hex.classList.remove('hex-player1-hover');
            }
        });
        game_over = false;

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
                    'hexid': lastMove
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
            
            // toggle the hover class for each hexagon
            cells.forEach(cell => {
                // remove the disabled attribute from the hex cell
                if (cell.getAttribute('disabled')) {
                    cell.removeAttribute('disabled');
                }
            });
        }
    } // end of undo_move

    window.undo_move2 = function () {
        undo_move();
        undo_move();
    }
}

