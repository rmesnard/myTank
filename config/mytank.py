#!/usr/bin/env python

# #define API_KEY   "1c90a0dc-0c8c-439f-b97b-a600d67a451a"
import socket 
import requests
from requests.exceptions import HTTPError
from http.server import HTTPServer, SimpleHTTPRequestHandler
from arduino import *
from tankobj import *
from httpcom import *
from json import JSONEncoder
import json

PORT_NUMBER = 8000

mynumber = 0
line =""


theTank = tank()


def processEngine():

    global theTank

    theTank.status.gear = theTank.Arduino[theTank.status.CORE_Id].gear
    theTank.status.hum = theTank.Arduino[theTank.status.CORE_Id].hum
    theTank.status.temp = theTank.Arduino[theTank.status.CORE_Id].temp
    theTank.status.pitch = theTank.Arduino[theTank.status.CORE_Id].pitch
    theTank.status.roll = theTank.Arduino[theTank.status.CORE_Id].roll
    theTank.status.yaw = theTank.Arduino[theTank.status.CORE_Id].yaw
    theTank.status.power = theTank.Arduino[theTank.status.CORE_Id].power
    theTank.status.speed = theTank.Arduino[theTank.status.CORE_Id].speed
    theTank.status.sonar_mode = theTank.Arduino[theTank.status.SONAR_Id].sonar_mode
    theTank.status.sonar_A = theTank.Arduino[theTank.status.SONAR_Id].sonar_A
    theTank.status.sonar_B = theTank.Arduino[theTank.status.SONAR_Id].sonar_B
    theTank.status.sonar_C = theTank.Arduino[theTank.status.SONAR_Id].sonar_C
    theTank.status.sonar_D = theTank.Arduino[theTank.status.SONAR_Id].sonar_D
    theTank.status.sonar_E = theTank.Arduino[theTank.status.SONAR_Id].sonar_E
    theTank.status.sonar_F = theTank.Arduino[theTank.status.SONAR_Id].sonar_F
    theTank.status.sonar_G = theTank.Arduino[theTank.status.SONAR_Id].sonar_G
    theTank.status.sonar_H = theTank.Arduino[theTank.status.SONAR_Id].sonar_H
    theTank.status.stopA = theTank.Arduino[theTank.status.SONAR_Id].stopA
    theTank.status.stopB = theTank.Arduino[theTank.status.SONAR_Id].stopB

    theTank.calculatePosition()


def sendUpdatetoServer():
    global theTank

    #print('sendUpdatetoServer')
    data = tankEncoder().encode(theTank.status)
    response = requests.post('http://' + theTank.host_ip + '/api/setstatus', data=json.dumps(data),headers={"Content-Type": "application/json"})
    json_response = response.json()
    #print(json_response['status'])
    return


def main():
    global mynumber
    global line
    global theTank
    print('mytank start')

    # getlocal IP for REST API
    theTank.host_name = "raspberry_django" 
    theTank.host_ip = "192.168.4.10"

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
                        theTank.status.SONAR_Id = 0
                    if theTank.Arduino[0].id == "CORE":
                        theTank.status.CORE_Id = 0
                if ( arduinoInfo != ""):
                    updateNeedeed = True             
            if theTank.Arduino[1].isOpen:
                arduinoInfo = theTank.Arduino[1].processSerial()
                if ( arduinoInfo == "init"):    
                    if theTank.Arduino[1].id == "SONAR":
                        theTank.status.SONAR_Id = 1
                    if theTank.Arduino[1].id == "CORE":
                        theTank.status.CORE_Id = 1
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