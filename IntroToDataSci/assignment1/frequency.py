import sys
import json
import collections
import string, re
#import io 

punctuation = [',', '.', '!', '?', '"', "'"]
stopwords = ['a', 'an', 'the', 'is', 'am', 'are'] 


#WordCounter = {} #collecions.Counter()
# https://docs.python.org/2.7/library/collections.html

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def getTwtList(tweetfile):
    twtlist= []
    for line in open(tweetfile):
        jsonObj = json.loads(line)
        if 'text' in jsonObj:
            twtlist.append(jsonObj['text'])
        else:
            twtlist.append("")
    return twtlist                        


def main():
    #sent_file = sys.argv[1]
    #tweet_file = sys.argv[2]
    sent_file = "AFINN-111.txt"
    tweet_file = "problem_1_submission.txt"
    #tweet_file = "output.txt"
    #hw()
    #lines(open(sent_file))
    #lines(tweet_file)
     
    
    
    
    twtList = getTwtList(tweet_file)
    
    
    WordCounter = collections.Counter();
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    
    for twt in twtList:
        twtex = regex.sub('', twt)
        words = twtex.split()
       
        for word in words:
            vwd = word.lower().strip() 
            if vwd not in stopwords:
                WordCounter.update([vwd])
    
    print WordCounter.most_common(20)
    
    #twtScoreList = getScoresList(scoreDict,twtList)
    #for score in twtScoreList:
    #    print "{0}".format(score)
    
   # for key, value in afinnFoundWordCounter.iteritems():
   #     if sum(value.values()) > 0:
   #         #print key, value
   #         print key, value.most_common(3)
            
if __name__ == '__main__':
    main()
