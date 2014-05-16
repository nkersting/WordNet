#!/usr/bin/env python

import csv


#  This maps words from the (data).txt files to their assigned base synset number
#  If a word appears multiple times (such as 'smart', for different parts of speech),
#  then a list is written, e.g.
#  "smart  14331873 01513376 00980144 00438707 00182718"

# "14331873 26 n 03 smart 0 smarting 0 smartness 0 005 @ 14322699 n 0000 + 01513376 a 0301 + 02122164 v 0202 + 01513376 a 0101 + 02122164 v 0102 | a kind of pain such as that caused by a wound or a burn or a sore"
#  "smart" is in fact associated with "smarting", though the latter doesn't have an entry in tot.txt.
#  Thus, "smarting" is set to the same collection of synsets that "smart" is assigned to.


# In NLTK this is equivalent to
##############################################
#import nltk 
#from nltk.corpus import wordnet as wn
##    
#for syn in wn.synsets('gold'):
#    print syn.offset
##############################################

inputfile = "tot.txt"     # should be a concatenation:  "cat adv.txt adj.txt noun.txt verb.txt > tot.txt"

inputReader = csv.reader(open(inputfile,'rb'), delimiter=' ')

words = {}



inputReader = csv.reader(open(inputfile,'rb'), delimiter=' ')
for input in inputReader:
    numwords = int(input[3],16)     # the number of words is actually in hexadecimal
    for i in range (0, numwords):     # iterate over number of words
        w_idx = 4 + 2*i              # this happens to be the position of the word in the line
        if words.has_key(input[w_idx]):
            words[input[w_idx]] += ' ' + input[0]
        else: 
            words[input[w_idx]] = input[0] # if the word doesn't already have synsets, mimic its base word


for w in sorted(words):
    print w,
    print words[w]



