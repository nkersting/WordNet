#!/usr/bin/env python

# this finds the synsets associated with a given word, up to 2 levels removed
# For example, "molybdenum" has one synset 14645661, as seen by grepping
# the dictionary,
# and this has associated synsets 14625458 and 14682469, as seen by grepping
# the synset file.
# Soo "molybdenum" is mapped to those three numbers, yielding a line of output:
#  "molybdenum 14625458 14645661 14682469"



import csv
import sys

wordfile = "dictionary.txt"         # i.e. map of English words to primary synsets
synfile = "synsets.txt"               # i.e. map of primary synsets to secondary synsets


wordReader = csv.reader(open(wordfile,'rb'), delimiter=' ')
synReader = csv.reader(open(synfile,'rb'), delimiter=' ')


##################################
def uniq(list):
    set = {}
    return [set.setdefault(x,x) for x in list if x not in set]

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

words = []
syns = []

for wordline in wordReader:
    words.append(wordline)

for synline in synReader:
    syns.append(synline)

worddict = make_dict(words)
syndict = make_dict(syns)

for entry in sorted(worddict.keys()):        # loop over dictionary
    syn_entries = set()
    for syn in worddict[entry]:    # synsets for this word
        syn_entries.add(syn)     # add the primary synsets
        for syn2 in syndict[syn]: 
            syn_entries.add(syn2) # add the secondary synsets

    print entry,
    for synval in sorted(syn_entries):
        print synval,
    print

