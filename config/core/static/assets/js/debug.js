
$( "#button_main" ).click(function() {
  twPleinEcran();
});

$( "#button_refresh" ).click(function() {
  window.location.reload(true);
});

$( "#button_gamepad" ).click(function() {
  window.location.href = 'index';
});


$(document).ready(function() {

  $('body').bootstrapMaterialDesign();


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