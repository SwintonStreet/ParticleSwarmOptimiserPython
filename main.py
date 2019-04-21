#!/usr/bin/python3

import random
import math
import copy
import sys

def help() :
    print ( "\
\
A python implementation of a particle swarm optimisation.\n\
\n\
Takes the following mandatory variables,\n\
\n\
    -s  <Number of swarms>\n\
    -sp <Number of particles per swarm>\n\
    -i  <Number of iterations to use for the simulation>\n\
    -p  <Number of parameters being optimised>")


"""number of swarms"""
noSwarms = 0

"""number of particles per swarm"""
noPar = 0

"""number of iterations"""
noIt = 0

"""number of params being optimised"""
noParam = 0

# read in values from script
# start at 1 as 0 is the script name
i = 1
while i < len(sys.argv) :
    if sys.argv[i] == "-s" :
        noSwarms = int(sys.argv[i+1])
    elif sys.argv[i] == "-i" :
        noIt     = int(sys.argv[i+1])
    elif sys.argv[i] == "-sp" :
        noPar    = int(sys.argv[i+1])
    elif sys.argv[i] == "-p" :
        noParam  = int(sys.argv[i+1])
    else:
        print("unrecognised parameter [" + sys.argv[i] + "]")
    i += 2

# if the mandatory paramters are missing print help and exit
if  noSwarms == 0 or \
    noIt     == 0 or \
    noPar    == 0 or \
    noParam  == 0 :
    help()
    exit()

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
            print ("Velocity")
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
    phi1 = 0.4
    for i in range(len(Par.param)):
        Par.vel[i] = Par.vel[i] + (
                   phi1 * random.uniform(0,1) * (bestPar.param[i] -
                                                 Par.param[i]))
        if (Par.vel[i] > 1) :
            Par.vel[i] = 1
        elif (Par.vel[i] < -1) :
            Par.vel[i] = -1

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
                sw.bestPar = copy.deepcopy(par)

        # if we have found the best fit of all the swarms then
        # update it
        if sw.bestPar.fit < bestOfTheBestPar.fit :
            bestOfTheBestPar = copy.deepcopy(sw.bestPar)

def prettyPrintSys(inIt,
                   inSw,
                   inPar,
                   inParam):
    print ("System settings:" +
           "\nIterations          : [" + str(inIt)    + "]" +
           "\nSwarms              : [" + str(inSw)    + "]" +
           "\nParticles per swarm : [" + str(inPar)   + "]" +
           "\nParameters          : [" + str(inParam) + "]")



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
            self.vel   += [random.uniform(0,maxVel) - (maxVel / 2.0)]

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
                self.bestPar = copy.deepcopy(tempPar)
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

# open the output file
output    = open("Output.txt",'w')
outputPar = open("OutputPar.txt",'w')

# performing the simulation now
print("Performing PSO simulation now!")
prettyPrintSys(noIt,
               noSwarms,
               noPar,
               noParam)
endChar = ""

# we are ready to perform the iterations to try optimise
for i in range(1,noIt+1):
    scale = int((i/(noIt + 1)) * 51)
    reverseScale = 50 - scale
    if i == noIt :
        endChar = "\n"
    print("[" + "=" * scale        +
                " " * reverseScale + "]" +
                endChar, end="\r" )
    updatePosition(swarms)
    updateVelocity(swarms)
    updateSystemFit(swarms,
                    posData,
                    refData,
                    bestOfTheBest)

    # print out swarm information
    j = 1
    for sw in swarms:
        #print ( "best fit for swarm [" + str(j) + "] is [" + str(sw.bestPar.fit) + "]"  )
        output.write(str(i) + " " +
                     str(j) + " " +
                     str(sw.bestPar.fit))

        for pm in sw.bestPar.param:
            output.write(" " + str(pm))

        k = 1
        for Par in sw.particles:
            for pm in Par.param:
                outputPar.write(str(i)  + " " +
                                str(j)  + " " +
                                str(k)  + " " +
                                str(pm) + "\n")
            k += 1

        output.write("\n")
        j += 1

output.close()
outputPar.close()

