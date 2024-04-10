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

async function fetchFirstMoveJSON() {
    const response = await fetch('/first_move_IA',{method:'POST',headers:{'Content-Type': 'application/json'}});
    const data = response.json();
    return data;
}

window.onload = async function () {
    let player = 0; // Player default value 
    let IA = 0; // IA default value 

    let game_over = false;
    let short_path = [];
    let winner = 0;

    const game_history = []; // stack to store game history
    const cells = document.querySelectorAll('.hex'); // Get all hex cells
    
    // Initialise correct player's and IA's values 
    const data1 = await fetchPlayersJSON() 
    player = data1.player;
    document.getElementById('player').value = player;

    IA = data1.IA;
    //console.log("player",player,"IA",IA);
    
    // If IA is playing Blue, she play first move
    if (player===2){
        const data2 = await fetchFirstMoveJSON();
        let iamove = data2.iamove;
        var iahex = document.getElementById(iamove);
        game_history.push(iamove);
        toggle_colour(iahex,IA);
    }
        
    
    cells.forEach(hex => {    
        // Add correct hover class for each cell
        if (player===1){
            hex.classList.add('hex-player1-hover');
        }
        if (player===2){
            hex.classList.add('hex-player2-hover');            
        }
        
        // Add click event listener to each hex cell
        hex.onclick = function () {

            // show spinner
            document.getElementById('spinner').style.display = 'block';

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

                        // hide spinner
                        document.getElementById('spinner').style.display = 'none';
                        return;
                    }
                }
                // hide spinner
                document.getElementById('spinner').style.display = 'none';
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
            let colorelem = document.getElementById("hidden_data_blue");
            let color = colorelem.getAttribute("value");
            // change the colour of the hex cell
            hex.style.backgroundColor = color;

            hex.classList.remove('hex-player1-hover');
            hex.classList.remove('hex-player2-hover');
            // deactive the hex
            // hex.setAttribute('disabled', true);
        } else {
            // change the colour of the hex cell
            let colorelem = document.getElementById("hidden_data_red");
            let color = colorelem.getAttribute("value");
            // change the colour of the hex cell
            hex.style.backgroundColor = color;
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


function gestionnairePressionTouche(event) {
    // Vérifier si la touche pressée est la touche "H" (code 72 pour 'H')
    if (event.keyCode === 72) {
        changerFichiers();
    }
}

// Ajouter un écouteur d'événement pour le pressage de touche
document.addEventListener("keydown", gestionnairePressionTouche);




function changerFichiers() {
    var Mblue = "rgb(81, 130, 155)";
    var Mred = "rgb(248, 124, 41)";
    var blue = "rgb(41, 51, 92)";
    var red = "rgb(165, 22, 19)";
    var styleSheet = document.getElementById('stylesheet');
    var div1 = document.getElementById("hidden_data_red");
    var div2 = document.getElementById("hidden_data_blue");
    if (styleSheet.getAttribute('href') === "../static/css/game_hex_styles.css") {
        //console.log("touché");
        styleSheet.setAttribute('href', "../static/css/game_hex_marine_skin.css");
        div1.setAttribute("value", Mred);
        div2.setAttribute("value", Mblue);
        changecolor(blue,Mblue,red,Mred)
    } else {
        styleSheet.setAttribute('href', "../static/css/game_hex_styles.css");
        div1.setAttribute("value",red);
        div2.setAttribute("value", blue);
        changecolor(Mblue,blue,Mred,red)
    }

}

function changecolor(b1,b2,r1,r2){
    const cells = document.querySelectorAll('.hex');
    cells.forEach(hex => {
        console.log(hex.style.backgroundColor);
        if (hex.style.backgroundColor == b1) {
            hex.style.backgroundColor = b2;
        }
        if (hex.style.backgroundColor == r1) {
            hex.style.backgroundColor = r2;
        }
    })
}
