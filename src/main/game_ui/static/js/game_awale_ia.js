let values = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
let score_1 = 0
let score_2 = 0


function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_awale'
}

function submitForm(type) {
    if (type == 1){
    document.forms[0].submit();}
    if (type == 2){
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


// ========= "main" =======================================================================


window.onload = async function () {
    displayCircles(); //init des cercless
    let player = 0; // Player default value 
    let IA = 0; // IA default value 

    let recup_error = false; // Variable qui empêche que l'IA joue si on clic sur un hex pas bon
    let playable = true; // Check if player can play or not 
    let game_over = false;
    let winner = 0;
    //const game_history = []; // stack to store game history
    const pits = document.querySelectorAll('.pit'); // Get all pits

    const data1 = await fetchPlayersJSON()
    player = data1.player;
    document.getElementById('player').value = player;
    IA = data1.IA;
    console.log(player)
    document.getElementById('player').value = player;

    if (player === 2) {
        const data2 = await fetchFirstMoveJSON();
        let iamove = data2.iamove;
        console.log("iamove", iamove);
        values = []
        values = data2.values;
        score_1 = data2.score_1;
        score_2 = data2.score_2;
        displayscores();
        displayCircles();
    }

    pits.forEach(pit => {

        pit.onclick = async function () {

            // to do add spinner

            const pitid = this.id;
            console.log(player);
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
                    'current_player': player
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
                        displayCircles();
                        console.log(values);
                        if (data.game_over === true) {
                            // set game to over
                            game_over = true;
                        }

                    }
                })
            if (game_over != true) {
                playable = false;
                const data = await fetchIAMoveJSON_awale(IA);
                values = []
                values = data.values;
                score_1 = data.score_1;
                score_2 = data.score_2;
                displayscores();
                displayCircles();
            }


        }
    }
    )
}


function survolPit(element) {
    return function (event) {

        if (event.type === "mouseover") {
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
            }
        }

        if (event.type === "mouseout") {
            //console.log(values);
            displayCircles();
        }

    };
}

// Sélection des éléments à surveiller pour le survol
var pits = document.querySelectorAll('.pit');

// Ajout des gestionnaires d'événements hover à chaque élément surveillé
pits.forEach(function (element) {
    element.addEventListener("mouseover", survolPit(element));
    element.addEventListener("mouseout", survolPit(element));
});