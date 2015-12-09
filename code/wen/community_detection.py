import csv
import numpy as np
#the original 52 89 91 92 93 user were dropped cos of their wrong mac address

def countComponent(relation):
    myidx = range(len(relation)+1)
    del myidx[0]
    myidx = set(myidx)
#    print list(myidx)
    component = 0
    q = []

    while myidx:
        component += 1
        tempidx = list(myidx)[0]
        myidx.discard(tempidx)
        q += [tempidx]
        while q:
            tempidx = q.pop(0)
            for eleidx in range(len(relation[tempidx-1])):
                if relation[tempidx-1][eleidx] != 0 and eleidx+1 in myidx:
                    q += [eleidx+1]
                    myidx.discard(eleidx+1)

    print "number of component", component
    return component

#def findShortestPath(relation,x):



####
####
####main starts here

#data initialization

f = open("relation.csv")
reader = csv.reader(f, delimiter=',')
relation = list(reader)
f.close()

f = open("community.csv")
reader = csv.reader(f, delimiter=',')
community = list(reader)
f.close()

single1 = set()
print "before filtering"
for x in range(len(relation)):
    for y in range(len(relation[0])):
        relation[x][y] = int(relation[x][y])
    if sum(relation[x]) == 0:
        print x+1
        single1.add(x+1)

#drop the edges with low weight
single2 = set()
print "after filtering"
for x in range(len(relation)):
    for y in range(len(relation[0])):
        if relation[x][y] <= 5:
            relation[x][y] = 0
        else:
            relation[x][y] = 1
    if sum(relation[x]) == 0:
        print x+1
        single2.add(x+1)
#37 40 54 60 68 79 are empty

#make the graph symmetric
contro = 0
for x in range(len(relation)):
    for y in range(len(relation[0])):
        if (relation[x][y]>0 and relation[y][x] == 0) or (relation[x][y]==0 and relation[y][x]>0):
            contro += 1
            relation[x][y],relation[y][x] = 1,1
print "controdiction",contro

single3 = set()
for x in range(len(relation)):
    if sum(relation[x]) == 0:
        print x+1
        single3.add(x+1)

#drop the single vertex
newrelation = []
newcommunity = []
for x in range(len(relation)):
    line = []
    if x+1 in single3:
        continue
    for y in range(len(relation[0])):
        if y+1 in single3:
            continue
        line += [relation[x][y]]
    newcommunity += community[x]
    newrelation += [line]
relation = newrelation
community = newcommunity

print "new relation",len(newrelation),len(newrelation[0])
print "new community",len(community)
print community

countComponent(relation)








