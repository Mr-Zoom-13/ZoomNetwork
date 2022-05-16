$(document).ready(function() {
    var socket = io('https://fbb9-94-41-167-123.ngrok.io/main');

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