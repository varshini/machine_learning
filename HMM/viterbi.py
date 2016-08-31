# Viterbi Algorithm (Decoding)

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

class cell(object) :
  def __init__(self, val, prow, pcol, crow, ccol, cstate, pstate = None) :
    self.val = val
    self.pastrow = prow
    self.pastcol = pcol
    self.pastState = pstate
    self.currow = crow
    self.curcol = ccol
    self.curState = cstate

  def __repr__(self) :
    return  "%s" % self.pastState

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

def viterbi(line) :
  global prior, emit, trans
  values = []

  # initial/prior values
  firstline = []
  for i in range(len(prior)) : 
    score = prior[i] + emit[i][line[0]]
    newcell = cell(score, 0, 0, 0, i, listing[i], None)
    firstline.append(newcell)
  values.append(firstline)

  # viterbi algorithm
  for word in range(1, len(line)) :
    recent = values[-1] # states at time t-1
    posterior = [] # states at time t
    for i in range(len(prior)) : # for each of the s_i calculated
      bestScore = -float('inf')
      bestCol = 0
      for j in range(len(prior)) : # for each of the s_j at t-1
        #print(listing[i], listing[j])
        numval = emit[i][line[word]] + recent[j].val + trans[j][i] # b_i(o_t) + a_t(j) + a_ji
        if numval > bestScore :
          bestScore = numval
          bestCol = j
      newcell = cell(bestScore, word-1, bestCol, word, i, listing[i], listing[bestCol])
      posterior.append(newcell)
    values.append(posterior)
  return values

def viterbi_algorithm(sentences) :
  for line in sentences:
    matrix = viterbi(line)

    # find maximum score from last row
    bestScore = -float('inf')
    bestCol = 0
    for i in range(len(prior)) :
      if matrix[-1][i].val > bestScore : 
        bestScore = matrix[-1][i].val
        bestCol = matrix[-1][i].curcol

    # backtracking
    backtrack = True
    states = [] # backtrack through the states
    row, col = len(matrix)-1, bestCol
    while(backtrack) :
      states.append(matrix[row][col].curState)
      if matrix[row][col].pastState == None : backtrack = False
      newrow, newcol = matrix[row][col].pastrow, matrix[row][col].pastcol
      row, col = newrow, newcol
      
    n = len(states)
    for elem in range(len(states)) :
      sys.stdout.write(line[elem] + "_" + states[n-1-elem] + " ")
    sys.stdout.write("\n")

################################################################################
# main
################################################################################

# alpha.py <dev> <hmm-trans> <hmm-emit> <hmm-prior>
listing, prior = readPrior(sys.argv[4])
dev = readDev(sys.argv[1])
trans = readTrans(sys.argv[2])
emit, symbols = readEmit(sys.argv[3])
viterbi_algorithm(dev)









