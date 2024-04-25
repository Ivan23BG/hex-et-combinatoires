let values = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
let score_1 = 0
let score_2 = 0


function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_awale';
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


window.onload = function () {
    let current_player = 1; // Player 1 starts the game
    let game_over = false;
    let winner = 0;
    let tabP1 = [0, 1, 2, 3, 4, 5]; // Tableau des id des pits rouges
    let tabP2 = [11, 10, 9, 8, 7, 6]; // Tableau des id des pits bleu
    displayCircles();
    displayscores();
    const game_history = [[values, score_1, score_2]]; // stack to store game history
    const pits = document.querySelectorAll('.pit'); // Get all pits

    // Ajout des gestionnaires d'événements hover à chaque élément surveillé
    pits.forEach(function (element) {
        element.addEventListener("mouseover", survolPit(element));
        element.addEventListener("mouseout", survolPit(element));
    });


    pits.forEach(pit => {
        // add hover for pits
        pit.classList.add("pit-hover");

        pit.onclick = function () {
            const pitid = this.id;

            if (this.getAttribute('disabled')) {
                return;
            }

            if (game_over) {
                // remove all hovers
                pits.forEach(pit => {
                    pit.setAttribute('disabled', true);
                });
                // stop game immediately if game is over
                return;
            }

            fetch('/awale_place_piece', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'pitid': pitid,
                    'current_player': current_player
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        // briefly change the color of the pit to red
                        pit.style.backgroundColor = 'red';

                        // disable the cell
                        pit.setAttribute('disabled', true);

                        setTimeout(() => {
                            pit.style.backgroundColor = '#cc945b';

                            // remove the disabled attribute from the hex cell
                            pit.removeAttribute('disabled');
                        }, 500);
                    }
                    else {
                        values = []
                        values = data.values;
                        score_1 = data.score_1;
                        score_2 = data.score_2;
                        // Add new board to history
                        game_history.push([values, score_1, score_2]);
                        console.log(game_history);

                        // Show board
                        displayscores();
                        displayCircles();

                        if (data.game_over === true) {
                            winner = data.winner;
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
                        current_player = data.current_player;
                    }
                }) // End of fetch
        } // End of Onclick
    })// End of pits.forEach


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
            }//End if

            if (event.type === "mouseout" && game_over === false) {
                element.style.backgroundColor = "#cc945b";
                //console.log(values);
                displayCircles();
            } // End if
        }; // End function
    } // End survolPit

    // Charge le board avant le dernier coup
    window.undo_move = function () {
        // pop last element in stack and set it to default colour
        if (game_history.length > 1) {

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
                current_player = current_player === 1 ? 2 : 1;
            } // End if game_over
            current_player = current_player === 1 ? 2 : 1;

            pits.forEach(pit => {
                // remove the disabled attribute from the hex cell
                if (pit.getAttribute('disabled')) {
                    pit.removeAttribute('disabled');
                }
            });
        }
    } // End of undo_move

} // End of window.onload




