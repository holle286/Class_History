import numpy as np
import random
def weighted_choice(sequence, 
                    weights,
                    secure=True):
    if secure:
        crypto = random.SystemRandom()
        x = crypto.random()
    else:
        x = np.random.random()
    cum_weights = [0] + list(np.cumsum(weights))
    index = find_interval(x, cum_weights)
    return sequence[index]

def find_interval(x, 
                  partition, 
                  endpoints=True):
    for i in range(0, len(partition)):
        if x < partition[i]:
            return i-1 if endpoints else i
    return -1 if endpoints else len(partition)

from collections import Counter
nodes = ['a', 'b', 'c', 'd', 'e', 'f','g','h','i','j','k']
weights = [3/10, 6/10, 41/100, 52/100, 52/100, 5/10, 48/100,52/100,5/10,48/100,5/10] #calculated individual probabilities on my own
outcomes = []
n = 10000
for _ in range(n):
    outcomes.append(weighted_choice(nodes, weights))
c = Counter(outcomes)
for key in c:
    c[key] = c[key] / n
    
print(sorted(c.values()))


#Took some code from https://www.python-course.eu/weighted_choice_and_sample.php
