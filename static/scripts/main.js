$(document).ready(function() {
    var socket = io('http://localhost:5000/main');

    socket.on('connect', function () {
        socket.emit('add_sid');
    })

    socket.on('user_connected', function (data) {
        if(data.data in window.location.href){
            document.getElementById("last_seen").textContent = data.last_seen;
        }
    })

    window.onbeforeunload = function () {
        socket.emit('delete_sid');
    }
})