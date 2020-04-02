import os
import json
import serial

class arduinoModule():
    
    
    def __init__(self,COMPORT):
        self.isOpen = False
        self.status =""
        self.id =""
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
            self.processLine(newline)

    def processLine(self,cmdline):
        #parse JSON
        # print ('data %s' % cmdline)
        try:
            parsed_json = (json.loads(cmdline))
            print(json.dumps(parsed_json, indent=4, sort_keys=True))
        except:
            print ('Invalid data from Arduino %s' % cmdline)
        
        self.status = parsed_json['status']

        if ( self.id==""):
            self.id = parsed_json['id']
            return "init"

        return "update"

    def Flash(self):
        os.system("avrdude -C avrdude.conf -v -p atmega328p -c arduino -P /dev/ttyUSB0 -b 57600 -D -U flash:w:sonar_parking.ino.hex:i")

