from http.server import HTTPServer, SimpleHTTPRequestHandler
from arduino import *
from tankobj import *

class myHandler(SimpleHTTPRequestHandler):


    #Handler for the GET requests
    def do_GET(self):
        
        # print (self.path)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        if ( self.path == "/debug"):
            self.wfile.write(b"<body><table><tr><td>variable</td><td>value</td></tr>")
            self.wfile.write(b"<tr><td>temperature</td><td>%d</td></tr>" % self.server.tank.status.temp)
            self.wfile.write(b"<tr><td>humidity</td><td>%d</td></tr>" % self.server.tank.status.hum)
            self.wfile.write(b"<tr><td>pitch</td><td>%d</td></tr>" % self.server.tank.status.pitch)
            self.wfile.write(b"<tr><td>roll</td><td>%d</td></tr>" % self.server.tank.status.roll)
            self.wfile.write(b"<tr><td>yaw</td><td>%d</td></tr>" % self.server.tank.status.yaw)
            self.wfile.write(bytes("<tr><td>power</td><td>%s</td></tr>" % self.server.tank.status.power,"utf-8"))
            self.wfile.write(b"<tr><td>speed</td><td>%d </td></tr>" % self.server.tank.status.speed)
            self.wfile.write(bytes("<tr><td>sonar mode</td><td>%s</td></tr>" % self.server.tank.status.sonar_mode,"utf-8"))
            self.wfile.write(b"<tr><td>sonar A</td><td>%d </td></tr>" % self.server.tank.status.sonar_A)
            self.wfile.write(b"<tr><td>sonar B</td><td>%d </td></tr>" % self.server.tank.status.sonar_B)
            self.wfile.write(b"<tr><td>sonar C</td><td>%d </td></tr>" % self.server.tank.status.sonar_C)
            self.wfile.write(b"<tr><td>sonar D</td><td>%d </td></tr>" % self.server.tank.status.sonar_D)
            self.wfile.write(b"<tr><td>sonar E</td><td>%d </td></tr>" % self.server.tank.status.sonar_E)
            self.wfile.write(b"<tr><td>sonar F</td><td>%d </td></tr>" % self.server.tank.status.sonar_F)
            self.wfile.write(b"<tr><td>sonar G</td><td>%d </td></tr>" % self.server.tank.status.sonar_G)
            self.wfile.write(b"<tr><td>sonar H</td><td>%d </td></tr>" % self.server.tank.status.sonar_H)
            self.wfile.write(b"<tr><td>stop A</td><td>%d </td></tr>" % self.server.tank.status.stopA)
            self.wfile.write(b"<tr><td>stop B</td><td>%d </td></tr>" % self.server.tank.status.stopB)
            self.wfile.write(b"</table></body>")
        elif ( self.path.startswith("/command/forward/")):
            cmds = self.path.split("/")
            if (len(cmds)==5):
                self.wfile.write(bytes("forward %s %s" % (cmds[3],cmds[4]),"utf-8"))
                self.server.tank.cmd_forward(int(cmds[3]),int(cmds[4]))
        elif ( self.path.startswith("/command/backward/")):
            cmds = self.path.split("/")
            if (len(cmds)==5):
                self.wfile.write(bytes("backward %s %s" % (cmds[3],cmds[4]),"utf-8"))
                self.server.tank.cmd_backward(int(cmds[3]),int(cmds[4]))
        elif ( self.path.startswith("/command/left/")):
            cmds = self.path.split("/")
            if (len(cmds)==5):
                self.wfile.write(bytes("left %s %s" % (cmds[3],cmds[4]),"utf-8"))
                self.server.tank.cmd_left(int(cmds[3]),int(cmds[4]))
        elif ( self.path.startswith("/command/right/")):
            cmds = self.path.split("/")
            if (len(cmds)==5):
                self.wfile.write(bytes("right %s %s" % (cmds[3],cmds[4]),"utf-8"))
                self.server.tank.cmd_right(int(cmds[3]),int(cmds[4]))                
        elif ( self.path.startswith("/command/stop")):
            self.wfile.write(bytes("stop","utf-8"))
            self.server.tank.cmd_stop()        
        else:
            self.wfile.write(b"unknown command")
        

