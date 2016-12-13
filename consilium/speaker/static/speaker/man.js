$(document).ready(function(){
  // Capture item id
  var iid = $("#meeting-item-id").val();

  // Hide the add-speaker field
  $("#manual-add-name").parent().hide();

  // Hide the strike-speaker confirmation buttons
  $("#strike-confirm").hide();
  $("#manual-strike-confirm").hide();

  // Hide the end-meeting confirmations
  $("#end-meeting-confirm").hide();

  // Hide start-meeting field
  $("#start-meeting-name").parent().hide();

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
    else if(data.method == 'end'){
      location.reload(true);
    }
  };

  // Speak button
  $("#speak").click(function(){
    ws.send('speak::' + iid);
  });

  // Strike button
  $("#strike").click(function(){
    // Wake the confirmation buttons
    $("#strike-confirm").slideDown(250, function(){
      // Rebrand the strike button
      var orig_text = $("#strike").text();
      $("#strike").attr("disabled", true).text("Bekräfta strykning?")

      // Shared tasks between buttons
      var common_tasks = function(){
        // Strip listeners
        $("#strike-confirm-yes").off();
        $("#strike-confirm-no").off();
        // Hide and reset
        $("#strike-confirm").slideUp(250, function(){
          $("#strike").attr("disabled", false).text(orig_text);
        });
      }

      // Start listening on the confirm buttons
      $("#strike-confirm-yes").click(function(){
        // Run the common tasks
        common_tasks();
        // Pass data to WebSocket
        ws.send('strike::' + iid);
      });
      $("#strike-confirm-no").click(function(){
        // Run the common tasks
        common_tasks();
      });
    });
  });

  // Next speaker button
  $("#next").click(function(){
    ws.send('next::' + iid);
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
      ws.send('new:' + data + ':' + iid);
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
        // Strip listeners
        $("#manual-strike-confirm-yes").off();
        $("#manual-strike-confirm-no").off();
        // Hide and reset
        $("#manual-strike-confirm").slideUp(250, function(){
          $("#manual-strike").attr("disabled", false).text(orig_text);
        });
      }

      // Start listening on the confirm buttons
      $("#manual-strike-confirm-yes").click(function(){
        // Run the common tasks
        common_tasks();
        // Pass data to WebSocket
        ws.send('kill:' + target.text() + ':' + iid);
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
  
  // End meeting button
  $("#end-meeting").click(function(){
    // Wake the confirmation buttons
    $("#end-meeting-confirm").slideDown(250, function(){
      // Rebrand the end-meeting button
      var orig_text = $("#end-meeting").text();
      $("#end-meeting").attr("disabled", true).text("Bekräfta Avslut?")

      // Shared tasks between buttons
      var common_tasks = function(){
        // Strip listeners
        $("#end-meeting-confirm-yes").off();
        $("#end-meeting-confirm-no").off();
        // Hide and reset
        $("#end-meeting-confirm").slideUp(250, function(){
          $("#end-meeting").attr("disabled", false).text(orig_text);
        });
      }

      // Start listening on the confirm buttons
      $("#end-meeting-confirm-yes").click(function(){
        // Run the common tasks
        common_tasks();
        // Pass data to WebSocket
        ws.send('end-meeting::' + iid);
      });
      $("#end-meeting-confirm-no").click(function(){
        // Run the common tasks
        common_tasks();
      });
    });
  });

  // Function for use by the add-meeting event handlers
  var try_add_meeting = function(){
    var data = $("#start-meeting-name").val();
    if(data.length > 0){
      // Pass to WebSocket
      ws.send('open:' + data + ':');
    } // If the string is empty, do nothing
  }

  // Add speaker button
  $("#start-meeting").click(function(){
    // Show the text field and focus
    $("#start-meeting-name").parent().slideDown(250, function(){
      $("#start-meeting-name").focus();
    });
    // Call the handler, in case the button was re-used
    try_add_meeting()
  });

  // Listener for the enter key on add-speaker text field
  $("#start-meeting-name").on("keypress", function(e){
    if(e.which == 13){
      try_add_meeting();
    }
  });

});
