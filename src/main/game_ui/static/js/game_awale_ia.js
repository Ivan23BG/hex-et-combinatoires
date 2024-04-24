let values = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4];
let score_1 = 0;
let score_2 = 0;
check_error = false;

function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_awale';
}

function submitForm(type) {
    if (type == 1) {
        document.forms[0].submit();
    }
    if (type == 2) {
        document.querySelector('form[action="/game_awaleia"]').submit();
    }
}

function createCircles(pitId, n, type) {
    var cont = document.getElementById(pitId);
    for (var i = 0; i < n; i++) {
        var circle = document.createElement("div");
        if (type == 2) {
            circle.classList.add("temp");
        }
        circle.classList.add("circle");
        cont.appendChild(circle);
    }
}

// Fonction pour afficher les cercles dans chaque conteneur en fonction des valeurs de l'array
function displayCircles() {
    for (var i = 0; i < values.length; i++) {
        var pitId = (i);
        // Vider le contenu du conteneur
        var cont = document.getElementById("c" + pitId);
        cont.innerHTML = '';
        createCircles("c" + pitId, values[i], 1);
    }
}

function displayscores() {
    var rhole = document.getElementById("redhole")
    //var dis = document.getElementById("score1")
    //dis.innerHTML = '';
    rhole.innerHTML = '';
    //dis.innerHTML = 'player 1 score:' + score_1;
    createCircles("redhole", score_1);//ajouter les cercles dans les compteurs

    var bhole = document.getElementById("bluehole")
    //var dis2 = document.getElementById("score2")
    //dis2.innerHTML = '';
    bhole.innerHTML = '';
    //dis2.innerHTML = 'player 2 score:' + score_2;
    createCircles("bluehole", score_2);//ajouter les cercles dans les compteurs
}

//============================================================================================================
// async

async function fetchPlayersJSON() {
    const response = await fetch('/players_awaleia', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
    const data = response.json();
    return data;
}

// Request for IA's first move
async function fetchFirstMoveJSON() {
    const response = await fetch('/first_move_IA_awale', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
    const data = response.json();
    return data;
}

// request for IA's move
async function fetchIAMoveJSON_awale(IA) {
    const response = await fetch('/awaleia_place_piece', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'current_IA': IA }) });
    const data = response.json();
    return data;
}

// request for place player's move
async function fetchPlayerMoveJSON(pitid, player) {
    const response = await fetch('/awale_place_piece', { method: 'POST', headers: { 'Content-Type': 'application/json', }, body: JSON.stringify({ 'pitid': pitid, 'current_player': player }), });
    const data = response.json().catch((error) => {
        // log error
        console.log('Unknown error, should never happen, if you get this please warn your supervisor' + error);
    }) //End of fetch player
        ;
    return data;
}


// ========= "main" =======================================================================


window.onload = async function () {
    displayCircles(); //init des cercles

    let player = 0; // Player default value 
    let IA = 0; // IA default value 
    let tabP1 = [0, 1, 2, 3, 4, 5]; // Tableau des id des pits rouges
    let tabP2 = [11, 10, 9, 8, 7, 6]; // Tableau des id des pits bleu

    let recup_error = false; // Variable qui empêche que l'IA joue si on clic sur un hex pas bon
    let playable = true; // Check if player can play or not 
    let game_over = false;
    let winner = 0;

    const game_history = [[values, score_1, score_2]]; // stack to store game history
    const pits = document.querySelectorAll('.pit'); // Get all pits

    // Ajout des gestionnaires d'événements hover à chaque élément surveillé
    pits.forEach(function (element) {
        element.addEventListener("mouseover", survolPit(element));
        element.addEventListener("mouseout", survolPit(element));
    });

    // Donne les bonnes valeurs à player et à l'IA
    const data1 = await fetchPlayersJSON();
    player = data1.player;
    document.getElementById('player').value = player;
    IA = data1.IA;

    // L'IA joue le premier coup si elle est rouge
    if (player === 2) {
        const data2 = await fetchFirstMoveJSON();
        values = [];
        values = data2.values;
        score_1 = data2.score_1;
        score_2 = data2.score_2;
        displayscores();
        displayCircles();
    }

    pits.forEach(pit => {

        pit.onclick = async function () {
            // add hover for pits
            pit.classList.add("pit-hover");

            // show spinner
            document.getElementById('spinner').style.display = 'block';


            if (this.getAttribute('disabled') || playable === false) {
                // hide spinner
                document.getElementById('spinner').style.display = 'none';
                return;
            }

            const pitid = this.id;

            if (game_over) {
                // remove all hovers
                pits.forEach(pit => {
                    pit.setAttribute('disabled', true);
                });
                // stop game immediately if game is over

                // hide spinner
                document.getElementById('spinner').style.display = 'none';
                return;
            }

            // On fait jouer le coup au joueur
            const data = await fetchPlayerMoveJSON(pitid, player);
            if (data.error) {
                check_error = true;
                alert(data.error);
            }
            else {
                check_error = false;
                values = data.values;
                score_1 = data.score_1;
                score_2 = data.score_2;

                // Add new board to history
                game_history.push([values, score_1, score_2]);

                displayscores();
                displayCircles();

                if (data.game_over === true) {
                    winner = player;

                    // set game to over
                    game_over = true;
                    pits.forEach(pit => {
                        pit.setAttribute('disabled', true);
                    });

                    // Show winner and points
                    console.log("Gagnant:", winner);
                    console.log(score_1, score_2);

                    // Show board
                    displayscores();
                    displayCircles();

                    // Show winnner's pits
                    if (winner === 1) {
                        let k = 0;
                        let intervalId = setInterval(() => {
                            let p = tabP1[tabP1.length - k - 1];
                            document.getElementById(String(p)).style.backgroundColor = '#FFD700';
                            k++;
                            if (k === 6) {
                                document.getElementById("redhole").style.backgroundColor = '#FFD700';
                                clearInterval(intervalId);
                            }
                        }, 200);
                    }
                    if (winner === 2) {
                        let k = 0;
                        let intervalId = setInterval(() => {
                            let p = tabP2[k];
                            document.getElementById(String(p)).style.backgroundColor = '#FFD700';
                            k++;
                            if (k === 6) {
                                document.getElementById("bluehole").style.backgroundColor = '#FFD700';
                                clearInterval(intervalId);
                            }
                        }, 200);
                    }
                    return;
                } // End of winner player
            } // End of player's turn

            // Place piece if player doesn't win
            if (game_over != true && recup_error != true) {
                if (check_error) {
                    check_error = false;
                }
                else {
                    playable = false;
                    const data = await fetchIAMoveJSON_awale(IA);
                    values = data.values;
                    score_1 = data.score_1;
                    score_2 = data.score_2;

                    // Add new board to history
                    game_history.push([values, score_1, score_2]);

                    displayscores();
                    displayCircles();
                    console.log("L'IA a joué");

                    // hide spinner
                    document.getElementById('spinner').style.display = 'none';
                    playable = true;

                    // Check if IA won
                    if (data.game_over === true) {
                        winner = IA;

                        // set game to over
                        game_over = true;

                        // Disabled pits
                        pits.forEach(pit => {
                            pit.setAttribute('disabled', true);
                        });

                        // Show winner and points
                        console.log("Gagnant:", winner);
                        console.log(score_1, score_2);

                        // Show board
                        displayscores();
                        displayCircles();

                        // Show winnner's pits
                        if (winner === 1) {
                            let k = 0;
                            let intervalId = setInterval(() => {
                                let p = tabP1[tabP1.length - k - 1];
                                document.getElementById(String(p)).style.backgroundColor = '#FFD700';
                                k++;
                                if (k === 6) {
                                    document.getElementById("redhole").style.backgroundColor = '#FFD700';
                                    clearInterval(intervalId);
                                }
                            }, 200);
                        }
                        if (winner === 2) {
                            let k = 0;
                            let intervalId = setInterval(() => {
                                let p = tabP2[k];
                                document.getElementById(String(p)).style.backgroundColor = '#FFD700';
                                k++;
                                if (k === 6) {
                                    document.getElementById("bluehole").style.backgroundColor = '#FFD700';
                                    clearInterval(intervalId);
                                }
                            }, 200);
                        }
                        // Add disabled attribute 
                        pits.forEach(pit => {
                            pit.setAttribute('disabled', true);
                        });
                        return;
                    } // End of winner
                }
            }// End IA's turn


            //console.log(check_error);


        }// End of pit.onclick
    });// End forEach


    function survolPit(element) {
        return function (event) {

            if (event.type === "mouseover" && game_over === false) {
                // correct hover color for pits
                element.style.backgroundColor = "#63372C";

                let position = parseInt(element.id);
                let valu = values[element.id];
                //let temp =  values;
                let current_position = position;
                let pitId = "c" + current_position;
                // Vider le contenu du conteneur
                var cont = document.getElementById(pitId);
                cont.innerHTML = '';
                while (valu > 0) {
                    current_position = ((current_position - 1) % 12 + 12) % 12;
                    if (current_position == position) {
                        current_position = ((current_position - 1) % 12 + 12) % 12;
                    }
                    pitId = "c" + current_position;
                    //console.log(pitId);
                    createCircles(pitId, 1, 2);
                    valu = valu - 1;
                }// End while
            }//End mouseover

            if (event.type === "mouseout" && game_over === false) {
                element.style.backgroundColor = "#cc945b";

                displayCircles();
            } // End if
        }; // End function
    } // End survolPit



    // Charge le board avant le dernier coup
    window.undo_move = function () {
        // pop last element in stack and set it to default colour
        if (game_history.length >= 2) {

            game_history.pop();
            // Selectionne le plateau précédent
            const lastBoard = game_history[game_history.length - 1];

            // Associe les bonnes valeurs pour l'affichage
            values = lastBoard[0];
            score_1 = lastBoard[1];
            score_2 = lastBoard[2];
            displayscores();
            displayCircles();

            // Modifie le game_board
            fetch('/undo_move_awale', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'values': values,
                    'score_1': score_1,
                    'score_2': score_2,
                }),
            })

            if (game_over) {
                if (winner === 1) {
                    document.getElementById("redhole").style.backgroundColor = '#cc945b';
                    let k = 0;
                    let intervalId = setInterval(() => {
                        let p = tabP1[k];
                        document.getElementById(String(p)).style.backgroundColor = '#cc945b';
                        k++;
                        if (k === 6) {
                            clearInterval(intervalId);
                        }
                    }, 200);
                }
                if (winner === 2) {
                    document.getElementById("bluehole").style.backgroundColor = '#cc945b';
                    let k = 0;
                    let intervalId = setInterval(() => {
                        let p = tabP2[tabP2.length - k - 1];
                        document.getElementById(String(p)).style.backgroundColor = '#cc945b';
                        k++;
                        if (k === 6) {
                            clearInterval(intervalId);
                        }
                    }, 200);
                }
                game_over = false;
            } // End if game_over

            pits.forEach(pit => {
                // remove the disabled attribute from the hex cell
                if (pit.getAttribute('disabled')) {
                    pit.removeAttribute('disabled');
                }
            });
        }

        if (player === 1 && game_history.length === 1) {
            // Associe les bonnes valeurs pour l'affichage
            values = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4];
            score_1 = 0;
            score_2 = 0;

            // Modifie le game_board
            fetch('/undo_move_awale', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'values': values,
                    'score_1': score_1,
                    'score_2': score_2,
                }),
            })
            displayscores();
            displayCircles();
        }
    } // End of undo_move

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
} // End window.onload

