import sys
import os
import math

################################################################################
# variables & classes
################################################################################

positives = ["yes", "democrat", "A", "+"]
tree = []

# PosNumY = # of cohort with positive phenotype that has posFeat
# PosNumN = # of cohort with positive phenotype that has negFeat
# negNumY = # of cohort with negative phenotype that has posFeat
# negNumN = # of cohort with negative phenotype that has negFeat

class node(object) :
    def __init__(self, feature, posFeat, negFeat, posNumY, posNumN, negNumY, negNumN, entropy) :
        self.type = feature
        self.posFeat = posFeat
        self.negFeat = negFeat
        self.posNumY = posNumY
        self.posNumN = posNumN
        self.negNumY = negNumY
        self.negNumN = negNumN
        self.posChildren = []
        self.negChildren = []
        self.entropy = entropy

    def __repr__(self) :
        return  "%s" % self.type

################################################################################
# file IO 
################################################################################

# from 15-112 Fall 2015 Website
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

# read from the file and return only the outcome #'s & cohort size
def readArg(doc) :
    global total
    attributes = []
    cohort = []

    readDoc = readFile(doc).splitlines()
    for line in range(len(readDoc)) :
        if line == 0 : # attributes (A)
            for attribute in readDoc[line].split(",") :
                attributes.append(attribute)
        if line > 0 : # cohort members (x) 
            member = []
            for value in readDoc[line].split(",") :
                member.append(value)
            cohort.append(member)
    total = len(cohort)
    return attributes, cohort

# output proper printing format and print to stdout
def printFormat(initPos, initNegerror_test, error_train, error_test) :
    lines = []
    lines.append("[" + str(initPos) + "+/" + str(initNeg) + "-]\n")
    node = tree[0]
    lines.append(node.type + " = " + node.posFeat + ": [" + str(node.posNumY) + "+/" + str(node.posNumN) + "-]\n")
    for child in node.posChildren :
        lines.append("| " + child.type + " = " + child.posFeat + ": [" + str(child.posNumY) + "+/" + str(child.posNumN) + "-]\n")
        lines.append("| " + child.type + " = " + child.negFeat + ": [" + str(child.negNumY) + "+/" + str(child.negNumN) + "-]\n")
    lines.append(node.type + " = " + node.negFeat + ": [" + str(node.negNumY) + "+/" + str(node.negNumN) + "-]\n")
    for child in node.negChildren :
        lines.append("| " + child.type + " = " + child.posFeat + ": [" + str(child.posNumY) + "+/" + str(child.posNumN) + "-]\n")
        lines.append("| " + child.type + " = " + child.negFeat + ": [" + str(child.negNumY) + "+/" + str(child.negNumN) + "-]\n")
    lines.append("error(train): " + str(error_train) + "\n")
    lines.append("error(test): " + str(error_test) + "\n")

    for line in lines : 
        sys.stdout.write(line)

################################################################################
# data Analysis
################################################################################

# return list of sub-cohort that classify as 'trait' for 'best Attribute'
# a = index of the attribute that is being eliminated
# trait = value of the cohort's attribute at index a 
def newList(attr, cohort, trait, a) :
    newCohort = []
    for member in range(len(cohort)) :
        if cohort[member][a] == trait : 
            newTraits = []
            for char in range(len(attr)) :
                if char != a : 
                    newTraits.append(cohort[member][char])
            newCohort.append(newTraits)
    return newCohort

# calculate entropy of 2 values of an attribute
def calcEntropy(num1, num2) : 
    global positives
    total = num1 + num2
    if total == 0 : return 0
    P1, P2 = num1 / float(total), num2 / float(total)
    entropy = 0
    if P1 > 0 : entropy += P1 * math.log(1/P1, 2)
    if P2 > 0 : entropy += P2 * math.log(1/P2, 2)
    return entropy

# analysis of feature - values of attributes and their phenotypes
def featureAnalysis(cohort, index) :
    posFeat, negFeat = "", ""
    posNumY, posNumN, negNumY, negNumN = 0, 0, 0, 0
    for member in cohort : 
        if posFeat == "" : posFeat = member[index]
        elif negFeat == "" and posFeat != member[index] : negFeat = member[index]
        if member[index] == posFeat : 
            if member[-1] in positives : posNumY += 1
            else : posNumN += 1
        else : # member[index] = negFeat 
            if member[-1] in positives : negNumY += 1
            else : negNumN += 1
    if posNumY > negNumY : return posFeat, negFeat, posNumY, posNumN, negNumY, negNumN
    else : return negFeat, posFeat, negNumY, negNumN, posNumY, posNumN

# recursively build tree, as long as Mutual Information >= 0.1
def buildTree(attr, cohort, entropy, parentNode = None, att = False) :
    if len(attr) == 1 : return
    bestFeat = None
    bestMI = 0
    bestIndex = 0
    bestEntropy = 0
    if parentNode != None : 
        if att : entropy = calcEntropy(parentNode.posNumY, parentNode.posNumN)
        else : entropy = calcEntropy(parentNode.negNumY, parentNode.negNumN)
    for a in range(len(attr)-1) :
        posFeat, negFeat, posNumY, posNumN, negNumY, negNumN = featureAnalysis(cohort, a)
        posW = (posNumY + posNumN) / float(len(cohort))
        negW = (negNumY + negNumN) / float(len(cohort))
        newEntropy = posW * calcEntropy(posNumY, posNumN) + negW * calcEntropy(negNumY, negNumN)
        MI = entropy - newEntropy
        if MI > bestMI : 
            newNode = node(attr[a], posFeat, negFeat, posNumY, posNumN, negNumY, negNumN, entropy)
            bestFeat, bestIndex, bestEntropy, bestMI = newNode, a, newEntropy, MI

    if bestMI < 0.1 : return
    if len(tree)> 0 and parentNode != tree[0] : return 
    else : 
        if parentNode != None : 
            if att : parentNode.posChildren.append(bestFeat)
            else : parentNode.negChildren.append(bestFeat)
        tree.append(bestFeat)
        newAttr = [at for at in attr if at != bestFeat.type]
        chL = newList(attr, cohort, bestFeat.negFeat, bestIndex)
        chR = newList(attr, cohort, bestFeat.posFeat, bestIndex)
        return (buildTree(newAttr, chL, bestEntropy, bestFeat, False)), (buildTree(newAttr, chR, bestEntropy, bestFeat, True)) 

# initial count of positive & negative phenotype in cohort
def countInitialCohort(data) :
    pos, neg = 0, 0
    for line in range(len(data)) :
        if data[line][-1] in positives : pos += 1
        else : neg += 1
    return pos, neg

# test hypothesis on dataset
def testHypothesis(data, attr, node) :
    total = float(len(data))
    hits = 0
    positivePhenotype = False
    falsePositive = 0
    falseNegative = 0
    firstIndex = attr.index(node.type)
    for member in data : 
        if member[firstIndex] == node.posFeat :
            if len(node.posChildren) == 0 : positivePhenotype = True
            elif len(node.posChildren) > 0 :
                for child in node.posChildren : 
                    secondIndex = attr.index(child.type)
                    if member[secondIndex] == child.posFeat : 
                        hits += 1
                        positivePhenotype = True                
        else : 
            if len(node.negChildren) > 0 :
                for child in node.negChildren : 
                    if child.posNumY > child.posNumN : 
                        secondIndex = attr.index(child.type)
                        if member[secondIndex] == child.posFeat : 
                            hits += 1
                            positivePhenotype = True
        if positivePhenotype and member[-1] not in positives : 
            falsePositive += 1
        elif not positivePhenotype and member[-1] in positives : 
            falseNegative += 1
        positivePhenotype = False

    errorRate = (falseNegative + falsePositive)/total

    return errorRate

################################################################################
# main
################################################################################

attr1, trainingData = readArg(sys.argv[1])
attr2, testingData = readArg(sys.argv[2])

initPos, initNeg = countInitialCohort(trainingData)
initEntropy = calcEntropy(initPos, initNeg)

buildTree(attr1, trainingData, initEntropy)

error_train = testHypothesis(trainingData, attr1, tree[0])
error_test = testHypothesis(testingData, attr2, tree[0])

printFormat(initPos, initNeg, error_train, error_test)

