#!/usr/bin/env python

import requests
from requests.exceptions import HTTPError
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT_NUMBER = 8000

mynumber = 0

class myHandler(SimpleHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        global mynumber
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(b"Hello World ! %i" % mynumber)



def main():
    global mynumber
    print('mytank start')
    #response = requests.post('http://192.168.1.13/test',  data=[('apikey', '1c90a0dc-0c8c-439f-b97b-a600d67a451a'),('command', 'set_servo_speed'),('param', '1500')])
    #json_response = response.json()
    #print(json_response['status'])
    #print(json_response['value'])

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
            mynumber+=1
            if mynumber > 1024:
                mynumber=0

    except KeyboardInterrupt:
        print ('^C received, shutting down the web server')
        server.socket.close()

if __name__ == '__main__':
    main()