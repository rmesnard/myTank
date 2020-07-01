from json import JSONEncoder
import json

class tank():
    
    
    def __init__(self):
        self.isRunning = False
        
        
        self.gear =""
        self.hum = 0
        self.temp = 0
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.power = ""
        self.speed = 0
        self.sonar_mode = ""
        self.sonar_A = 0
        self.sonar_B = 0
        self.sonar_C = 0
        self.sonar_D = 0
        self.sonar_E = 0
        self.sonar_F = 0
        self.sonar_G = 0
        self.sonar_H = 0
        self.stopA = 0
        self.stopB = 0

        self.Arduino = [] 

        self.SONAR_Id=-1
        self.CORE_Id=-1

    def calculatePosition(self):
        return

    def cmd_forward(self,speed,duration):
        #print("forward %i %i" % (speed,duration))
        self.Arduino[self.CORE_Id].sendcmd(">forward:%i:%i." % (speed,duration))
        return

    def cmd_backward(self,speed,duration):
        #print("backward %i %i" % (speed,duration))
        self.Arduino[self.CORE_Id].sendcmd(">backward:%i:%i." % (speed,duration))
        return

    def cmd_left(self,speed,duration):
        #print("left %i %i" % (speed,duration))
        self.Arduino[self.CORE_Id].sendcmd(">left:%i:%i." % (speed,duration))
        return

    def cmd_right(self,speed,duration):
        #print("right %i %i" % (speed,duration))
        self.Arduino[self.CORE_Id].sendcmd(">right:%i:%i." % (speed,duration))
        return        

    def cmd_stop(self):
        #print("stop")
        self.Arduino[self.CORE_Id].sendcmd(">stop:0:0.")
        return                

class tankEncoder(JSONEncoder):

    def default(self, object):

        if isinstance(object, tank):

            return object.__dict__

        else:

            # call base class implementation which takes care of

            # raising exceptions for unsupported types

            return json.JSONEncoder.default(self, object)        