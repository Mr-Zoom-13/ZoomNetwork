$(document).ready(function() {
    var socket = io();
    socket.on('connect', function () {
        socket.emit('my_event', {data: 'I\'m connected!'});
    })
})