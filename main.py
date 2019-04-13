#!/usr/bin/python

import random
import math

"""number of swarms"""
noSwarms = 2

"""number of particles per swarm"""
noPar = 2

"""number of iterations"""
noIt = 5

"""number of params being optimised"""
noParam = 1

""" position data  """
posData = []

""" reference data """
refData = []

###############################################################################
####                         READING IN DATA                               ####
###############################################################################

def readInData(fileName, storingVar):
    f = open(fileName,'r')

    try:
        for line in f:
            storingVar += [line.strip().split(',')]
    finally:
        f.close()

readInData("PosData.txt",posData)
readInData("RefData.txt",refData)

###############################################################################
####                              END                                      ####
###############################################################################

def printSystem(inSwarms):
    # counting variables
    i = 1
    j = 1

    for sw in inSwarms:
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

# The model we are optimising
def model(inPos, inPar):
    # the test model is f(x) = n + sin(x) where we are optimising n
    value = inPar[0] + math.sin(inPos[0])

    return value

# applies the model to the data and sums the difference between
def fitFromData(inData,inRefValues,inPar):

    # value representing how good the fit is
    # the smaller the better!
    fitValue = 0

    for i in range(len(inData)):
        fitVale += ( (model(pos[i],inPar) - refData[i])**2 )

    return fitValue


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

#printSystem(swarms)

