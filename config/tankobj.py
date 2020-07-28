from json import JSONEncoder
import json

import requests
from requests.exceptions import HTTPError

import logging
import time
from logging.handlers import RotatingFileHandler

class tankstatus():

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



class tanksettings():

    def __init__(self):
        self.step_time = 1000
        self.proximity_enabled = 1
        self.idle_time = 10000
        self.proximity_distance = 30
        self.log_level = 2

    def set(self,payload):
        self.step_time = int(payload['step_time'])
        self.idle_time = int(payload['idle_time'])
        self.log_level = int(payload['log_level'])
        self.proximity_enabled = int(payload['proximity_enabled'])
        self.proximity_distance = int(payload['proximity_distance'])

    def update(self,payload):
        self.step_time = int(payload['step_time'][0])
        self.idle_time = int(payload['idle_time'][0])
        self.log_level = int(payload['log_level'][0])
        self.proximity_enabled = int(payload['proximity_enabled'][0])
        self.proximity_distance = int(payload['proximity_distance'][0])


class tankstodo():

    def __init__(self):
        self.action = 0
        self.speed = 0
        self.duration = 0
        self.blocking = 0

        self.buttonpushed = 0
        self.axe0 = 0
        self.axe1 = 0
        self.axe2 = 0
        self.axe3 = 0

    def set(self,action,speed,duration,button,axe0,axe1,axe2,axe3,blocking):
        self.action = action
        self.speed = speed
        self.duration = duration

        self.buttonpushed = button
        self.axe0 = axe0
        self.axe1 = axe1
        self.axe2 = axe2
        self.axe3 = axe3

        self.blocking = blocking


    def isblocking(self):
        if self.blocking == 1 :
            return True
        return False


class tankstodolist():

    def __init__(self):
        self.queue = [] 
        self.position = 0

        for offset in range(1,30):
            todo = tankstodo()
            self.queue.append(todo) 

    def clean(self):
        for offset in range(1,30):
            self.queue[offset].action = 0
        self.position = 0

    def enqueue(self,action,speed,duration,button,axe0,axe1,axe2,axe3,blocking):
        
        # action 
        # 1 button pushed
        # 2 move

        offset = self.position + 1
        if (offset == 29):
            offset=0

        while offset != self.position:
            if self.queue[offset].action == 0:
                todo = tankstodo()
                todo.set(action,speed,duration,button,axe0,axe1,axe2,axe3,blocking)
                self.queue[offset] = todo
                break
            
            offset+=1
            if (offset == 29):
                offset=0



class tank():

    def __init__(self):
        self.isRunning = False

        self.initialized = False

        # getlocal IP for REST API
        self.host_name="raspberry_django"
        self.host_ip="192.168.4.10"

        self.status = tankstatus()
        self.settings = tanksettings()
        self.Arduino = [] 
        self.todolist = tankstodolist()

        self.SONAR_Id=-1
        self.CORE_Id=-1

        self.req_counter = 0

        self.logger = logging.getLogger("Rotating Log")
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        
        # add a rotating handler
        self.handler = RotatingFileHandler("tank.log",'a', 1000000, 1)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

        # getsettings
        self.getsettings()

        self.log('started',2)

    def log(self,message,level):
        if self.settings.log_level >= 0 and level == 0:
            self.logger.error(message)
        if self.settings.log_level > 0 and level == 1:
            self.logger.warning(message)
        if self.settings.log_level > 1 and level == 2:
            self.logger.info(message)
        if self.settings.log_level > 2 and level == 3:
            self.logger.debug(message)


    def getsettings(self):

        response = requests.post('http://' + self.host_ip + '/api/getsettings', headers={"Content-Type": "application/json"})

        self.settings.set(response.json())

        self.log('initialized',2)
        self.initialized = True        
        return


    def sendUpdatetoServer(self):

        data = tankEncoder().encode(self.status)
        response = requests.post('http://' + self.host_ip + '/api/setstatus', data=json.dumps(data),headers={"Content-Type": "application/json"})
        return


    def processEngine(self):

        self.status.gear = self.Arduino[self.CORE_Id].gear
        self.status.hum = self.Arduino[self.CORE_Id].hum
        self.status.temp = self.Arduino[self.CORE_Id].temp
        self.status.pitch = self.Arduino[self.CORE_Id].pitch
        self.status.roll = self.Arduino[self.CORE_Id].roll
        self.status.yaw = self.Arduino[self.CORE_Id].yaw
        self.status.power = self.Arduino[self.CORE_Id].power
        self.status.speed = self.Arduino[self.CORE_Id].speed
        self.status.sonar_mode = self.Arduino[self.SONAR_Id].sonar_mode
        self.status.sonar_A = self.Arduino[self.SONAR_Id].sonar_A
        self.status.sonar_B = self.Arduino[self.SONAR_Id].sonar_B
        self.status.sonar_C = self.Arduino[self.SONAR_Id].sonar_C
        self.status.sonar_D = self.Arduino[self.SONAR_Id].sonar_D
        self.status.sonar_E = self.Arduino[self.SONAR_Id].sonar_E
        self.status.sonar_F = self.Arduino[self.SONAR_Id].sonar_F
        self.status.sonar_G = self.Arduino[self.SONAR_Id].sonar_G
        self.status.sonar_H = self.Arduino[self.SONAR_Id].sonar_H
        self.status.stopA = self.Arduino[self.SONAR_Id].stopA
        self.status.stopB = self.Arduino[self.SONAR_Id].stopB
        return

    def calculatePosition(self):
        return

    def go_forward(self,speed,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">forward:%i:%i." % (speed,duration))
        return

    def go_backward(self,speed,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">backward:%i:%i." % (speed,duration))
        return

    def go_left(self,speed,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">left:%i:%i." % (speed,duration))
        return

    def go_right(self,speed,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">right:%i:%i." % (speed,duration))
        return        

    def crane_down(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">cranedown:%i." % (duration))
        return        

    def crane_up(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">craneup:%i." % (duration))
        return        

    def crane_extand(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">craneexand:%i." % (duration))
        return        

    def crane_retract(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">craneretract:%i." % (duration))
        return        

    def winch_up(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">winchup:%i." % (duration))
        return        

    def winch_down(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">winchdown:%i." % (duration))
        return   

    def main_up(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">mainup:%i." % (duration))
        return        

    def main_down(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">maindown:%i." % (duration))
        return     

    def side_up(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">sideup:%i." % (duration))
        return        

    def side_down(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">sidedown:%i." % (duration))
        return   

    def crane_rotate_left(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">rotatel:%i." % (duration))
        return        

    def crane_rotate_right(self,duration):
        
        self.Arduino[self.CORE_Id].sendcmd(">rotater:%i." % (duration))
        return   

    def cmd_stop(self):
        self.Arduino[self.CORE_Id].sendcmd(">stop:0:0.")
        return                

    def cmd_button(self,payload):
        buttonid = int(payload['buttonid'][0])
        self.log('receive button',2)
        self.log(buttonid,2)
        if (buttonid == 10):
            #STOP  button X
            self.cmd_stop()
            self.todolist.clean()
        else:
            duration = self.settings.step_time
            self.todolist.enqueue(1,0,self.settings.step_time,buttonid,0,0,0,0,0)

        return     

    def cmd_move(self,payload):
        axe0 = int(payload['axe0'][0])
        axe1 = int(payload['axe1'][0])
        axe2 = int(payload['axe2'][0])
        axe3 = int(payload['axe3'][0])

        duration = self.settings.step_time

        speed = 0

        self.req_counter = self.req_counter + 1
       
        return     

    def process_todolist(self):

        offset = self.todolist.position

        if self.todolist.queue[offset].action == 1:
            self.process_todo_button(self.todolist.queue[offset].buttonpushed)
        #elif self.queue[offset].action == 2:
        #    process_todo_move(self.queue[offset].buttonpushed)

        self.todolist.queue[offset].action == 0

        offset+=1
        if (offset == 29):
            offset=0

        self.todolist.position = offset

        return

    def process_todo_move(self,payload):
        axe0 = int(payload['axe0'][0])
        axe1 = int(payload['axe1'][0])
        axe2 = int(payload['axe2'][0])
        axe3 = int(payload['axe3'][0])
 

        duration = self.settings.step_time

        speed = 0

        if (axe3 > 0):
            #go forward
            speed = abs(axe3)
            self.go_forward(speed,duration)
        elif (axe3 < 0):
            #go backward
            speed = abs(axe3)
            self.go_backward(speed,duration)

        if (axe2 > 0):
            #turn right
            if (speed ==0):
                speed = abs(axe2)
            turnduration = (duration * abs(axe2)) / 100
            self.go_right(speed,duration)
        elif (axe2 < 0):
            #turn left
            if (speed ==0):
                speed = abs(axe2)
            turnduration = (duration * abs(axe2)) / 100
            self.go_left(speed,duration)
        
        if (speed==0):
            self.cmd_stop()

        #crane
        if (axe1 > 0):
            #go down
            duration = abs(axe1)
            self.crane_down(duration)
        elif (axe1 < 0):
            #go up
            duration = abs(axe1)
            self.crane_up(duration)

        if (axe0 > 0):
            #retract arm
            duration = abs(axe0)
            self.crane_extand(duration)
        elif (axe0 < 0):
            #extand arm
            duration = abs(axe0)
            self.crane_retract(duration)

        return     

    def process_todo_button(self,buttonid):
        
        if (buttonid == 10):
            #STOP  button X
            self.cmd_stop()
        elif (buttonid == 12):
            #up main actuator (benne lame)
            duration = self.settings.step_time
            self.main_up(duration)
        elif (buttonid == 13):
            #down main actuator (benne lame)
            duration = self.settings.step_time
            self.main_down(duration)
        elif (buttonid == 14):
            #godet down
            duration = self.settings.step_time
            self.side_down(duration)
        elif (buttonid == 15):
            #godet up
            duration = self.settings.step_time
            self.side_up(duration)
        elif (buttonid == 3):
            #treuil up
            duration = self.settings.step_time
            self.winch_up(duration)
        elif (buttonid == 0):
            #treuil down
            duration = self.settings.step_time
            self.winch_down(duration)
        elif (buttonid == 4):
            #crane rotate counterclockwise
            duration = self.settings.crane_rotate_left
            self.winch_up(duration)
        elif (buttonid == 5):
            #crane rotate clockwise
            duration = self.settings.crane_rotate_right
            self.winch_down(duration)

        return   

class tankEncoder(JSONEncoder):

    def default(self, object):

        if isinstance(object, tankstatus):

            return object.__dict__

        else:

            # call base class implementation which takes care of

            # raising exceptions for unsupported types

            return json.JSONEncoder.default(self, object)        