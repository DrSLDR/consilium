$(document).ready(function(){
  // Spawn the socket
  var addr = window.location.host;
  if(window.location.protocol == "http"){
    addr = 'ws://' + addr;
  }
  else{
    addr = 'ws://' + addr;
  }
  ws = new WebSocket(addr);

  // Message retrieve
  ws.onmessage = function(message){
    console.log(message);
    var data = JSON.parse(message.data);
    if(data.method == 'add'){
      var list;
      if(data.queue == 1){
        list = $("#primary-list");
      }else{
        list = $("#secondary-list");
      }
      list.append('<p>' + data.speaker + '</p>')
    }
  };

  // Speak button
  $("#speak").click(function(){
    ws.send('speak');
  });
});
