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
    var cont = document.getElementById(pitId);
    for (var i = 0; i < n; i++) {
        var circle = document.createElement("div");
        circle.classList.add("circle");
        cont.appendChild(circle);
    }
}

// Fonction pour afficher les cercles dans chaque conteneur en fonction des valeurs de l'array
function displayCircles() {
    for (var i = 0; i < values.length; i++) {
        var pitId = (i);
        // Vider le contenu du conteneur
        var cont = document.getElementById("c"+pitId);
        cont.innerHTML = '';
        createCircles("c"+pitId, values[i]);
    }
}

function displayscores() {
    var rhole = document.getElementById("redhole")
    var dis = document.getElementById("score1")
    dis.innerHTML = '';
    rhole.innerHTML = '';
    dis.innerHTML = 'player 1 score:' + score_1;
    createCircles("redhole", score_1);//ajouter les cercles dans les compteurs

    var bhole = document.getElementById("bluehole")
    var dis2 = document.getElementById("score2")
    dis2.innerHTML = '';
    bhole.innerHTML = '';
    dis2.innerHTML = 'player 2 score:' + score_2;
    createCircles("bluehole", score_2);//ajouter les cercles dans les compteurs
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


function survolPit(element) {
    return function(event) {
        console.log("Élément survolé : " + element.id);
        // Vous pouvez ajouter d'autres actions à exécuter ici
    };
}

// Sélection des éléments à surveiller pour le survol
var pits = document.querySelectorAll('.pit');

// Ajout des gestionnaires d'événements hover à chaque élément surveillé
pits.forEach(function(element) {
    element.addEventListener("mouseover", survolPit(element));
    element.addEventListener("mouseout", survolPit(element));
});