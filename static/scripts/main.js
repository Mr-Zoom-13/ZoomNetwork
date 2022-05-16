$(document).ready(function() {
    var socket = io('http://localhost:5000/main');

    socket.on('connect', function () {
        socket.emit('add_sid', {data: window.location.href});
    })

    window.onbeforeunload = function () {
        socket.emit('delete_sid', {data: window.location.href});
    }
})