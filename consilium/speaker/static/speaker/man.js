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
});
