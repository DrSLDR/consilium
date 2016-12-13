$(document).ready(function(){
  // Hide the add-speaker field
  $("#manual-add-name").parent().hide();

  // Hide the strike-speaker confirmation buttons
  $("#manual-strike-confirm").hide();

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

  // Function for use by the add-speaker event handlers
  var try_add_speaker = function(){
    var data = $("#manual-add-name").val();
    if(data.length > 0){
      // There was some name supplied. Clear the field
      $("#manual-add-name").val('');
      // Hide the input field
      $("#manual-add-name").parent().slideUp(250);
      // Pass to WebSocket
      ws.send('new:' + data);
    } // If the string is empty, do nothing
  }

  // Add speaker button
  $("#manual-add").click(function(){
    // Show the text field and focus
    $("#manual-add-name").parent().slideDown(250, function(){
      $("#manual-add-name").focus();
    });
    // Call the handler, in case the button was re-used
    try_add_speaker()
  });

  // Listener for the enter key on add-speaker text field
  $("#manual-add-name").on("keypress", function(e){
    if(e.which == 13){
      try_add_speaker();
    }
  });

  // Manual strike name-click listener
  var strike_click_listener = function(target){
    // Unmark all listed speakers and unbind listeners
    $("#primary-list").children().removeClass('text-danger').off();
    $("#secondary-list").children().removeClass('text-danger').off();

    // Mark the target
    target.addClass('bg-danger');

    // Wake the confirmation buttons
    $("#manual-strike-confirm").slideDown(250, function(){
      // Rebrand the manual strike button
      var orig_text = $("#manual-strike").text();
      $("#manual-strike").attr("disabled", true).text("Bekräfta Strykning?");

      // Shared tasks between buttons
      var common_tasks = function(){
        $("#manual-strike-confirm").slideUp(250, function(){
          $("#manual-strike").attr("disabled", false).text(orig_text);
        });
      }

      // Start listening on the confirm buttons
      $("#manual-strike-confirm-yes").click(function(){
        // Run the common tasks
        common_tasks();
        // Pass data to WebSocket
        ws.send('kill:' + target.text());
      });
      $("#manual-strike-confirm-no").click(function(){
        // Unmark the target
        target.removeClass('bg-danger');
        // Run the common tasks
        common_tasks();
      });
    });
  }

  // Manual strike button
  $("#manual-strike").click(function(){
    // Mark all listed speakers
    $("#primary-list").children().addClass('text-danger').click(function(){
      var target = $(this);
      strike_click_listener(target);
    });
    $("#secondary-list").children().addClass('text-danger').click(function(){
      var target = $(this);
      strike_click_listener($(this));
    });
  });
});
