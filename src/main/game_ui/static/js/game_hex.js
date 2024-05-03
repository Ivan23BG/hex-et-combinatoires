var hover1 = "#344792"
var hover2 = "#BA3533"
var hex_color = "#B0BFB1"

window.onload = function () {
    let current_player = 1; // Player 1 starts the game
    let game_over = false;
    let short_path = [];

    const game_history = []; // stack to store game history
    const cells = document.querySelectorAll('.hex'); // Get all hex cells

    cells.forEach(function (element) {
        element.addEventListener("mouseover", survolHex(element));
        element.addEventListener("mouseout", survolHex(element));
    });

    cells.forEach(hex => {
        // Add initial hover class
        hex.classList.add('hex-player1-hover');
        console.log(hex.getAttribute('disabled'));
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
            fetch('/hex_place_piece', {
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
                        // add move to stack
                        game_history.push(hexid);

                        // check if the game is over
                        if (data.game_over === true) {
                            //save shortest_parth
                            short_path = data.hexid;
                            // set game to over
                            game_over = true;
                        }

                        // toggle the colour of the hex cell
                        toggle_colour(this);
                        // Pour le hover
                        this.setAttribute('disabled', true);
                        this.removeAttribute('nimp');
                        this.setAttribute('couleur', true);

                        // toggle the current player
                        current_player = current_player === 1 ? 2 : 1;

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
            let colorelem = document.getElementById("hidden_data_blue");
            let color = colorelem.getAttribute("value");
            //console.log(color)
            // change the colour of the hex cell
            hex.style.backgroundColor = color;
            // remove the hover class for the hex cell
            hex.classList.remove('hex-player1-hover');
            hex.classList.remove('hex-player2-hover');
            // deactive the hex
            // hex.setAttribute('disabled', true);
        } else {
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
            fetch('/hex_undo_move', {
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
                if (current_player === 1) {
                    let k = 0;
                    let intervalId = setInterval(() => {
                        let hex = document.getElementById(short_path[short_path.length - k - 1]);
                        hex.style.backgroundColor = '#A51613';
                        k++;
                        if (k === short_path.length) {
                            clearInterval(intervalId);
                        }
                    }, 100);
                }
                if (current_player === 2) {
                    let k = 0;
                    let intervalId = setInterval(() => {
                        let hex = document.getElementById(short_path[short_path.length - k - 1]);
                        hex.style.backgroundColor = '#29335C';
                        k++;
                        if (k === short_path.length) {
                            clearInterval(intervalId);
                        }
                    }, 100);
                }

                game_over = false;
            }

            // toggle the current player
            current_player = current_player === 1 ? 2 : 1;

            // Le dernier coup n'est plus disabled ni en couleur
            hex.removeAttribute('disabled');
            hex.removeAttribute('couleur');

            // toggle the hover class for each hexagon
            cells.forEach(cell => {
                // remove the disabled attribute from the hex cell
                if (cell.getAttribute('disabled') && !cell.getAttribute('couleur')) {
                    cell.removeAttribute('disabled');
                }
                toggle_hover(cell, current_player);
            });
        }
    } // end of undo_move

    function survolHex(element) {
        return function (event) {
            // Hover uniquement si on n'est ni une couleur ni désactivé
            if (event.type === "mouseover" && game_over===false && !element.getAttribute('couleur') && !element.getAttribute("disabled")){
                if (current_player===1){
                    element.style.backgroundColor = hover1;
                }
                if (current_player===2){
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

function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_hex'
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

