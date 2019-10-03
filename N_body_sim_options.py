import N_body_parameters as param
from N_body_Particle import Particle
import N_body_sim_manager as sim

'''
the issue is that, its possible to have >2 simultaneous collisions with the same particle
example: (P1,P2), (P1,P3)
then we create two new particles instead of one
'''



def collision_detect():
    new_particles = []
    dead_particles = []
    for i in range(0,sim.num_particles,1):
        for j in range(i+1,sim.num_particles,1):
            p1 = sim.particles[i]
            p2 = sim.particles[j]
            if Particle.get_collided(p1,p2):
                #Remove both colliding particles
                dead_particles.append(p1)
                dead_particles.append(p2)
                #Replace with a single particle with their properties
                mv_x = p1.mass*p1.vel[0] + p2.mass*p2.vel[0]
                mv_y = p1.mass*p1.vel[1] + p2.mass*p2.vel[1]
                mass = p1.mass + p2.mass
                new_particles.append(Particle(
                    [(p1.pos[0]*p1.mass+p2.pos[0]*p2.mass)/mass,(p1.pos[1]*p1.mass+p2.pos[1]*p2.mass)/mass], #center of mass
                    [mv_x/mass, mv_y/mass], #momentum is conserved but not kinetic energy (inelastic collision)
                    mass
                ))
    if len(dead_particles) != 0:
        temp = []#will be filled with all the particles that did not experience a collision
        for p in sim.particles:
            if p in dead_particles: continue
            temp.append(p)
        sim.particles = temp
    sim.particles += new_particles#now add the new particles
    sim.num_particles = len(sim.particles)




def COM_dragging():#pretty useless method
#calculates COM, then shifts all positions s.t COM coincides with COF
    total_mass=param.num_particles_orig*param.common_mass
    COM=[0,0]
    for p in sim.particles:
        COM[0]+=p.mass*p.pos[0]
        COM[1]+=p.mass*p.pos[1]
      

    COM=[e/total_mass for e in COM]

    for p in sim.particles:
        p.pos[0]=p.pos[0]-COM[0]+600
        p.pos[1]=p.pos[1]-COM[1]+350
          
    
    
def clamp_to_edges():
    for p in sim.particles:
        r = p.get_radius()
        if p.pos[0]<=               r: p.vel[0]= abs(p.vel[0])
        if p.pos[1]<=               r: p.vel[1]= abs(p.vel[1])
        if p.pos[0]>=param.screen_size[0]-r: p.vel[0]=-abs(p.vel[0])
        if p.pos[1]>=param.screen_size[1]-r: p.vel[1]=-abs(p.vel[1])

    
