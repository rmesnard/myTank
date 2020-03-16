/*
Mytank
arduino ethenet controller for actuators and sensors
*/

#include <SPI.h>
#include <Ethernet.h>
#include <Servo.h>

#define API_KEY   "1c90a0dc-0c8c-439f-b97b-a600d67a451a"
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
unsigned long beatime = 0;

unsigned long mytime;


byte todolist_action[10] = { 0x00,0x00,0x00,0x00,0x00 };
int todolist_param[10] = { 0x00,0x00,0x00,0x00,0x00 };
int todolist_status[10] = { 0x00,0x00,0x00,0x00,0x00 };

// Action ARRAY
//
#define ACTION_MOVE     0
#define ACTION_SPEED    1
#define ACTION_ACS1     2    //  Accesory 1  ( Main linear actuator )
#define ACTION_ACS2_A   3    //  Accesory 2  ( Linear actuator A )
#define ACTION_ACS2_B   4    //  Accesory 2  ( Linear actuator B )

#define ACTION_STOP     1
#define ACTION_FORWARD  2
#define ACTION_BACCWARD 3

#define ACTION_UP     2    
#define ACTION_DOWN   3    

#define ACTION_SERVO_LEFT     1    
#define ACTION_SERVO_RIGHT    2
#define ACTION_SERVO_GEAR     3
#define ACTION_SERVO_SPEED    4
#define ACTION_SERVO_SPEEDSW  5
#define ACTION_VERIN1_UP      6
#define ACTION_VERIN2_UP      7
#define ACTION_VERIN3_UP      8
#define ACTION_VERIN1_DOWN    9
#define ACTION_VERIN2_DOWN    10
#define ACTION_VERIN3_DOWN    11

// Hardware
//
// PWM 0 a 13
// Ethernet Use 10,11,12,13

// LEFT brake (servo)
#define SERVO_LEFT_PIN  9
#define SERVO_LEFT_MAX  359
#define SERVO_LEFT_MIN  1500
// RIGHT brake (servo)
#define SERVO_RIGHT_PIN  8
#define SERVO_RIGHT_MAX  359
#define SERVO_RIGHT_MIN  1500
// GEAR engage (servo)
#define SERVO_GEAR_PIN  7
#define SERVO_GEAR_MAX  359
#define SERVO_GEAR_MIN  1500
// SPEED Switch LOW - HIGHT  (servo)
#define SERVO_SPEEDSW_PIN  6
#define SERVO_SPEEDSW_MAX  359
#define SERVO_SPEEDSW_MIN  1500
// SPEED Variator (servo)
#define SERVO_SPEED_PIN  5
#define SERVO_SPEED_MAX  359
#define SERVO_SPEED_MIN  1500
// ACCESSORY 1  (Linear Actuator)
#define LINEA_ACS1_PINA  43
#define LINEA_ACS1_PINB  42
// ACCESSORY 2  (Linear Actuator A)
#define LINEA_ACS2_PINA  41
#define LINEA_ACS2_PINB  40
#define LINEB_ACS2_PINA  39
#define LINEB_ACS2_PINB  38
#define LINEA_ACS2_TIME  3000
#define LINEA_ACS2_TIME  3000
// FORWARD - BACKWARD (relay default forward)
#define RELAY_DIRECTION_PIN 45
// CONTACT ON OFF 
#define RELAY_ONOFF_PIN     44

bool power_is_on=false;
bool going_forward=true;

Servo myservo_LEFT;  
Servo myservo_RIGHT;  
Servo myservo_GEAR;  
Servo myservo_SPEEDSW;  
Servo myservo_SPEED;  
  
void setup() {
  // You can use Ethernet.init(pin) to configure the CS pin
  //Ethernet.init(10);  // Most Arduino shields

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

  // Setup Hardware
  pinMode(RELAY_ONOFF_PIN, OUTPUT);
  pinMode(RELAY_DIRECTION_PIN, OUTPUT);

  myservo_LEFT.attach(SERVO_LEFT_PIN);  
  myservo_RIGHT.attach(SERVO_RIGHT_PIN);  
  myservo_GEAR.attach(SERVO_GEAR_PIN);  
  myservo_SPEEDSW.attach(SERVO_SPEEDSW_PIN);  
  myservo_SPEED.attach(SERVO_SPEED_PIN);  

  // move servo to HOME position
  myservo_LEFT.writeMicroseconds(SERVO_LEFT_MIN);          
  myservo_RIGHT.writeMicroseconds(SERVO_RIGHT_MIN);          
  myservo_GEAR.writeMicroseconds(SERVO_GEAR_MIN);          
  myservo_SPEEDSW.writeMicroseconds(SERVO_SPEEDSW_MIN);          
  myservo_SPEED.writeMicroseconds(SERVO_SPEED_MIN);          
  
}



String processCommand(String topic) {
  if (debug)
    Serial.println(topic);

  int startcmd = topic.indexOf('=');
  int endcmd = topic.indexOf('&',startcmd);
  String cmd = topic.substring(startcmd+1,endcmd);

  if ( String(API_KEY) != cmd )
      return("{\"status\":\"not authorized\"}");
      
  startcmd = topic.indexOf('=',endcmd);
  endcmd = topic.indexOf('&',startcmd);
  cmd = topic.substring(startcmd+1,endcmd);
      
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
  else if (cmd=="power")
  {
    if( param=="ON")
    { 
      digitalWrite(RELAY_ONOFF_PIN, HIGH);
      power_is_on=true;
      return("{\"status\":\"power\",\"value\":\"on\"}");
    }
    else if( param=="OFF")
    { 
      digitalWrite(RELAY_ONOFF_PIN, LOW);
      power_is_on=false;
      return("{\"status\":\"power\",\"value\":\"off\"}");
    }
  }
  else if (cmd=="set_servo_left")
  {
    myservo_LEFT.writeMicroseconds(param.toInt());          
  }
  else if (cmd=="set_servo_right")
  {
    myservo_RIGHT.writeMicroseconds(param.toInt());          
  }
  else if (cmd=="set_servo_gear")
  {
    myservo_GEAR.writeMicroseconds(param.toInt());          
  }
  else if (cmd=="set_servo_speed")
  {
      myservo_SPEED.writeMicroseconds(param.toInt()); 
  }
  else if (cmd=="set_servo_speedswitch")
  {
      myservo_SPEEDSW.writeMicroseconds(param.toInt());            
  }
  else if (cmd=="set_linea_acs1_A")
  {
      todolist_action[ACTION_ACS1] = HIGH;
      todolist_param[ACTION_ACS1] = param.toInt();
  }
  else if (cmd=="set_linea_acs2_A")
  {
      todolist_action[ACTION_ACS2_A] = HIGH;
      todolist_param[ACTION_ACS2_A] = param.toInt();
  }
  else if (cmd=="set_linea_acs2_B")
  {
      todolist_action[ACTION_ACS2_B] = HIGH;
      todolist_param[ACTION_ACS2_B] = param.toInt();
  }
      
  return("{\"status\":\"ok\"}");
}


unsigned long timeSpend() {

unsigned long newtime = millis();

if ( newtime > mytime )
  return( newtime - mytime );
else
  return( newtime );

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
  mytime = millis();
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
          String result="{\"status\":\"what\"}";
          if (command.startsWith("apikey=")) 
            result = processCommand(command);
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: application/json");
          client.println("Connection: close");  // the connection will be closed after completion of the response
          client.println();
          client.println(result);
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

  beatime += timeSpend();
  
  if ( beatime > 3000 ) {
    heartBeat();
    beatime=0;
  }
    
}
