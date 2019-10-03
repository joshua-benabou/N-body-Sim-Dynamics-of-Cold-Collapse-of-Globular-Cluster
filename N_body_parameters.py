#BOOLEANS

#Collisions
collisions = False
#Whether tracing is enabled
tracing=False
#Whether to contrain particles to the edges.  Not affected by the collisions enabled flag.
edge_clamp = False
#Whether to center the COM at the COF
center_COM=True#note the boolean has the same name as the function COM_dragging()
#Whether gravitational softening is on:
softening=True
#Whether to use Barnes-Hut algorithm
barnes_hut=True
#Whether to DRAW the Barnes-Hut tree
'''note that even if the tree is not diplayed, drawing takes computation time'''
draw_tree=True
#Whether to DRAW the initial cluster radius and core radius
'''note that even if the tree is not diplayed, drawing takes computation time'''
draw_radii=True
#Whether to calculate the energy
'''this is to see whether calculting energy slows down the sim'''
calculate_energy=True
#Whether to color particles
coloring=False
#language
lang="English"
dimmension=2

def display_status(boolean):#auxilary function for function draw()
    if boolean: return "ON"
    return "OFF"

'''
Observation:

-with no collisions, softening greatly reduces the energy variation,
probably since the energy variation in close encounters is bounded

-with collisions, softening doesn't make much difference, probably because encounters close enough to create big errors are almost always collisions

'''

#Whether to take snapshots at periodic intervals
camera=False

#Radius scaling
radius_scaling=True

#----------------------------------------------------------------------------------------
#CONSTANTS

num_particles_orig=500

G = 10**4
'''
-Setting G=1 and imposing 200 pix/AU gives 1 mass unit = 1.05*10^12 M_e

-units=pixels^3 kg^-1 s^-2   ; actual value = 6.67384*(10^-11) m^3 kg^-1 s^-2

-G=10^4 is probably too high for our purposes because 2 particles placed at opposite sides of the screen
with equal mass (=common_mass) come close to eachother on a time scale smaller than the "equilibrium time"
of a N-large sim. This means far away particles have a significant effect on eachother,
in which case Barnes-Hut can't be applied

'''
common_mass=100
epsilon=0
if softening: epsilon=1
max_initial_speed = 100.0#Particles' maximum (random) speed (pixels/sec)

ccradius=300
core_radius=ccradius/3


#Timing
target_fps = 10**5
dt =1/target_fps
movement_substeps = 1#Movement substeps at the given timestep (what purpose does this serve???)
max_num_runs=10**20#effectively unlimited
drawing_interval=10#this greatly affects the sim speed since drawing is computationally expensive
'''
there is a trade-off between accuracy and speed. increasing target_fps decreases dt, increases accuracy.
increases drawing_interval increases rendering speed, but only to a ceartain point, if target_fps is too high,
rendering speed is limited by the computation speed
'''

#Pygame display
screen_size = [1200,700]#center of mass=center of window=[600,350]


#Radius scaling
radius_scale = 0.5
default_radius=3

#Camera
capture_point=drawing_interval*(10**4)# number of runs after which a picture is taken
file_name='N-body_sim'


#max value of force

max_force=G*common_mass**2/epsilon#only valid if softening is on
















