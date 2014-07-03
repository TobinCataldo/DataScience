import sys
import json
import collections
import string, re, math
#import io 

punctuation = [',', '.', '!', '?', '"', "'"]
stopwords = ['a', 'an', 'the', 'is', 'am', 'are'] 


twtListFTWithValue = []
afinnFoundWordCounter = {} #collecions.Counter()
# https://docs.python.org/2.7/library/collections.html

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def getScoresDict(afinnfile):    
    scores = {} # initialize an empty dictionary
    for line in open(afinnfile):        
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
        
        # init counter
        afinnFoundWordCounter[term] = collections.Counter()
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
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    
    for twt in twtList:
        twtex = regex.sub('', twt)
        words = twtex.split()
        twtScore = 0
        nonafinn = []           
        afinns = []

        for word in words:
            vwd = word.lower().strip() 
            
            if scoreDict.has_key(vwd):                
                twtScore += scoreDict[vwd]
                afinns.append(vwd)
            else:
                # non-afinn word
                if vwd not in stopwords:
                    nonafinn.append(vwd)

        twtScoreList.append(twtScore)

        #counter time
        for aword in afinns:
            afinnFoundWordCounter[aword].update(nonafinn)

    return twtScoreList

def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    #sent_file = "AFINN-111.txt"
    #tweet_file = "problem_1_submission.txt"
    #tweet_file = "output.txt"
    #hw()
    #lines(open(sent_file))
    #lines(tweet_file)
    
    scoreDict = getScoresDict(sent_file)  
    twtList = getTwtList(tweet_file)
    twtScoreList = getScoresList(scoreDict,twtList)
    #for score in twtScoreList:
    #    print "{0}".format(score)
    
    myNewWords = {}

    for key, value in afinnFoundWordCounter.iteritems():
        if sum(value.values()) > 0:
            #print key, value
            # get the score for key, increment  nonafinn dict 
            # (abs) afinn score * occurences * (sign) afinn score)

            for nlist in value.most_common(10):
                sc = math.copysign(abs(scoreDict[key]) * nlist[1], scoreDict[key])
                myNewWords[nlist[0]] = myNewWords.setdefault(nlist[0],0) + sc
 #    for counter, statetwt in enumerate(statelist):
 #       stateScores[statetwt] = stateScores.setdefault(statetwt, 0) + twtScoreList[counter]            
            #print key, scoreDict[key], value.most_common(3)
    for key,value in myNewWords.iteritems():
        print key.encode("utf-8"), value
            
if __name__ == '__main__':
    main()
