import random
from random import random as rand

samples = {"a" : 1, "b" : 0, "c" : 1, "d" : 1, "e" : 1, "f" : 1, "g" : 1, "h" : 1, "i" : 1, "j" : 1, "k" : 1}


Pa = 0.3
Pb = 0.6
Pda = [0.4, 0.8]
Pca = [0.5, 0.2]
Peb = [0.1, 0.8]
Pf = 0.5
Pgcde = [[[0.8, 0.7], [0.6, 0.5]],[[0.4, 0.3], [0.2, 0.1]]]
Phe = [0.7, 0.4]
Pifg = [[0.2, 0.4], [0.6, 0.8]]
Pjgh = [[0.1, 0.9], [0.7, 0.2]]
Pki = [0.7, 0.3]

evidence = {"c", "b", "k"}


def main(count):
    probability = 0
    for _ in range(count):
        num = random.choice(list(given))
        while (num in evidence or num == None):
            num = random.choice(list(samples.keys()))
        if (num in given):
            raise ValueError("Can't have things in evidence: {}".format(sample))
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
        if (nodes.get("G")):
            probability += 1/count
    return probability

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
    e = samples.get("e")

        # positive case
        b = 1
        pb = Pb
        peb = Peb[b] if e else (1 - Peb[b])
        b_num = pb * peb

        # negative case
        b = 0
        pb = 1 - Pb
        peb = Peb[b] if e else (1 - Peb[b])
        neg_b_num = pb * peb

        pb_markov = b_num / (b_num + neg_b_num)
        samples["b"] = 1 if rand() < pb_markov else 0
def probab_c():
     a = samples.get("a")
        d = samples.get("d")
        g = samples.get("g")
        e = samples.get("e")

        # positive case
        c = 1
        pgcde = Pgcde[c][d][e] if g else (1 - Pgcde[c][d][e])
        pca = Pca[a]
        c_num = pca * pgcde

        # negative case
        c = 0
        pgcde = Pgcde[c][d][e] if g else (1 - Pgcde[c][d][e])
        pca = 1 - Pca[a]
        neg_c_num = pca * pgcde

        pc_markov = c_num / (c_num + neg_c_num)
        samples["c"] = 1 if rand() < pc_markov else 0

def probab_d():
    a = samples.get("a")
        c = samples.get("c")
        g = samples.get("g")
        e = samples.get("e")
        d = samples.get("d")

        # positive case
        d = 1
        pda = Pda[a]
        pgcde = Pgcde[c][d][e] if g else (1 - Pgcde[c][d][e])
        d_num = pda * pgcde

        # negative case
        d = 0
        pda = 1 - Pda[a]
        pgcde = Pgcde[c][d][e] if g else (1 - Pgcde[c][d][e])
        neg_d_num = pda * pgcde

        pd_markov = d_num / (d_num + neg_d_num)
        samples["d"] = 1 if rand() < pd_markov else 0

def probab_e():
    c = samples.get("c")
        b = samples.get("b")
        d = samples.get("d")
        g = samples.get("g")
        h = samples.get("h")

        # positive case 
        e = 1
        peb = Peb[b]
        phe = Phe[e] if h else (1 - Phe[e])
        pgcde = Pgcde[c][d][e] if g else (1 - Pgcde[c][d][e])
        e_num = peb * phe * pgcde

        # negative case
        e = 0
        peb = 1 - Peb[b]
        phe = Phe[e] if h else (1 - Phe[e])
        pgcde = Pgcde[c][d][e] if g else (1 - Pgcde[c][d][e])
        neg_e_num = peb * phe * pgcde

        pe_markov = e_num / (e_num + neg_e_num)
        samples["e"] = 1 if rand() < pe_markov else 0

def probab_f():
    i = samples.get("i")
        g = samples.get("g")

        # positive case
        f = 1 
        pf = Pf
        pifg = Pifg[f][g] if i else (1 - Pifg[f][g])
        f_num = pf * pifg

        # negative case
        f = 0
        pf = 1 - Pf
        pifg = Pifg[f][g] if i else (1 - Pifg[f][g])
        neg_f_num = pf * pifg
        pf_markov = f_num / (f_num + neg_f_num)
        samples["f"] = 1 if rand() < pf_markov else 0

def probab_g():
     c = samples.get("c")
        d = samples.get("d")
        e = samples.get("e")
        f = samples.get("f")
        i = samples.get("i")
        j = samples.get("j")
        h = samples.get("h")

        # positive case 
        g = 1
        pgcde = Pgcde[c][d][e]
        pifg = Pifg[f][g] if i else (1 - Pifg[f][g])
        pjgh = Pjgh[g][h] if j else (1 - Pjgh[g][h])
        g_num = pgcde * pifg * pjgh

        # negative case
        g = 0
        pgcde =  1 - Pgcde[c][d][e]
        pifg = Pifg[f][g] if i else (1 - Pifg[f][g])
        pjgh = Pjgh[g][h] if j else (1 - Pjgh[g][h])
        neg_g_num = pgcde * pifg * pjgh

        pg_markov = g_num / (g_num + neg_g_num)
        samples["g"] = 1 if rand() < pg_markov else 0

def probab_h():
    e = samples.get("e")
        g = samples.get("g")
        j = samples.get("j")

        # positive case
        h = 1
        phe = Phe[e]
        pjgh = Pjgh[g][h] if j else (1 - Pjgh[g][h])
        h_num = phe * pjgh

        # negative case
        h = 0
        phe = 1 - Phe[e]
        pjgh = Pjgh[g][h] if j else (1 - Pjgh[g][h])
        neg_h_num = phe * pjgh

        ph_markov = h_num / (h_num + neg_h_num)
        samples["h"] = 1 if rand() < ph_markov else 0
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
