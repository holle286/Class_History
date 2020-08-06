from __future__ import division
import random
import pandas as pd
import csv
import math
from random import random as rand


fields = []
rows = []
array = []
smolarr = []
out = []
labels = []
counter = 0
temper = []
with open('p2Tree.csv') as csvfile:
    readCSV = csv.reader(csvfile)
    field = readCSV.next()
    for row in readCSV:
        rows.append(row)
        length = len(row)
    for i in range(length -1)[1:]:
        out = []
        for row in rows:
            smolarr.append(row[i])
            out.append(row[i+1])
        array.append(smolarr)
        smolarr=[]
    #print(array)
    #print(out)
    #print(field)
    labels = field[1:6]
    temper = field[1:6]

finalans = [' '] * 200
for i in range(200):
    finalans[i] = ' '

maxindex = 1
def maketree(arr, output, index, label):
    global maxindex
    global labels
    if(index > maxindex):
            maxindex = index
    istrue = True
    isfalse = True
    numF = 0
    numT = 0
    #print(output)
    for i in range(len(output)):
        if(output[i] == '1'):
            numT += 1
            isfalse = False
        if(output[i] == '0'):
            numF += 1
            istrue = False
    total = numT + numF
    if(istrue):
        finalans[index] = '1_'
    elif(isfalse):
        finalans[index] = '0_'
    elif(arr == []):
        True
    else:
        #print(numT)
        #print(total)
        #print(numT/total)
        before = (-1 * (numT/total) * math.log(numT/total,2)) - ((numF/total) * math.log(numF/total,2))
        gain = 0
        collength = len(arr[0])
        #print(arr)
        #print(collength)
        newrightarr = []
        newleftarr = []
        for ro in arr:
            #print(len(ro))
            #print(collength)
            nexttrueout = []
            nextfalseout = []
            truetrue = 0
            truefalse = 0
            falsetrue = 0
            falsefalse = 0
            trueAttrib = 0
            falseAttrib = 0
            trueafter = 0
            falseafter = 0
            truetruepct = 0
            truefalsepct = 0
            falsetruepct = 0
            falsefalspct = 0
            randomVar = 0
            for i in range(collength):
                if(ro[i] == '1'):
                    nexttrueout.append(output[i])
                    trueAttrib += 1
                    if(output[i] == '1'):
                        truetrue += 1
                    else:
                        truefalse += 1
                else:
                    nextfalseout.append(output[i])
                    falseAttrib += 1
                    if(output[i] == '1'):
                        falsetrue += 1
                    else:
                        falsefalse += 1
            #print(newrightarr)
            if(truetrue == 0 and truefalse == 0):
                trueafter = 0
            else:
                truetruepct = (truetrue/(truetrue+truefalse))
                truefalsepct = (truefalse/(truetrue+truefalse))
                if(truetruepct == 0):
                    trueafter =  -1* (truefalsepct * math.log(truefalsepct,2))
                elif(truefalsepct == 0):
                    trueafter = (-1*truetruepct * math.log(truetruepct,2))
                else:
                    trueafter = (-1*truetruepct * math.log(truetruepct,2)) - (truefalsepct * math.log(truefalsepct,2))
            if(falsetrue == 0 and falsefalse == 0):
                falseafter = 0
            else:
                falsetruepct = (falsetrue/(falsetrue+falsefalse))
                falsefalsepct = (falsefalse/(falsetrue+falsefalse))
                if(falsetruepct == 0):
                    falseafter =  -1 * (falsefalsepct * math.log(falsefalsepct,2))
                elif(falsefalse == 0):
                    falseafter = (-1*falsetruepct * math.log(falsetruepct,2))
                else:
                    falseafter = (-1*falsetruepct * math.log(falsetruepct,2)) - (falsefalsepct * math.log(falsefalsepct,2))
            randomVar = trueAttrib/(trueAttrib + falseAttrib)
            after = (randomVar * trueafter) + ((1 -randomVar) * falseafter)
            tempgain = 0
            tempgain = before - after
            if(tempgain > gain):
                gain = tempgain
                currentBest = ro
                fintrueout = nexttrueout
                finfalseout = nextfalseout
        count = arr.index(currentBest)
        print(label)
        #print(arr)
        print(count)
        finalans[index] = label[count] + '_'
        label.remove(labels[count])
        #labels.remove[finalans[index]]
        #print(currentBest)
        arr.remove(currentBest)
        #print(fintrueout)
        newrightarr = []
        newleftarr = []
        for cur in arr:
            tsmallarr = []
            fsmallarr = []
            for i in range(len(currentBest)):
                #print(cur[i])
                if(currentBest[i] == '1'):
                    tsmallarr.append(cur[i])
                else:
                    fsmallarr.append(cur[i])
                #print(tsmallarr)
            newrightarr.append(tsmallarr)
            newleftarr.append(fsmallarr)
        #print(newrightarr)
        maketree(newrightarr, fintrueout, index*2, labels)
        maketree(newleftarr, finfalseout, index*2+1, labels)

def main():
    maketree(array, out, 1, labels)
    #finalans = finalans[:maxindex]
    print(finalans[:maxindex+1])
    #print(maxindex)

if __name__ == '__main__':
    main()

