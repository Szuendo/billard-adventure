
import math

from vpython import *

import numpy as np


class Ball:
    def __init__(self,pos,texture,name):
        """
        ball is a sphere (vpython 3D object)

        - methods and attributes are defined to use und change spheres Atributes(pos, orientation, visibility)
  
        """
        self.pos = pos
        self.radius = 5      
        self.velocity = vec(0,0,0)
        self.inholed = False         #pointer if Ball is in pocked
        self.initialrailpnter = True #pointer for initial railcollisionpoint calculation in GameEngine.calculategame
        self.railcollpnt = []        #balls potential collisionpoint with a rail and corresponding rail is stored and updated here after orientation of balls velocity changes
        self.texture=texture
        self.visible = True
        self.sphere_=sphere(pos = self.pos, radius = self.radius, velocity = self.velocity, texture = self.texture, visible=self.visible)
        self.name = name
        
    def rotate(self,angle,axis):
        """
        setter function to rotate displayed vpython-sphere 
        """
        self.sphere_.rotate(angle = angle, axis = axis)      
        
    def change_pos(self,pos_): 
        """
        setter function to change displayed vpython-spheres position

        and to update balls attribute 'pos'
        """
        self.pos = pos_
        self.sphere_.pos = self.pos  # otherwise sphere_.pos would be not changed .. 
        
    def set_visible(self,visible):
        """
        setter function to set spheres visibilty 
        """
        self.visbile=visible
        self.sphere_.visible=visible
        
    def pocketing(self,holepos):
        """
        computing a ball falling in a hole 
        
        - position is set to z=-20 at hole position
        - velocity is changed to vec(0,0,0)
        -visibility is changes to False 
        """

        self.change_pos(holepos)
        self.velocity = vec(0,0,0)
        self.sphere_.visible = False
        self.inholed = True

class Tablerail :   
    def __init__(self,name,edgepoints):
        """
        tablerail is a linesegment defined by two points
        """
        self.name = name
        self.edgepoints = edgepoints


