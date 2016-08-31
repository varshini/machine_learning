# Backward Algorithm (Evaluation)

import os
import sys
import math
from math import *

################################################################################
# globals, definitions & notes 
################################################################################

symbols = [] # V - set of all possible symbols (that O can be drawn from)
listing = [] # S - 1D list of states PR, NN, etc. s 
trans = [] # A - transition probabilities ; 2D list
emit = [] # B - emission probabilities ; 1D list of dict()
prior = [] # pi - priors ; 1D list
dev = [] # sentences for calculating probabilities 

################################################################################
# file IO & Initialization
################################################################################

# from 15-112 Fall 2015 Website
def readFile(path):
  with open(path, "rt") as f:
    return f.read()

def readPrior(doc) :
  prior = []
  listing = []
  readDoc = readFile(doc).splitlines()
  for line in readDoc :
    words = line.split()
    for index in range(len(words)) :
      if index == 0 : listing.append(words[index])
      elif index == 1 : prior.append(math.log(float(words[index])))
  return listing, prior

def readDev(doc) :
  sentences = []
  readDoc = readFile(doc).splitlines()
  for line in readDoc :
    eachline = []
    words = line.split()
    for word in words :
      eachline.append(word)
    sentences.append(eachline)
  return sentences

def readTrans(doc) :
  globaltrans = []
  readDoc = readFile(doc).splitlines()
  for line in readDoc : 
    eachTrans = []
    words = line.split()
    for num in range(1, len(words)) :
      eachTrans.append(math.log(float(words[num][3:])))
    globaltrans.append(eachTrans)
  return globaltrans

def readEmit(doc) :
  emissions = []
  symbols = []
  readDoc = readFile(doc).splitlines()
  for line in readDoc : 
    newdict = dict()
    words = line.split()
    for num in range(1, len(words)) :
      splitted = words[num].split(":")
      newdict[splitted[0]] = math.log(float(splitted[1]))
      if words[0] == listing[0] :
        symbols.append(splitted[0])
    emissions.append(newdict)
  return emissions, symbols

################################################################################
# algorithm
################################################################################

# hw10 handout - 10-601 logsum.py
# computes log sum of two exponentiated log numbers efficiently
def log_sum(left,right):
  if right < left:
    return left + log1p(exp(right - left))
  elif left < right:
    return right + log1p(exp(left - right));
  else:
    return left + log1p(1)

def backward(line) :
  # initialize matrix
  matrix = []
  for i in range(len(prior)) :
    newRow = []
    for j in range(len(line)) :
      newRow.append(0)
    newRow.append(1)
    matrix.append(newRow)

  # backward algorithm
  for t in range(len(line)-1, 0, -1) : # go back the list of words (col)
    for i in range(len(prior)) : # for each row/state that is being calculated
      calc_o = -float('inf')
      for j in range(len(prior)) :
        numval = matrix[j][t+1] + trans[i][j] + emit[j][line[t]] # beta_t+1 + a_ij + b_j(o_t+1)
        calc_o = log_sum(calc_o, numval)
      matrix[i][t] = calc_o

  # first column is special :)
  for z in range(len(prior)) :
    matrix[z][0] = prior[z] + emit[z][line[0]] + matrix[z][1]

  # compile the first column values
  firstcol = []
  for i in range(len(prior)) :
    firstcol.append(matrix[i][0])
  return firstcol

def backward_algorithm(sentences) :
  for line in sentences :
    prob = backward(line)
    value = -float('inf')
    for elem in prob : 
      value = log_sum(value, elem)
    value = value - 1
    sys.stdout.write(str(value) + "\n")

################################################################################
# main
################################################################################

# alpha.py <dev> <hmm-trans> <hmm-emit> <hmm-prior>
listing, prior = readPrior(sys.argv[4])
dev = readDev(sys.argv[1])
trans = readTrans(sys.argv[2])
emit, symbols = readEmit(sys.argv[3])
backward_algorithm(dev)





