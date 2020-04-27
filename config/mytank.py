#!/usr/bin/env python

# #define API_KEY   "1c90a0dc-0c8c-439f-b97b-a600d67a451a"

import requests
from requests.exceptions import HTTPError
from http.server import HTTPServer, SimpleHTTPRequestHandler
from arduinosonar import ModuleSONAR
from arduinocore import ModuleCORE
from arduino import arduinoModule
from httpcom import myHandler

PORT_NUMBER = 8000

mynumber = 0
line =""

def main():
    global mynumber
    global line
    print('mytank start')
    #response = requests.post('http://192.168.1.13/test',  data=[('apikey', '1c90a0dc-0c8c-439f-b97b-a600d67a451a'),('command', 'set_servo_speed'),('param', '1500')])
    #json_response = response.json()
    #print(json_response['status'])
    #print(json_response['value'])

    Arduino = []

    Arduino.append(arduinoModule('/dev/ttyUSB0'))
    Arduino.append(arduinoModule('/dev/ttyUSB1'))

#    Arduino_B = arduinoModule('/dev/ttyUSB1')

#    if Arduino_B.isOpen== False:
#        return

    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print ('Started httpserver on port ' , PORT_NUMBER)
        
        #Wait forever for incoming htto requests
        #server.serve_forever()
        server.socket.settimeout(0)
        while True:
            server.handle_request()
            #check serial port HERE !
            if Arduino[0].isOpen:
                arduinoInfo = Arduino[0].processSerial()
                if ( arduinoInfo == "init"):    
                    if Arduino[0].id == "SONAR":
                        Arduino_SONAR.arduinoId = 0
                    if Arduino[0].id == "CORE":
                        Arduino_CORE.arduinoId = 0
            if Arduino[1].isOpen:
                arduinoInfo = Arduino[1].processSerial()
                if ( arduinoInfo == "init"):    
                    if Arduino[1].id == "SONAR":
                        Arduino_SONAR.arduinoId = 1
                    if Arduino[1].id == "CORE":
                        Arduino_CORE.arduinoId = 1


    except KeyboardInterrupt:
        print ('^C received, shutting down the web server')
        server.socket.close()
        ser.close()

if __name__ == '__main__':
    main()