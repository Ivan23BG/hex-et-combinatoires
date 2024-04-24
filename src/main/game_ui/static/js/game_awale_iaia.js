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
        document.querySelector('form[action="/game_awaleiaia"]').submit();
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
    displayscores();
    displayCircles();
    let current_IA = 1;
    let game_over = false;
    let winner = 0;
    let stopped = false; // While condition

    const pits = document.querySelectorAll('.pit'); // Get all pits

    while (!stopped) {
        const data = await fetchIAMoveJSON_awale(current_IA);  // Get current_IA's move
        values = []
        values = data.values;
        score_1 = data.score_1;
        score_2 = data.score_2;
        displayscores();
        displayCircles();

        console.log(data.game_over);
        // check if current_IA won
        if (data.game_over === true) {
            winner = current_IA;
            game_over = true;
            stopped = true;
        }
        else {
            current_IA = current_IA === 1 ? 2 : 1;
        }
    }
}


/*function survolPit(element) {
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
});*/