
 #TO DO
'''
0.FIXING THE CODE:
    -collisions not working: gives false reading of particle number
    also moves the particles in a weird way

    -also changed something in the code by mistake: wanted to figure out why tree depth was so large,
    so i adjusted the size of the root node to make it smaller, but now the tree isnt displaying

    -number of force calculations per step seems to be reporting erroneous values for N=5 (for example)

    -find out how to properly scale colors
    
    -Figure out how to draw the frames at a constant speed

    -How to zoom in/out to view all the particles in the system


ANALYZING THE CODE

1.Test BH for accuracy/speed 
    -Finish implementing data collection methods for analysis of BH algorithm
    -Ensure that BH is as fast as it should be (it seems to be twice as slow as it should be)

2.Investigate energy drift
    -Why is the sim with (inelastic) collisions and no softening showing an increase in total energy, whereas energy should be lost!
    -How is the Verlet algorithm self correcting? (How does energy spike up and then come back to its previous value?)
    -How to choose the softening parameter epsilon so as to minimize energy drift 

***THE REAL PHYSICS STARTS HERE:

-Proper choice of units

COLLISIONAL

3.Figure out how to set up intial conditions for solar system formation
    -if we initialize the COM to coincide with the COF and to have 0 velocity, we can avoid the calculation for COM dragging
    -how come we haven't seen the formation of any moons thus far?

COLLISIONLESS

4.Simulation of cold collapse
    -plummer sphere (note: the sim is 2D, so the theoretical results don't apply!)
    -measure evolution of virial ratio
    -measure time in units of crossing/relaxation times
    -measure production of binaries
    -measurement of Virial radius
    -number of stars escaping the system
    -mass density vs radius

****FOR THE FUTURE:*****

5. Simulation of rotating galaxy
    -measure velocity rotation curve (velocity vs distance)

6. Galaxy merger sim

'''
#-----------------------------------------
#KEYBOARD COMMANDS
'''
tracing: t (doesn't work fully because in the way it displays the quad_tree)
collisions: c
COM dragging: d
capture image: i
edge-clamping: e
pause: p
end simulation: ESC
reset: r (does not reset clocks/graphs!)+relies on the no longer existent method sim.initialization

'''
#------------------------------------------
#IMPORTS

#modules external to this project
import pygame
import sys, os, traceback
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"


#N_body modules

import N_body_parameters as param
import N_body_sim_manager as sim
import N_body_integrate as integrate
import N_body_sim_options as option
import N_body_data_collection as data
import N_body_drawing as drawing
import N_body_plots as plots

#variables
pause=False

#---------------------------------------------------------------------------------------
def get_input():
    '''
    variables which are defined outside of method need the identifier "global"...
    if they are to be modified inside the method; if they are only to be referenced, no identifier is needed
    '''
    
    keys_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    mouse_rel = pygame.mouse.get_rel()
    
    
    for event in pygame.event.get():
        if   event.type == pygame.QUIT: return False #what does this do?
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_t: param.tracing=not param.tracing
            if event.key==pygame.K_c: param.collisions=not param.collisions
            if event.key==pygame.K_i: data.take_photo()
            if event.key==pygame.K_d: param.center_COM=not param.center_COM
            if event.key==pygame.K_e: param.edge_clamp=not param.edge_clamp
            if event.key==pygame.K_p: global pause; pause = not pause
            if event.key == pygame.K_ESCAPE: return False
            elif event.key == pygame.K_r:#reset is broken, it only resets postions but not the clocks
                sim.initialization()#this no longer exists
                
    return True
     

def main():
   
    while True and sim.run<=param.max_num_runs:
        
        if not get_input(): break
        if not pause:
        
            integrate.move()
            
            if param.collisions: option.collision_detect()
            if param.edge_clamp: option.clamp_to_edges()
            
            if sim.run%(param.drawing_interval)==0:
                drawing.draw()
                sim.clock.tick(param.target_fps)
                if param.center_COM: option.COM_dragging()
                '''
                Note:
                
                If the COM is removed to coincide with the COF only every k drawing intervals (k>10),
                then if COM_dragging is set on, the planets will appear to shake.
                Increasing the frequency at which COM is reset to coincide with the COF removes the shaking
                
                '''
                #data collection
                data.update_times()
                if param.calculate_energy: data.update_energy()#!!!calculating the energy or not DOES affect the computation time!!!
                data.update_binaries()#new addition; note that the collection of data about binaries only needs to be done infrequently
                data.update_evaporation_ratio()
                data.update_central_density()
                #data.update_angular_momentum() #method doesn't exist yet
                data.update_particle_number()
                data.update_computation_speed()
                data.update_force_calculations()


            if param.camera and sim.run==param.capture_point:#takes an image when run=capture_point, but the image is of the last run drawn
                data.take_photo()
                
            sim.run+=1
    #--------------------------------end of while loop
    data.take_photo()
    pygame.quit()
    
    #plots
    if param.calculate_energy: plots.energy_vs_time()
    
    #plots.N_vs_time()  
    plots.computation_speed_vs_time()
    plots.force_calculations_vs_time()
    plots.num_binaries_vs_time()
    plots.central_density_vs_time()
    plots.evaporation_ratio_vs_time()
    
    
    

#--------------------------------------- 
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()
