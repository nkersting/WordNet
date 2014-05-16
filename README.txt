To generate omegaO2.txt:

1. Strip the headers from the raw WordNet data files (data.*) downloaded from http://wordnet.princeton.edu/, and
 the result should be what you see as:
adj.txt  adv.txt  noun.txt   verb.txt

2. Concatenate those above files into "tot.txt".
3. Next run "print-dictionary.py > dictionary.txt". That should print to stdout the 'dictionary' D, i.e. a list of English words and their primary synsets.
4. Run "print-synsets.py > synsets.txt" which prints the synset map to stdout, i.e. a list of primary synsets and their secondary synsets.
5. Next run "print-omega-O2.py > omegaO2.txt"
6. To see a representation of Omega which is just words (good for checking), run print-omegaToWords.py 
