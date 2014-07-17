import MapReduce
import sys

"""
Relational Join Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[1]
    rectag= record[0]
    value = [rectag,record]
    
    mr.emit_intermediate(key,value)
    
    #words = value.split()
    #for w in record:
    #  mr.emit_intermediate(key, 1)
    #  #mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    total = []
    count = 0
    orderline = []
    for v in list_of_values:
      if count == 0:
          count = 1
          orderline = v[1]
          continue
      
      listline = v[1]
      
      mr.emit(orderline + listline)
      #total.append(myli)
      count += 1
   

# Do not modify below this line
# =============================
if __name__ == '__main__':
  
  #inputdata = open("data/records.json")
  inputdata = open(sys.argv[1])
  
  mr.execute(inputdata, mapper, reducer)
