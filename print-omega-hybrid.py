#!/usr/bin/env python

# this finds the words associated with a given word, 2 levels removed
# For example, "molybdenum" has one synset 14645661, as seen by grepping
# in wordfile,
# and this has associated synsets 14625458 and 14682469, as seen by grepping
# in synfile.
# Those synsets enclose one word each, as seen by searching wordfile again,
#  so "molybdenum" is mapped to those three numbers, yielding a line of output:
#  "molybdenum 14625458 14645661 14682469"

# This is tantamount to mapping each word in the dictionary to its primary synsets, secondary synsets, and
# the primary synsets of all the words whose
# secondary synsets have any non-zero intersect with the word's secondary synsets.
 


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
syns = []

for wordline in wordReader:
    words.append(wordline)

for synline in synReader:
    syns.append(synline)

worddict = make_dict(words)
syndict = make_dict(syns)


reversedict = make_reverse_dict(worddict)


for entry in sorted(worddict.keys()):        # loop over dictionary
    syn_entries = []
    for syn in worddict[entry]:    # synsets for this word
        syn_entries.append(syn)     # add the primary synsets
        for syn2 in syndict[syn]: 
            syn_entries.append(syn2) # add the secondary synsets 
            if reversedict.has_key(syn2):
                for entry2 in reversedict[syn2]:  # all words whose synsets contain this value
                    for syn1 in worddict[entry2]: # record all the synsets for this word
                        syn_entries.append(syn1)


    print entry,
    for synval in sorted(uniq(syn_entries)):
        print synval,
    print

