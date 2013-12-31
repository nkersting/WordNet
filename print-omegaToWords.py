#!/usr/bin/env python

# this simply represents omega.txt as words, to check reasonableness
 


import csv
import sys

wordfile = "dictionary.txt"         # i.e. map of English words to primary synsets


omegafile = "omega-hybrid.txt"             
#omegafile = "omegaO2.txt"             
#omegafile = "omegaO3.txt"             


wordReader = csv.reader(open(wordfile,'rb'), delimiter=' ')
omegaReader = csv.reader(open(omegafile,'rb'), delimiter=' ')



####################################
def uniq(input):
  output = []
  for x in input:
    if x not in output:
      output.append(x)
  return output
#########################################
def make_dict(origlist):

    thedict = {}
    for test in origlist:
        if thedict.has_key(test[0]) == False:
            templist = []
            for j in range (1, len(test)):
                if (test[j] != ''):
                    templist.append(test[j])
            thedict[test[0]] = templist
                    
    return thedict

###################################

def make_reverse_dict(worddict):


    reversedict = {}
    for entry in worddict.keys():
        for syn in worddict[entry]:
            if reversedict.has_key(syn) == False:
                reversedict[syn] = []
            reversedict[syn].append(entry)

    return reversedict

###############################3

words = []

for wordline in wordReader:
    words.append(wordline)

worddict = make_dict(words)
reversedict = make_reverse_dict(worddict)

for line in sorted(omegaReader):
    print line[0] + ': ',
    templist = []
    for i in range (1, len(line)):
        if reversedict.has_key(line[i]):
            for entry in reversedict[line[i]]:
                templist.append(entry)
    print uniq(templist)
    print
    print


