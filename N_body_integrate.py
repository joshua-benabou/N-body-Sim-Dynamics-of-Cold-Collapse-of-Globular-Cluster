import N_body_parameters as param
import N_body_sim_manager as sim
import N_body_Barnes_Hut as BH
from N_body_Particle import Particle

#------------------------Methods initializing and moving Particle() objects

def move():#update the state of the entire system
    global num_calculations_tot
    num_calculations_tot=0
    num_calculations_tot+=update_forces()
    for p in sim.particles:
        if p not in sim.fixed_particles:
            p.move_Verlet(param.dt,1)#first step of Verlet integrator
    num_calculations_tot+=update_forces()
    for p in sim.particles:
        if p not in sim.fixed_particles:
            p.move_Verlet(param.dt,2)#second step of Verlet integrator

def update_forces():#service method for move()
    num_calculations=0#number of force calculations in one step
    
    if param.barnes_hut: BH.construct_tree()
    for i in range(param.movement_substeps):
        for j in range(0,sim.num_particles,1):#all the forces between pairs of particles are calculated
            if param.barnes_hut:
                num_calculations+=BH.force(BH.root,sim.particles[j])
            else:
                for k in range(j+1,sim.num_particles,1):
                    Particle.add_forces(sim.particles[j],sim.particles[k])
                    num_calculations+=1
    if param.barnes_hut: BH.reset_tree()

    return num_calculations
  
