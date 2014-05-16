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

###############################
def RandRect(collection, worldDim):
    maxDim = 10
    minDim = 5
    passed = False
    while (not passed):
        passed = True
        x = random.randint(1, worldDim - maxDim)       # ensure rectangles inside
        y = random.randint(1, worldDim - maxDim) 
        width = random.randint(minDim, maxDim)
        height = random.randint(minDim, maxDim)
        for member in collection:
            x2 = member[0]
            y2 = member[1]
            width2 = member[2]
            height2 = member[3]
            if (x + width >= x2 and            # if any intersection with previous, pick another
                y <= y2 + height2 and
                y + height >= y2 and
                x <= x2 + width2):
                    passed = False
        
    collection.append((x,y,width,height))
################################
def MakePermHash(worldDim):            # hash sequence of ints to a random permutation of such
    topInt = worldDim * worldDim
    perm = []
    posHash = {}
    for i in range(1, topInt + 1):  
        perm.append(i)

    for i in range (0, topInt):
        j = random.randint(i,topInt - 1)
        perm[i], perm[j] = perm[j], perm[i]

    for i in range (0, topInt):
        posHash[i+1] = perm[i]

    return posHash

####################################
def MakeHash(worldDim):          # hash sequence to large unused integers
    maxHash = 100000000            # store the reverse hash as well
    topInt = worldDim * worldDim    # maxHash must be chosen large enough to make the encryption give
    used = set()                    # useful results, but not so large that decryption easily betrays
    posHash = {}                    # the input set
    revHash = {}                     # For worldDim = 50, maxHash = 100000000 works well
    
    for i in range(1, topInt + 1):
        passed = False
        while (not passed):
            key = random.randint(1,maxHash)
            if (key not in used):
                used.add(key)
                posHash[i] = key
                revHash[key] = i
                passed = True

    return posHash, revHash

###################################
def MakeSumDict(posHash):
    sumToPoints = {}
    allkeys = posHash.keys()

    for i in range (0, len(allkeys)):
        for j in range (i, len(allkeys)):
            s = posHash[allkeys[i]] + posHash[allkeys[j]]
            if sumToPoints.has_key(s):
                sumToPoints[s].append(allkeys[i])
                sumToPoints[s].append(allkeys[j])
            else:
                sumToPoints[s] = []
                sumToPoints[s].append(allkeys[i])
                sumToPoints[s].append(allkeys[j])
    return sumToPoints
####################################
def MapSumsToPoints(sumlist, sumToPoints):    # takes a list of sums and returns all possible points that may have given it

    candidates = set()
    for s in sumlist:
        for v in sumToPoints[s]:
            candidates.add(v)
        
    return candidates
################################
def MakeSumEvenHash(worldDim):       # want a distribution of keys that makes the sum distribution flat
    maxHash = 1000000000
    topInt = worldDim * worldDim
    used = set()
    posHash = {}

    for i in range(1, topInt + 1):
        passed = False
        while (not passed):
            randsum = random.randint(2, 2*maxHash)  # flat sum distribution
            x = maxHash - randsum / 2
            if (x > randsum / 2):
                x = randsum / 2
            key = random.randint(randsum / 2 - x + 1, randsum / 2 + x - 1)
            if (key not in used and (randsum - key) not in used):
                used.add(key)
                posHash[i] = key
                i += 1
                posHash[i] = randsum - key
                passed = True

    return posHash


###############################
def FillColonyOmega(colonies, positionHash, worldDim):

    omega = {}
    count = 0
    for colony in colonies:
        count += 1
        vals = []
        for i in range(0,colony[2]):
            for j in range(0,colony[3]):
                vals.append(positionHash[colony[0] + i + worldDim*(colony[1] + j)])
        omega[str(count)] = vals

    return omega

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
        templist.append(entry)
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
colony1file = open("colony1.txt", "w")
colony2file = open("colony2.txt", "w")
userfile1 = open("user1.txt", "w")
userfile2 = open("user2.txt", "w")
guessfile = open("guess.txt", "w")


random.seed()

N = 10   # number of colonies in each collection
worldDim = 50  # size of the world

matchStats = []
usertext = ""
for i in range (1, N+1):
    usertext += (str(i) + ' ')

userwords = shlex.split(usertext)

for trial in range(0, 1):


    # hash from coordinate position to particular random int
    positionHash, reverseHash = MakeHash(worldDim)

    colonies1 = []
    for i in range(0,N):
        RandRect(colonies1, worldDim)

    colonies2 = []
    for i in range(0,N):
        RandRect(colonies2, worldDim)

    omega1 = FillColonyOmega(colonies1, positionHash, worldDim)
    omega2 = FillColonyOmega(colonies2, positionHash, worldDim)

    currwords = []
    sumdict1 = {}
    stopwords = []
    SumNEncrypt(userwords, currwords, omega1, stopwords, 2, sumdict1)

    currwords = []
    sumdict2 = {}
    stopwords = []
    SumNEncrypt(userwords, currwords, omega2, stopwords, 2, sumdict2)


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

    naked1 = set()
    for key in omega1.keys():
        for val in omega1[key]:
            naked1.add(val)

    naked2 = set()
    for key in omega2.keys():
        for val in omega2[key]:
            naked2.add(val)

    nakedoverlap = naked1.intersection(naked2)   # these are the raw overlap points

    commonPoints1 = encryptedPoints1.intersection(nakedoverlap)
    commonPoints2 = encryptedPoints2.intersection(nakedoverlap) 
    if (len(nakedoverlap) == 0 and len(encryptedPoints1) == 0 and len(encryptedPoints2) == 0):
        matchStats.append(1)
    elif (len(nakedoverlap) == 0 and (len(encryptedPoints1) != 0 or len(encryptedPoints2) != 0)):
        matchStats.append(0)
    else:
#        matchStats.append(1.0*math.sqrt(len(commonPoints1)*len(commonPoints2)) / math.sqrt(len(nakedoverlap)*len(nakedoverlap)))
        matchStats.append(1.0*math.sqrt(len(commonPoints1)*len(commonPoints2)) / math.sqrt(len(encryptedPoints1)*len(encryptedPoints2)))

    print len(sumlist1), len(overlap),  len(totalPoints1), len(encryptedPoints1)

    firstCollection = []
    for point in encryptedPoints1:
        x, y =  PointToCoords(reverseHash[point], worldDim)
        firstCollection.append([x,y,1,1])

    secCollection = []
    for point in encryptedPoints2:
        x, y =  PointToCoords(reverseHash[point], worldDim)
        secCollection.append([x,y,1,1])



    print "Match of " + str(matchStats[-1])
    print '\n'
    print '\n'
#    print colonies1
#    print colonies2
#    print '\n'    
#    print "Encrypted: \n"
#    print firstCollection


    decryptCollection = []
    sumDict = MakeSumDict(positionHash)
    candidates = MapSumsToPoints(sumlist1, sumDict)
    for c in candidates:
        x, y = PointToCoords(c, worldDim)
        decryptCollection.append([x,y,1,1])


    WriteRecs(colonies1, colony1file)
    WriteRecs(colonies2, colony2file)
    WriteRecs(firstCollection, userfile1)
    WriteRecs(secCollection, userfile2)
    WriteRecs(decryptCollection, guessfile)


#    print '\n'    
#    print "Decrypted: \n"
#    print decryptCollection

print '\n'
print "Average matching: %s +/- %s" % (numpy.mean(matchStats), numpy.std(matchStats))



"""
print "Naked Lengths %s %s , Intersection %s" % (len(naked1), len(naked2), len(nakedoverlap))

for commonPoint in sorted(nakedoverlap):
    print commonPoint,

print '\n'
print str(len(encryptedPoints)) + " From Encryption:"
for commonPoint in sorted(encryptedPoints):
    print commonPoint,



print colonies1

print colonies2

print omega1
print sorted(sumlist1)

"""
