#!/usr/bin/python3

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

""" param min and max data """
paramData = []

###############################################################################
####                         READING IN DATA                               ####
###############################################################################

def readInData(fileName, storingVar):
    # open file for reading only
    f = open(fileName,'r')

    try:
        for line in f:
            # get this point's data and convert it to a float
            pointData = []
            for val in line.strip().split(','):
                pointData += [float(val)]

            # add it to the set of data
            storingVar += [pointData]
    finally:
        f.close()

readInData("PosData.txt",posData)
readInData("RefData.txt",refData)
readInData("ParamData.txt",paramData)

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
        fitValue += ( (model(inData[i],inPar.param) -
                       inRefValues[i][0])**2 )

    return fitValue

# update particles postion
def updateParticlePosition(Par):
    for i in range(len(Par.param)):
        Par.param[i] += Par.vel[i]

# update particles velocity
def updateParticleVelocity(Par,bestPar):
    phi1 = 2.0
    for i in range(len(Par.param)):
        Par.vel[i] = Par.vel[i] + (
                   phi1 * random.uniform(0,1) * (bestPar.param[i] -
                                                 Par.param[i]))

# updates all the swarm's particle's positions
def updatePosition(swarms):
    for sw in swarms:
        for par in sw.particles:
            updateParticlePosition(par)


# updates all the swarm's particle's velocity
def updatePosition(swarms):
    for sw in swarms:
        for par in sw.particles:
            updateParticleVelocity(par,sw.bestPar)

""" the solution particle"""
class SolPart:

    def __init__(self, inParam, inVel):
        """ array of parameters being optimised """
        self.param = inParam
        """ array of velocity """
        self.vel = inVel

""" swarm class """
class Swarm:

    def __init__(self,
                 inNumber,
                 inNoParams,
                 inParamData,
                 inRefData,
                 inPosData):
        """number of particles in the swarm"""
        self.number = inNumber

        """number of paramters being optimised"""
        self.noParams = inNoParams

        """ particles initialisation """
        self.particles = []

        """ best fit particle and value for the swarm """
        self.bestPar = SolPart([],[])
        self.bestFit = -1
        bestFit      = -1

        for i in range(inNumber):
            tempPar = SolPart([],[])
            for j in range(inNoParams):

                minVal = inParamData[j][0]
                maxVal = inParamData[j][1]
                maxVel = (maxVal - minVal) / 10
                tempPar.param += [random.uniform(minVal,maxVal)]
                tempPar.vel   += [random.uniform(0,maxVel)]
            self.particles += [tempPar]

            # we store the best found part
            parFit = fitFromData(inPosData,inRefData,tempPar)
            if parFit < bestFit or bestFit < 0 :
                self.bestFit = parFit
                self.bestPar = tempPar





"""all the swarms!"""
swarms = []

""" Initialise the swarms and their particles! """
for i in range(noSwarms):
    swarms += [Swarm(noPar,
                     noParam,
                     paramData,
                     refData,
                     posData)]

#print (len(swarms))
#print(swarms[0].particles[0].param)
#printSystem(swarms)
print(posData)
print(refData)
print(paramData)

for i in range(noIt):
    print (i)
    i+=1

