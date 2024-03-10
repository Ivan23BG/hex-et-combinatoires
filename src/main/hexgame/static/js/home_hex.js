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
    // Update the value of the hidden input field with the current size
    document.querySelector("input[name='size']").value = size;

    // Submit the form
    document.forms[0].submit();
}

function back() {
    window.location.href = '/';
}


