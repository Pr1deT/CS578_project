import csv
import numpy as np
#the original 52 89 91 92 93 user were dropped cos of their wrong mac address

#count the number of components in current graph
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

#    print "number of component", component
    return component

#find all shortest path from x to each vertex
def findShortestPath(relation,x):
    q = [x]
    mypath = {}
    mypath[x] = []
    myweight = {}
    myweight[x] = 0
    while q:
        v = q.pop(0)
        for idx in range(len(relation[0])):
            if relation[v][idx] != 0:
                if idx not in myweight:
                    mypath[idx] = mypath[v]+[(v,idx)]
                    myweight[idx] = myweight[v]+1
                    q += [idx]
                else:
                    if myweight[idx]>myweight[v]+1:
                        mypath[idx] = mypath[v]+[(v,idx)]
                        myweight[idx] = myweight[v]+1
                    if myweight[idx]==myweight[v]+1:
                        mypath[idx] += mypath[v] + [(v,idx)]

    return mypath

def evalue(relation,community):
    myidx = range(len(relation))
    myidx = set(myidx)
    q = []

    while myidx:
        tempidx = list(myidx)[0]
        myidx.discard(tempidx)
        q += [tempidx]
        mycomm = {}
        mycomm[community[tempidx]] = 1
        while q:
            tempidx = q.pop(0)
            for eleidx in range(len(relation[tempidx])):
                if relation[tempidx][eleidx] != 0 and eleidx in myidx:
                    q += [eleidx]
                    if community[eleidx] not in mycomm:
                        mycomm[community[eleidx]] = 1
                    else:
                        mycomm[community[eleidx]] += 1
                    myidx.discard(eleidx)
        total = 0
        maxval = 0
        for ele in mycomm:
            total += mycomm[ele]
            if mycomm[ele] > maxval:
                maxval = mycomm[ele]
        print "total:",total,"max",maxval
        print mycomm
    return

####
####
####main starts here

#data initialization

f = open("friend_5.csv")
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
        if relation[x][y] <= 0:
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

#check isolated vertex
print "after make graph symmetric"
single3 = set()
for x in range(len(relation)):
    if sum(relation[x]) == 0:
        print x+1
        single3.add(x+1)

#drop the isolated vertex
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

# add by Ting
# save newrelation as csv file for friendInfer.py
np.savetxt("../../Data/bluetooth_net.csv", newrelation, delimiter=",")


print "new relation",len(newrelation),len(newrelation[0])
print "new community",len(community)
print community


#evalue current clustering and break components
component = 0

while component<10:
    newcomponent = countComponent(relation)

    #if new component number, then evaluate new clustering
    if newcomponent != component:
        print "component:",newcomponent
        evalue(relation,community)
        component = newcomponent

    #compute initial edge weight
    path = []
    for x in range(len(relation)):
        path += [findShortestPath(relation,x)]

    #summarise result
    edgeWeight = {}
    for v in path:
        for ele in v:
            for edge in v[ele]:
                if edge not in edgeWeight:
                    edgeWeight[edge] = 1
                else:
                    edgeWeight[edge] += 1

    maxkey,maxvalue = None,0
    for e in edgeWeight:
#        print e,":",edgeWeight[e]
        if edgeWeight[e]>maxvalue:
            maxkey = e
            maxvalue = edgeWeight[e]

    #remove max edge
#    print "max edge:",maxkey,":",maxvalue
    x,y = maxkey
    relation[x][y],relation[y][x] = 0,0











