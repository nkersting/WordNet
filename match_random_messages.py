#!/usr/bin/env python


#################3
# Generates many random colony-collection pairs and compares overlap,
# i.e. S_1 vs. S_2
#################
# We have the following problem summarizing the results of this MC:
# --There are bound to be many false positives in the encrypted data (this is the fuzziness), but no false negatives:
#   the real intersection is always a subset of the encrypted intersection
# --If we just report the ratio of intersection with real data to all these positives (some false), we get a low result
# --It should be possible to eliminate most(all?) of the false positives by geometric reasoning
# --Sometimes the intersection in the real data contains points which are not obtained by back-solving the encrypted data. 
#   This can be explained if there is only one intersecting pair of unique rectangles, for then S_2 really does give nothing.


import random
import numpy
import shlex
import math
import csv


#########################################

def findlist(entryword, syndict, stopwords):
    newlist = []
    if (syndict.has_key(entryword) and entryword not in stopwords):
        return syndict[entryword]
    else:
        return newlist

####################################
def SumWordsDFSRecursive(currwords, index, syndict, stopwords, sublist, sumdict):
    if index == len(currwords):
        total = sum(sublist)
        if (sumdict.has_key(total)):
            for item in sublist:
                sumdict[total].append(item)
        else:
            templist = []
            sumdict[total] = templist
            for item in sublist:
                sumdict[total].append(item)
        return

    word = currwords[index]
    currints = findlist(word, syndict, stopwords)
    for entry in currints:
        templist = sublist[:]
        templist.append(int(entry))
        SumWordsDFSRecursive(currwords, index+1, syndict, stopwords, templist, sumdict)

#####################################
def SumNEncrypt(userwords, currwords, syndict, stopwords, N, sumdict):
    if len(currwords) == N:
        sublist = []
        SumWordsDFSRecursive(currwords, 0, syndict, stopwords, sublist, sumdict)
        return

    for i in range(0, len(userwords)):
        newwords = currwords[:]
        newwords.append(userwords[i])
        SumNEncrypt(userwords[i+1:], newwords, syndict, stopwords, N, sumdict)

##########################################
def PointToCoords(point, worldDim):
    x = point % worldDim
    y = point / worldDim
    return x, y

#################################
def WriteRecs(col, outfile):
    for c in col:
        outfile.write(str(c[0]) + ' ' + str(c[1]) + ' ' + str(c[2]) + ' ' + str(c[3]) + '\n')

##################################
#########################################
def randomlist(N, syns):

    list = []
    for i in range (0,N):
        theword = syns[random.randint(0, len(syns)-1)][0]
        list.append(theword)

    
    return list
############################################
def NakedKeys(userwords, syndict):
    currwords = []
    sumdict = {}
    stopwords = []
    SumNEncrypt(userwords, currwords, syndict, stopwords, 1, sumdict)
    total = set()
    for key in sumdict.keys():
        total.add(int(sumdict[key][0]))
    return total

#################################

random.seed()

N = 10   # number of words in each message
level = 2    # encryption level
NumTrials = 10  
synfile = "omegaO2.txt"
outfile = open("match-overlap.txt", "w")

synReader = csv.reader(open(synfile,'rb'), delimiter=' ')

syns = []
for synline in synReader:
    syns.append(synline)

syndict = {}
for test in syns:
    if syndict.has_key(test[0]) == False:
        templist = []
        for j in range (1, len(test)):
            if (test[j] != ''):
                templist.append(test[j])
        syndict[test[0]] = templist



matchStats = []
overlapStats = []
for k in range(0,10):
    tolerance = (k+1)*0.05
    trialNum = 0
    print tolerance
    while trialNum <= NumTrials:

        userwords1 = randomlist(N, syns)
        userwords2 = randomlist(N, syns)

        naked1 = NakedKeys(userwords1, syndict)
        naked2 = NakedKeys(userwords2, syndict)
        nakedoverlap = naked1.intersection(naked2)   # these are the raw overlap points
        if (1.0*len(nakedoverlap)/math.sqrt(len(naked1)*len(naked2)) < tolerance): 
            continue

        currwords = []
        sumdict1 = {}
        stopwords = []
        SumNEncrypt(userwords1, currwords, syndict, stopwords, level, sumdict1)

        currwords = []
        sumdict2 = {}
        stopwords = []
        SumNEncrypt(userwords2, currwords, syndict, stopwords, level, sumdict2)


        sumlist1 = set(sumdict1.keys())
        sumlist2 = set(sumdict2.keys())
        overlap = sumlist1.intersection(sumlist2)

        encryptedPoints1 = set()     # the points responsible for the overlap
        encryptedPoints2 = set()
        for commCrypt in overlap:
            for comm in sumdict1[commCrypt]:
                encryptedPoints1.add(comm)
            for comm in sumdict2[commCrypt]:
                encryptedPoints2.add(comm)

        totalPoints1 = set()
        for s in sumlist1:
            for comm in sumdict1[s]:
                totalPoints1.add(comm)

        commonPoints1 = encryptedPoints1.intersection(nakedoverlap)
        commonPoints2 = encryptedPoints2.intersection(nakedoverlap) 

        if (len(nakedoverlap) == 0 or len(commonPoints1) == 0):
            continue
        else:
    #        matchStats.append(1.0*math.sqrt(len(commonPoints1)*len(commonPoints2)) / math.sqrt(len(encryptedPoints1)*len(encryptedPoints2)))
            matchStats.append(1.0*len(commonPoints1) / len(encryptedPoints1))
            matchStats.append(1.0*len(commonPoints2) / len(encryptedPoints2))
            overlapStats.append(1.0*len(overlap) / len(sumlist1))
            overlapStats.append(1.0*len(overlap) / len(sumlist2))
#            print str(matchStats[-1])
            trialNum += 1


#print '\n'
#print "Average matching: %s +/- %s" % (numpy.mean(matchStats), numpy.std(matchStats))
#print matchStats
#print overlapStats
for i in range (0, len(matchStats)):
    outfile.write(str(matchStats[i]) + ' ' +  str(overlapStats[i]) + '\n')
