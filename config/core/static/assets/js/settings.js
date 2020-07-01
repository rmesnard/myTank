
$( "#button_main" ).click(function() {
  twPleinEcran();
});

$( "#button_refresh" ).click(function() {
  window.location.reload(true);
});

$( "#button_gamepad" ).click(function() {
  window.location.href = 'index';
});

$( "#button_debug" ).click(function() {
  window.location.href = 'debug';
});

$( "#btn_steplus" ).click(function() {
  var stepval = parseInt($("#steptime" ).val());
  stepval+=10;
  $("#steptime" ).val(stepval.toString());
});

$( "#btn_stepmoins" ).click(function() {
  var stepval = parseInt($("#steptime" ).val());
  stepval-=10;
  $("#steptime" ).val(stepval.toString());
});


$( "#btn_anticolplus" ).click(function() {
  var stepval = parseInt($("#anticollisiondistance" ).val());
  stepval+=10;
  $("#anticollisiondistance" ).val(stepval.toString());
});

$( "#btn_anticolmoins" ).click(function() {
  var stepval = parseInt($("#anticollisiondistance" ).val());
  stepval-=10;
  $("#anticollisiondistance" ).val(stepval.toString());
});


$( "#btn_idleplus" ).click(function() {
  var stepval = parseInt($("#idletime" ).val());
  stepval+=10;
  $("#idletime" ).val(stepval.toString());
});

$( "#btn_idlemoins" ).click(function() {
  var stepval = parseInt($("#idletime" ).val());
  stepval-=10;
  $("#idletime" ).val(stepval.toString());
});

$( "#btn_secureenab" ).click(function() {
  if ( $("#secureenabled" ).val() == 1 )
  {
    $("#secureenabled" ).val(0);
    $("#btn_secureenab" ).css("background", "Red");
    $("#btn_secureenab").find("i").html("close");
  }
  else
  {
    $("#secureenabled" ).val(1);
    $("#btn_secureenab" ).css("background", "Green");
    $("#btn_secureenab").find("i").html("done");
  }
});

$(document).ready(function() {

  $('body').bootstrapMaterialDesign();

  if ( $("#secureenabled" ).val() == 1 )
  {
    $("#btn_secureenab" ).css("background", "Green");
    $("#btn_secureenab").find("i").html("done");
  }
  else
  {
    $("#btn_secureenab" ).css("background", "Red");
    $("#btn_secureenab").find("i").html("close");
  }

});


function twPleinEcran(_element) {
  var monElement = _element||document.documentElement;

  if (document.fullscreenElement) {
if (!document.fullscreenElement) {
      monElement.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  }
  if (document.webkitFullscreenEnabled) {
if (!document.webkitFullscreenElement) {
      monElement.webkitRequestFullscreen();
    } else {
      document.webkitExitFullscreen();
    }
  }
  if (document.msFullscreenEnabled) {
if (!document.msFullscreenElement) {
      monElement.msRequestFullscreen();
    } else {
      document.msExitFullscreen();
    }
  }
};