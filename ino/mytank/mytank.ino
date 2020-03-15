/*

 */

#include <SPI.h>
#include <Ethernet.h>

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network.
// gateway and subnet are optional:
byte mac[] = {
  0x00, 0xAA, 0xBB, 0xCC, 0xDE, 0x02
};
IPAddress ip(192, 168, 2, 150);
IPAddress myDns(192, 168, 2, 1);
IPAddress gateway(192, 168, 2, 1);
IPAddress subnet(255, 255, 0, 0);

EthernetServer server(80);
boolean debug = true;
int beatime = 0;
  
void setup() {
  // You can use Ethernet.init(pin) to configure the CS pin
  //Ethernet.init(10);  // Most Arduino shields
  //Ethernet.init(5);   // MKR ETH shield
  //Ethernet.init(0);   // Teensy 2.0
  //Ethernet.init(20);  // Teensy++ 2.0
  //Ethernet.init(15);  // ESP8266 with Adafruit Featherwing Ethernet
  //Ethernet.init(33);  // ESP32 with Adafruit Featherwing Ethernet

  // Open serial communications and wait for port to open:

  if (debug)
  {
    Serial.begin(9600);
    while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
    }
  }

  // start the Ethernet connection:
  if (debug)
    Serial.println("Trying to get an IP address using DHCP");
  if (Ethernet.begin(mac) == 0) {
    if (debug)
      Serial.println("Failed to configure Ethernet using DHCP");
    // Check for Ethernet hardware present
    if (Ethernet.hardwareStatus() == EthernetNoHardware) {
      if (debug)
        Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
      while (true) {
        delay(1); // do nothing, no point running without Ethernet hardware
      }
    }
    if (Ethernet.linkStatus() == LinkOFF) {
      if (debug)
        Serial.println("Ethernet cable is not connected.");
    }
    // initialize the Ethernet device not using DHCP:
    Ethernet.begin(mac, ip, myDns, gateway, subnet);
  }
  // print your local IP address:
  if (debug) 
  {
    Serial.print("My IP address: ");
    Serial.println(Ethernet.localIP());
  }
  // start listening for clients
  server.begin();
}

byte todolist_action[10] = { 0x00,0x00,0x00,0x00,0x00 };
int todolist_param[10] = { 0x00,0x00,0x00,0x00,0x00 };
int todolist_status[10] = { 0x00,0x00,0x00,0x00,0x00 };

// Action ARRAY
//
#define ACTION_MOVE   0
#define ACTION_SPEED  1
#define ACTION_ACS1   2    //  Accesory 1  ( Main linear actuator )
#define ACTION_ACS2   3    //  Accesory 2  ( Second group of linear actuators )

#define ACTION_STOP     1
#define ACTION_FORWARD  2
#define ACTION_BACCWARD 3

#define ACTION_UP     2    
#define ACTION_DOWN   3    



String processCommand(String topic) {
  if (debug)
    Serial.println(topic);

  int startcmd = topic.indexOf('=');
  int endcmd = topic.indexOf('&',startcmd);
  String cmd = topic.substring(startcmd+1,endcmd);

  startcmd = topic.indexOf('=',endcmd);
  String param = topic.substring(startcmd+1);

  if (cmd=="forward")
  {
      todolist_action[ACTION_MOVE] = ACTION_FORWARD;
      todolist_param[ACTION_MOVE] = param.toInt();
  }
  else if (cmd=="backward")
  {
      todolist_action[ACTION_MOVE] = ACTION_BACCWARD;
      todolist_param[ACTION_MOVE] = param.toInt();
  }
  else if (cmd=="stop")
  {
      todolist_action[ACTION_MOVE] = ACTION_STOP;
      todolist_param[ACTION_MOVE] = 0;
  }
  else if (cmd=="mainup")
  {
      todolist_action[ACTION_ACS1] = ACTION_UP;
      todolist_param[ACTION_ACS1] = param.toInt();
  }
  else if (cmd=="maindown")
  {
      todolist_action[ACTION_ACS1] = ACTION_DOWN;
      todolist_param[ACTION_ACS1] = param.toInt();
  }

    
  return("status:ok");
}

void checkTodoList() {

}

void checkSensors() {

}


void heartBeat() {
      if (debug)
        Serial.println("  * heartbeat *");
}


void loop() {
  char thisChar = 0x0D;
  String command=""; 

  // wait for a new client:
  EthernetClient client = server.available();

  // when the client sends the first byte, say hello:
  if (client) {
      while (client.connected()) {
        if (client.available()) {
          char c = client.read();
          //Serial.write(c);
          command+=c;  
          if (c == '\n' ) 
            command="";
        }
        else
        {
          String result="what";
          if (command.startsWith("command=")) 
            result = processCommand(command);
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/json");
          client.println("Connection: close");  // the connection will be closed after completion of the response
          client.println();
          client.print("{'result' : '");
          client.print(result);
          client.print("'}");
          break;          
        }
      }                
    
    delay(1);
    // close the connection:
    client.stop();
    }
    Ethernet.maintain();

    delay(2);

  checkTodoList();

  checkSensors();

  beatime++;
  if ( beatime > 2000 ) {
    heartBeat();
    beatime=0;
  }
    
}
