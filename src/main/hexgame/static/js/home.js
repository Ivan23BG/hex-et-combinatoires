function parallax_height() {
    var scroll_top = $(this).scrollTop();
    var section_top = $(".container").offset().top;
    var header_height = $(".header-section").outerHeight();
    $(".container").css({ "margin-top": header_height });
    $(".header").css({ height: header_height - scroll_top });
}

parallax_height();
$(window).scroll(function () {
    parallax_height();
});

$(window).resize(function () {
    parallax_height();
});


function redirectToHex() {
    window.location.href = '/home_hex';
}

function redirectToAwale() {
    window.location.href = '/home_awale';
}