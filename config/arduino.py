import os
import json
import serial

class arduinoModule():
    
    
    def __init__(self,COMPORT):
        self.isOpen = False
        self.status =""
        self.id =""
        self.gear =""
        self.hum = 0
        self.temp = 0
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.power = ""
        self.speed = 0
        self.sonar_mode = ""
        self.sonar_A = 0
        self.sonar_B = 0
        self.sonar_C = 0
        self.sonar_D = 0
        self.sonar_E = 0
        self.sonar_F = 0
        self.sonar_G = 0
        self.sonar_H = 0
        self.stopA = 0
        self.stopB = 0
        try:
            #open first serial port  '/dev/ttyUSB0'
            self.serial_Arduino = serial.Serial(COMPORT,115200, timeout=1)  # open serial 
            self.isOpen = True

        except:
            print ('ERROR openning Serial Port %s' % COMPORT)
            return

        print ('port %s open' % COMPORT)

    def processSerial(self):
        if self.serial_Arduino.in_waiting > 0:
            newline = self.serial_Arduino.readline()
            return self.processLine(newline)
        else:
            return ""

    def processLine(self,cmdline):
        #parse JSON
        # print ('data %s' % cmdline)
        notinit = False

        try:
            parsed_json = (json.loads(cmdline))
            #print(json.dumps(parsed_json, indent=4, sort_keys=True))
        except:
            print ('Invalid data from Arduino %s' % cmdline)
        
        self.status = parsed_json['status']

        if ( self.id==""):
            notinit = True

        #parse all attributes
        self.id = parsed_json['id']

        if ( self.id== "SONAR" ):
            self.sonar_mode = parsed_json['mode']
            self.sonar_A = parsed_json['A']
            self.sonar_B = parsed_json['B']
            self.sonar_C = parsed_json['C']
            self.sonar_D = parsed_json['D']
            self.sonar_E = parsed_json['E']
            self.sonar_F = parsed_json['F']
            self.sonar_G = parsed_json['G']
            self.sonar_H = parsed_json['H']
            self.stopA = parsed_json['stopA']
            self.stopB = parsed_json['stopB']


        if ( self.id== "CORE" ):
            self.gear = parsed_json['gear']
            self.hum = parsed_json['hum']
            self.temp = parsed_json['temp']
            self.pitch = parsed_json['pitch']
            self.roll = parsed_json['roll']
            self.yaw = parsed_json['yaw']
            self.power = parsed_json['power']
            self.speed = parsed_json['speed']

        if notinit:
            return "init"

        return "update"


    def Flash(self):
        os.system("avrdude -C avrdude.conf -v -p atmega328p -c arduino -P /dev/ttyUSB0 -b 57600 -D -U flash:w:sonar_parking.ino.hex:i")

