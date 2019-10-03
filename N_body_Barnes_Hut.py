import N_body_sim_manager as sim
import pygame
import N_body_drawing as drawing
import N_body_parameters as param
from math import *

theta=1
root_length=(2**4)*1000

class Node(object):
    #a node is some data + a list of 4 nodes (its children)
    def __init__(self,TR,BL): 

        self.mass=0
        self.COM=[0,0]

        self.TR=TR
        self.BL=BL
        
        self.center=[(self.TR[0]+self.BL[0])/2,(self.TR[1]+self.BL[1])/2]  

        self.particles_contained=[]
        '''
        note that storing all the particles contained in a node is not necessary,
        however we do need a way to tell if the node is empty and to identify the single particle
        it contains if the node is a non-empty external node
        '''

        self.side_length=TR[0]-BL[0]

        self.children=[]
        
        #displaying the tree
        if param.draw_tree:
            red=255,0,0
            pygame.draw.rect(sim.surface, (red), (self.BL[0],self.TR[1],self.side_length,self.side_length),1)
        
    def add_particle(self,p):#adds particle to node and updates data accordingly
        self.particles_contained+=[p]
        temp=self.mass#is this a reference?
        self.mass+=p.mass#updates node mass
        self.COM[0]=(self.COM[0]*temp+p.pos[0]*p.mass)/self.mass#updates node COM
        self.COM[1]=(self.COM[1]*temp+p.pos[1]*p.mass)/self.mass
        
    def birth_children(self):#subdivides the node into 4 quadrants (the node "gives birth" to 4 children)
        c=self.center
        
        child_1=Node([c[0],self.TR[1]],[self.BL[0],c[1]])
        self.children+=[child_1]
        
        child_2=Node(self.TR,self.center)
        self.children+=[child_2]
        
        child_3=Node(c,self.BL)
        self.children+=[child_3]
        
        child_4=Node([self.TR[0],c[1]],[c[0],self.BL[1]])
        self.children+=[child_4]

root=Node([root_length,-root_length],[-root_length,root_length])#definition of root node
'''
note that the root of the tree must contain all particles, otherwise an error is produced!!!
meaning if a particle is ejected from the system and moves off to infinity, the root node of the quadtree
would either have to continue increasing in size in order to include this particle,
or forget about this particle and remain a fix size (after all, the gravitational influence of this particle will go to zero)
'''
num_nodes=1#number of nodes in tree which starts from root

def reset_tree():
    '''
    this is a bad reset because all the other nodes still exist in the memory,
    so we will rapidly fill up the memory, no?
    '''
    global root
    root=Node([root_length,-root_length],[-root_length,root_length])
    num_nodes=1

def construct_tree():
    for p in sim.particles:
        '''careful, while the above line of code fixes the maximum recursion depth error,
it means that particles are being included in the force calculation, which lowers the run time, thus giving the
impression that BH is faster than it actually is
'''
        if abs(p.pos[0])<root_length and abs(p.pos[1])<root_length:#if p inside root node
            traverse(root,p)#we will traverse the tree from the root up

'''
recursive function such that the input traverse(root,p) places the particle p in the tree,
creating new nodes if necessary
'''
def traverse(node,p):#particles 
    if node.particles_contained==[]: node.add_particle(p)#if empty, add the particle
    elif not node.children==[]: #if the node is internal
        node.add_particle(p)
        #find which child of node p is contained in then do traverse(child,p)
        traverse(node.children[identify_quadrant(node,p)-1],p)
    else: #the only remaining case: the node is external and contains exactly one body
        q=node.particles_contained[0]#q is the single particle already contained in node
        node.add_particle(p)
        place_two_particles(node,p,q)
        
def place_two_particles(node,p,q):
    global num_nodes
    
    #places the particles p and q which are the only 2 particles contained in node
    #assumes node is external and when passed contains exactly 2 particle's (p and q) (but has no children yet)
    node.birth_children()
    num_nodes+=4
    quadrant_p=identify_quadrant(node,p)
    child_p=node.children[quadrant_p-1]#child of node containing p
    child_p.add_particle(p)
  
    quadrant_q=identify_quadrant(node,q)
    child_q=node.children[quadrant_q-1]#child of node containing q
    child_q.add_particle(q)

    if quadrant_p==quadrant_q: place_two_particles(child_p,p,q)#if p and q lie in the same quadrant, recurse

    #the recursion must finish since p!=q

        
#returns which quadrant of node contains the particle p (assumes p is contained in node)
#quadrants are labeled 1 (TL),2 (TR),3 (BL),4 (BR)
def identify_quadrant(node,p):
    #because in pygame the coordinates are given with the normal y-axes of the Cartesian plane flipped
    if p.pos[1]>node.center[1]: TB_half=[3,4]
    else: TB_half=[1,2]
    
    if p.pos[0]<node.center[0]: quadrant=TB_half[0]
    else: quadrant=TB_half[1]
    
    return quadrant


def force(node,p):#this doesn't make sense if p is contained in node, because then COM and mass include the mass of p
    num_calculations=0
    dx = p.pos[0]-node.COM[0]
    dy = p.pos[1]-node.COM[1]
    d_squared = dx*dx + dy*dy+param.epsilon
    d = d_squared**0.5

    if node.particles_contained!=[] and node.particles_contained!=[p]:#only calculate face for nonemtpy nodes not consisting only of the particle p
        if node.children==[] or node.side_length/d<theta: #if the node is external or internal and sufficeintly far from particle p
        
            force_magnitude =  (param.G * p.mass * node.mass)/d_squared#F=G*M1*M2/(d^2)
            dx_normalized_scaled = -(dx / d) * force_magnitude
            dy_normalized_scaled = -(dy / d) * force_magnitude
            p.forces[0] += dx_normalized_scaled
            p.forces[1] += dy_normalized_scaled

            num_calculations+=1  
        else:
            for child in node.children:
                num_calculations+=force(child,p)#simultaneously updates num_calculations and exectues force(child,p)

    return num_calculations
        
def tree_depth(node):
    if node.children==[]: return 1
    else: return 1+max([tree_depth(child) for child in node.children])

def number_leafs(node):
    if node.children==[]: return 1
    else:
        l=[number_leafs(child) for child in node.children]
        return l[0]+l[1]+l[2]+l[3]    

