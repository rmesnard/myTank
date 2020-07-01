/*
 * Gamepad API Test
 * Written in 2013 by Ted Mielczarek <ted@mielczarek.org>
 *
 * To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this software to the public domain worldwide. This software is distributed without any warranty.
 *
 * You should have received a copy of the CC0 Public Domain Dedication along with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
 */
var haveEvents = 'GamepadEvent' in window;
var haveWebkitEvents = 'WebKitGamepadEvent' in window;
var controllers = {};


var rAF = window.mozRequestAnimationFrame ||
  window.webkitRequestAnimationFrame ||
  window.requestAnimationFrame;

function connecthandler(e) {
  addgamepad(e.gamepad);
}

function addgamepad(gamepad) {
  controllers[gamepad.index] = gamepad; 

  $("#button_gamepad").css("background", "Blue");
  

  rAF(updateStatus);
}

function disconnecthandler(e) {
  $("#button_gamepad").css("background", "Grey");
  
  removegamepad(e.gamepad);
}

function removegamepad(gamepad) {

  delete controllers[gamepad.index];
}

function updateStatus() {
  scangamepads();

// TODO select gamepad to use in config

  for (j in controllers) {
    var controller = controllers[j];
   // var d = document.getElementById("controller" + j);
   // var gamebuttons = d.getElementsByClassName("gamebutton");

   if (typeof controller.buttons !== 'undefined') {

   //alert ( controller.id );
    for (var i=0; i<controller.buttons.length; i++) {
  //    var b = gamebuttons[i];
      var val = controller.buttons[i];
      var pressed = val == 1.0;
      if (typeof(val) == "object") {
        pressed = val.pressed;
        val = val.value;
      }
      var pct = Math.round(val * 100) + "%";
      //b.style.backgroundSize = pct + " " + pct;
      if (pressed) {
        $("#game_button_debug").html("gamebutton pressed " + i);
        sendButton(i);
      } 
      /*
        IPEGA 9023

        0 - A
        1 - B
        2 - X
        3 - Y

        4 - L
        5 - R
        6 - L2
        7 - R2

        12 - Cross up
        13 - Cross down
        14 - Cross left
        15 - Cross right

        Axe

        0 - Left X 
        1 - Left Y
        2 - Right X
        3 - Right Y

      */
    }


      $("#game_axe0_debug").html("axe 0  = " + Math.round(controller.axes[0] * 100) + "%");
      $("#game_axe1_debug").html("axe 1  = " + Math.round(controller.axes[1] * 100) + "%");
      $("#game_axe2_debug").html("axe 2  = " + Math.round(controller.axes[2] * 100) + "%");
      $("#game_axe3_debug").html("axe 3  = " + Math.round(controller.axes[3] * 100) + "%");

      sendMoves(Math.round(controller.axes[0] * 100),Math.round(controller.axes[1] * 100),Math.round(controller.axes[2] * 100),Math.round(controller.axes[3] * 100));

  }
  }
  rAF(updateStatus);
}

function scangamepads() {
  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
  for (var i = 0; i < gamepads.length; i++) {
    if (gamepads[i]) {
      if (!(gamepads[i].index in controllers)) {
        addgamepad(gamepads[i]);
      } else {
        controllers[gamepads[i].index] = gamepads[i];
      }
    }
  }
}


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



if (haveEvents) {
  window.addEventListener("gamepadconnected", connecthandler);
  window.addEventListener("gamepaddisconnected", disconnecthandler);
} else if (haveWebkitEvents) {
  window.addEventListener("webkitgamepadconnected", connecthandler);
  window.addEventListener("webkitgamepaddisconnected", disconnecthandler);
} else {
  setInterval(scangamepads, 500);
}

$(function(){

$( "#button_main" ).click(function() {
  twPleinEcran();
});

$( "#button_gamepad" ).click(function() {
  $("#gamepad_pop").toggle();
});
  
$( "#button_debug" ).click(function() {
  sendMoves(10,10,10,10);
});
  
$( "#button_settings" ).click(function() {
  window.location.href = 'settings';
});
});

$(document).ready(function() {

  $('body').bootstrapMaterialDesign();

});