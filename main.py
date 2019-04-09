#!/usr/bin/python

import random

"""number of swarms"""
noSwarms = 2

"""number of particles per swarm"""
noPar = 2

"""number of iterations"""
noIt = 5

"""number of params being optimised"""
noParam = 1

""" the solution particle"""
class SolPart:

    def __init__(self, inParam, inVel):
        """ array of parameters being optimised """
        self.param = inParam
        """ array of velocity """
        self.vel = inVel

""" swarm class """
class Swarm:
    
    def __init__(self, inNumber, inNoParams):
        """number of particles in the swarm"""
        self.number = inNumber

        """number of paramters being optimised"""
        self.noParams = inNoParams

        """ particles initialisation """
        self.particles = []

        for i in range(inNumber):
            tempPar = SolPart([],[])
            for j in range(inNoParams):
                tempPar.param += [random.uniform(0,1)]
                tempPar.vel   += [random.uniform(0,1)]
            self.particles += [tempPar]


"""all the swarms!"""
swarms = []

""" Initialise the particles! """
for i in range(noSwarms):
    swarms += [Swarm(noPar,noParam)]

#print (len(swarms))

print(swarms[0].particles[0].param)

i = 1
j = 1

for sw in swarms:
    print ("===========")
    print ("Swarm " + str(i))
    for par in sw.particles:
        print ("===========")
        print ("Particle " + str(j))
        print ("Parameters")
        for pm in par.param:
            print (pm)
        print ("Veloctiy")
        for v in par.vel:
            print (v)
        j += 1
    i += 1
    j = 1


