
import math

from vpython import *

import numpy as np


class KickOff:    
    
    def __init__(self,gameengine):
        """
        Class for Simulating KickOff through mouseinteraktion
        """
        
        self.G = gameengine
        self.b_vel = button(text='set kickoffvel', pos=self.G.scene.title_anchor, bind=self.kickoff_vel)
        self.b_dir = button(text='set kickoffdir', pos=self.G.scene.title_anchor, bind=self.kickoff_dir)
        self.calc_vel = False 
        self.R_queue = (self.G.scene.mouse.pos + vec(0,0,15)) - self.G.cueball.pos
        self.drag_queue = False
        self.mouseactual = vec(0,0,0)


    def kickoff_dir(self):
        #show queue and kick-dir arrow
        self.G.queue.visible = True
        self.G.kick_dir_vec.visible = True
        #unbind mouseinteraktion for kickoff velocity setting 
        self.G.scene.unbind("mouseup", self.up_kick_vel)
        self.G.scene.unbind("mousemove", self.move_kick_vel)
        #bind mouseinteraktion for kickoff direction setting 
        self.G.scene.bind("mousedown", self.down_kick_dir) 
        self.G.scene.bind("mousemove", self.move_kick_dir)
        #some initial setting for updating queues and arrows postion and axis-direction at KickOffstart after cueballs position changed
        self.G.queue.pos = self.G.cueball.pos - self.G.kick_dir*20 + vec(0,0,7) 
        self.G.queue.axis = (-self.G.kick_dir*150 + vec(0,0,22))
        self.G.kick_dir_vec.pos = self.G.cueball.pos + vec(0,0,7) + self.G.kick_dir*20       
        self.G.kick_dir_vec.axis = (self.G.kick_dir*150)         
        
    def down_kick_dir(self): #function is called when mouse is clicked in kickoff_dir mode
        """ 
        mouse-interaktion-settings to manipulate KickOffs direction 
        """
        #updating queues and arrows postion and axis-direction while self.G.kick_dir changes
        self.G.kick_dir = norm((self.G.scene.mouse.pos + vec(0,0,15)) - self.G.cueball.pos) #is set trough mouse position! and always normalized .. also it defines direction of queue
        self.G.queue.pos = self.G.cueball.pos - self.G.kick_dir*20 + vec(0,0,7) 
        self.G.queue.axis = (-self.G.kick_dir*150 + vec(0,0,22))
        self.G.kick_dir_vec.pos = self.G.cueball.pos + vec(0,0,7) + self.G.kick_dir*20      
        self.G.kick_dir_vec.axis = (self.G.kick_dir*150)        

    
    def move_kick_dir(self): #function is called when mouse is clicked and moves in kickoff_dir mode
        self.down_kick_dir()

        
    def kickoff_vel(self,b):
        
        self.drag_queue = False # if it is set to True then queue can be draged by mouse in kickoff direction 
        self.calc_vel = False # if it is set to True(by clicking d) then KickOff Animation starts
        self.G.scene.unbind("mousedown", self.down_kick_dir) 
        self.G.scene.unbind("mousemove", self.move_kick_dir)

        self.G.scene.bind("mousemove", self.move_kick_vel)
        self.G.scene.bind('mouseup', self.up_kick_vel)
        self.G.scene.bind('keydown', self.calcvel)
            
        mousemovement = vec(0,0,0) # vector to decribes mousemovment between two timepoints
        self.mouseactual = vec(0,0,0)
        queue_cue = 0
        veh_cue = 0
        

        
        
        
        while True: #  queue (length = 150mm) position is defined by the end of cyclinder and cueball position by Focus of ball.. 
            rate(1/self.G.dt)# dt =0.01, 100 calculations per second !--> real time!  
            if self.drag_queue:
                mousemovement.value = self.mouseactual - self.R_queue #vector to decribe mousemovment between two timepoints (Magnitute and direcetion)
                self.mouseactual.value = self.R_queue 
                mouse_queue_val = dot(norm(self.G.kick_dir),norm(mousemovement))*mag(mousemovement) 
                #mouse_queue_val is a variable which is influenced by how much mousemovement goes in kick_dir direction and how long the mousemovementvektor is
                #checking if distanz between nextposition of queue and cueball is < 50mm/>5mm and if queue is postioned infront of cueball
                if  5 < mag((self.G.queue.pos - mouse_queue_val*norm(self.G.kick_dir)) - self.G.cueball.pos) < 50 and dot(self.G.cueball.pos - (self.G.queue.pos - mouse_queue_val*norm(self.G.kick_dir)), self.G.kick_dir) > 0 :  
                        self.G.queue.pos = self.G.queue.pos - mouse_queue_val*norm(self.G.kick_dir) #the magnitude of mouse_queue_val within 0.01 sec is addet to queue.pos in kick_dir 
                        queue_cue = mag(self.G.queue.pos - self.G.cueball.pos)    #magnite between queue and cueballsposition is used to calculate queue und cueballs velocity  
            
            if self.calc_vel: #self.calc_vel = True by clicking "D" (Keyboardevent)  
                # animation of moving queue
                #calculation of velocity:  queue in kickoff and cueball in calculategame() should maximal move min(queue_cue/7,9.9) after one calculation section(self.G.dt)
                self.G.scene.unbind('mousemove', self.move_kick_vel)
                self.G.scene.unbind('mouseup', self.up_kick_vel)
                self.G.queue.pos = self.G.queue.pos + norm(self.G.kick_dir)* min(queue_cue/7,9.9)       
                if sqrt((self.G.queue.pos.x - self.G.cueball.pos.x)**2 + (self.G.queue.pos.y - self.G.cueball.pos.y)**2) < 5 :
                    print('veh_output ='+' '+ str(min(queue_cue/7,9.9)/self.G.dt))
                    self.G.cueball.velocity = min(queue_cue/7,9.9)/self.G.dt*norm(self.G.kick_dir)
                    break 
                
            
    def move_kick_vel(self): #function is called when mouse is clicked and moves in kickoff_vel mode
        """ 
        mouse-interaktion-settings to manipulate KickOffs velocity 
        """
        self.R_queue= (self.G.scene.mouse.pos + vec(0,0,15))
        self.drag_queue = True 

    def up_kick_vel(self): #function is called when mouse is not clicked anymore in kickoff_vel mode
        self.drag_queue = False 
        self.mouseactual.value = vec(0,0,0)

    def calcvel(self,ev): #function is called when a key on keyboard is clicked kickoff_vel mode
        """
        eventbased velocity-calculation and animation of a moving queue 
        """               
        if ev.key == 'd': #if key is d self.calc_vel is set to true
            self.calc_vel = True
            print('vehicle calculated')

 
