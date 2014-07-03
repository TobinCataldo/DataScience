import sys
import json
#import io 

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def getScoresDict(afinnfile):    
    scores = {} # initialize an empty dictionary
    for line in open(afinnfile):        
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    #print scores.items() # Print every (term, score) pair in the dictionary
    return scores

def getTwtList(tweetfile):
    twtlist= []
    for line in open(tweetfile):
        jsonObj = json.loads(line)
        if 'text' in jsonObj:
            twtlist.append(jsonObj['text'])
        else:
            twtlist.append("")
    return twtlist                        

def getScoresList(scoreDict,twtList):
    twtScoreList = []
   
    for twt in twtList:
        words = twt.split()
        twtScore = 0
        for word in words:
            vwd = word.lower().strip()
            if scoreDict.has_key(vwd):                
                twtScore += scoreDict[vwd]

        twtScoreList.append(twtScore)
    return twtScoreList

def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    #sent_file = "AFINN-111.txt"
    #tweet_file = "output.txt"
    #hw()
    #lines(open(sent_file))
    #lines(tweet_file)
    
    scoreDict = getScoresDict(sent_file)  
    twtList = getTwtList(tweet_file)
    twtScoreList = getScoresList(scoreDict,twtList)
    for score in twtScoreList:
        print "{0}".format(score)
    

if __name__ == '__main__':
    main()
