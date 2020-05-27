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


theTank = tank()


def processEngine():

    global theTank

    theTank.gear = theTank.Arduino[theTank.CORE_Id].gear
    theTank.hum = theTank.Arduino[theTank.CORE_Id].hum
    theTank.temp = theTank.Arduino[theTank.CORE_Id].temp
    theTank.pitch = theTank.Arduino[theTank.CORE_Id].pitch
    theTank.roll = theTank.Arduino[theTank.CORE_Id].roll
    theTank.yaw = theTank.Arduino[theTank.CORE_Id].yaw
    theTank.power = theTank.Arduino[theTank.CORE_Id].power
    theTank.speed = theTank.Arduino[theTank.CORE_Id].speed
    theTank.sonar_mode = theTank.Arduino[theTank.SONAR_Id].sonar_mode
    theTank.sonar_A = theTank.Arduino[theTank.SONAR_Id].sonar_A
    theTank.sonar_B = theTank.Arduino[theTank.SONAR_Id].sonar_B
    theTank.sonar_C = theTank.Arduino[theTank.SONAR_Id].sonar_C
    theTank.sonar_D = theTank.Arduino[theTank.SONAR_Id].sonar_D
    theTank.sonar_E = theTank.Arduino[theTank.SONAR_Id].sonar_E
    theTank.sonar_F = theTank.Arduino[theTank.SONAR_Id].sonar_F
    theTank.sonar_G = theTank.Arduino[theTank.SONAR_Id].sonar_G
    theTank.sonar_H = theTank.Arduino[theTank.SONAR_Id].sonar_H
    theTank.stopA = theTank.Arduino[theTank.SONAR_Id].stopA
    theTank.stopB = theTank.Arduino[theTank.SONAR_Id].stopB

    theTank.calculatePosition()


def sendUpdatetoServer():
    #print('sendUpdatetoServer')
    #response = requests.post('http://127.0.0.1/test',  data=[('apikey', '1c90a0dc-0c8c-439f-b97b-a600d67a451a'),('command', 'set_servo_speed'),('param', '1500')])
    #json_response = response.json()
    return

def main():
    global mynumber
    global line
    global theTank
    print('mytank start')

    #response = requests.post('http://192.168.1.13/test',  data=[('apikey', '1c90a0dc-0c8c-439f-b97b-a600d67a451a'),('command', 'set_servo_speed'),('param', '1500')])
    #json_response = response.json()
    #print(json_response['status'])
    #print(json_response['value'])

    theTank.Arduino.append(arduinoModule('/dev/ttyUSB0'))
    theTank.Arduino.append(arduinoModule('/dev/ttyUSB1'))

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
            if theTank.Arduino[0].isOpen:
                arduinoInfo = theTank.Arduino[0].processSerial()
                if ( arduinoInfo == "init"):    
                    if theTank.Arduino[0].id == "SONAR":
                        theTank.SONAR_Id = 0
                    if theTank.Arduino[0].id == "CORE":
                        theTank.theTank.CORE_Id = 0
                if ( arduinoInfo != ""):
                    updateNeedeed = True             
            if theTank.Arduino[1].isOpen:
                arduinoInfo = theTank.Arduino[1].processSerial()
                if ( arduinoInfo == "init"):    
                    if theTank.Arduino[1].id == "SONAR":
                        theTank.SONAR_Id = 1
                    if theTank.Arduino[1].id == "CORE":
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