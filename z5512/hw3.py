from random import choices
from collections import Counter
prob = ["low", "med", "high"]
px0 = [.3,.3,.3]
plow = [.6,.35,.05]
pmed = [.2,.6,.2]   # intitalize a bunch of globabl vars for probabilites
phigh = [0,.5,.5]
e = [0,0,1,1,0,0,0,1,0]   #  e = 0 when not flooded, e = 1 when flooded

def main():
    px = [.3,.3,.3]  #  initially set probabilites to be 1/3 for x0
    split = choices(prob,px, k = 100)
    counter = Counter(split)  #  create random array of low med and high
    low = counter.get("low")  #  get count of 3 vars in array
    med = counter.get("med")
    high = counter.get("high")
    lowlist = choices(prob,plow, k = low)  #  create new array for each var based on probabilites given
    medlist = choices(prob,pmed, k = med)
    highlist = choices(prob,phigh, k = high)
    for i in range(0,10):    
        templowlist = Counter(lowlist)  #  start for loop and create new lists for each x
        tempmedlist = Counter(medlist)  #  temporary though since need to normalize
        temphighlist = Counter(highlist)
        if templowlist.get("low") == None:
            templow = tempmedlist.get("low")  #  must handle for null case for templow
        else:
            templow = templowlist.get("low") + tempmedlist.get("low")  # get number of each var in each
        if templowlist.get("med") == None:
            tempmed = tempmedlist.get("med") + temphighlist.get("med")
        else:
            tempmed = templowlist.get("med") + tempmedlist.get("med") + temphighlist.get("med")
        if templowlist.get("high") == None:
            temphigh = tempmedlist.get("high") + temphighlist.get("high")
        else:
            temphigh = templowlist.get("high") + tempmedlist.get("high") + temphighlist.get("high")
        if(e[i-1]):  # if case is flooded use these weights
            templow = templow * 0
            tempmed = tempmed * .05  #  normalize vars
            temphigh = temphigh * .4
            total = tempmed + temphigh
            px = [templow/total, tempmed/total, temphigh/total]  # find new px
            split = choices(prob,px, k = 100)
            counter = Counter(split)
            low = counter.get("low")
            med = counter.get("med")
            high = counter.get("high")
            lowlist = []
            medlist = choices(prob,pmed, k = med)
            highlist = choices(prob,phigh, k = high)
        else:  # if case is not flooded use this weights
            templow = templow * 1
            tempmed = tempmed * .95
            temphigh = temphigh * .6
            total = templow + tempmed + temphigh
            px = [templow/total, tempmed/total, temphigh/total]
            split = choices(prob,px, k = 100)
            counter = Counter(split)
            low = counter.get("low")
            med = counter.get("med")
            high = counter.get("high")
            lowlist = choices(prob,plow, k = low)
            medlist = choices(prob,pmed, k = med)
            highlist = choices(prob,phigh, k = high)
        print("x",  i+1,  " ")  #  print new px for each x
        print(px)
    return 0

if __name__ == '__main__':
    main()

