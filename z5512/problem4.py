import random
from random import random as rand

nodes = {"A" : 1, "B" : 0, "C" : 1, "D" : 1, "E" : 1, "F" : 1, "G" : 1, "H" : 1, "I" : 1, "J" : 1, "K" : 1}

given = {"C","B","K"}

prob_a = 0.3

prob_b = 0.6

prob_da = [0.4, 0.8]

prob_ca = [0.5, 0.2]

prob_eb = [0.1, 0.8]

prob_f = 0.5

prob_gcde = [[[0.8, 0.7],
              [0.6, 0.5]],
             [[0.4, 0.3],
              [0.2, 0.1]]]

prob_he = [0.7, 0.4]

prob_ifg = [[0.2, 0.4],
            [0.6, 0.8]]

prob_jgh = [[0.1, 0.9],
            [0.7, 0.2]]

prob_ki = [0.7, 0.3]



def main(count):
    probability = 0
    for _ in range(count):
        num = random.choice(list(given))
        while (num in given or num == None):
            num = random.choice(list(nodes.keys()))
        mark(num)
        if (nodes.get("G")):
            probability += 1/count
    return probability

def mark(num):
    if (num == "A"):
        probab_a()
    elif (num == "B"):
        probab_b()
    elif (num == "C"):
        probab_c()
    elif (num == "D"):
        probab_d()
    elif (num == "E"):
        probab_e()
    elif (num == "F"):
        probab_f()
    elif (num == "G"):
        probab_g()
    elif (num == "H"):
        probab_h()
    elif (num == "I"):
        probab_i()
    elif (num == "J"):
        probab_j()
    elif (num == "K"):
        probab_k()

def probab_a():
    pa = prob_a
            
    a = 1

    if nodes.get("D"):
        pda = prob_da[a]
    else:
        pda = 1 - prob_da[a]
    if nodes.get("C"):
        pca = prob_ca[a]
    else:
        pca = 1 - prob_ca[a]

    aval = pa * pda * pca

    a = 0
            
    if nodes.get("D"):
        pda = prob_da[a]
                
    else:
        pda = 1 - prob_da[a]

    if nodes.get("C"):
        pca = prob_ca[a]

    else:
        pca = 1 - prob_ca[a]
                
    negative_a = (1 - pa) * pda * pca
    prob_a_mark = aval / (aval + negative_a)

    
    if rand() < prob_a_mark:
        nodes["A"] = 1
    else:
        nodes["A"] = 0

def probab_b():
     b = 1
     
     pb = prob_b
     
     if nodes.get("E"):
         peb = prob_eb[b]
     else:
         peb = 1 - prob_eb[b]

     bval = pb * peb

     b = 0

     pb = 1 - prob_b

     if nodes.get("E"):
         peb = prob_eb[b]
     else:
         (1 - prob_eb[b])

     negative_b = pb * peb

     prob_b_mark = bval / (bval + negative_b)

     if rand() < prob_b_mark:
         nodes["B"] = 1
         
     else:
         nodes["B"] = 0

def probab_c():
    c = 1
    if nodes.get("G"):
        pgcde = prob_gcde[c][nodes.get("D")][nodes.get("E")]
    else:
        pgcde = 1 - prob_gcde[c][nodes.get("D")][nodes.get("E")]

    pca = prob_ca[nodes.get("A")]
    
    cval = pca * pgcde
    
    c = 0
    pca = 1 - prob_ca[nodes.get("A")]
    if nodes.get("G"):
        pgcde = prob_gcde[c][nodes.get("D")][nodes.get("E")]
    else:
        pgcde = 1 - prob_gcde[c][nodes.get("D")][nodes.get("E")]
    
    negative_c = pca * pgcde
    prob_c_mark = cval / (cval + negative_c)
    if rand() < prob_c_mark:
         nodes["C"] = 1
    else:
         nodes["C"] = 0

def probab_d():
    d = 1
    pda = prob_da[nodes.get("A")]
    if nodes.get("G"):
        pgcde = prob_gcde[nodes.get("C")][d][nodes.get("E")]
    else:
        pgcde = 1 - prob_gcde[nodes.get("C")][d][nodes.get("E")]

    dval = pda * pgcde
    
    d = 0
    
    pda = 1 - prob_da[nodes.get("A")]

    if nodes.get("G"):
        pgcde = prob_gcde[nodes.get("C")][d][nodes.get("E")]
    else:
        pgcde = 1 - prob_gcde[nodes.get("C")][d][nodes.get("E")]
        
    negative_d = pda * pgcde
    prob_d_mark = dval / (dval + negative_d)
    if rand() < prob_d_mark:
        nodes["D"] = 1
        
    else:
        nodes["D"] = 0

def probab_e():
    e = 1
    peb = prob_eb[nodes.get("B")]
    if nodes.get("H"):
        phe = prob_he[nodes.get("E")]
    else:
        phe = 1 - prob_he[nodes.get("E")]

    if nodes.get("G"):
        pgcde = prob_gcde[nodes.get("C")][nodes.get("D")][e]
    else:
        pgcde = 1 - prob_gcde[nodes.get("C")][nodes.get("D")][e]
        
    e_val = peb * phe * pgcde
    e = 0
    peb = 1 - prob_eb[nodes.get("B")]
    
    if nodes.get("H"):
        phe = prob_he[e]
    else:
        phe = 1 - prob_he[e]

    if nodes.get("G"):
        pgcde = prob_gcde[nodes.get("C")][nodes.get("D")][e]
    else:
        pgcde = 1 - prob_gcde[nodes.get("C")][nodes.get("D")][e]
    negative_e = peb * phe * pgcde
    prob_e_mark = e_val / (e_val + negative_e)
    if rand() < prob_e_mark:
        nodes["E"] = 1
    else:
        nodes["E"] = 0

def probab_f():
    f = 1 
    pf = prob_f
    if nodes.get("I"):
        pifg = prob_ifg[f][nodes.get("G")]
    else:
        pifg = (1 -  prob_ifg[f][nodes.get("G")])

    fval = pf * pifg
    f = 0
    pf = 1 - prob_f
    if nodes.get("I"):
        pifg = prob_ifg[f][nodes.get("G")]
    else:
        pifg = (1 -  prob_ifg[f][nodes.get("G")])
    negative_f = pf * pifg
    prob_f_mark = fval / (fval + negative_f)
    if rand() < prob_f_mark:
        nodes["F"] = 1
    else:
        nodes["F"] = 0

def probab_g():
     g = 1
     pgcde = prob_gcde[nodes.get("C")][nodes.get("D")][nodes.get("E")]
     if nodes.get("I"):
         pifg = prob_ifg[nodes.get("F")][g]
     else:
         pifg = 1 - prob_ifg[nodes.get("F")][g]

     if nodes.get("J"):
         pjgh = prob_jgh[g][nodes.get("H")]
     else:
         pjgh = 1 - prob_jgh[g][nodes.get("H")]

     gval = pgcde * pifg * pjgh
     g = 0
     pgcde = 1 -  prob_gcde[nodes.get("C")][nodes.get("D")][nodes.get("E")]
     if nodes.get("I"):
         pifg = prob_ifg[nodes.get("F")][g]
     else:
         pifg = 1 - prob_ifg[nodes.get("F")][g]

     if nodes.get("J"):
         pjgh = prob_jgh[g][nodes.get("H")]
     else:
         pjgh = 1 - prob_jgh[g][nodes.get("H")]
        
     negative_g = pgcde * pifg * pjgh
     prob_g_mark = gval / (gval + negative_g)
     if rand() < prob_g_mark:
         nodes["G"] = 1
     else:
         nodes["G"] = 0

def probab_h():
    h = 1
    phe = prob_he[nodes.get("E")]
    if nodes.get("J"):
         pjgh = prob_jgh[nodes.get("G")][h]
    else:
         pjgh = 1 - prob_jgh[nodes.get("G")][h]
    hval = phe * pjgh
    h = 0
    phe = 1 - prob_he[nodes.get("E")]
    if nodes.get("J"):
         pjgh = prob_jgh[nodes.get("G")][h]
    else:
         pjgh = 1 - prob_jgh[nodes.get("G")][h]
    negative_h = phe * pjgh  
    prob_h_mark = hval / (hval + negative_h)
    if rand() < prob_h_mark:
        nodes["H"] = 1
    else:
        nodes["H"] = 0

def probab_i():
    i = 1
    pifg = prob_ifg[nodes.get("F")][nodes.get("G")]
    if nodes.get("K"):
        pk = prob_ki[i]
    else:
        pk = 1-prob_ki[i]
    ival = pifg * pk
    i = 0
    pifg = 1 - prob_ifg[nodes.get("F")][nodes.get("G")]
    if nodes.get("K"):
        pk = prob_ki[i]
    else:
        pk = 1-prob_ki[i]
    negative_i = pifg * pk
    prob_i_mark = ival / (ival + negative_i)
    if rand() < prob_i_mark:
        nodes["I"] = 1
    else:
        nodes["I"] = 0

def probab_j():
    prob_j_mark = prob_jgh[nodes.get("G")][nodes.get("H")]
    if rand() < prob_j_mark:
        nodes["J"] = 1
    else:
        nodes["J"] = 0

def probab_k():
    prob_k_mark = prob_ki[nodes.get("I")]
    if rand() < prob_k_mark:
        nodes["K"] = 1
    else:
        nodes["K"] = 0

print(main(1000000))