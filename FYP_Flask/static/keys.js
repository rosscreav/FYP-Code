$(document).keydown(function(e) {
  console.log("Call")
  if (e.which==37) {
    $('.left').addClass('pressed'); 
    sendMQTT("left");
    $('.lefttext').text('LEFT');
    $('.left').css('transform', 'translate(0, 2px)');
  } else if (e.which==38) {
    $('.up').addClass('pressed');
    sendMQTT("forward");
    $('.uptext').text('UP');
    $('.left').css('transform', 'translate(0, 2px)');
    $('.down').css('transform', 'translate(0, 2px)');
    $('.right').css('transform', 'translate(0, 2px)');
  } else if (e.which==39) {
    $('.right').addClass('pressed');
    sendMQTT("right");
    $('.righttext').text('RIGHT'); 
    $('.right').css('transform', 'translate(0, 2px)'); 
  } else if (e.which==40) {
    $('.down').addClass('pressed');
    sendMQTT("back");
    $('.downtext').text('DOWN');
    $('.down').css('transform', 'translate(0, 2px)');
  } else if (e.which==66) {
    $('.b').text('B');  
  } else if (e.which==65) {
    $('.a').text('A');  
  }
});

$(document).keyup(function(e) {
  if (e.which==37) {
    $('.left').removeClass('pressed');
    $('.lefttext').text('');   
    $('.left').css('transform', 'translate(0, 0)');  
  } else if (e.which==38) {
    $('.up').removeClass('pressed');
    $('.uptext').text('');
    $('.left').css('transform', 'translate(0, 0)');
    $('.down').css('transform', 'translate(0, 0)');
    $('.right').css('transform', 'translate(0, 0)');
  } else if (e.which==39) {
    $('.right').removeClass('pressed'); 
    $('.righttext').text(''); 
    $('.right').css('transform', 'translate(0, 0)');
  } else if (e.which==40) {
    $('.down').removeClass('pressed');
    $('.downtext').text('');
    $('.down').css('transform', 'translate(0, 0)');
  } else if (e.which==66) {
    $('.b').text('');  
  } else if (e.which==65) {
    $('.a').text('');  
  }
});

$('.left').mousedown(function() {
  $('.lefttext').text('LEFT');
  $('.left').css('transform', 'translate(0, 2px)');
});

$('.left').mouseup(function() {
  $('.lefttext').text('');
  $('.left').css('transform', 'translate(0, 0)');
});

$('.right').mousedown(function() {
  $('.righttext').text('RIGHT');
  $('.right').css('transform', 'translate(0, 2px)');
});

$('.right').mouseup(function() {
  $('.righttext').text('');
  $('.right').css('transform', 'translate(0, 0)');
});

$('.up').mousedown(function() {
  $('.uptext').text('UP');
  $('.left').css('transform', 'translate(0, 2px)');
  $('.down').css('transform', 'translate(0, 2px)');
  $('.right').css('transform', 'translate(0, 2px)');
});

$('.up').mouseup(function() {
  $('.uptext').text('');
  $('.left').css('transform', 'translate(0, 0)');
  $('.down').css('transform', 'translate(0, 0)');
  $('.right').css('transform', 'translate(0, 0)');
});

$('.down').mousedown(function() {
  $('.downtext').text('DOWN');
  $('.down').css('transform', 'translate(0, 2px)');
});

$('.down').mouseup(function() {
  $('.downtext').text('');
  $('.down').css('transform', 'translate(0, 0)');
});

var mqtt_server  = "broker.mqttdashboard.com";
var mqtt_port  = Number(1883);
var mqtt_destname  = "FYP_Mqtt_Messaging/Pi";

function sendMQTT(direction){
  const socket = io('http://localhost:5000');
  socket.emit('message', direction);
}
