$(document).ready(function() {
    var socket = io('http://localhost:5000/main');
    socket.on('connect', function () {
        socket.emit('my_event', {data: 'I\'m connected!'});
    })
})