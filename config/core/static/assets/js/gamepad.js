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

  // TODO select gamepad to use in config
  console.log("add gamepad");

  $("#joystick_available").html('<i class="material-icons">bluetooth_connected</i> ' + gamepad.id)

  $("#joystick_enabled").removeClass("card-header-warning");
  $("#joystick_enabled").addClass("card-header-success");
  $("#joystick_enabled").find("h3").html("Enabled");

  rAF(updateStatus);
}

function disconnecthandler(e) {
  $("#joystick_available").html('<i class="material-icons">bluetooth_connected</i>  Not available')
  $("#joystick_enabled").removeClass("card-header-success");
  $("#joystick_enabled").addClass("card-header-warning");
  $("#joystick_enabled").find("h3").html("Disabled");      

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
        //b.className = "gamebutton pressed";
        $("#joystick_enabled").find("h3").html("gamebutton pressed");
        console.log("gamebutton pressed:");
      } 
      /*
      else {
        alert( "gamebutton pressed " + i );
        //b.className = "gamebutton";
      }
      */
    }
    /*
    var axes = d.getElementsByClassName("axis");
    for (var i=0; i<controller.axes.length; i++) {
      var a = axes[i];
      a.innerHTML = i + ": " + controller.axes[i].toFixed(4);
      a.setAttribute("value", controller.axes[i]);
    }
    */
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

if (haveEvents) {
  window.addEventListener("gamepadconnected", connecthandler);
  window.addEventListener("gamepaddisconnected", disconnecthandler);
} else if (haveWebkitEvents) {
  window.addEventListener("webkitgamepadconnected", connecthandler);
  window.addEventListener("webkitgamepaddisconnected", disconnecthandler);
} else {
  setInterval(scangamepads, 500);
}
