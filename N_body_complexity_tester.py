import time
import N_body_integrate as integrate
import N_body_parameters as param
import N_body_sim_manager as sim

list_n=[]
exec_time_DC=[]
exec_time_BH=[]

n=1000

initial_conditions=sim.reset_initial_conditions(n)
param.barnes_hut=False
start_time = time.time()
print( len(sim.particles))
integrate.move()
exec_time_DC=time.time() - start_time
print('exec_time_DC: ' + str(exec_time_DC))


particles=initial_conditions
param.barnes_hut=True
start_time = time.time()
integrate.update_forces()
exec_time_BH=time.time() - start_time
print('exec_time_BH: ' + str(exec_time_BH))


