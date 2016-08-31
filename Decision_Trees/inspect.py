import sys
import os
import math

# from 15-112 Fall 2015 Website
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

# read from the file and return only the outcome #'s & cohort size
def readArg(doc) :
    dictionary = {}
    readDoc = readFile(doc).splitlines()
    for line in range(len(readDoc)) :
        if line > 0 :
            phenotype = readDoc[line].split(",")[-1]
            if phenotype not in dictionary : dictionary[phenotype] = 0
            dictionary[phenotype] += 1
    return dictionary, len(readDoc)-1

# print out entropy and error rate
def calculate(phenotypes, total) :
    number = len(phenotypes)
    prob = []
    entropy = 0
    majority, minority = "", ""
    for elem in phenotypes :
        prob.append(phenotypes[elem]/float(total))
        if phenotypes[elem] > total/2 : majority = elem 
        else : minority = elem
    for probabilities in prob :
        entropy += probabilities * math.log((1/probabilities), 2)
    error = phenotypes[minority] / float(total)
    sys.stdout.write("entropy: " + str(entropy) + "\n")
    sys.stdout.write("error: " + str(error) + "\n")

#############################################################################

phenotypes, total = readArg(sys.argv[1])
calculate(phenotypes, total)
