/*
 

,
    data: { name: "John", location: "Boston" }

*/

//var controllers = {};


function sendGamePadInfos(axe0,axe1,axe2,axe3) {

  $.ajax({
    method: "POST",
    url: "http://mytank.home.lijah.net:8000/debug"
  })
    .done(function( msg ) {

    $("#view_debug").html(msg);
      
    });


}
