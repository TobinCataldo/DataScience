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
        if 'entities' in jsonObj:
            if len(jsonObj['entities']['hashtags']) > 0:
                for hashtags in jsonObj['entities']['hashtags']:
                    twtlist.append(hashtags['text'])
               # twtlist.append([jsonObj['entities']['hashtags']['text']])
        #else:
        #    twtlist.append("")
    return twtlist                        


def main():
    #sent_file = sys.argv[1]
    tweet_file = sys.argv[1]
    #sent_file = "AFINN-111.txt"
    #tweet_file = "problem_1_submission.txt"
    #tweet_file = "output.txt"
    #hw()
    #lines(open(sent_file))
    #lines(tweet_file)
                
    twtList = getTwtList(tweet_file)    
    
    WordCounter = collections.Counter();
    #regex = re.compile('[%s]' % re.escape(string.punctuation))
    
    for twt in twtList:
        #twtex = regex.sub('', twt)
        #words = twtex.split()
       
        #for word in words:
        vwd = twt.lower().strip() 
        #    if vwd not in stopwords:
        WordCounter.update([vwd])
    
    mc = WordCounter.most_common(10)
    for item in mc:
        print item[0].encode("utf-8"), item[1]
            
if __name__ == '__main__':
    main()
