let values = [4,4,4,4,4,4,4,4,4,4,4,4]
let score_1 = 0
let score_2 = 0


function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_awale'
}


function createCircles(pitId, n) {
    var pit = document.getElementById(pitId);
    for (var i = 0; i < n; i++) {
        var circle = document.createElement("div");
        circle.classList.add("circle");
        pit.appendChild(circle);
    }
}

// Fonction pour afficher les cercles dans chaque conteneur en fonction des valeurs de l'array
function displayCircles() {
    for (var i = 0; i < values.length; i++) {
        var pitId = (i);

        // Vider le contenu du conteneur
        var pit = document.getElementById(pitId);
        pit.innerHTML = '';

        createCircles(pitId, values[i]);
    }
}

function displayscores() {
    var dis = document.getElementById("score1")
    dis.innerHTML = '';
    dis.innerHTML = 'player 1 score:' + score_1
    var dis2 = document.getElementById("score2")
    dis2.innerHTML = '';
    dis2.innerHTML = 'player 2 score:' + score_2
}





window.onload = function () {
    let current_player = 1; // Player 1 starts the game
    let game_over = false;
    displayCircles();
    //const game_history = []; // stack to store game history
    const pits = document.querySelectorAll('.pit'); // Get all pits

    pits.forEach(pit => {


        pit.onclick = function () {
            const pitid = this.id;
            console.log(current_player);
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
                        alert(data.error);
                    }
                    else {
                        values = []
                        values = data.values;
                        score_1 = data.score_1
                        score_2 = data.score_2
                        displayscores()
                        console.log(values);
                        if (data.game_over === true) {
                            // set game to over
                            game_over = true;
                        }

                        

                        displayCircles();

                        current_player = data.current_player;
                    }
                })


        }
    }
    )
}
