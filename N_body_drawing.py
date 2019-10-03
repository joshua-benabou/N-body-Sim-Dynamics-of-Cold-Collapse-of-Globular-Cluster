#Colors
black=0,0,0
white=255,255,255
red=255,0,0

import pygame
import time

import N_body_parameters as param
import N_body_sim_manager as sim

#---------------------------------------------------

def draw():
    sim.surface.fill(black,[0,650,1200,50])
    if (not param.tracing):
        sim.surface.fill(black)
    
    for p in sim.particles:
        pygame.draw.circle(sim.surface,
                           p.color,
                           (rndint(p.pos[0]),rndint(p.pos[1])),
                            rndint(p.get_radius()),
                            0)
    
    font = pygame.font.SysFont('Consolas', 30)
    font2 = pygame.font.SysFont('Consolas', 15)
    time_elapsed=pygame.time.get_ticks()/1000 #converted to seconds
    mlsec = repr(time_elapsed).split('.')[1][:2]
    timer=time.strftime("runtime=%H:%M:%S".format(mlsec), time.gmtime(time_elapsed))  
    sim.surface.blit(font.render(timer, True, (white)), (50,650))#displays program run time hr:min:sec

    sim_time="{0:.3f}".format(sim.run*param.dt)###ISSUE:it seems the sim_time is not changing the last 0###
    sim.surface.blit(font.render('simtime= '+sim_time, True, (white)), (400,650))

    sim.surface.blit(font.render('N= '+str(sim.num_particles), True, (white)), (700,650))

    sim.surface.blit(font2.render('collisions: '+param.display_status(param.collisions), True, (white)), (820,650))
    sim.surface.blit(font2.render('softening: '+param.display_status(param.softening), True, (white)), (820,670))
    sim.surface.blit(font2.render('COM dragging: '+param.display_status(param.center_COM), True, (white)), (970,650))
    sim.surface.blit(font2.render('Barnes-Hut: '+param.display_status(param.barnes_hut), True, (white)), (970,670))

    if param.draw_radii:
        
        red=255,0,0
        pygame.draw.circle(sim.surface,
                           (red),
                           (600,350),
                            rndint(param.ccradius),
                            1)
        pygame.draw.circle(sim.surface,
                           (red),
                           (600,350),
                            rndint(param.core_radius),
                            1)
        






    pygame.display.flip()




#------------Service method---------------------------
def rndint(num): return int(round(num))
    
