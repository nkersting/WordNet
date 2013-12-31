#!/usr/bin/env python

import csv


#  This maps words from the (data).txt files to their related synset numbers,
#  For example,
# "15284285 28 n 03 speed_of_light 0 light_speed 0 c 0 002 @ 15282696 n 0000 @ 13585429 n 0000 | the speed at which light travels in a vacuum; the constancy and universality of the speed of light is recognized by defining it to be exactly 299,792,458 meters per second"  would be written as one line of output "15284285 15282696 13585429"


inputfile = "tot.txt"  # should be a concatenation:  "cat adv.txt adj.txt noun.txt verb.txt > tot.txt"

inputReader = csv.reader(open(inputfile,'rb'), delimiter=' ')

syns = []

for input in inputReader:

    count_idx = 4 + 2*int(input[3],16)      # index showing the number of synsets
    if (input[count_idx] > 0):
        syns = []
        for i in range (0, int(input[count_idx])):     # iterate over pointer symbols ^&!+ etc.
            p_idx = count_idx + 1 + 4*i
            s_idx = p_idx + 1
            if (input[p_idx] != '!'):        # exclude only antonyms (see below for what is thus included)
                syns.append(input[s_idx])
        print input[0],
        for s in syns:
            print s,
        print '\n',


"""
From http://wordnet.princeton.edu/wordnet/man/wninput.5WN.html,

The pointer_symbol s for nouns are:

!    Antonym 
@    Hypernym 
@i    Instance Hypernym 
 ~    Hyponym 
 ~i    Instance Hyponym 
#m    Member holonym 
#s    Substance holonym 
#p    Part holonym 
%m    Member meronym 
%s    Substance meronym 
%p    Part meronym 
=    Attribute 
+    Derivationally related form         
;c    Domain of synset - TOPIC 
-c    Member of this domain - TOPIC 
;r    Domain of synset - REGION 
-r    Member of this domain - REGION 
;u    Domain of synset - USAGE 
-u    Member of this domain - USAGE 
The pointer_symbol s for verbs are:

!    Antonym 
@    Hypernym 
 ~    Hyponym 
*    Entailment 
>    Cause 
^    Also see 
$    Verb Group 
+    Derivationally related form         
;c    Domain of synset - TOPIC 
;r    Domain of synset - REGION 
;u    Domain of synset - USAGE 
The pointer_symbol s for adjectives are:

!    Antonym 
&    Similar to 
<    Participle of verb 
\    Pertainym (pertains to noun) 
=    Attribute 
^    Also see 
;c    Domain of synset - TOPIC 
;r    Domain of synset - REGION 
;u    Domain of synset - USAGE 
The pointer_symbol s for adverbs are:

!    Antonym 
\    Derived from adjective 
;c    Domain of synset - TOPIC 
;r    Domain of synset - REGION 
;u    Domain of synset - USAGE 

"""

