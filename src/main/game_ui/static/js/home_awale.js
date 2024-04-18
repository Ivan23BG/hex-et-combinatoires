var player = 1;


function back() {
    window.location.href = '/';
}


function start1v1() {
    window.location.href = '/game_awale';
}

function submitForm(type) {
    if (type == 1){
    document.forms[0].submit();}
    else if (type == 2){
        document.getElementById('player').value = player;
        document.querySelector('form[action="/game_awaleia"]').submit();
    }
    else if (type == 3){
        document.querySelector('form[action="/game_awaleiaia"]').submit();
    }
}



function player_red(){
    document.getElementById("button_red").classList.add("selected_2")
    document.getElementById("button_blue").classList.remove("selected_2")
    player = 1;
}

function player_blue(){
    document.getElementById("button_red").classList.remove("selected_2")
    document.getElementById("button_blue").classList.add("selected_2")
    player = 2;
}