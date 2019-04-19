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
def fitFromData(posData,inRefValues,inPar):

    # value representing how good the fit is
    # the smaller the better!
    fitValue = 0

    for i in range(len(posData)):
        fitValue += ( (model(posData[i],inPar.param) -
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
    i = 0
    j = 0
    #print("Position update")
    for sw in swarms:
        #print("Updating swarm: " + str(i))
        i += 1
        j = 0
        for par in sw.particles:
            updateParticlePosition(par)
            #print("Updating particle: " + str(j))
            #print(par.param)
            j+=1


# updates all the swarm's particle's velocity
def updateVelocity(swarms):
    for sw in swarms:
        for par in sw.particles:
            updateParticleVelocity(par,sw.bestPar)

# update the fit of each particle and the best particle of the swarm and all the
# swarms
def updateSystemFit(swarms,
                    posData,
                    refData,
                    bestOfTheBestPar):
    for sw in swarms:
        for par in sw.particles:
            par.fit = fitFromData(posData, refData, par)

            # if we find the best fit of all the particles
            # in the swamr then update the swarm to reflect this
            if par.fit < sw.bestPar.fit :
                sw.bestPar = par

        # if we have found the best fit of all the swarms then
        # update it
        if sw.bestPar.fit < bestOfTheBestPar.fit :
            bestOfTheBestPar = sw.bestPar



""" the solution particle"""
class SolPart:

    def __init__(self,
                 inParam,
                 inPosData,
                 inRefData):
        """ array of parameters being optimised """
        self.param = []
        """ array of velocity """
        self.vel   = []
        """ fit value """
        self.fit = -1

        for j in range(len(inParam)):

            minVal = inParam[j][0]
            maxVal = inParam[j][1]
            maxVel = (maxVal - minVal) / 10
            self.param += [random.uniform(minVal,maxVal)]
            self.vel   += [random.uniform(0,maxVel)]

        # we store the best found part
        self.fit = fitFromData(inPosData,
                               inRefData,
                               self)

""" swarm class """
class Swarm:

    def __init__(self,
                 inNumber,
                 inNoParams,
                 inParamData,
                 inPosData,
                 inRefData):
        """number of particles in the swarm"""
        self.number = inNumber

        """number of paramters being optimised"""
        self.noParams = inNoParams

        """ particles initialisation """
        self.particles = []

        """ best fit particle and value for the swarm """
        bestFit = -1

        for i in range(inNumber):
            tempPar = SolPart(inParamData,
                              inPosData,
                              inRefData)
            self.particles += [tempPar]

            if tempPar.fit < bestFit or bestFit < 0 :
                self.bestPar = tempPar
                bestFit      = tempPar.fit





"""all the swarms!"""
swarms = []

""" Initialise the swarms and their particles! """
for i in range(noSwarms):
    swarms += [Swarm(noPar,
                     noParam,
                     paramData,
                     posData,
                     refData)]

#print (len(swarms))
#print(swarms[0].particles[0].param)
#printSystem(swarms)
#print(posData)
#print(refData)
#print(paramData)


""" the best solution found of all the swarms """
bestOfTheBest = SolPart(paramData,
                        posData,
                        refData)

# we are ready to perform the iterations to try optimise
for i in range(1,noIt+1):
    print("Performing iteration: " + str(i) )
    updatePosition(swarms)
    updateVelocity(swarms)
    updateSystemFit(swarms,
                    posData,
                    refData,
                    bestOfTheBest)
    j = 1
    for sw in swarms:
        print ( "best fit for swarm [" + str(j) + "] is [" + str(sw.bestPar.fit) + "]"  )
        j += 1


