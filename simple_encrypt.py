#!/usr/bin/env python


#######################################################################
#########################################################################
# Additional needed improvements:
# 1. handle punctuation (note convert "read." to "read" but not "U.S." to "U.S")
# 2. hash words not in the omega.txt to unused unique integers 
# 3. convert plural nouns to singular (WordNet has no plurals)
########################################################################################

import csv
import sys
import shlex
import time

#########################################

def uniq(list):
    set = {}
    return [set.setdefault(x,x) for x in list if x not in set]

##########################
def findlist(entryword, syndict, stopwords):
    newlist = []
    if (syndict.has_key(entryword) and entryword not in stopwords):
        return syndict[entryword]
    else:
        return newlist


##########################################

synfile = "omega-hybrid.txt"    
stopfile = "stopwords.txt"

saveplace = "diy_keys" + time.strftime("%Y_%m_%d_%H_%M_%S_%P") + ".kyx"
outfile = open(saveplace, "w")

synReader = csv.reader(open(synfile,'rb'), delimiter=' ')
stopReader = csv.reader(open(stopfile,'rb'), delimiter=' ')

syns = []
for synline in synReader:
    syns.append(synline)

stopwords = []
for sline in synReader:
    stopwords.append(sline[0])

syndict = {}
for test in syns:
    if syndict.has_key(test[0]) == False:
        templist = []
        for j in range (1, len(test)):
            if (test[j] != ''):
                templist.append(test[j])
        syndict[test[0]] = templist
            


usertext = raw_input('Your text (hit Enter to quit): ')

if usertext == '':
    sys.exit()                ## quit the program


userwords = shlex.split(usertext)


sumlist = []
for i in range(0,len(userwords)):        # all possible word pairs considered
    for j in range(i+1, len(userwords)):  
        word1 = userwords[i]
        word2 = userwords[j]
        if word1 == word2:
            continue
                     
        total1 = findlist(word1.lower(), syndict, stopwords)  # find the set of synsets associated with this word
        total2 = findlist(word2.lower(), syndict, stopwords)
           
        for w1 in total1:         # take the Cartesian product of the two sets
            for w2 in total2:
                sumlist.append(int(w1)+int(w2)) # this is the heart of the secure algorithm;
                                                # the sum retains information about the individual synsets,
                                                # but is impossible to resolve back into its constituents



for key in sorted(uniq(sumlist)):              # write output with one sum per line
    outfile.write(str(key) + '\n')
