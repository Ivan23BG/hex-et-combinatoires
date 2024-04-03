function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_hex'
}

async function fetchIAMoveJSON(current_IA) {
    const response = await fetch('/hexiaia_place_piece', {method: 'POST',headers: {'Content-Type': 'application/json'},body: JSON.stringify({'current_IA': current_IA})});
    const data = response.json();
    return data;
}

window.onload = async function () {
    let current_IA = 1;

    let game_over = false;
    let short_path = [];
    let winner = 0;

    const game_history = []; // stack to store game_history
    const cells = document.querySelectorAll('.hex'); // Get all hex cells    

    while(winner===0){
        
        console.log("ça tourne");
        const data = await fetchIAMoveJSON(current_IA);  // Get current_IA's move
        let iamove = data.iamove;
        var iahex = document.getElementById(iamove);
        game_history.push(iamove);
        toggle_colour(iahex,current_IA);

        // check if current_IA won
        if (data.game_over_IA === true) {
            //save the winner
            winner = current_IA;
            //save shortest_parth
            short_path = data.hexid;
            // set game to over
            game_over = true;
        }
        else{
            current_IA = current_IA === 1 ? 2 : 1;
        }

        
    } // End of while

    // display winning path
    if (game_over) {
        let k = 0;
        let intervalId = setInterval(() => {
            let hex = document.getElementById(short_path[k]);
            hex.style.backgroundColor = '#FFD700';
            k++;
            if (k === short_path.length) {
                clearInterval(intervalId);
            }
        }, 100);
        return;
    }
    

    // Function to toggle the colour of the hex cell
    // also adds the hover class for the next player
    function toggle_colour(hex,current_player) {
        
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
            }
            else{
                hex.classList.add('hex-player2-hover');
            }
        });
        game_over = false;

    } // end of reset_board

    // Function to undo the last move
    window.undo_move = function () {
        // pop last element in stack and set it to default colour
        if (game_history.length >=2) {

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
        }
        if (player===1 && game_history.length===1){
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
        }    
            // toggle the hover class for each hexagon
            cells.forEach(cell => {
                // remove the disabled attribute from the hex cell
                if (cell.getAttribute('disabled')) {
                    cell.removeAttribute('disabled');
                }
                if (player===1){
                    cell.classList.add('hex-player1-hover');
                }
                else{
                    cell.classList.add('hex-player2-hover');
                }
            });
        
    } // end of undo_move

    window.undo_move2 = function () {
        if (player===1 && winner===1){
            undo_move();
        }
        else if (player===2 && winner===2){
            undo_move();
        }
        else {
            undo_move();
            undo_move();
        }
    }
}

