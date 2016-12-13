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
    var list;
    if(data.queue == 1){
      list = $("#primary-list");
    }else{
      list = $("#secondary-list");
    }
    if(data.method == 'add'){
      list.append('<p>' + data.speaker + '</p>')
    }
    else if(data.method == 'strike'){
      list.children().filter('p:contains(' + data.speaker +')').remove();
    }
  };

  // Speak button
  $("#speak").click(function(){
    ws.send('speak');
  });

  // Strike button
  $("#strike").click(function(){
    ws.send('strike');
  });

  // Next speaker button
  $("#next").click(function(){
    ws.send('next');
  });
});
