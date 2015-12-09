import csv
import numpy as np

f = open("relation.csv")
reader = csv.reader(f, delimiter=',')
relation = list(reader)
#stopWords = [c[0] for c in stopWords]
for x in range(len(relation)):
    for y in range(len(relation[0])):
        if relation[x][y] == '0':
            relation[x][y] = 0
        else:
            relation[x][y] = 1

print relation


