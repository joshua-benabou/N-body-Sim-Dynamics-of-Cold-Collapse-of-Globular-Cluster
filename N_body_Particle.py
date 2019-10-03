from math import *
import random

import N_body_parameters as param
import pygame
import colorsys

class Particle(object):
    def __init__(self, pos=None,vel=None, mass=None, color=None):#default: particles initialized with random velocities and positions
        if pos == None:
            self.pos = [random.uniform(10.0,param.screen_size[0]-10.0),random.uniform(10.0,param.screen_size[1]-10.0)]

        else: self.pos = pos
        
        if vel == None:
            angle = random.uniform(0.0,2.0*pi)
            r = 50 # modulus of the intial speeds
            self.vel = [r*cos(angle),r*sin(angle)]
            
        else: self.vel = vel
        
        if mass == None: self.mass = param.common_mass
        else:            self.mass = mass

        if color==None: self.color=pygame.Color(255,255,255)#default color is white
        else: self.color=color

        
        self.forces = [0.0,0.0]
    def get_radius(self):
        #Assuming these objects are actually spheres, the radius scales with the cube root of
        #the mass.  If you prefer circle, change to the square root.
        if param.radius_scaling==True:
            return param.radius_scale*(self.mass**(1.0/3.0))
        else:
            return param.default_radius

    def update_color(self):#is called only if param.coloring=True
        force_mag=sqrt(self.forces[0]**2+self.forces[1]**2)#magnitude of force
        s=sqrt(force_mag/param.max_force)
        #s is a quantity bewteen 0 and 1, but since force is proportional to 1/r^2,
        #the scaling messses things up: the particles change color only if they're very close
        
        [a,b,c]=colorsys.hsv_to_rgb(s, 1, 1)#converts HSV to RGB
        self.color=[255*a,255*b,255*c]
   
        
    @staticmethod
    def add_forces(particle1,particle2):
        dx = particle2.pos[0] - particle1.pos[0]
        dy = particle2.pos[1] - particle1.pos[1]
        r_squared = dx*dx + dy*dy+param.epsilon
        r = r_squared**0.5
        
        force_magnitude =  (param.G * particle1.mass * particle2.mass)/r_squared#F=G*M1*M2/(r^2)
        dx_normalized_scaled = (dx / r) * force_magnitude
        dy_normalized_scaled = (dy / r) * force_magnitude
        particle1.forces[0] += dx_normalized_scaled
        particle1.forces[1] += dy_normalized_scaled
        particle2.forces[0] -= dx_normalized_scaled
        particle2.forces[1] -= dy_normalized_scaled
    @staticmethod
    def get_collided(particle1,particle2):
        r1 = particle1.get_radius()
        r2 = particle2.get_radius()
        both = r1 + r2
        abs_dx = abs(particle2.pos[0] - particle1.pos[0])
        if abs_dx > both: return False
        abs_dy = abs(particle2.pos[1] - particle1.pos[1])
        if abs_dy > both: return False
        #The above lines are just some optimization.  This is the real test.
        if abs_dx*abs_dx + abs_dy*abs_dy > both*both: return False
        return True


    def move_Verlet(self, dt,step):#update position and velocity vectors of a particle using Verlet integration

        if step==1:
            self.vel[0] += 0.5*dt * self.forces[0] / self.mass
            self.vel[1] += 0.5*dt * self.forces[1] / self.mass
        
            self.pos[0] += self.vel[0]*dt
            self.pos[1] += self.vel[1]*dt            
        if step==2:
            self.vel[0] += 0.5*dt * self.forces[0] / self.mass
            self.vel[1] += 0.5*dt * self.forces[1] / self.mass

            '''
            now that all the forces are calculated, we should update the colors of each particle
            we are forced to update colors in this module because in the main method, we first do integrate.move, which updates the forces,
            moves the particles, then resets the forces to 0; then we do drawing.draw().
            of course, architecturally this is an awkward place to put this line, as the
            moving method has nothing to do with (a priori) the method which updates color
            '''
            if param.coloring: self.update_color()
            
        self.forces[0] = 0.0
        self.forces[1] = 0.0
