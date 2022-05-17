$(document).ready(function() {
    var socket = io('https://flasktest.school-score.online/main');

    socket.on('connect', function () {
        socket.emit('add_sid', {data: window.location.href});
    })

    socket.on('user_update', function (data) {
        console.log("ZASHEL");
        if(window.location.href.slice(window.location.href.length - 1) == data.data){
            console.log(data.data);
            document.getElementById("last_seen").textContent = data.last_seen;
        }
    })
})