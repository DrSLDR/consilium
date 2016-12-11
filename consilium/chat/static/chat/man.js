$(document).ready(function(){
  var username;
  var ws;
  $("#send").hide();

  $("#login").click(function(){
    event.preventDefault();
    username = $("#uname").val();
    if(username.length == 0){
      alert("Your username can't be blank, foo'");
      return;
    }
    var butten = $("#login");
    butten.after("<input type=\"text\" id=\"chat\">");
    $("#send").show();
    $('#uname').remove();
    $("#login").remove();

    // Spawn the socket
    var addr = window.location.host + '?username=' + username;
    if(window.location.protocol == "http"){
      addr = 'ws://' + addr;
    }
    else{
      addr = 'ws://' + addr;
    }
    ws = new WebSocket(addr);
    ws.id = username;
    ws.onmessage = function(message){
      var data = JSON.parse(message.data);
      $("#chatter").after("<p>" + data.username + ": " + data.message + "</p>");
    };
    ws.onopen = function(){
      this.send(this.id + " signing on");
    }
  });

  $("#send").click(function(){
    event.preventDefault();
    var text = $("#chat").val();
    if(text.length == 0){
      return
    }
    ws.send(text);
  });
});
