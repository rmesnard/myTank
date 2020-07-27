#!/usr/bin/env python

# #define API_KEY   "1c90a0dc-0c8c-439f-b97b-a600d67a451a"
import socket 

from http.server import HTTPServer, SimpleHTTPRequestHandler
from arduino import *
from tankobj import *
from httpcom import *
from json import JSONEncoder
import json

PORT_NUMBER = 8000

mynumber = 0
line =""



def main():
    global mynumber
    global line
    print('mytank start')


    try:

        server = HTTPServer(('', PORT_NUMBER), myHandler)
        server.tank = tank()

 

        server.tank.Arduino.append(arduinoModule('/dev/ttyUSB0'))
        server.tank.Arduino.append(arduinoModule('/dev/ttyUSB1'))

        #Create a web server and define the handler to manage the
        #incoming request
        print ('Started httpserver on port ' , PORT_NUMBER)
        
        #Wait forever for incoming htto requests
        #server.serve_forever()
        server.socket.settimeout(0)
        while True:
            updateNeedeed=False
            server.handle_request()
            #check serial port HERE !
            if server.tank.Arduino[0].isOpen:
                arduinoInfo = server.tank.Arduino[0].processSerial()
                if ( arduinoInfo == "init"):    
                    if server.tank.Arduino[0].id == "SONAR":
                        server.tank.SONAR_Id = 0
                    if server.tank.Arduino[0].id == "CORE":
                        server.tank.CORE_Id = 0
                if ( arduinoInfo != ""):
                    updateNeedeed = True             
            if server.tank.Arduino[1].isOpen:
                arduinoInfo = server.tank.Arduino[1].processSerial()
                if ( arduinoInfo == "init"):    
                    if server.tank.Arduino[1].id == "SONAR":
                        server.tank.SONAR_Id = 1
                    if server.tank.Arduino[1].id == "CORE":
                        server.tank.CORE_Id = 1
                if ( arduinoInfo != ""):
                    updateNeedeed = True               

            server.tank.processEngine()
            if updateNeedeed and server.tank.server_ready:
                server.tank.sendUpdatetoServer()
            if server.tank.server_ready:
                server.tank.process_todolist()         

    except KeyboardInterrupt:
        print ('stop received, shutting down the web server')
        server.socket.close()
        

if __name__ == '__main__':
    main()