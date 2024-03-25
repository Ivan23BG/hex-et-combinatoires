function back() {
    window.location.href = '/';
}

function home() {
    window.location.href = '/home_awale'
}

window.onload = function () {
    let current_player = 1; // Player 1 starts the game
    let game_over = false;

    const game_history = []; // stack to store game history
    const pits = document.querySelectorAll('.pit'); // Get all pits

    pits.forEach(pit => {


        pit.onclick = function () {
            const pitid = this.id;
            console.log(pitid);
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
                        if (data.game_over === true) {
                            // set game to over
                            game_over = true;
                        }

                    }
                })


        }
    }
    )
}
