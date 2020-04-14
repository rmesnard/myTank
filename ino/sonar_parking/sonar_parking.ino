
#include <FastLED.h>

FASTLED_USING_NAMESPACE

/*
Information obtained:
16 bits total not including start 
bits 14-16   always  000
bit 13    0 for front 1 for rear ( part of sensor id )
bit 12    0 for valid data present 
bits 9-11 ( + bit 13 )
    sensor A  0
    sensor B  8
    sensor C  4
    sensor D  12
    sensor E  1
    sensor F  9
    sensor G  5
    sensor H  13
    
Blue connected alone :  EFGH  ( 4 Front )  Connect to +12v Always
Green connected with or without blue:  ABCD EH  ( 2 Front + 4 Rear )  controlled by optocopler to send +12v


*/

int pin = 7;
int pinStopA = 6;
int pinStopB = 8;
int greenPin = 5;
int dataOffset = 0;

bool isforward = true;
#define DATA_SIZE 17
unsigned long pulse_length;
byte distances[8]; 
byte pulse_value[DATA_SIZE];          
byte temp = 0;
bool datachange = true;
String currmsg ="";
int safetystopA = 0;
int safetystopB = 0;

bool stringComplete=false;
String serialcommand=""; 
int serialcommandLen =0;

#define DATA_PIN    4
#define LED_TYPE    WS2812
#define COLOR_ORDER GRB
#define NUM_LEDS    256
#define NUM_PANEL   4
CRGB leds[NUM_LEDS];
#define BRIGHTNESS          50
uint8_t gHue = 0; // rotating "base color" used by many of the patterns
bool gphase=true;
byte motifselected[NUM_PANEL];
byte animselected[NUM_PANEL];
byte colorselected[NUM_PANEL];

#define ANIM_NONE     0
#define ANIM_BLINK    1
#define ANIM_MOVE     2

#define MOTIF_NONE          0
#define MOTIF_FULL          1
#define MOTIF_LARROW_A      2
#define MOTIF_LARROW_B      3
#define MOTIF_RARROW_A      4
#define MOTIF_RARROW_B      5

#define COLOR_ORANGE        2
#define COLOR_RED           3
#define COLOR_BLUE          4
#define COLOR_GREEN         5
#define COLOR_WHITE         6
#define COLOR_PINK          7



const PROGMEM char motifTable[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,   // MOTIF_NONE
                                    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,   // MOTIF_FULL   
                                    0x18, 0x3C, 0x7E, 0xFF, 0x18, 0x18, 0x18, 0x18,   // MOTIF_LARROW_A
                                    0x00, 0x00, 0x00, 0x00, 0x18, 0x3C, 0x7E, 0xFF,   // MOTIF_LARROW_B
                                    0x18, 0x18, 0x18, 0x18, 0xFF, 0x7E, 0x3C, 0x18,   // MOTIF_RARROW_A
                                    0xFF, 0x7E, 0x3C, 0x18, 0x00, 0x00, 0x00, 0x00,   // MOTIF_RARROW_B
                                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

void setup()
{
pinMode(pin, INPUT);
pinMode(pinStopA, INPUT);
pinMode(pinStopB, INPUT);
pinMode(greenPin, OUTPUT);

for ( int i=0; i< NUM_PANEL; i++)
  {
  animselected[i]=ANIM_NONE;
  motifselected[i]=MOTIF_NONE;
  }

// enable 4 rear and 2 front sensors by default
digitalWrite(greenPin, LOW);

// enable 4 front sensors
//digitalWrite(greenPin, HIGH);

FastLED.addLeds<LED_TYPE,DATA_PIN,COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
FastLED.setBrightness(BRIGHTNESS);

Serial.begin(115200);
currmsg="STARTED";
sendSensors();

led_display(COLOR_BLUE,0,MOTIF_FULL);
delay(300);
led_display(COLOR_BLUE,1,MOTIF_FULL);
delay(300);
led_display(COLOR_BLUE,2,MOTIF_FULL);
delay(300);
led_display(COLOR_BLUE,3,MOTIF_FULL);
delay(1000);
FastLED.clear();
FastLED.show();

}

void led_print(int startled,CRGB mycolor,byte motifidx)
{
    int x,y;
    byte set;
    byte thebit;
    int pixelnum=startled;

    for (x=0; x < 8; x++) {
        for (y=0; y < 8; y++) {
            thebit = pgm_read_byte_near(motifTable + ( motifidx * 8 ) + x );
            set = thebit & 1 << y;
            if ( set != 0 )
              leds[pixelnum]=mycolor;
            else
              leds[pixelnum]=CRGB::Black;
            pixelnum++;
        }
    }
}


void led_display(byte selcolor,byte panelNum,byte motif)
{
  CRGB mycolor;
  if ( selcolor == COLOR_ORANGE )
    mycolor = CRGB::Orange;
  if ( selcolor == COLOR_RED )
    mycolor = CRGB::Red;
  if ( selcolor == COLOR_BLUE )
    mycolor = CRGB::Blue;
  if ( selcolor == COLOR_WHITE )
    mycolor = CRGB::White;
  if ( selcolor == COLOR_PINK )
    mycolor = CRGB::Pink;
  
  int startpanel = panelNum*64;
     
  led_print(startpanel,mycolor,motif);
    
  FastLED.show();
}


void led_clear(byte panelNum)
{
  int startpanel = panelNum*64;
  int endpanel = (panelNum + 1)*64;
  for ( int iled = startpanel ;iled < endpanel; iled++ ) 
    leds[iled] = CRGB::Black;
  FastLED.show();
}


void setDistance(byte sensorIdx,byte newdistance)
{
  if ( distances[sensorIdx] != newdistance )
  {
    datachange = true;
    distances[sensorIdx] = newdistance ;
  }
}

void sendSensors()
{

  Serial.print("{\"id\":\"SONAR\"");

  if (isforward)
    Serial.print(",\"mode\":\"F\"");
  else
    Serial.print(",\"mode\":\"B\"");

  Serial.print(",\"status\":\"");
  Serial.print(currmsg);
  Serial.print("\",");

  Serial.print("\"stopA\":");
  Serial.print(safetystopA);
  Serial.print(",\"stopB\":");
  Serial.print(safetystopB);

  for( int i=0; i <8; i++)
  {
    Serial.print(",");
    Serial.print("\"");
    Serial.print(char(i+'A'));
    Serial.print("\":");
    Serial.print(distances[i]);
    
  }

  Serial.println("} ");
  datachange = false;
}

void processCMD()
{
//print as sensor id and distance -- valid data only

if ( (pulse_value[0] == 1 )&(pulse_value[14] == 0 )&(pulse_value[15] == 0 )&(pulse_value[16] == 0 ) )   //data valid
  {

    if ( pulse_value[12] == 1) // distance info valid 
    {

    byte sensor_id = 0;   //will hold sensor id bin
    if (pulse_value[13]==1) bitSet(sensor_id,0);
    if (pulse_value[11]==1) bitSet(sensor_id,1);
    if (pulse_value[10]==1) bitSet(sensor_id,2);
    if (pulse_value[9]==1) bitSet(sensor_id,3);
    byte sensor_dist_c = 0;  //will hold sensor distance
    if (pulse_value[8]==1) bitSet(sensor_dist_c,7);
    if (pulse_value[7]==1) bitSet(sensor_dist_c,6);
    if (pulse_value[6]==1) bitSet(sensor_dist_c,5);
    if (pulse_value[5]==1) bitSet(sensor_dist_c,4);
    if (pulse_value[4]==1) bitSet(sensor_dist_c,3);
    if (pulse_value[3]==1) bitSet(sensor_dist_c,2);
    if (pulse_value[2]==1) bitSet(sensor_dist_c,1);
    if (pulse_value[1]==1) bitSet(sensor_dist_c,0);

    if (sensor_id == 0) 
      setDistance(0,sensor_dist_c);
    if (sensor_id == 8)  
      setDistance(1,sensor_dist_c);
    if (sensor_id == 4)  
      setDistance(2,sensor_dist_c);
    if (sensor_id == 12) 
      setDistance(3,sensor_dist_c);
    if (sensor_id == 1)  
      setDistance(4,sensor_dist_c);
    if (sensor_id == 9)  
      setDistance(5,sensor_dist_c);
    if (sensor_id == 5)  
      setDistance(6,sensor_dist_c);
    if (sensor_id == 13)  
      setDistance(7,sensor_dist_c);
  
    }
    
    else
    {
      // reset sensor values
      for( int i=0; i <8; i++)
      {
        if ( distances[i] != 0)
          datachange = true;
        distances[i]=0;
        
      }
      
    }
  currmsg="OK";
  } 
else
  {
    currmsg="INVALID DATA";
    /*
    Serial.print("INVALID DATA : ");
    for( int i=0; i <DATA_SIZE; i++)
      Serial.print(pulse_value[i]);
    Serial.println(".");
    */
  }
}

void readSensors()
  {
    if (pulse_length > 800) {           //start pulse
      dataOffset=0;
   // Serial.println(".");
      pulse_value[dataOffset] = 1;
    }
    else if (pulse_length < 300) 
      pulse_value[dataOffset] = 1;
    else 
      pulse_value[dataOffset] = 0;
  
    // Debug pulse
   // if (pulse_length != 0) 
   //   Serial.print(pulse_value[dataOffset]);
  
    dataOffset++;
    // Command Completed 
    if (dataOffset == DATA_SIZE )
    {
      dataOffset = 0; 
      processCMD();
    }
  }
  
void processSERIAL()
{

    int offset =0;
    String mycmd="";
    String myparamA="";
    String myparamB="";
    String myparamC="";
    String myparamD="";
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
      if ( mychar == ':')
        break;
      myparamB+= mychar;
    }

    while(offset < serialcommandLen)
    {
      mychar= serialcommand.charAt(offset++);
      if ( mychar == ':')
        break;
      myparamC+= mychar;
    }
    
    while(offset < serialcommandLen)
    {
      mychar= serialcommand.charAt(offset++);
      if ( mychar == '.')
        break;
      myparamD+= mychar;
    }
  
    if (mycmd=="backward") {
      // Backward
      // enable 4 rear sensors
      isforward=false;
      digitalWrite(greenPin, HIGH);
      sendSensors();
    }
    if (mycmd=="forward") {
      // Forward
      // enable 4 front and 2 front sensors
      isforward=true;
      digitalWrite(greenPin, LOW);
      sendSensors();
    }
    if (mycmd == "led") {
      byte numpanel = byte(myparamA.toInt());
      byte motif = byte(myparamB.toInt());
      if ( motif != MOTIF_NONE ){
        byte anim = byte(myparamC.toInt());
        byte color = byte(myparamD.toInt());
        animselected[numpanel]=anim;
        motifselected[numpanel]=motif;
        colorselected[numpanel]=color;
        }
      else
        {
        animselected[numpanel]=ANIM_NONE;
        motifselected[numpanel]=MOTIF_NONE;
        colorselected[numpanel]=0;
        led_clear(numpanel);
        }
    }
}

void AnimLeds()
{

for ( byte i=0; i< NUM_PANEL; i++)
  {
    if (( animselected[i] == ANIM_BLINK ) &  (gphase) )
      {
        led_clear(i);
      }
    else if (( animselected[i] == ANIM_MOVE ) &  (gphase) )
      {
        motifselected[i]++; 
        led_display(colorselected[i],i,motifselected[i]);
        motifselected[i]--;        
      }      
    else 
    {
        led_display(colorselected[i],i,motifselected[i]);
    }   
  }

if (  gphase  )
  gphase=false;
else
 gphase=true;
  
}

void loop(){
  
  pulse_length = pulseIn(pin, HIGH);

  if (pulse_length != 0) // Data Received
    readSensors();

  int stopStatus = digitalRead(pinStopA);

  if ( safetystopA != stopStatus )
  {
    safetystopA = stopStatus;
    datachange = true;
  }

  stopStatus = digitalRead(pinStopB);

  if ( safetystopB != stopStatus )
  {
    safetystopB = stopStatus;
    datachange = true;
  }

  if (datachange)
    sendSensors();


  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if ( serialcommandLen < 50 )
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
    processSERIAL();
    serialcommand="";
    serialcommandLen=0;
    stringComplete=false;
   }

  AnimLeds();  

}
