/*
 

,
    data: { name: "John", location: "Boston" }

*/

//var controllers = {};


function sendMoves(axe0,axe1,axe2,axe3) {

  $.ajax({
    url: '/ajax/sendmove',
    data: {
      'axe0': axe0
    },
    dataType: 'json',
    success: function (data) {
      
      $("#view_debug").html(data.dgb_text);
      
    }
  });


}

function sendButton(buttonclicked) {

  $.ajax({
    url: '/ajax/sendbutton',
    data: {
      'buttonclicked': buttonclicked
    },
    dataType: 'json',
    success: function (data) {
      
      $("#view_debug").html(data.dgb_text);
      
    }
  });


}