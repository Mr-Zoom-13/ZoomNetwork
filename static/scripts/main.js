$(document).ready(function() {
    var socket = io('http://1b50-79-140-31-217.ngrok.io/main');

    socket.on('connect', function (event) {
        socket.emit('add_sid', {data: window.location.href});
    })

    socket.on('user_update', function (data) {
        if(window.location.href.slice(window.location.href.length - 1) == data.data){
            console.log(data.data);
            document.getElementById("last_seen").textContent = data.last_seen;
        }
    })

    window.onbeforeunload = function () {
        socket.emit('delete_sid');
    }
})