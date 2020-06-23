

$( "#button_gamepad" ).click(function() {
  window.location.href = 'index';
});

$( "#steplus" ).click(function() {
  var stepval = parseInt($("#steptime" ).val());
  stepval+=10;
  $("#steptime" ).val(stepval.toString());
});

$( "#stepmoins" ).click(function() {
  var stepval = parseInt($("#steptime" ).val());
  stepval-=10;
  $("#steptime" ).val(stepval.toString());
});

$(document).ready(function() {

  $('body').bootstrapMaterialDesign();

});