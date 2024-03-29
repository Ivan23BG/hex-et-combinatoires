var size = 11; // Valeur initiale de la variable 'size'
var selectedDiv = div4;

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
    if(formNumber === 1) {
        document.getElementById('size_input_1').value = size;
        document.querySelector('form[action="/game_hex"]').submit();
    } else if(formNumber === 2) {
        document.getElementById('size_input_2').value = size;
        document.querySelector('form[action="/game_hexia"]').submit();
    }
}


function back() {
    window.location.href = '/';
}


