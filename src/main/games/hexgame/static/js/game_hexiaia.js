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

    let jeu = setInterval(async () => {  // Boucle du jeu
        
        const data = await fetchIAMoveJSON(current_IA);  // Get current_IA's move
        let iamove = data.iamove;
        var iahex = document.getElementById(iamove);

        game_history.push(iamove);
        toggle_colour(iahex,current_IA);

        // check if current_IA won
        if (data.game_over_IA === true) {
            winner = current_IA;
            short_path = data.hexid;
            game_over = true;
            
            // Stop the game
            clearInterval(jeu);

            // Display winning path when game is over
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
        else{
            current_IA = current_IA === 1 ? 2 : 1;
        }
    }, 50); // Game speed = 50
    // End of jeu
    

    // Function to toggle the colour of the hex cell
    function toggle_colour(hex,current_player) {
        
        if (current_player === 1) {
            // change the colour of the hex cell
            hex.style.backgroundColor = '#29335C';
        } else {
            // change the colour of the hex cell
            hex.style.backgroundColor = '#A51613';
        }
    }

    // Reset game 
    window.reset_board = function () {
        cells.forEach(hex => {
            // reset the colour of all hex cells
            hex.style.backgroundColor = '#B0BFB1';
        });
        game_over = false;
    } // end of reset_board
    
}

