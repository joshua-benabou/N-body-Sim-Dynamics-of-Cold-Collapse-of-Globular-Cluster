import pygame 
from pygame.locals import *
from N_body_Particle import Particle
import N_body_parameters as param
import math
import random


###dense=False
test_collapse=True
dense=False
circular_random=True 

#-----------------INITIALIZATION OF PARTICLES
num_particles = param.num_particles_orig

particles=[Particle() for i in range(num_particles)]

fixed_particles=[]

#velocity distribution
if test_collapse:
    for p in particles:
        p.vel=[0,0]

#position distribution        
if dense:
    for p in particles:
        p.pos =[random.uniform(400,param.screen_size[0]-400),random.uniform(200,param.screen_size[1]-200)]

#position distribution
if circular_random:
    for p in particles:
        radius =param.ccradius*(random.uniform(0,1))
        phi = random.uniform(0,2*math.pi);
        x = radius*math.cos(phi);
        y = radius*math.sin(phi);
        p.pos =[600+x,350+y]

 
    
def reset_initial_conditions(N):#used for comparing complexity of BH vs. DC
    global num_particles
    global particles
    num_particles = N
    particles=[Particle() for i in range(num_particles)]
    return particles
#------------------------OTHER INITIALIZATIONS 
run=0

screen_shots=0

pygame.display.init()
pygame.font.init()
icon = pygame.Surface((1,1)); icon.set_alpha(0);pygame.display.set_icon(icon)
pygame.display.set_caption("TIPE N-body sim/Verlet/N large")

surface = pygame.display.set_mode(param.screen_size)

global clock
clock = pygame.time.Clock()


    


