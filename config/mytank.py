#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import struct
from threading import Timer 
import os
import sys
from time import sleep
import requests
import serial
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

VERSION = '1.0.0'

ARDUINO_COM_PORT = "/dev/ttyUSB0"

retry_call = 0
runphase = 0

#Handler class for htpp request received

class myHandlerClass(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8") 

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("hi!"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(self._html("POST!"))

def on_timer():
    global retry_call
    global runphase
    print('time out')
    if runphase == 1 :
        print('runphase 1')


def read_serial(serport):
    #read incomming serial json from arduino
    line = serport.readline() 
    if line != b'':
        print('serial =')
        print(line)

def write_serial(serport):
    serport.write(b'f')

def main():
    
    try:
        print('mytank start')

        serport = serial.Serial(ARDUINO_COM_PORT, 38400, timeout=1)    

        print(f"open serial port {ARDUINO_COM_PORT}")

        httpserver_address = ("localhost", 8000)
        httpd = server_class(server_address, myHandlerClassS)

        print(f"Starting httpd server on localhost:8000")

        while True:
            #process serial in message
            read_serial(serport)
            httpd.handle_request()
            time.sleep(0.100)

    except KeyboardInterrupt: 
        print("End.")
    except:
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        serport.close()

if __name__ == "__main__":
    main()