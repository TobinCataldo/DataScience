import MapReduce
import sys

"""
Matrix Multiplication Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    #key = record[0]
    #value = record[1]
    #words = value.split()
    
    if record[0]=='a':
         #mr.emit_intermediate((record[1],record[2]),("A",record[3]))
         mr.emit_intermediate(("A",record[1]), (record[2],"A",record[3]))
    if record[0]=='b':
         #mr.emit_intermediate((record[2],record[1]),("B",record[3]))
         mr.emit_intermediate(("B",record[2]), (record[1],"B",record[3]))
    
def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts        

    if key[0] == "B":
        return

    for x in range(0,5):
        bitem = []
        total = 0
        if mr.intermediate.has_key(('B',x)):
            bitem = mr.intermediate[('B',x)]
        else:
            print "no b key"
            pass 

        for item in list_of_values:            
            for inneritem in bitem:
                if item[0] == inneritem[0]:
                        total += item[2] * inneritem[2]
        #print (key[0], key[1],x,total)
        mr.emit((key[1], x, total))

   

# Do not modify below this line
# =============================
if __name__ == '__main__':
  #inputdata = open("data/matrix.json")
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
