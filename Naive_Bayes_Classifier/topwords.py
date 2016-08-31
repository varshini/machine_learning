import os
import sys
import math

################################################################################
# globals, definitions & notes 
################################################################################

train_files = [] # list of files for training

# training set data
liberals = dict() # maintain word frequency from liberal blogs
conservatives = dict() # maintain word frequency from conservative blogs
allwords = dict()


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
# count
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

def topwords(dictionary, label, cutoff) :
  totalwords = float(sum(dictionary.values())) # |Vocabulary|
  denominator = len(dictionary) + totalwords # n + |Vocabulary|
  counter = 1
  for word in sorted(dictionary, key=dictionary.get, reverse=True) :
    score = (dictionary[word] + 1) / denominator
    sys.stdout.write(word + " %.04f \n" % score)
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

# post-process values
topwords(liberals, "liberal", 20)
sys.stdout.write("\n")
topwords(conservatives, "conservative", 20)