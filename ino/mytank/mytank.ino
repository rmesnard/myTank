/*
Mytank
arduino controller for actuators and sensors
*/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>


Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x40);

unsigned long mytime;

byte todolist_action[10] = { 0x00,0x00,0x00,0x00,0x00 };
int todolist_param[10] = { 0x00,0x00,0x00,0x00,0x00 };
int todolist_time[10] = { 0x00,0x00,0x00,0x00,0x00 };


// Action ARRAY
//
#define ACTION_MOVE       0
#define ACTION_DIRECTION  1
#define ACTION_ACS1       2    //  Accesory 1  ( Main linear actuator )
#define ACTION_ACS2_A     3    //  Accesory 2  ( Linear actuator A )
#define ACTION_ACS2_B     4    //  Accesory 2  ( Linear actuator B )

#define ACTION_STOP       0
#define ACTION_FORWARD    2
#define ACTION_BACKWARD   3
#define ACTION_TURN_RIGHT 4
#define ACTION_TURN_LEFT  5


#define ACTION_UP     2    
#define ACTION_DOWN   3    

#define ACTION_SERVO_LEFT     1    
#define ACTION_SERVO_RIGHT    2

#define ACTION_SERVO_SPEEDSW  5
#define ACTION_VERIN1_UP      6
#define ACTION_VERIN2_UP      7
#define ACTION_VERIN3_UP      8
#define ACTION_VERIN1_DOWN    9
#define ACTION_VERIN2_DOWN    10
#define ACTION_VERIN3_DOWN    11

// Hardware
//
// PWM Servo  Library
//  SDA 20
//  SCL 21

// LEFT brake (servo)
#define SERVO_LEFT_PIN  0
#define SERVO_LEFT_MAX  370
#define SERVO_LEFT_MIN  150
// RIGHT brake (servo)
#define SERVO_RIGHT_PIN  1
#define SERVO_RIGHT_MAX  330
#define SERVO_RIGHT_MIN  550
// GEAR engage (servo)
#define SERVO_GEAR_PIN  3
#define SERVO_GEAR_MAX  550
#define SERVO_GEAR_MIN  150
// SPEED Variator (servo)
#define SERVO_SPEED_PIN  5
#define SERVO_SPEED_MAX  550
#define SERVO_SPEED_MIN  150
// SPEED Switch LOW - HIGHT  (motor)
#define MOTOR_SPEEDSW_PINA  42
#define MOTOR_SPEEDSW_PINB  43
// RFU  (motor)
#define MOTOR_RFU_PINA  44
#define MOTOR_RFU_PINB  45
// ACCESSORY 1  (Linear Actuator)
#define LINEA_ACS1_PINA  35
#define LINEA_ACS1_PINB  34
// ACCESSORY 2  (Linear Actuator A)
#define LINEA_ACS2_PINA  41
#define LINEA_ACS2_PINB  40
#define LINEB_ACS2_TIME  3000
#define LINEB_ACS2_PINA  39
#define LINEB_ACS2_PINB  38
#define LINEA_ACS2_TIME  3000
// ACCESSORY RFU  (Linear Actuator)
#define LINEA_RFU_PINA  37
#define LINEA_RFU_PINB  36

// CONTACT ON OFF General (key)
#define RELAY_POWER_PIN     33
// FORWARD - BACKWARD (relay default forward)
#define RELAY_DIRECTION_PIN 32
// CONTACT ON OFF sur Gear Bx
#define RELAY_GEAR_PIN     31
// CONTACT RFU RELAY
#define RELAY_RFU_PIN     30

#define IDLE_TIME         5000

bool power_is_on=false;
bool gear_is_on=false;
bool going_forward=true;
int speedpercent=0;

bool stringComplete=false;
String serialcommand=""; 
int serialcommandLen =0;
bool datachange = true;
String currmsg ="ok";
  
void setup() {

  // Open serial communications and wait for port to open:

  Serial.begin(115200);
  while (!Serial) {
  ; // wait for serial port to connect. Needed for native USB port only
  }

  // Setup Hardware
  pinMode(RELAY_POWER_PIN, OUTPUT);
  pinMode(RELAY_DIRECTION_PIN, OUTPUT);
  pinMode(RELAY_GEAR_PIN, OUTPUT);
  pinMode(RELAY_RFU_PIN, OUTPUT);

  digitalWrite(RELAY_POWER_PIN, HIGH);
  digitalWrite(RELAY_DIRECTION_PIN, HIGH);
  digitalWrite(RELAY_GEAR_PIN, HIGH);
  digitalWrite(RELAY_RFU_PIN, HIGH);

  pinMode(MOTOR_SPEEDSW_PINA, OUTPUT);
  pinMode(MOTOR_SPEEDSW_PINB, OUTPUT);
  pinMode(MOTOR_RFU_PINA, OUTPUT);
  pinMode(MOTOR_RFU_PINB, OUTPUT);

  digitalWrite(MOTOR_SPEEDSW_PINA, LOW);
  digitalWrite(MOTOR_SPEEDSW_PINB, LOW);
  digitalWrite(MOTOR_RFU_PINA, LOW);
  digitalWrite(MOTOR_RFU_PINB, LOW);

  pinMode(LINEA_ACS1_PINA, OUTPUT);
  pinMode(LINEA_ACS1_PINB, OUTPUT);
  digitalWrite(LINEA_ACS1_PINA, LOW);
  digitalWrite(LINEA_ACS1_PINB, LOW);
 
  pinMode(LINEA_ACS2_PINA, OUTPUT);
  pinMode(LINEA_ACS2_PINB, OUTPUT);
  digitalWrite(LINEA_ACS2_PINA, LOW);
  digitalWrite(LINEA_ACS2_PINB, LOW);

  pinMode(LINEB_ACS2_PINA, OUTPUT);
  pinMode(LINEB_ACS2_PINB, OUTPUT);
  digitalWrite(LINEB_ACS2_PINA, LOW);
  digitalWrite(LINEB_ACS2_PINB, LOW);

  pinMode(LINEB_ACS2_PINA, OUTPUT);
  pinMode(LINEB_ACS2_PINB, OUTPUT);
  digitalWrite(LINEB_ACS2_PINA, LOW);
  digitalWrite(LINEB_ACS2_PINB, LOW);
  
  pwm1.begin();  
  pwm1.setPWMFreq(60);

  // move servo to HOME position
 pwm1.setPWM(SERVO_SPEED_PIN, 0, SERVO_SPEED_MIN);
 pwm1.setPWM(SERVO_LEFT_PIN, 0, SERVO_LEFT_MIN);
 pwm1.setPWM(SERVO_RIGHT_PIN, 0, SERVO_RIGHT_MIN);     
 pwm1.setPWM(SERVO_GEAR_PIN, 0, SERVO_GEAR_MIN);     

  
}

void set_speed(int percent)
{
    int myspeed = map(percent,0,100,SERVO_SPEED_MIN,SERVO_SPEED_MAX);
    pwm1.setPWM(SERVO_SPEED_PIN, 0, myspeed);
    speedpercent = percent;
}

void set_gear(bool isOn)
{
  if ( isOn )
  {
    pwm1.setPWM(SERVO_GEAR_PIN, 0, SERVO_GEAR_MAX);
    digitalWrite(RELAY_GEAR_PIN, LOW);
  }
  else
  {
    pwm1.setPWM(SERVO_GEAR_PIN, 0, SERVO_GEAR_MIN);
    digitalWrite(RELAY_GEAR_PIN, HIGH);
  }
  gear_is_on =isOn;
}


void processCommand() {
  int offset =0;
  String mycmd="";
  String myparamA="";
  String myparamB="";
  char mychar;

  while (offset < serialcommandLen)
  {
    if ( serialcommand.charAt(offset++) == '>')
      break;
  }
  
  while (offset < serialcommandLen)
  {
    mychar= serialcommand.charAt(offset++); 
    if ( mychar == ':')
      break;
    mycmd+= mychar;
  }
  
  while(offset < serialcommandLen)
  {
    mychar= serialcommand.charAt(offset++);
    if ( mychar == ':')
      break;
    myparamA+= mychar;
  }

  while(offset < serialcommandLen)
  {
    mychar= serialcommand.charAt(offset++);
    if ( mychar == '.')
      break;
    myparamB+= mychar;
  }
  
  if (mycmd=="forward")
  {
      todolist_action[ACTION_MOVE] = ACTION_FORWARD;
      todolist_param[ACTION_MOVE] = myparamA.toInt();   // Set speed
      todolist_time[ACTION_MOVE] = myparamB.toInt();    // Set duration
  }
  else if (mycmd=="backward")
  {
      todolist_action[ACTION_MOVE] = ACTION_BACKWARD;
      todolist_param[ACTION_MOVE] = myparamA.toInt();   // Set speed
      todolist_time[ACTION_MOVE] = myparamB.toInt();    // Set duration
  }
  else if (mycmd=="left")
  {
      todolist_action[ACTION_DIRECTION] = ACTION_TURN_LEFT;
      todolist_param[ACTION_DIRECTION] = myparamA.toInt();   // Set minimum speed
      todolist_time[ACTION_DIRECTION] = myparamB.toInt();    // Set duration
  }
  else if (mycmd=="right")
  {
      todolist_action[ACTION_DIRECTION] = ACTION_TURN_RIGHT;
      todolist_param[ACTION_DIRECTION] = myparamA.toInt();   // Set minimum speed
      todolist_time[ACTION_DIRECTION] = myparamB.toInt();    // Set duration
  }
  else if (mycmd=="stop")
  {
      todolist_action[ACTION_MOVE] = ACTION_STOP;
      todolist_param[ACTION_MOVE] = 0;
      todolist_time[ACTION_MOVE] = 0; 
      set_speed(0);
      set_gear(false);
  }
  else if (mycmd=="mainup")
  {
      todolist_action[ACTION_ACS1] = ACTION_UP;
      todolist_param[ACTION_ACS1] = myparamA.toInt();
  }
  else if (mycmd=="maindown")
  {
      todolist_action[ACTION_ACS1] = ACTION_DOWN;
      todolist_param[ACTION_ACS1] = myparamA.toInt();
  }
  else if (mycmd=="power")
  {
    if( myparamA=="on")
    { 
      digitalWrite(RELAY_POWER_PIN, HIGH);
      power_is_on=true;
      currmsg="ok";
    }
    else if( myparamA=="off")
    { 
      digitalWrite(RELAY_POWER_PIN, LOW);
      power_is_on=false;
      currmsg="ok";
    }
  }
  else if (mycmd=="gear")
  {
    if( myparamA=="on")
    { 
      pwm1.setPWM(SERVO_GEAR_PIN, 0, SERVO_GEAR_MAX);
      gear_is_on=true;
      currmsg="ok_gear_on";
    }
    else if( myparamA=="off")
    { 
      pwm1.setPWM(SERVO_GEAR_PIN, 0, SERVO_GEAR_MIN);
      gear_is_on=false;
      currmsg="ok_gear_off";
    }
  }  
  else if (mycmd=="speed")
  {
    set_speed(myparamA.toInt());
    currmsg="ok_speed";
  }  
  else if (mycmd=="set_servo_left")
  {
    Serial.print("debug set_servo_left : ");
    Serial.println(myparamA.toInt());
    pwm1.setPWM(SERVO_LEFT_PIN, 0, myparamA.toInt());
    
    currmsg="ok_set_servo_left";
  }
  else if (mycmd=="set_servo_right")
  {
    Serial.print("debug set_servo_right : ");
    Serial.println(myparamA.toInt());
    pwm1.setPWM(SERVO_RIGHT_PIN, 0, myparamA.toInt());
    
    currmsg="ok_set_servo_right"; 
  }
  else if (mycmd=="set_servo_gear")
  {
    Serial.print("debug set_servo_gear : ");
    Serial.println(myparamA.toInt());
    pwm1.setPWM(SERVO_GEAR_PIN, 0, myparamA.toInt());
    
    currmsg="ok_set_servo_gear";      
  }
  else if (mycmd=="set_servo_speed")
  {
    Serial.print("debug speed : ");
    Serial.println(myparamA);
    pwm1.setPWM(SERVO_SPEED_PIN, 0, myparamA.toInt());
    
    currmsg="ok_set_servo_speed";
  }
  else if (mycmd=="set_linea_acs1_A")
  {
      todolist_action[ACTION_ACS1] = HIGH;
      todolist_param[ACTION_ACS1] = myparamA.toInt();
  }
  else if (mycmd=="set_linea_acs2_A")
  {
      todolist_action[ACTION_ACS2_A] = HIGH;
      todolist_param[ACTION_ACS2_A] = myparamA.toInt();
  }
  else if (mycmd=="set_linea_acs2_B")
  {
      todolist_action[ACTION_ACS2_B] = HIGH;
      todolist_param[ACTION_ACS2_B] = myparamA.toInt();
  }
  
  datachange=true;    
}


unsigned long timeSpend() {

unsigned long newtime = millis();

if ( newtime > mytime )
  return( newtime - mytime );
else
  return( newtime );

}

void checkTodoList() {

  // Do moves
  do_moves();

}

void do_reverse(bool newdirection)
{
  if ( going_forward != newdirection )
  {
    set_gear(false);
    set_speed(0);
    delay(500); // time to stop before reverse
    if ( newdirection )
      digitalWrite(RELAY_DIRECTION_PIN, LOW);  // default relay position is forward
    else
      digitalWrite(RELAY_DIRECTION_PIN, HIGH);
    set_gear(true);
    going_forward=newdirection;
  }
  else
    set_gear(true);
}

void brake_left(bool goleft)
{
  if ( goleft )
    pwm1.setPWM(SERVO_LEFT_PIN, 0, SERVO_LEFT_MAX);
  else
    pwm1.setPWM(SERVO_LEFT_PIN, 0, SERVO_LEFT_MIN);
}

void brake_right(bool goright)
{
  if ( goright )
    pwm1.setPWM(SERVO_RIGHT_PIN, 0, SERVO_RIGHT_MAX);
  else
    pwm1.setPWM(SERVO_RIGHT_PIN, 0, SERVO_RIGHT_MIN);
}

void engage(int newspeed)
{
  if ( !gear_is_on )
    set_gear(true);
  if ( speedpercent == 0 )    
    set_speed(newspeed);
}

void do_moves()
{
  byte myaction = todolist_action[ACTION_MOVE];
  
  bool dobrake = true;
  
  if ( myaction == ACTION_FORWARD )
  {
    do_reverse(true);
    brake_left(false);
    brake_right(false);
    set_speed(todolist_param[ACTION_MOVE]);
  }
  if ( myaction == ACTION_BACKWARD )
  {
    do_reverse(false);
    brake_left(false);
    brake_right(false);
    set_speed(todolist_param[ACTION_MOVE]);
  }

  if ( myaction != 0 )
  {
    int todotime = todolist_time[ACTION_MOVE];
    todotime = todotime - (int)timeSpend();
    if ( todotime < 0 )
    {
      todotime=0;
      todolist_action[ACTION_MOVE]=0;
      dobrake = true;
      todolist_time[ACTION_MOVE] = IDLE_TIME;
    }
    else
    {
      dobrake = false;
      todolist_time[ACTION_MOVE] = todotime;
    }
  }

  myaction = todolist_action[ACTION_DIRECTION];

  if ( myaction == ACTION_TURN_LEFT )
  {
    engage(todolist_param[ACTION_DIRECTION]);
    brake_right(false);
    brake_left(true);
  }
  if ( myaction == ACTION_TURN_RIGHT )
  {
    engage(todolist_param[ACTION_DIRECTION]);
    brake_right(true);
    brake_left(false);
  }

  if ( myaction != 0 )
  {
    int todotime = todolist_time[ACTION_DIRECTION];
    todotime = todotime - (int)timeSpend();
    if ( todotime < 0 )
    {
      todotime=0;
      todolist_action[ACTION_DIRECTION]=0;
      myaction=0;
    }
    todolist_time[ACTION_DIRECTION] = todotime;
  }
  
  if ( myaction == 0 )
  {
      if ( dobrake )
      {
      brake_left(true);
      brake_right(true);
      }
      else
      {
      brake_left(false);
      brake_right(false);
      }
  }
  
  byte idle = todolist_action[ACTION_MOVE] + todolist_action[ACTION_DIRECTION];

  if ( idle == 0 )
  {
    int todotime = todolist_time[ACTION_MOVE];
    todotime = todotime - (int)timeSpend();
    if ( todotime < 0 )
    {
      todotime=0;
      set_speed(0);
      set_gear(false);
    }
    todolist_time[ACTION_MOVE] = todotime;
  }
  
}


void checkSensors() {

}


void sendSensors()
{

  Serial.print("{\"id\":\"CORE\"");

  Serial.print(",\"status\":\"");
  Serial.print(currmsg);
  Serial.print("\",\"speed\":");
  Serial.print(speedpercent);
  if ( power_is_on )
    Serial.print(",\"power\":\"on\"");
  else
    Serial.print(",\"power\":\"off\"");
  if ( gear_is_on )
    Serial.print(",\"gear\":\"on\"");
  else
    Serial.print(",\"gear\":\"off\"");

  Serial.println("} ");
  datachange = false;
}

void loop() {
  mytime = millis();

  delay(100);

  checkTodoList();
  checkSensors();

  if (datachange)
    sendSensors();

  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if ( serialcommandLen < 100 )
    {
    serialcommand += inChar;
    serialcommandLen++;
    }
    if (inChar == '.') {
      stringComplete = true;
    }
  }

   if ( stringComplete )
   {
    processCommand();
    serialcommand="";
    serialcommandLen=0;
    stringComplete=false;
   }
    
}
