from math import *
import pygame

import N_body_parameters as param
import N_body_sim_manager as sim
import N_body_integrate as integrate
import time

#------------------------------------------------
#lists storing values collected when N_body_data_collection is called

times=[]#stores list of times taken at at every drawing interval
kinetic_energy=[]
potential_energy=[]
total_energy=[]
particle_number=[]
evaporation_ratio=[]
central_density=[]
speed=[]
force_calculations=[]
num_binaries=[]

#below lists used for method complexity_comparison
list_n=[]
exec_time_DC=[]
exec_time_BH=[]

#------------------------------------------------

def energy():#returns kinetic and potential energy of the system
    kinetic_energy=0
    for p in sim.particles:
        [vx,vy]=p.vel
        
        kinetic_energy+=0.5*p.mass*(vx*vx+vy*vy)
        
    potential_energy=0
    for i in range(sim.num_particles):
        sum=0
        for j in range(i+1,sim.num_particles):
            dx = sim.particles[i].pos[0] - sim.particles[j].pos[0]
            dy = sim.particles[i].pos[1] - sim.particles[j].pos[1]
            r= sqrt(dx*dx + dy*dy)
            sum+=sim.particles[j].mass/r
        potential_energy+=-param.G*sim.particles[i].mass*sum
        
    return [kinetic_energy,potential_energy]

def binaries():# calculates the number of binaries in the simulation
    d_threshold=5
    counter=0

    for i in range(sim.num_particles):
        for j in range(i+1,sim.num_particles):
            dx = sim.particles[i].pos[0] - sim.particles[j].pos[0]
            dy = sim.particles[i].pos[1] - sim.particles[j].pos[1]
            r= sqrt(dx*dx + dy*dy)
            if r<d_threshold:
                [vx,vy]=sim.particles[i].vel
                [vx1,vy1]=sim.particles[j].vel
        
                K=0.5*sim.particles[i].mass*(vx*vx+vy*vy)+0.5*sim.particles[j].mass*(vx1*vx1+vy1*vy1)
                U=-param.G*sim.particles[i].mass*sim.particles[j].mass/r

                if K+U<0: counter+=1
    return counter

def num_particles_radius(r):
    counter=0
    
    for i in range(sim.num_particles):
        x=sim.particles[i].pos[0]
        y=sim.particles[i].pos[1]
        if sqrt((x-600)**2 + (y-350)**2)<r: counter+=1
        
    return counter

def complexity_comparison(n_max,step):
    global list_n
    global exec_time_DC
    global exec_time_BH
    
    for n in range(1,n_max,step):
        list_n+=[n]
        
        initial_conditions=sim.reset_initial_conditions(n)
        param.barnes_hut=False
        start_time = time.time()
        integrate.move()
        exec_time_DC+=[time.time() - start_time]

        particles=initial_conditions
        param.barnes_hut=True
        start_time = time.time()
        integrate.move()
        exec_time_BH+=[time.time() - start_time]


def angular_momentum():
    return '' #do nothing for now

def computation_speed():
    simtime=sim.run*param.dt
    runtime=pygame.time.get_ticks()
    
    if simtime==0:  return 0
    else: return runtime/simtime

#!!!ISSUE!!!: because of the way the file is saved, it rewrites over the photos taken from
    #the previous simulation
def take_photo():
    pygame.image.save(sim.surface,param.file_name+str(sim.screen_shots)+'.jpg')
    sim.screen_shots+=1

def update_times():
    global times
    times+=[sim.run*param.dt]

def update_energy():
    
    global kinetic_energy
    global potential_energy
    global total_energy
    
    [K,U]=energy()
    kinetic_energy+=[K]
    potential_energy+=[U]
    total_energy+=[K+U]

def update_particle_number():
    global particle_number
    particle_number+=[sim.num_particles]
    
def update_computation_speed():
    global speed
    speed+=[computation_speed()]

def update_force_calculations():
    global force_calculations
    force_calculations+=[integrate.num_calculations_tot]
    
def update_binaries():
    global num_binaries
    num_binaries+=[binaries()]
    
def update_evaporation_ratio():
    global evaporation_ratio
    evaporation_ratio+=[num_particles_radius(param.ccradius)/param.num_particles_orig]
    
def update_central_density():
    global central_density
    central_density+=[num_particles_radius(param.core_radius)/param.num_particles_orig]
