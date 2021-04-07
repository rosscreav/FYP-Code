$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];
    numbers_string = '';

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg);
        numbers_string = '<p>' + msg.toString() + '</p>' + numbers_string;
        $('#log').html(numbers_string);
    });

});