var hover1 = "#344792"
var hover2 = "#BA3533"
var hex_color = "#B0BFB1"


function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_hex'
}

// Request for correct IA's and player's values
async function fetchPlayersJSON() {
    const response = await fetch('/players_hexia', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
    const data = response.json();
    return data;
}

// Request for IA's first move
async function fetchFirstMoveJSON() {
    const response = await fetch('/first_move_IA_hex', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
    const data = response.json();
    return data;
}

// request for IA's move
async function fetchIAMoveJSON_hex(IA) {
    console.log(IA);
    const response = await fetch('/hexiaia_place_piece', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'current_IA': IA }) });
    const data = response.json();
    return data;
}

// request for place player's move
async function fetchPlayerMoveJSON(hexid, player) {
    const response = await fetch('/hex_place_piece', { method: 'POST', headers: { 'Content-Type': 'application/json', }, body: JSON.stringify({ 'hexid': hexid, 'current_player': player }), });
    const data = response.json().catch((error) => {
        // log error
        console.log('Unknown error, should never happen, if you get this please warn your supervisor' + error);
    }) //End of fetch player
        ;
    return data;
}

window.onload = async function () {
    let player = 1; // Player default value 
    let IA = 2; // IA default value 

    let recup_error = false; // Variable qui empêche que l'IA joue si on clic sur un hex pas bon
    let playable = true; // Check if player can play or not 
    let game_over = false;
    let short_path = [];
    let winner = 0;

    const game_history = []; // stack to store game history
    const cells = document.querySelectorAll('.hex'); // Get all hex cells

    // Initialise correct player's and IA's values 
    const data1 = await fetchPlayersJSON()
    player = data1.player;
    IA = data1.IA;
    console.log(player, IA);
    document.getElementById('player').value = player;

    cells.forEach(function (element) {
        element.addEventListener("mouseover", survolHex(element));
        element.addEventListener("mouseout", survolHex(element));
    });

    // If IA is playing Blue, she play first move
    if (player === 2) {
        const data2 = await fetchFirstMoveJSON();
        let iamove = data2.iamove;
        var iahex = document.getElementById(iamove);
        game_history.push(iamove);
        toggle_colour(iahex, IA);
        iahex.setAttribute('disabled', true);
    }

    

    cells.forEach(hex => {

        // Add click event listener to each hex cell
        hex.onclick = async function () {

            // show spinner
            document.getElementById('spinner').style.display = 'block';


            if (this.getAttribute('disabled') || playable === false) {
                return;
            }

            const hexid = this.id;

            // Check if the game is over
            if (game_over) {
                // remove all hovers
                cells.forEach(cell => {
                    cell.setAttribute('disabled', true);
                });
                // stop game immediately if game is over

                // hide spinner
                document.getElementById('spinner').style.display = 'none';
                return;
            }
            const data = await fetchPlayerMoveJSON(hexid, player);
            if (data.error) {
                let error = data.error
                recup_error = true;
                // log error
                console.log(error);
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
                recup_error = false;
                game_history.push(hexid);
                toggle_colour(this, player);
                // Pour le hover
                this.setAttribute('disabled', true);
                this.removeAttribute('nimp');
                this.setAttribute('couleur', true);

                // check if player 1 won
                if (data.game_over === true) {
                    //save the winner
                    winner = player;
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


            //Place piece if player doesn't win
            if (game_over != true && recup_error != true) {
                playable = false;
                const data = await fetchIAMoveJSON_hex(IA);  // Get IA's move            
                let iamove = data.iamove;
                console.log(data.iamove);
                var iahex = document.getElementById(iamove);
                console.log(iahex);

                game_history.push(iamove);
                toggle_colour(iahex, IA);
                iahex.setAttribute('disabled', true);
                iahex.removeAttribute('nimp');
                iahex.setAttribute('couleur', true);

                // hide spinner
                document.getElementById('spinner').style.display = 'none';
                playable = true;
                // check if current_IA won
                if (data.game_over === true) {
                    winner = IA;
                    short_path = data.hexid;
                    game_over = true;

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
                    cells.forEach(cell => {
                        cell.classList.remove('hex-player1-hover');
                        cell.classList.remove('hex-player2-hover');
                        cell.setAttribute('disabled', true);
                    });
                    // hide spinner
                    document.getElementById('spinner').style.display = 'none';
                    return;
                }

            }; // end of IA's turn 
            // hide spinner
            document.getElementById('spinner').style.display = 'none';
        }// End of onclick
    });// end of cells.forEach

    // Function to toggle the colour of the hex cell
    // also adds the hover class for the next player
    function toggle_colour(hex, current_player) {
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
            if (player === 1) {
                hex.classList.add('hex-player1-hover');
            }
            else {
                hex.classList.add('hex-player2-hover');
            }
        });
        game_over = false;

    } // end of reset_board

    // Function to undo the last move
    window.undo_move = function () {
        // pop last element in stack and set it to default colour
        if (game_history.length >= 2) {

            const lastMove = game_history.pop();
            fetch('/hex_undo_move', {
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

            // Le dernier coup n'est plus disabled ni en couleur
            hex.removeAttribute('disabled');
            hex.removeAttribute('couleur');
            if (game_over) {
                console.log(short_path);
                let index = short_path.indexOf(lastMove);
                short_path.splice(index, 1);
                if (winner === 2) {
                    let k = 0;
                    let intervalId = setInterval(() => {
                        let hex = document.getElementById(short_path[short_path.length - k - 1]);
                        hex.style.backgroundColor = '#A51613';
                        k++;
                        if (k === short_path.length) {
                            clearInterval(intervalId);
                        }
                    }, 100);
                    winner = 0;
                }
                if (winner === 1) {
                    let k = 0;
                    let intervalId = setInterval(() => {
                        let hex = document.getElementById(short_path[short_path.length - k - 1]);
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
        if (player === 1 && game_history.length === 1) {
            const lastMove = game_history.pop();
            fetch('/hex_undo_move', {
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
            // Le dernier coup n'est plus disabled ni en couleur
            hex.removeAttribute('disabled');
            hex.removeAttribute('couleur');
        }
        // toggle the hover class for each hexagon
        cells.forEach(cell => {
            // remove the disabled attribute from the hex cell
            if (cell.getAttribute('disabled') && !cell.getAttribute('couleur')) {
                cell.removeAttribute('disabled');
            }
        });

    } // end of undo_move

    window.undo_move2 = function () {
        if (player === 1 && winner === 1) {
            undo_move();
        }
        else if (player === 2 && winner === 2) {
            undo_move();
        }
        else {
            undo_move();
            undo_move();
        }
    }

    function survolHex(element) {
        return function (event) {
            // Hover uniquement si on n'est ni une couleur ni désactivé
            if (event.type === "mouseover" && game_over===false && !element.getAttribute('couleur') && !element.getAttribute("disabled")){
                if (player===1){
                    element.style.backgroundColor = hover1;
                }
                if (player===2){
                    element.style.backgroundColor = hover2;
                }
                element.setAttribute("nimp", true);
            }
            // Enlève le hover si on quitte un hex ni en couleur ni disabled
            else if (event.type === "mouseout" && game_over===false && element.getAttribute("nimp") && !element.getAttribute('disabled')){
                element.style.backgroundColor = hex_color;
                element.removeAttribute("nimp");
            }
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
    var bhover1 = "#344792"
    var bhover2 = "#BA3533"
    var mhover1 = "#5197BA"
    var mhover2 = "#F6995C"
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
        hex_color = "#ADBBC6"
        hover1 = mhover1;
        hover2 = mhover2;
        div1.setAttribute("value", Mred);
        div2.setAttribute("value", Mblue);
        changecolor(blue,Mblue,red,Mred,hex_color)
    } else {
        styleSheet.setAttribute('href', "../static/css/game_hex_styles.css");
        hex_color = "#B0BFB1"
        hover1 = bhover1;
        hover2 = bhover2;
        div1.setAttribute("value",red);
        div2.setAttribute("value", blue);
        changecolor(Mblue,blue,Mred,red,hex_color)
    }

}

function changecolor(b1,b2,r1,r2,hex_color){
    const cells = document.querySelectorAll('.hex');
    cells.forEach(hex => {
        //console.log(hex.style.backgroundColor);
        if (hex.style.backgroundColor == b1) {
            hex.style.backgroundColor = b2;
        }
        else if (hex.style.backgroundColor == r1) {
            hex.style.backgroundColor = r2;
        }
        else {
            hex.style.backgroundColor = hex_color;
        }
    })
}
