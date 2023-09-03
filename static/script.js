$(document).ready(function () {
    // Smooth-scroll to sections when a link is clicked
    $('.sidenav a').on('click', function (event) {
        event.preventDefault();
        var target = $(this).attr('href');
        $('html, body').animate({
            scrollTop: $(target).offset().top
        }, 800);
    });

    // Toggle the hidden class on the navigation bar
    function toggleSideNav(show) {
        $('#js-sidenav').toggleClass('sidenav-hidden', !show);
    }

    var isMouseOverNav = false;

    // Show the navigation bar when cursor enters the left side
    $(document).on('mousemove', function (event) {
        var mouseX = event.clientX;
        var mouseY = event.clientY;
        var navWidth = $('#js-sidenav').width(); // Width of the navigation bar

        if (mouseX <= 60) {
            toggleSideNav(true);
            isMouseOverNav = true;
        } else if (!isMouseOverNav || (mouseX > navWidth && mouseY > navWidth)) {
            toggleSideNav(false);
            isMouseOverNav = false;
        }
    });
});

async function getRequest(url = '') {
    const response = await fetch(url, {
        method: 'GET',
        cache: 'no-cache'
    })
    return response.json()
}
document.addEventListener('DOMContentLoaded', function () {
    let url = document.location
    let route = "/flaskwebgui-keep-server-alive"
    let interval_request = 3 * 1000 //sec
    function keep_alive_server() {
        getRequest(url + route)
            .then(data => console.log(data))
    }
    setInterval(keep_alive_server, interval_request)()
})
