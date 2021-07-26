import math

from vpython import *   

import numpy as np

from PhysicsEngine import PhysicsEngine

from KickOff import KickOff

from BillardProperties import Ball, Tablerail

class GameEngine:  # Großkleinschreibung beachten
    
    def __init__(self):
        
        """
        table is created trough sketch-extrusion and 3D objects in vpython 
        
        table ground is at z=10mm

        unit is in mm

        balls and tablerails are objects of classes in BillardProperties

        balls radius equals 5mm 
        
        """
        #canvas scene as GUI for Billardsimulation
        self.scene = canvas(title='Billiard Simulation ', width=500, height=500,background=color.white)

        #arrows to get spatial orientation
        arrow( pos=vec(0,0,0),axis=vec(300,0,0), shaftwidth=1, color=color.cyan)
        arrow( pos=vec(0,0,0),axis=vec(0,300,0), shaftwidth=1, color=color.black)
        arrow( pos=vec(0,0,0),axis=vec(0,0,50), shaftwidth=1, color=color.blue)

        # table_top (green) with holes in it und table_rail are created through extrusion of 2D sketches:
        #sketch of table_top with holes in it (rectangular with circles)
        table_top = shapes.rectangle( width=290, height=172)
        hole_1 = shapes.circle(pos=[135.75,76.75], radius=6.75)
        hole_2 = shapes.circle(pos=[-135.75,76.75], radius=6.75)
        hole_3 = shapes.circle(pos=[135.75,-76.75], radius=6.75)
        hole_4 = shapes.circle(pos=[-135.75,-76.75], radius=6.75)
        hole_5 = shapes.circle(pos=[0,76.75], radius=6.75)
        hole_6 = shapes.circle(pos=[0,-76.75], radius=6.75)
        #extrusion of tabletop-sketch 
        extrusion(path=[vec(0,0,0), vec(0,0,10)], shape= [table_top ,hole_1, hole_2, hole_3, hole_4, hole_5, hole_6], color=vec(0.239, 0.600, 0.439))

        #creating Edge of the table (brown) trough sketch-extrusion
        table_rail = shapes.rectangle( width=320, height=200, thickness=0.09)
        extrusion(path=[vec(0,0,-10), vec(0,0,20)], shape= table_rail, color=vec(.6,.3,0)) 

        #creating tables feet through boxes!
        box(pos=vec(135.75,76.75,-25), length=13.5, height=13.5, width=50, color=vec(0.8,0.5,0))
        box(pos=vec(-135.75,76.75,-25), length=13.5, height=13.5, width=50, color=vec(0.8,0.5,0))
        box(pos=vec(-135.75,-76.75,-25), length=13.5, height=13.5, width=50, color=vec(0.8,0.5,0))
        box(pos=vec(135.75,-76.75,-25), length=13.5, height=13.5, width=50, color=vec(0.8,0.5,0))
        box(pos=vec(0,76.75,-25), length=13.5, height=13.5, width=50, color=vec(0.8,0.5,0))
        box(pos=vec(0,- 76.75,-25), length=13.5, height=13.5, width=50, color=vec(0.8,0.5,0))
        
        #creating holes as objects of vpython-class 'cylinder'- hole-positions are called in calculategame()
        self.cyl_hole_1 = cylinder(pos= vec(135.75,76.75,21), axis=vec(0,0,-20), radius=7, color=color.black)
        self.cyl_hole_2 = cylinder(pos= vec(-135.75,76.75,21), axis=vec(0,0,-20), radius=7, color=color.black)
        self.cyl_hole_3 = cylinder(pos= vec(135.75,-76.75,21), axis=vec(0,0,-20), radius=7, color=color.black)
        self.cyl_hole_4 = cylinder(pos= vec(-135.75,-76.75,21), axis=vec(0,0,-20), radius=7, color=color.black)
        self.cyl_hole_5 = cylinder(pos= vec(0,76.75,21), axis=vec(0,0,-20), radius=7, color=color.black)
        self.cyl_hole_6 = cylinder(pos= vec(0,-76.75,21), axis=vec(0,0,-20), radius=7, color=color.black)
        
        #Tablerail construction: 
        
        # for each of 6 rails: 
            #first tablerails (table_x) are created as extrusion of trapez-scretch trough definition of the 4 edgepoints of the trapez
            #then 5 mm  (ballsradius) from tablerail-outersurface tablerail-linesegments (self.table_rail_x_ls, .._x_a_ls, .._x_b_ls) are defined as object of class Tablerail(BillardProperties.py) 
        # table_rail 1:
        table_rail_1 = shapes.points(pos=[ [0,83.5], [13.5 ,70], [119,70], [135.75, 83.5] ])
        extrusion(path=[vec(0,0,0), vec(0,0,20)], shape= table_rail_1, color=vec(0.239, 0.600, 0.439))
        self.table_rail_1_ls = Tablerail(name='table_rail_1_ls',edgepoints=[vec(13.5- 2.07, 65,15), vec(119 + 2.39,65,15)]) #edge.points points need to be distanced with value ball.radius!
        self.table_rail_1_a_ls = Tablerail(name='table_rail_1_a_ls',edgepoints=[vec(13.5-2.07, 65, 15), vec(-5*sqrt(2),83.5,15)])
        self.table_rail_1_b_ls = Tablerail(name='table_rail_1_b_ls',edgepoints=[vec(119+2.39,65,15), vec(135.75+6.42,83.5,15)])
        # table_rail 2:
        table_rail_2 = shapes.points(pos=[ [142.5,76.75], [129,56], [129,-56], [142.5,-76.75] ])
        extrusion(path=[vec(0,0,0), vec(0,0,20)], shape= table_rail_2, color=vec(0.239, 0.600, 0.439))
        self.table_rail_2_ls = Tablerail(name='table_rail_2_ls',edgepoints=[vec(129-5,-(56+2.3),15) ,vec(129-5,56+2.3,15)])
        self.table_rail_2_a_ls = Tablerail(name='table_rail_2_a_ls',edgepoints=[vec(129-5,56+2.3,15),vec(142.5-3.25,76.75+3.8,15)])
        self.table_rail_2_b_ls = Tablerail(name='table_rail_2_b_ls',edgepoints=[vec(129-5,-(56+2.3),15), vec(142.5-3.25,-(76.75+3.8),15)])
        # table_rail 3:
        table_rail_3 = shapes.points(pos=[[0,83.5], [-13.5,70], [-114,70], [-135.75, 83.5] ])
        extrusion(path=[vec(0,0,0), vec(0,0,20)], shape= table_rail_3, color=vec(0.239, 0.600, 0.439))    
        self.table_rail_3_ls = Tablerail(name='table_rail_3_ls',edgepoints=[vec(-13.5 + 2.07 ,65 ,15), vec(-114 - 2.39,65 ,15)])
        self.table_rail_3_a_ls = Tablerail(name='table_rail_3_a_ls',edgepoints=[vec(-13.5+2.07, 65, 15), vec(5*sqrt(2),83.5,15)])
        self.table_rail_3_b_ls = Tablerail(name='table_rail_3_b_ls',edgepoints=[vec(-114-2.39,65,15), vec(-135.75-6.42,83.5,15)])
        # table_rail 4:
        table_rail_4 = shapes.points(pos=[ [-142.5,76.75], [-129,56], [-129,-56], [-142.5,-76.75] ])
        extrusion(path=[vec(0,0,0), vec(0,0,20)], shape= table_rail_4, color=vec(0.239, 0.600, 0.439))
        self.table_rail_4_ls = Tablerail(name='table_rail_4_ls',edgepoints=[vec(-129+5,56+2.3,15), vec(-129+5,-56-2.3,15)])
        self.table_rail_4_a_ls = Tablerail(name='table_rail_4_a_ls',edgepoints=[vec(-(129-5),56+2.3,15), vec(-(142.5-3.25),76.75+3.8,15)])
        self.table_rail_4_b_ls = Tablerail(name='table_rail_4_b_ls',edgepoints=[vec(-(129-5),-(56+2.3),15), vec(-(142.5-3.25),-(76.75+3.8),15)])
        # table_rail 5:
        table_rail_5 = shapes.points(pos=[ [0,-83.5], [13.5,-70], [114,-70], [135.75, -83.5] ])
        extrusion(path=[vec(0,0,0), vec(0,0,20)], shape= table_rail_5, color=vec(0.239, 0.600, 0.439))
        self.table_rail_5_ls = Tablerail(name='table_rail_5_ls',edgepoints=[vec(13.5-2.07, -65 ,15), vec(114+2.39,-65,15)])
        self.table_rail_5_a_ls = Tablerail(name='table_rail_5_a_ls',edgepoints=[vec(13.5-2.07, -65, 15), vec(-5*sqrt(2),-83.5,15)])
        self.table_rail_5_b_ls = Tablerail(name='table_rail_5_b_ls',edgepoints=[vec(114+2.39,-65,15), vec(135.75+6.42,- 83.5,15)])
        # table_rail 6:
        table_rail_6 = shapes.points(pos=[[0,-83.5], [-13.5,-70], [-114,-70], [-135.75, -83.5] ])
        extrusion(path=[vec(0,0,0), vec(0,0,20)], shape= table_rail_6, color=vec(0.239, 0.600, 0.439))
        self.table_rail_6_ls = Tablerail(name='table_rail_6_ls',edgepoints=[vec(-(13.5-2.07), -65 ,15), vec(-(114+2.39),-65,15)])
        self.table_rail_6_a_ls = Tablerail(name='table_rail_6_a_ls',edgepoints=[vec(-(13.5-2.07), -65,15), vec(5*sqrt(2),-83.5,15)])
        self.table_rail_6_b_ls = Tablerail(name='table_rail_6_b_ls',edgepoints=[vec(-(114+2.39),- 65,15), vec(-135.75- 6.42,- 83.5,15)],)

        # definition of balls as objects of class Ball (Billard_properties.py) 
        self.cueball = Ball(pos=vec(-80,0 ,15),texture={'file':'/balls/0.png'},name = 'cueball')
        self.balls = [self.cueball,Ball(pos=vec(45,0,15),texture={'file':'/balls/1.png'},name = 'ball_1'),
                      Ball(pos=vec(75,-15,15), texture={'file':'/balls/2.png'},name = 'ball_2'),
                      Ball(pos=vec(85,-20,15), texture={'file':'/balls/3.png'},name = 'ball_3'),
                      Ball(pos=vec(75,15,15), texture={'file':'/balls/4.png'},name = 'ball_4'),
                      Ball(pos=vec(85,0,15), texture={'file':'/balls/5.png'},name = 'ball_5'),
                      Ball(pos=vec(65,10,15),texture={'file':'/balls/6.png'},name = 'ball_6'),
                      Ball(pos=vec(85,20,15), texture={'file':'/balls/7.png'},name = 'ball_7'),
                      Ball(pos=vec(65,0,15),texture={'file':'/balls/8.jpg'},name = 'ball_8'),
                      Ball(pos=vec(75,5,15), texture={'file':'/balls/9.png'},name = 'ball_9'),
                      Ball(pos=vec(85,10,15), texture={'file':'/balls/10.png'},name = 'ball_10'),
                      Ball(pos=vec(75,-5,15), texture={'file':'/balls/11.png'},name = 'ball_11'),
                      Ball(pos=vec(85,-10,15), texture={'file':'/balls/12.png'},name = 'ball_12'),
                      Ball(pos=vec(55,-5,15),texture={'file':'/balls/13.png'},name = 'ball_13'),
                      Ball(pos=vec(65,-10,15),texture={'file':'/balls/14.png'},name = 'ball_14'),
                      Ball(pos=vec(55,5,15),texture={'file':'/balls/15.png'},name = 'ball_15')] 

        # kick_dir is set trough mouse position later (KickOff.kickoff_dir())! and are always normalized .. also it defines direction of queue and arrow
        self.kick_dir = vec(1,0,0) 
        #initially queue should end 15 mm before cueball and is defined trough substraction of 20*kickdir from cueballs position 
        #queue should have 150cm length and lifted up in z direction(addition of (0,0,22)) to not collidate with tablerail 
        self.queue = cylinder(pos= self.cueball.pos - self.kick_dir*20 + vec(0,0,7), axis=-self.kick_dir*150 + vec(0,0,22), radius=2, color=color.white) 
        #definiton of arrow , which is directed in kickdir- direction
        self.kick_dir_vec = arrow( pos=self.cueball.pos + vec(0,0,7) + self.kick_dir*20,axis=self.kick_dir*150, shaftwidth=1, color=vec(0.8,0.8,0.8))
        #time between Gamecalculation-iteration... 100 calculations per second !--> real time!
        self.dt = 0.01 
        # objects of class KickOff and PyhsicsEngine which are needed in class GameEngine
        self.K = KickOff(self)
        self.P = PhysicsEngine(self)
        
    def calculategame(self):
        """
        Billard-simulation (moving balls, ballcollision, railcollision, ball-pocketing) is performed in this function

        calculategame always starts after KickOff, where cueballs velocity(value and direction is setted)

        calculategame ends when no ball is moving anymore (nonmoving balls = 16)

        calculategame uses methods from PhysicEngine for mathematical/physikal calculations

        """
        self.scene.userzoom = True #user is able to spin and zoom on the Billardtable while calculategame() (Billard-Simulation) is called
        self.scene.userspin = True 
        self.queue.visible = False
        self.kick_dir_vec.visible = False #arrows and queues are not visisible anymore
        nonmoving_balls = []      # list will be appended with balls which are in hole or have velocity < 0.2   
        # pointer for initial railcollisionpoint calculation (ball.initialrailpnter) for each ball is set to True at the beginning  of every gamecalculation call (see line 192-195)
        # After that railcolisionpoints of each ball need to be calculated after every ballcollsion(line 221-230) and every railcollision(line 205-217) 
        for ball_ in self.balls:
            ball_.initialrailpnter = True

        
        while len(nonmoving_balls) < 16:
            rate(1/self.dt) # 100 calculations per second
            for b in range(16):
                ball = self.balls[b]
                
                if not ball.inholed: 
                    if mag(ball.velocity) > 0.2: #threshold of velocity at which ball seems to not move anymore
                        
                        if ball in nonmoving_balls:                                                            
                            nonmoving_balls.remove(ball)
                        
                        # ballsmovement by adding ball.velocity*self.dt to ballpos and rotation ball in ballvel direction
                        ball.change_pos(ball.pos + ball.velocity*self.dt)
                        rot_angle, rot_axis  = self.P.calculaterot(ball.velocity) 
                        ball.rotate(angle = rot_angle, axis = rot_axis)
                        ball.velocity = ball.velocity * 0.9965 #0.9965 # Reduction value from 'Studienarbeit von Andreas Herschbach'
                        # initial railcollisionpoint calclucaltion for each ball after velocity is set trough kickoff.. (will only get passed once for each ball: ball.initialrailpointer --> False)
                        if not self.P.calculaterailcollisionpnt(ball.velocity,ball.pos) == False and ball.initialrailpnter:   
                            ball.railcollpnt= self.P.calculaterailcollisionpnt(ball.velocity,ball.pos) 
                            ball.initialrailpnter = False 
    
                        if abs(ball.pos.x) > 114 or abs(ball.pos.y) > 54: # to reduce computing power railcollsion and ball-pocketing should just be checked near the tablerails
                            #checking if ball is near a hole to compute balls pocketing
                            for hole in [self.cyl_hole_1,self.cyl_hole_2,self.cyl_hole_3,self.cyl_hole_4,self.cyl_hole_5,self.cyl_hole_6]:
                                if mag(ball.pos - (hole.pos - vec(0,0,6))) < 10:  
                                    ball.pocketing(hole.pos) 
                                    if not (ball in nonmoving_balls):
                                        nonmoving_balls.append(ball)   #balls pocketing(move ball under table top and setting visibility) is performed in ball.pocketing()
                            #checking if ball is near a rails linesegement to compute balls railcollision
                            if not ball.railcollpnt == []: # balls.railcollpnt is initialised with [] but changes when potential railcollision point is found.. ball.railcollpnt[0] = collisionpoint and ball.railcollpnt[1] = corresponding tablerail 
                                if mag(ball.pos-ball.railcollpnt[0]): #checking if ball is near to railcollision point
                                    if self.P.check_ball_behind_rail(ball.velocity,ball.pos, ball.railcollpnt[0]): #checking if ball is allready behind railcollpnt     
                                        ball.change_pos(ball.railcollpnt[0]) #changing balls position to railcollisio point
                                        ball.velocity = self.P.calculaterailcollision(ball.velocity, ball.railcollpnt[1].edgepoints) #changing balls velocity acoording to reflection laws
                                        ball.change_pos(ball.pos + ball.velocity*self.dt) # moving ball along its velocity so that ball is definitely infront of the wall
                                        if not self.P.calculaterailcollisionpnt(ball.velocity,ball.pos) == False: 
                                            ball.railcollpnt = self.P.calculaterailcollisionpnt(ball.velocity,ball.pos) #because velocity of ball changed railcollision point need to be calculated again


                        #checking if ball is near a another ball to compute ballcollision                             
                        for ball_op in self.balls:    
                            if not ball.inholed and ball != ball_op:     
                                if mag(ball_op.pos - ball.pos) < 10:  # ball_op.pos - ball.pos --> vector from ballpos to ball_op.pos.                            
                                    ball.pos, ball.velocity, ball_op.velocity = self.P.calculateballcollision(ball.pos, ball_op.pos, ball.velocity, ball_op.velocity)  #changing balls velocity and positions according to the conservation of momentum and so that balls dont intrude                                         
                                    if not self.P.calculaterailcollisionpnt(ball.velocity,ball.pos) == False:  #because velocity of balls changed railcollision point for each ball need to be calculated again                              
                                        ball.railcollpnt = self.P.calculaterailcollisionpnt(ball.velocity,ball.pos)                                                    
                                    if not self.P.calculaterailcollisionpnt(ball_op.velocity,ball_op.pos) == False:                                
                                        ball_op.railcollpnt= self.P.calculaterailcollisionpnt(ball_op.velocity,ball_op.pos)                                          
                                
                    else:    #if balls velocity is < 0.2 then ball should be appended in nonmoving balls list and its velocity should be set to vec(0,0,0)
                        if not (ball in nonmoving_balls):                                    
                            ball.velocity = vec(0,0,0)                           
                            nonmoving_balls.append(ball)

                else: #if ball is in a pocket ball should be also appended in nonmoving_balls list
                    if not (ball in nonmoving_balls):  
                            nonmoving_balls.append(ball)
                    
                    continue

        if self.cueball.inholed: #if cueball got into pocket at previous run then it need to be positioned at initial kickoff position
            self.cueball.change_pos(vec(-80,0 ,15))
            self.cueball.set_visible(True)
            self.cueball.inholed = False
        
        
    def set_camera_for_kickoff(self): #before kickoff starts camera need to be directed and placed rightly for kickoff 
        """
        camera setting for KickOff
        """
        self.scene.camera.axis = vec(0,0,-270)
        self.scene.camera.pos = vec(0, 0,270)
        self.scene.userzoom = False
        self.scene.userspin = False #also userzoom and userspin need to be blocked to allow mouseinteraction to move queue
        
         
    def run(self): # 
        """
        mainprocedure between kickoff and gamecalculation
        """
        
        while True: # condition when game ends should be placed here
            self.set_camera_for_kickoff()
            self.K.kickoff_dir()
            
        
            while mag(self.cueball.velocity) < 0.2: #if cueballs velocity ist set > 0.2 then calculategame() is called
                pass
            
            self.calculategame()