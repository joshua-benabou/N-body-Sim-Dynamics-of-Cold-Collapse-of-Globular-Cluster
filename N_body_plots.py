import matplotlib.pyplot as plt

import N_body_parameters as param
import N_body_data_collection as data

def energy_vs_time():
    
    #------K+U+E graph
    fig=plt.figure()
    
    if param.lang=="French":
        fig.text(.80,.93,'lissage: '+param.display_status(param.softening))
    else:
        fig.text(.80,.93,'softening: '+param.display_status(param.softening))
    
    fig.text(.80,.96,'collisions: '+param.display_status(param.collisions))

    initial_energy=data.total_energy[0]
    energy_deviation= [abs((energy-initial_energy)/initial_energy) for energy in data.total_energy]

    
    plt.plot(data.times,data.kinetic_energy,'r', label='$K$')
    plt.plot(data.times,data.potential_energy,'b', label='$U$')
    plt.plot(data.times,data.total_energy,'k', label='$E_{tot}$')
    if param.lang=="French":
           plt.title('Energie vs temps')
    else:
        plt.title('Energy vs time')
    plt.xlabel('simtime',fontsize=18)
    if param.lang=="French":
         plt.ylabel('Energie ',fontsize=18)
    else:
        plt.ylabel('Energy ',fontsize=18)
    plt.legend()

    plt.show()
    
    #-------(delta E)/E graph
    fig=plt.figure()
    if param.lang=="French":
         fig.text(.80,.93,'lissage: '+param.display_status(param.softening))
    fig.text(.80,.93,'softening: '+param.display_status(param.softening))
    fig.text(.80,.96,'collisions: '+param.display_status(param.collisions))

    plt.plot(data.times,energy_deviation,'k')
    if param.lang=="French":
        plt.title("Variation d'energie vs temps")
    plt.title('Energy change vs time')
    plt.xlabel('simtime',fontsize=18)
    plt.ylabel('$ | \Delta E/E_0 |$',fontsize=18)
    plt.legend()

    plt.show()

    #------virial ratio
    virial_ratio= [data.kinetic_energy[k]/(-data.potential_energy[k]) for k in range (len(data.potential_energy))]

    fig=plt.figure()
    if param.lang=="French":
          fig.text(.80,.93,'lissage: '+param.display_status(param.softening))
    fig.text(.80,.93,'softening: '+param.display_status(param.softening))
    fig.text(.80,.96,'collisions: '+param.display_status(param.collisions))

    plt.plot(data.times,virial_ratio,'k')
    if param.lang=="French":
          plt.title('Rapport du viriel vs temps')
    plt.title('Virial ratio vs time')
    plt.xlabel('simtime',fontsize=18)
    plt.ylabel('$-K/U$',fontsize=18)
    plt.legend()

    plt.show()

def N_vs_time():        

    fig=plt.figure()
    if param.lang=="French":
         fig.text(.80,.93,'lissage: '+param.display_status(param.softening))
    fig.text(.80,.93,'softening: '+param.display_status(param.softening))
    fig.text(.80,.96,'collisions: '+param.display_status(param.collisions))   

    plt.plot(data.times,data.particle_number,'k')
    
    if param.lang=="French":
          plt.title('Nb de particles vs time')
    plt.title('Particle number vs time')
    plt.xlabel('simtime',fontsize=18)
    plt.ylabel('N',fontsize=18)
    plt.legend()

    plt.show()

def computation_speed_vs_time():
    fig=plt.figure()
    if param.lang=="French":
          fig.text(.80,.93,'lissage: '+param.display_status(param.softening))
    else:
        fig.text(.80,.93,'softening: '+param.display_status(param.softening))
    fig.text(.80,.96,'collisions: '+param.display_status(param.collisions))    

    plt.plot(data.times[1:],data.speed[1:],'k')
    if param.lang=="French":
          plt.title('Taux de calcul vs temps')
    else:
        plt.title('Computation speed vs time')
    plt.xlabel('simtime',fontsize=18)
    plt.ylabel('runtime/simtime',fontsize=18)
    plt.legend()

    plt.show()

def force_calculations_vs_time():
    fig=plt.figure()
    if param.lang=="French":
         fig.text(.80,.93,'lissage: '+param.display_status(param.softening))
    else:
        fig.text(.80,.93,'softening: '+param.display_status(param.softening))
    fig.text(.80,.96,'collisions: '+param.display_status(param.collisions))    

    plt.plot(data.times,data.force_calculations,'k')
    if param.lang=="French":
          plt.title('Nb de caluls de force par pas')
    else:
        plt.title('Number of force calculations per step')
    plt.xlabel('simtime',fontsize=18)
    if param.lang=="French":
         plt.ylabel('Nb de calculs de force',fontsize=18)
    else:
        plt.ylabel('Number of force calculations',fontsize=18)
    plt.legend()

    plt.show()

def num_binaries_vs_time():
    fig=plt.figure()
    if param.lang=="French":
        fig.text(.80,.93,'lissage: '+param.display_status(param.softening))
    else:
        fig.text(.80,.93,'softening: '+param.display_status(param.softening))
    fig.text(.80,.96,'collisions: '+param.display_status(param.collisions))    

    plt.plot(data.times,data.num_binaries,'k')
    if param.lang=="French":
         plt.title('Nb de binaires vs temps')
    else:
        plt.title('Number of binaries per time')
    plt.xlabel('simtime',fontsize=18)
    if param.lang=="French":
        plt.ylabel('Nb de binaires',fontsize=18)
    else: 
        plt.ylabel('Number of binaries',fontsize=18)
    plt.legend()

    plt.show()

def central_density_vs_time():
    fig=plt.figure()
    if param.lang=="French":
        fig.text(.80,.93,'lissage: '+param.display_status(param.softening))
    else:
        fig.text(.80,.93,'softening: '+param.display_status(param.softening))
    fig.text(.80,.96,'collisions: '+param.display_status(param.collisions))    

    plt.plot(data.times,data.central_density,'k')
    if param.lang=="French":
         plt.title('Densite centrale vs temps')
    else:
        plt.title('Central density per time')
    plt.xlabel('simtime',fontsize=18)
    if param.lang=="French":
        plt.ylabel('N_core/N_0',fontsize=18)
    else:
        plt.ylabel('Central density',fontsize=18)
    plt.legend()

    plt.show()

def evaporation_ratio_vs_time():
    fig=plt.figure()
    if param.lang=="French":
        fig.text(.80,.93,'lissage: '+param.display_status(param.softening))
    else:
        fig.text(.80,.93,'softening: '+param.display_status(param.softening))
    fig.text(.80,.96,'collisions: '+param.display_status(param.collisions))    

    plt.plot(data.times,data.evaporation_ratio,'k')
    if param.lang=="French":
       plt.title("Echelle de temps de l'évaporation")
    else:
        plt.title('Time scale of escape')
    

    plt.xlabel('simtime',fontsize=18)
    plt.ylabel('N/N_0',fontsize=18)
    plt.legend()

    plt.show()

def BH_vs_DC():
    fig=plt.figure()    

    plt.plot(data.list_n,data.exec_time_DC,'b', label='$DC$')
    plt.plot(data.list_n,data.exec_time_BH,'k', label='BH')

    if param.lang=="French":
        plt.title('Barnes-Hut vs Comparaison Directe')
    else:
        plt.title('Barnes-Hut vs Direct Comparison')

    if param.lang=="French":
        plt.xlabel('Nb de particules',fontsize=18)
    else:
        plt.xlabel('Particle number',fontsize=18)

    if param.lang=="French":
        plt.ylabel("Temps d'execution",fontsize=18)
    else:
        plt.ylabel('Execution time',fontsize=18)
 
    plt.legend()

    plt.show()


