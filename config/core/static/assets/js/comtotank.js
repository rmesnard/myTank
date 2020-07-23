/*
 

,
    data: { name: "John", location: "Boston" }

*/

//var controllers = {};


function sendMoves(axe0,axe1,axe2,axe3) {

  if ((axe0 == 0 ) & (axe1 == 0) & (axe2 == 0) & (axe3 == 0) & (window.lastaxe0 == 0 ) & (window.lastaxe1 == 0) & (window.lastaxe2 == 0) & (window.axelastaxe3 == 0) )
    return;

  $.ajax({
    url: '/ajax/sendmove',
    data: {
      'axe0': axe0,
      'axe1': axe1,
      'axe2': axe2,
      'axe3': axe3
    },
    dataType: 'json',
    success: function (data) {
      
      $("#view_debug").html(data.dgb_text);
      
    }
  });

  window.lastaxe0 = axe0;
  window.lastaxe1 = axe1;
  window.lastaxe2 = axe2;
  window.lastaxe3 = axe3;


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