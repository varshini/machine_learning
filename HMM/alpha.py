# Forward Algorithm (Evaluation)

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

def forward(line) :
  global prior, emit, trans
  values = []

  # initial/prior values
  firstline = []
  for i in range(len(prior)) : 
    newval = prior[i] + emit[i][line[0]]
    firstline.append(newval)
  values.append(firstline)

  # forward algorithm
  for word in range(1, len(line)) :
    recent = values[-1] # states at time t-1
    posterior = [] # states at time t
    for i in range(len(prior)) : # for each of the s_i calculated
      calc_o = -float('inf')
      for j in range(len(prior)) : # for each of the s_j at t-1
        numval = emit[i][line[word]] + recent[j] + trans[j][i] # b_i(o_t) + a_t(j) + a_ji
        calc_o = log_sum(calc_o, numval)
      posterior.append(calc_o)
    values.append(posterior)
  if line[0] == "near" : 
    for numbers in range(len(values)) :
      print(line[numbers], values[numbers])
  return values[-1]

def forward_algorithm(sentences) :
  for line in sentences:
    prob = forward(line)
    value = -float('inf')
    for elem in prob : 
      value = log_sum(value, elem)
    sys.stdout.write(str(value) + "\n")

################################################################################
# main
################################################################################

# alpha.py <dev> <hmm-trans> <hmm-emit> <hmm-prior>
listing, prior = readPrior(sys.argv[4])
dev = readDev(sys.argv[1])
trans = readTrans(sys.argv[2])
emit, symbols = readEmit(sys.argv[3])
forward_algorithm(dev)









