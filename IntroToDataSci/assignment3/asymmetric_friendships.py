import MapReduce
import sys

"""
Asymmetric Friendship Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
           
    for w in words:      
      mr.emit_intermediate(key, w)       

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    total = []
    for v in list_of_values:
      try:
          if key in set(mr.intermediate[v]):
            pass
          else:
            mr.emit((key,v))
            mr.emit((v,key))
      except:
          mr.emit((key,v))
          mr.emit((v,key))
     
    #mr.emit((key, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  #inputdata = open("data/friends.json")
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
