var size = 11; // Valeur initiale de la variable 'size'
var selectedDiv = div4;
var player = 1;

function changeSize(newSize) {
    size = newSize;
}

function handleClick(newSize, divNumber) {
    changeSize(newSize);
    selectDiv(divNumber);
}



function selectDiv(divNumber) {
    if (selectedDiv !== null) {
        // Désélectionner la div précédemment sélectionnée
        selectedDiv.classList.remove('selected');
        selectedDiv.classList.add('clickable');
    }
    // Sélectionner la nouvelle div
    selectedDiv = document.getElementById('div' + divNumber);
    selectedDiv.classList.remove('clickable');
    selectedDiv.classList.add('selected');
}

function submitForm(formNumber) {
    if (formNumber === 1) {
        document.getElementById('size_input_1').value = size;
        document.querySelector('form[action="/game_hex"]').submit();
    } else if (formNumber === 2) {
        document.getElementById('player').value = player;
        document.getElementById('size_input_2').value = size;
        document.querySelector('form[action="/game_hexia"]').submit();
    }
    else if (formNumber === 3) {
        document.getElementById('size_input_3').value = size;
        document.querySelector('form[action="/game_hexiaia"]').submit();
    }
}

function player_red() {
    document.getElementById("button_red").classList.add("selected_2")
    document.getElementById("button_blue").classList.remove("selected_2")
    player = 2;
}

function player_blue() {
    document.getElementById("button_red").classList.remove("selected_2")
    document.getElementById("button_blue").classList.add("selected_2")
    player = 1;
}


function back() {
    window.location.href = '/';
}

// ========== fenetre regles ==================================

const openModalBtn = document.getElementById('reglesBtn');
const modal = document.getElementById('modal');
const closeBtn = document.getElementsByClassName('close')[0];

// Fonction pour ouvrir la fenêtre regles
openModalBtn.onclick = function() {
    modal.style.display = 'block';
}

// Fonction pour fermer la fenêtre modale lorsque l'utilisateur clique sur le bouton de fermeture (×)
closeBtn.onclick = function() {
    modal.style.display = 'none';
}

// Fermer la fenêtre modale si l'utilisateur clique en dehors de la fenêtre modale
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
