import sys
import json
import collections
#import io 

#Point = collections.namedtuple('Point', ['x', 'y'], verbose=True)


# maxmind geoip list
# http://dev.maxmind.com/geoip/legacy/codes/state_latlon/
averagelatlong = {
'AK':[61.3850,-152.2683],
'AL':[32.7990,-86.8073],
'AR':[34.9513,-92.3809],
#'AS':[14.2417,-170.7197],
'AZ':[33.7712,-111.3877],
'CA':[36.1700,-119.7462],
'CO':[39.0646,-105.3272],
'CT':[41.5834,-72.7622],
'DC':[38.8964,-77.0262],
'DE':[39.3498,-75.5148],
'FL':[27.8333,-81.7170],
'GA':[32.9866,-83.6487],
'HI':[21.1098,-157.5311],
'IA':[42.0046,-93.2140],
'ID':[44.2394,-114.5103],
'IL':[40.3363,-89.0022],
'IN':[39.8647,-86.2604],
'KS':[38.5111,-96.8005],
'KY':[37.6690,-84.6514],
'LA':[31.1801,-91.8749],
'MA':[42.2373,-71.5314],
'MD':[39.0724,-76.7902],
'ME':[44.6074,-69.3977],
'MI':[43.3504,-84.5603],
'MN':[45.7326,-93.9196],
'MO':[38.4623,-92.3020],
#'MP':[14.8058,145.5505],
'MS':[32.7673,-89.6812],
'MT':[46.9048,-110.3261],
'NC':[35.6411,-79.8431],
'ND':[47.5362,-99.7930],
'NE':[41.1289,-98.2883],
'NH':[43.4108,-71.5653],
'NJ':[40.3140,-74.5089],
'NM':[34.8375,-106.2371],
'NV':[38.4199,-117.1219],
'NY':[42.1497,-74.9384],
'OH':[40.3736,-82.7755],
'OK':[35.5376,-96.9247],
'OR':[44.5672,-122.1269],
'PA':[40.5773,-77.2640],
#'PR':[18.2766,-66.3350],
'RI':[41.6772,-71.5101],
'SC':[33.8191,-80.9066],
'SD':[44.2853,-99.4632],
'TN':[35.7449,-86.7489],
'TX':[31.1060,-97.6475],
'UT':[40.1135,-111.8535],
'VA':[37.7680,-78.2057],
#'VI':[18.0001,-64.8199],
'VT':[44.0407,-72.7093],
'WA':[47.3917,-121.5708],
'WI':[44.2563,-89.6385],
'WV':[38.4680,-80.9696],
'WY':[42.7475,-107.2085],
}


# coordinates - coordinates [long, lat]    (point)
# place - bounding_box - coordinates [long, lat], [long,lat], [long,lat], [long,lat]  (polygon)

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
    statelist = []
    twtlist = []
    for line in open(tweetfile):
        jsonObj = json.loads(line)
        
        # coordinates - coordinates [long, lat]    (point)
        # place - bounding_box - coordinates [long, lat], [long,lat], [long,lat], [long,lat]  (polygon)
        # coordinates preferred, then place
        #
        # http://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
        # min(myList, key=lambda x:abs(x-myNumber))
        hasCoords = False
        cState = None
        if 'coordinates' in jsonObj:
            if jsonObj['coordinates'] is not None:
                longlat = jsonObj['coordinates']['coordinates']
                cState = getMinimumDistStateByLatLong(longlat[1],longlat[0])
                if cState is not None:
                    hasCoords = True
        
        if 'place' in jsonObj and cState is None:
                if jsonObj['place'] is not None:
                    longlats = jsonObj['place']['bounding_box']['coordinates'][0]
                    cslist = []
                    for longlat in longlats:
                        cst = getMinimumDistStateByLatLong(longlat[1],longlat[0])
                        if cst is not None:
                            cslist.append(cst)
                    if len(cslist) > 0:
                        cState = collections.Counter(cslist).most_common(1)[0][0]                
                        hasCoords = True
 
        if hasCoords:
            if 'text' in jsonObj:
                statelist.append(cState)
                twtlist.append(jsonObj['text'])
           
    return [statelist,twtlist]

def getMinimumDistStateByLatLong(lat,longi):
    # http://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
    # min(myList, key=lambda x:abs(x-myNumber))
    lats = []
    longs = []
    
    for key, value in averagelatlong.iteritems():
        lats.append(value[0])
        longs.append(value[1])             

    minlat = min(lats, key=lambda x:abs(x-lat))
    minlong = min(longs, key=lambda x:abs(x-longi))
    
    if abs(minlat - lat) > 20 or abs(minlong - longi) > 20:
        return None 
        # probably not US
        # need to be refined (distance by degrees...)
    else:
        for key, value in averagelatlong.iteritems():
            if value[0] == minlat and value[1] == minlong:
                return key
    return None

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
    #tweet_file = "output2.txt"
    #tweet_file = "problem_1_submission.txt"
    #hw()
    #lines(open(sent_file))
    #lines(tweet_file)
    
    scoreDict = getScoresDict(sent_file)  
    statelist, twtList = getTwtList(tweet_file)
    twtScoreList = getScoresList(scoreDict,twtList)
    
    #for testing
    #statelist.extend(['ND','SD','ND'])
    #twtScoreList.extend([2,2,1])
    
    stateScores = {}
    for counter, statetwt in enumerate(statelist):
        stateScores[statetwt] = stateScores.setdefault(statetwt, 0) + twtScoreList[counter]

    maxVal = -100
    maxState = None

    for key, value in stateScores.iteritems():
        if value > maxVal:
            maxVal = value
            maxState = key

    print maxState
  #  for score in twtScoreList:
  #      print "{0}".format(score)
    

if __name__ == '__main__':
    main()
