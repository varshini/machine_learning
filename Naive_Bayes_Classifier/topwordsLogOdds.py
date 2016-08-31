import os
import sys
import math

################################################################################
# globals, definitions & notes 
################################################################################

train_files = [] # list of files for training
test_files = [] # list of files for testing

# training set data
liberals = dict() # maintain word frequency from liberal blogs
conservatives = dict() # maintain word frequency from conservative blogs
allwords = dict()
plib = 0 # % of docs that are labeled liberal
pcon = 0 # % of docs that are labeled conservative
pwvlib = dict() # frequency count of liberal words, post-smoothing
pwvcon = dict() # frequency count of conservative words, post-smoothing
loglib = dict() # calculate log odds against conservative words
logcon = dict() # calculate log odds against liberal words

################################################################################
# file IO 
################################################################################

# from 15-112 Fall 2015 Website
def readFile(path):
  with open(path, "rt") as f:
    return f.read()

# update which files belong in test vs train
def categorize(doc, doclist) :
    global train_files, test_files
    readDoc = readFile(doc).splitlines()
    for filename in readDoc :
      doclist.append(filename)

################################################################################
# train
################################################################################

# update word count from labeled files
def wordcount(filelist, namepattern, freqcount, otherdict) :
  global allwords
  typecount = 0
  for blog in filelist :
    if namepattern in blog : 
      typecount += 1
      blogwords = readFile(blog).splitlines()
      for word in blogwords : 
        word = word.lower()
        if word not in allwords : 
          allwords[word] = 0
        if word not in freqcount : 
          freqcount[word] = 0
        if word not in otherdict: 
          otherdict[word] = 0
        allwords[word] += 1
        freqcount[word] += 1
  return typecount

# calculate P(w|v) - word given label
def calcpwv(dictionary, probdict) :
  global allwords
  totalwords = float(len(allwords)) # |Vocabulary|
  denominator = (sum(dictionary.values())) + totalwords # n + |Vocabulary|
  for word in dictionary : 
    probdict[word] = (dictionary[word] + 1) / denominator

################################################################################
# log odds
################################################################################

def logodds(topdict, botdict, destination, bonus) :
  for word in topdict : 
    destination[word] = math.log(topdict[word]/botdict[word])

def topwords(dictionary, cutoff) :
  global liberals, conservatives
  counter = 1
  for word in sorted(dictionary, key=dictionary.get, reverse=True) :
    sys.stdout.write(word + " %.04f \n" % dictionary[word])
    counter += 1
    if counter > cutoff : break

################################################################################
# main
################################################################################

# read from test/train (os.args) - and store which files are test vs train
categorize(sys.argv[1], train_files) # update list of train_files


# read from the actual files in the list above 
libdocs = wordcount(train_files, "lib", liberals, conservatives)
condocs = wordcount(train_files, "con", conservatives, liberals)
plib = libdocs / float(len(train_files))
pcon = condocs / float(len(train_files))

# calculate P(w|v)
calcpwv(liberals, pwvlib)
calcpwv(conservatives, pwvcon)

# calculate log odds
bonus = 0.5*(len(liberals) + len(conservatives))
logodds(pwvlib, pwvcon, loglib, bonus) # liberal
logodds(pwvcon, pwvlib, logcon, bonus) # conservative

# post-process values
topwords(loglib, 20) # liberal
sys.stdout.write("\n")
topwords(logcon, 20) # conservative

