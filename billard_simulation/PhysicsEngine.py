import math

from vpython import *

import numpy as np

class PhysicsEngine:
    
    def __init__(self,gameengine):
        """
        some physical and mathematical operations for GameEngine.calculategame()
        """
        self.G = gameengine
    
    
    def calculaterot(self,ball_vel):
        """ 
        calculates rotation_angle und rotation_axis of a rolling ball
        """         
        rotation_axis = cross(vec(0,0,1),norm(ball_vel)) #rotation_axis ist always perpendicular to balls velocity
        rotation_angle = (mag(ball_vel)*self.G.dt)/5 #value of rotation_angle depends on magnitute of balls velocity 
        return rotation_angle, rotation_axis
    
    def check_point_on_line(self,ballpos, rail):
        """
        check if 3D points is on (near) a 3D line-segment 
        """
        r1 = mag(ballpos-rail[0]) 
        r2 = mag(ballpos-rail[1])
        L = mag(rail[0]-rail[1])
        if r1 + r2 <= L + 1:  
            return True 
        
        else:   
            return False 
        
        
        
    def calculaterailcollision(self,ballvel,rail):
        """calculates output speed for an input speed after the colision reflection laws"""

        if diff_angle(ballvel,(rail[0]-rail[1])) < math.pi/2:
            alpha_in = diff_angle(ballvel,(rail[0]-rail[1]))
            
        else:  
            alpha_in = pi - diff_angle(ballvel,(rail[0]-rail[1])) # making sure to always calculate inner Angle.. diffangle() (vphyton function) sometimes calculates outer Angle 
        
        alpha_rot = - 2*alpha_in #reflection can be realised by rotating the vector by 2*diffangle so that diffangle between rail and input velocity equals diffangle between rail and output velocity
        ballvel_out = rotate(ballvel , angle=alpha_rot) * 0.9 # # Reduction value from 'Studienarbeit von Andreas Herschbach'
        if round(diff_angle(ballvel,rail[0]-rail[1]),2) == round(diff_angle(ballvel_out,rail[0]-rail[1]),2): 
            return(ballvel_out)
        
        else: 
            alpha_rot = 2*alpha_in
            ballvel_out = rotate(ballvel , angle=alpha_rot) * 0.9
            
            return(ballvel_out)
            
            
    
    def calculateballcollision(self,ball_a_pos, ball_b_pos, ball_a_vel, ball_b_vel):
        """
        calculates ballcollision according to the conservation of momentum
        """
        
        dn = norm(ball_b_pos - ball_a_pos)
        n = norm(cross(vec(0,0,1),dn)) # norm(rotate(dn, angle = math.pi/2)) also possilble
        ball_a_newpos = ball_b_pos - dn*10
        vd_a = dot(ball_a_vel, dn)
        vn_a = dot(ball_a_vel, n)
        vd_b = dot(ball_b_vel, dn)
        vn_b = dot(ball_b_vel, n)
        ball_a_newvel = (vd_b * dn + vn_a * n)*0.95  # Reduction value from 'Studienarbeit von Andreas Herschbach'
        ball_b_newvel = (vd_a * dn + vn_b * n)*0.95
        return ball_a_newpos, ball_a_newvel, ball_b_newvel
    
    def line_intersection(self,line1_3D, line2_3D): 
        """calculates 3D line_intersection by 2D-operations """
         # 2D line Intersection
        line1 = ((line1_3D[0].x,line1_3D[0].y),(line1_3D[1].x,line1_3D[1].y))
        line2 = ((line2_3D[0].x,line2_3D[0].y),(line2_3D[1].x,line2_3D[1].y))
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
           return vec(0,0, 15) # if lines do not intersec still move on!!!!!!!
    
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div  
        y = det(d, ydiff) / div        
        return vec(x, y, 15)

        
    def check_ball_behind_rail(self,ballvel,ballpos,intersec_pt):
        """
        check if ball is already behind the rail
        """
        #check if ball is already behind the rail by calculating dotproduct of distanzvector between balls positon and intersec_pt and balls velocity
        if dot(ballpos-intersec_pt, ballvel) > 0:  
            return True
        
        else: 
            return False
      
    def calculaterailcollisionpnt(self,ballvel, ballpos):
        """
        calculates potential rail collisionpnt and corresponding rail with current balls velocity
        """
        pot_collpts = []
        pot_collpts_dist = []
        table_rail_list = []
        
        for table_rail in [self.G.table_rail_1_a_ls, self.G.table_rail_1_b_ls, self.G.table_rail_1_ls, self.G.table_rail_2_ls, self.G.table_rail_2_a_ls,self.G.table_rail_2_b_ls, self.G.table_rail_3_ls, self.G.table_rail_3_a_ls,self.G.table_rail_3_b_ls, 
                                                self.G.table_rail_4_ls, self.G.table_rail_4_a_ls, self.G.table_rail_4_b_ls, self.G.table_rail_5_ls, self.G.table_rail_5_a_ls,self.G.table_rail_5_b_ls, self.G.table_rail_6_ls, self.G.table_rail_6_a_ls, 
                                                self.G.table_rail_6_b_ls]:
            
            #calculation of intersectionpoint between lines which are going in tablerail-linesegments and ball velocities direction
            intersec_pt = self.line_intersection((ballpos,(ballpos+ballvel)), (table_rail.edgepoints[0],table_rail.edgepoints[1]))  
            if self.check_point_on_line(intersec_pt,table_rail.edgepoints): # checking if intersectionpoint is on corresponding tablerail 
                if not self.check_ball_behind_rail(ballvel,ballpos,intersec_pt): # checking if intersectionpoint is ahead of moving ball

                    pot_collpts.append(intersec_pt)
                    pot_collpts_dist.append(mag(ballpos - intersec_pt)) # calculation of distanz between intersectionpoint and ball, because the nearest intersectionpoint is final potential railpoint (line 134-135)
                    table_rail_list.append(table_rail)                 
                
        if pot_collpts == []:
            return False
            
        else:
            pot_collpt = pot_collpts[int(pot_collpts_dist.index(min(pot_collpts_dist)))]
            table_rail_ = table_rail_list[int(pot_collpts_dist.index(min(pot_collpts_dist)))]   
            return[pot_collpt,table_rail_]
            

