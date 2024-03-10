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

function submitForm() {
    document.getElementById("size_input").value = size;
    document.forms[0].submit();
}

function back() {
    window.location.href = '/';
}


