var size = 11; // Valeur initiale de la variable 'size'
var selectedDiv = div3;

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
    }
    // Sélectionner la nouvelle div
    selectedDiv = document.getElementById('div' + divNumber);
    selectedDiv.classList.add('selected');
}

function submit() {
    var finalsize = size;
    fetch('/load_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'size': finalsize,
        }),
    })
    .then(response => response.json())
}


function back() {
    window.location.href = '/';
}


