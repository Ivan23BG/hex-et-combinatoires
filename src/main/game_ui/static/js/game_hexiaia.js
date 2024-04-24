function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_hex'
}

async function fetchIAMoveJSON_hex(current_IA) {
    const response = await fetch('/hexiaia_place_piece', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'current_IA': current_IA }) });
    const data = response.json();
    return data;
}

async function fetchRandomMoveJSON(current_IA) {
    const response = await fetch('/hexiaia_random', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'current_IA': current_IA }) });
    const data = response.json();
    return data;
}

window.onload = async function () {
    let current_IA = 1;

    let game_over = false;
    let short_path = [];
    let winner = 0;
    let stopped = false; // While condition

    const game_history = []; // stack to store game_history
    const cells = document.querySelectorAll('.hex'); // Get all hex cells    

    const data1 = await fetchRandomMoveJSON(1);  // Get current_IA's move
    let iamove = data1.iamove;
    var iahex = document.getElementById(iamove);

    game_history.push(iamove);
    toggle_colour(iahex, 1);

    const data2 = await fetchRandomMoveJSON(2);  // Get current_IA's move
    iamove = data2.iamove;
    iahex = document.getElementById(iamove);

    game_history.push(iamove);
    toggle_colour(iahex, 2);

    while (!stopped) {
        const data = await fetchIAMoveJSON_hex(current_IA);  // Get current_IA's move
        let iamove = data.iamove;
        var iahex = document.getElementById(iamove);

        game_history.push(iamove);
        toggle_colour(iahex, current_IA);

        // check if current_IA won
        if (data.game_over === true) {
            winner = current_IA;
            short_path = data.hexid;
            game_over = true;
            stopped = true;

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
        else {
            current_IA = current_IA === 1 ? 2 : 1;
        }
    }


    // End of jeu


    // Function to toggle the colour of the hex cell
    function toggle_colour(hex, current_player) {

        if (current_player === 1) {
            let colorelem = document.getElementById("hidden_data_blue");
            let color = colorelem.getAttribute("value");
            //console.log(color)
            // change the colour of the hex cell
            hex.style.backgroundColor = color;
        } else {
            // change the colour of the hex cell
            let colorelem = document.getElementById("hidden_data_red");
            let color = colorelem.getAttribute("value");
            // change the colour of the hex cell
            hex.style.backgroundColor = color;
        }
    }

    // Reset game 
    window.reset_board = function () {
        cells.forEach(hex => {
            // reset the colour of all hex cells
            hex.style.backgroundColor = '#B0BFB1';
        });
        game_over = false;
        current_IA = 1;
    } // end of reset_board

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
        changecolor(blue, Mblue, red, Mred)
    } else {
        styleSheet.setAttribute('href', "../static/css/game_hex_styles.css");
        div1.setAttribute("value", red);
        div2.setAttribute("value", blue);
        changecolor(Mblue, blue, Mred, red)
    }

}

function changecolor(b1, b2, r1, r2) {
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