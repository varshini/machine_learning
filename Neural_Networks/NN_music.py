import os
import sys
import math
import numpy
import random

################################################################################
# globals, definitions & notes 
################################################################################

# i is used to loop through the attributes (x_i)
# j is used to loop through hidden nodes (y_j)
# k is used to loop through each member of cohort
cohort = [] # list of all the objects of cohort
allData = [] # 2D list of all input data in a single location
targets = [] # list of only target values
attributes = [] # list of attributes
weightX = [] # weight from input to hidden layer (2D list)
weightY = [] # weight from hidden layer to output (1D list)
hiddenNodes = 3 # number of nodes to use in hidden layer
iterationCounter = 0 # how many times entire sample has been iterated
outputs = [] # keep track of output values
eta = 0.05 # step size / learning-rate
iterationNum = 3000 # how many times to iterate through training sample

################################################################################
# class definitions
################################################################################

class subject(object) :
  def __init__(self, idnum, inputs, target) :
    self.id = idnum
    self.input = inputs # given training data
    self.target = target # target value
    self.output = 0.0 # calculated output value
    self.error = 0.0 # error of the output
    self.yval = [0 for j in range(hiddenNodes)] # output at each hidden node
    self.yerr = [0 for j in range(hiddenNodes)] # errors of each hidden node

  def __repr__(self) :
    return  "%s" % self.target

################################################################################
# file IO 
################################################################################

# from 15-112 Fall 2015 Website
def readFile(path):
  with open(path, "rt") as f:
    return f.read()

# read from arguments and update globals
def readArg(doc) :
  global attributes, allData, targets
  readDoc = readFile(doc).splitlines()
  for line in range(len(readDoc)) :
    if line == 0 : # attributes (A)
      for attribute in readDoc[line].split(",") :
        attributes.append(attribute)
    if line > 0 : # cohort members (x) 
      member = []
      member.append(1)
      readData = readDoc[line].split(",")
      for value in range(len(readData)) :
        if value == 0 : member.append(modifyYear(readData[value]))
        elif value == 1 : member.append(float(readData[value])/10)
        else : 
          if readData[value] == "yes" : member.append(1)
          else : member.append(0)
      allData.append(member[:-1])
      targets.append(member[-1])
      newSubject = subject(line-1, numpy.array(member[:-1]), member[-1])
      cohort.append(newSubject)
  targets = numpy.array(targets)
  allData = numpy.array(allData)

# print error with correct format
pE = 1000
def printCurError(errorVal) :
  global iterationCounter, pE
  if errorVal < pE : 
    sys.stdout.write(str(errorVal) + "\n")
  else : 
    return
  pE = errorVal


def modifyYear(year) :
  newYear = int(year[:-2])
  return (newYear / 100)

################################################################################
# init & operations
################################################################################

# initially select random values for weight
def initWeight(num) :
  global cohort, weightX, weightY
  attrNum = len(attributes)
  # random weights from x to y
  for j in range(num) :
    weights = []
    for i in range(attrNum) :
      newWeight = (random.random() - 0.5)
      weights.append(newWeight/10)
    weightX.append(weights)
  weightX = numpy.array(weightX)
  # random weights from y to output
  for j in range(num) :
    newWeight = (random.random() - 0.5)
    weightY.append(newWeight)
  weightY = numpy.array(weightY)

# check if training should continue
def checkTraining(num) :
  if iterationCounter == iterationNum : return True
  else : return False

################################################################################
# Calculations
################################################################################

def transfer(num) :
  return 1 / (1 + math.exp(-num))

def calcYval(node) :
  for internal in range(hiddenNodes) :
    # list of weights from X(input) to a single internal node
    xyWeights = weightX[internal]
    #print(xyWeights)
    inputVal = numpy.array(node.input)
    node.yval[internal] = calcOutput(xyWeights, inputVal)

# calculate output value (output value at hidden nodes)
def calcOutput(weights, values) :
  calculated = sum(weights * values)
  return transfer(calculated)

# calculate the error given target and calculated value
def calcDeltaK(node) :
  node.error = node.output * (1 - node.output) * (node.target - node.output)
 
# calculate the error between target and output
def calcDeltaH(node) :
  for internal in range(hiddenNodes) :
    O_h = node.yval[internal]
    node.yerr[internal] = O_h * (1 - O_h) * weightY[internal] * node.error

################################################################################
# Backpropagation (much painful, very headache)
################################################################################

# update weights based on newly calculated errors
def updateWeights(node, eta) :
  global weightX, weightY, hiddenNodes
  # update weightX
  for internal in range(hiddenNodes) :
    factor = eta * node.yerr[internal]
    factors = [factor for i in range(len(attributes))]
    factors = numpy.array(factors)
    weightX[internal] = weightX[internal] + factors * node.input
  # update weightY
  factor = eta * node.error
  factors = [factor for i in range(hiddenNodes)]
  factors = numpy.array(factors)
  weightY = numpy.array(weightY + factors * node.yval)

# return the sum of errors for all output - target
def outputErrorSum() :
  global outputs, iterationCounter
  iterationCounter += 1
  outputs = numpy.array(outputs)
  difference = (outputs - targets) ** 2
  return sum(difference) / 2

# backpropagation master code
def bp() :
  global cohort, outputs, eta, iterationNum
  sampleSize = len(cohort)
  test_in_progress = True
  k = 0 # start with sample0
  while test_in_progress :
    curNode = cohort[k]
    # calculate output at each node
    calcYval(curNode) # hidden nodes
    curNode.output = calcOutput(weightY, curNode.yval) # output
    outputs.append(curNode.output)
    # calculate error at each node
    calcDeltaK(curNode) # delta_k
    calcDeltaH(curNode) # delta_h
    # update the weights (incremental gradient descent)
    updateWeights(curNode, eta)
    # check if ready to terminate training
    if checkTraining(k) : test_in_progress = False
    # move onto next sample / if at the end, loop around
    k += 1
    if k == sampleSize :
      # test new weights on entire data set & calculate new error
      globalError = outputErrorSum() 
      printCurError(globalError)
      k = 0
      outputs = []
      # if iterationCounter % (iterationNum/10) == 0 : 
      #   eta = eta * 0.85

################################################################################
# test Hypothesis
################################################################################

def readTestData(doc) :
  testData = []
  readDoc = readFile(doc).splitlines()
  for line in range(len(readDoc)) :
    if line > 0 : # cohort members (x) 
      member = []
      member.append(1)
      readData = readDoc[line].split(",")
      for value in range(len(readData)) :
        if value == 0 : member.append(modifyYear(readData[value]))
        elif value == 1 : member.append(float(readData[value])/10)
        else : 
          if readData[value] == "yes" : member.append(1)
          else : member.append(0)
      testData.append(member)
  testData = numpy.array(testData) 
  return testData

answerkeys = []
def readKey() :
  global answerkeys
  readData = readFile("music_dev_keys.txt").splitlines()
  for line in readData :
    if line == "yes" : answerkeys.append(1)
    else : answerkeys.append(0)

def testHypothesis(testData) :
  readKey()
  testYvals = []
  calcKeys = []
  global answerkeys
  # calculate values for the hidden nodes
  for tester in range(len(testData)) : 
    inputVal = numpy.array(testData[tester])
    intermedVal = []
    for internal in range(hiddenNodes) :
      # list of weights from X(input) to a single internal node
      xyWeights = weightX[internal]
      #print(xyWeights)
      intermedVal.append(calcOutput(xyWeights, inputVal))
    testYvals.append(intermedVal)
  # calculate the overal output from the hidden nodes
  errorcounter = 0
  for tester in range(len(testData)) :
    testValues = numpy.array(testYvals[tester])
    calculatedVal = calcOutput(weightY, testValues)
    calcKeys.append(calculatedVal)
    if calculatedVal >= 0.5 : 
      if answerkeys[tester] == 0 : errorcounter += 1
      sys.stdout.write("yes\n")
    else : 
      sys.stdout.write("no\n")
      if answerkeys[tester] == 1 : errorcounter += 1

################################################################################
# main
################################################################################

train_file = sys.argv[1]
test_file = sys.argv[2]
readArg(train_file) # read from file  and update the cohort list
initWeight(hiddenNodes) # randomly select weight values for all connections
bp()
sys.stdout.write("TRAINING COMPLETED! NOW PREDICTING.\n")
testData = readTestData(test_file)
testHypothesis(testData)

