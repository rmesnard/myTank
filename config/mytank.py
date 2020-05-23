#!/usr/bin/env python

# #define API_KEY   "1c90a0dc-0c8c-439f-b97b-a600d67a451a"

import requests
from requests.exceptions import HTTPError
from http.server import HTTPServer, SimpleHTTPRequestHandler
from arduino import arduinoModule
from tankobj import tank
from httpcom import myHandler

PORT_NUMBER = 8000

mynumber = 0
line =""

Arduino = []
theTank = tank()

def processEngine():
    global Arduino
    global theTank

    theTank.gear = Arduino[theTank.CORE_Id].gear
    theTank.hum = Arduino[theTank.CORE_Id].hum
    theTank.temp = Arduino[theTank.CORE_Id].temp
    theTank.pitch = Arduino[theTank.CORE_Id].pitch
    theTank.roll = Arduino[theTank.CORE_Id].roll
    theTank.yaw = Arduino[theTank.CORE_Id].yaw
    theTank.power = Arduino[theTank.CORE_Id].power
    theTank.speed = Arduino[theTank.CORE_Id].speed
    theTank.sonar_mode = Arduino[theTank.SONAR_Id].sonar_mode
    theTank.sonar_A = Arduino[theTank.SONAR_Id].sonar_A
    theTank.sonar_B = Arduino[theTank.SONAR_Id].sonar_B
    theTank.sonar_C = Arduino[theTank.SONAR_Id].sonar_C
    theTank.sonar_D = Arduino[theTank.SONAR_Id].sonar_D
    theTank.sonar_E = Arduino[theTank.SONAR_Id].sonar_E
    theTank.sonar_F = Arduino[theTank.SONAR_Id].sonar_F
    theTank.sonar_G = Arduino[theTank.SONAR_Id].sonar_G
    theTank.sonar_H = Arduino[theTank.SONAR_Id].sonar_H
    theTank.stopA = Arduino[theTank.SONAR_Id].stopA
    theTank.stopB = Arduino[theTank.SONAR_Id].stopB

    theTank.calculatePosition()


def sendUpdatetoServer():
    global Arduino
    #response = requests.post('http://127.0.0.1/test',  data=[('apikey', '1c90a0dc-0c8c-439f-b97b-a600d67a451a'),('command', 'set_servo_speed'),('param', '1500')])
    #json_response = response.json()

def main():
    global mynumber
    global line
    global Arduino
    global theTank
    print('mytank start')

    #response = requests.post('http://192.168.1.13/test',  data=[('apikey', '1c90a0dc-0c8c-439f-b97b-a600d67a451a'),('command', 'set_servo_speed'),('param', '1500')])
    #json_response = response.json()
    #print(json_response['status'])
    #print(json_response['value'])

    Arduino.append(arduinoModule('/dev/ttyUSB0'))
    Arduino.append(arduinoModule('/dev/ttyUSB1'))

#    Arduino_B = arduinoModule('/dev/ttyUSB1')

#    if Arduino_B.isOpen== False:
#        return

    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        server.tank = theTank
        print ('Started httpserver on port ' , PORT_NUMBER)
        
        #Wait forever for incoming htto requests
        #server.serve_forever()
        server.socket.settimeout(0)
        while True:
            updateNeedeed=False
            server.handle_request()
            #check serial port HERE !
            if Arduino[0].isOpen:
                arduinoInfo = Arduino[0].processSerial()
                if ( arduinoInfo == "init"):    
                    if Arduino[0].id == "SONAR":
                        theTank.SONAR_Id = 0
                    if Arduino[0].id == "CORE":
                        theTank.CORE_Id = 0
                if ( arduinoInfo != ""):
                    updateNeedeed = True             
            if Arduino[1].isOpen:
                arduinoInfo = Arduino[1].processSerial()
                if ( arduinoInfo == "init"):    
                    if Arduino[1].id == "SONAR":
                        theTank.SONAR_Id = 1
                    if Arduino[1].id == "CORE":
                        theTank.CORE_Id = 1
                if ( arduinoInfo != ""):
                    updateNeedeed = True               

            if ( updateNeedeed  ):
                sendUpdatetoServer()
            processEngine()
            server.tank = theTank                

    except KeyboardInterrupt:
        print ('stop received, shutting down the web server')
        server.socket.close()
        

if __name__ == '__main__':
    main()