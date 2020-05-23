from http.server import HTTPServer, SimpleHTTPRequestHandler
from arduino import arduinoModule
from tankobj import tank

class myHandler(SimpleHTTPRequestHandler):


    #Handler for the GET requests
    def do_GET(self):
        

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message

        self.wfile.write(b"Hello World ! %d" % self.server.tank.temp)
        

