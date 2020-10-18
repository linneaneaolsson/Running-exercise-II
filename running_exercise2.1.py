#!/usr/local/bin/python3

DNA_list = []

# TODO folk kan lägga in dumma bokstäver
# TODO folk kan ha olika långa 
# TODO if the fasta header line is longer than 3 characters 
# TODO make the creation of the dict into a part of the function? Is it okay like this after using sys.argv[] for the file form the command line? 


dnaDict = dict()
'''
# trying to make the program exclude rows with other characters than ATCG- 
c_set = ("ATCG-")
not_dna = []
dna1 = "TACG-A"
junk = "A-TCAB"

with open("data/score.extra.fna", "r") as f:
    data = f.read().replace('\n', '').split(">") # opens f and replaces alla new lines with nothing, everything at the same line. Then split it at ">"
    data.pop(0) #takes away empty 0th object in list, which is empty. 
    for line in data:
        dnaId = line[:3] #the ID is from 0 til 3, so 0-2 basically. 
        dna = line[3:] # dna is the string from 3 til the end. 
        for i in dna:
            check = [i in dna for i in c_set]
            if not check:
                not_dna.append(dna)
            dnaDict[dnaId] = dna # defines the dictionary as the ID as the key and dna as the value 
'''

with open("data/score.extra.fna", "r") as f:
    data = f.read().replace('\n', '').split(">") # opens f and replaces alla new lines with nothing, everything at the same line. Then split it at ">"
    data.pop(0) #takes away empty 0th object in list, which is empty. 
    for line in data:
        dnaId = line[:3] #the ID is from 0 til 3, so 0-2 basically. 
        dna = line[3:] # dna is the string from 3 til the end. 
        dnaDict[dnaId] = dna
        
def score_one_pair(x, y): # defines a function for scoring characters, x and y in stringx and stringy, But only two at the time 
    if x == '-' and y == '-': #both x and y are -
        return 0

    if x == '-' or y == '-': #x or y are -. Both could be, but the loop will break and return a score according to the previous line 
        return -1
    
    if x == y: # both are the same character, but neither can be -, since we already covered that
        return 1
    
    # A-G Transition. Could be put into a dictionary but is readable like this on the other hand
    if (x == "A" and y == "G") or (x == "G" and y == "A"):
        return -1
    
    # C-T Transition
    if (x == "C" and y == "T") or (x == "T" and y == "C"):
        return -1
    
    # transversions A <-> CT, G <-> CT 
    transversions = {"A": ["C", "T"], "G": ["C", "T"], "C": ["A", "G"], "T": ["A", "G"]}
    #tranversions is now a dictionary where one key corresponds to two values
    if y in transversions[x]: #if y is the value of x in transversions 
        return -2

    if x in transversions[y]: #if x is the value of the transversions 
        return -2


def score_two_ids(firstId, secondId): #defines a function for scoring 2 sequences from , puting in first (x) and second id (y)
    firstDna = dnaDict[firstId] # where the first sequence is the value in the dnadict with the first ID as the key
    secondDna = dnaDict[secondId] # same with the second 
    both = zip(firstDna, secondDna) # both will be a tuples of the integers. if the sequences would be of different lenght, it would align them in a tuple until the shortest sequence is exhausted

    score = 0
    for [x,y] in both: # for one character in the tuple (the sequences) at the time, until the nd of the tuple
        score = score + score_one_pair(x,y) # uses the scoring for one pair funciton, then adds that to the existing score
    return score


DNA_list = list(dnaDict)
n = len(DNA_list)
for a in range(n):
    for b in range(a + 1, n):
        firstId = DNA_list[a] #firstId is the key in the list
        secondId = DNA_list[b] 
        firstDna = dnaDict[firstId] #for key in dict
        secondDna = dnaDict[secondId]
        total_score = score_two_ids(firstId, secondId) # the totalscore is the return score of the used ids' sequences 
        print(firstId + "-" + secondId + ": Score=" + str(total_score))



