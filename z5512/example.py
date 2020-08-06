import random
from random import random as rand

# Given table values
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

samples = {"a" : 1,
           "b" : 0,
           "c" : 1,
           "d" : 1,
           "e" : 1,
           "f" : 1,
           "g" : 1,
           "h" : 1,
           "i" : 1,
           "j" : 1,
           "k" : 1}

def calc_markov(sample):

    if (sample in evidence):
        raise ValueError("Can't have things in evidence: {}".format(sample))

    if (sample == "a"):
        # positive case
        a = 1
        pa = Pa
        pda = Pda[a] if samples.get("d") else (1 - Pda[a])
        pca = Pca[a] if samples.get("c") else (1 - Pca[a])
        a_num = pa * pda * pca

        # negative case
        a = 0
        pda = Pda[a] if samples.get("d") else (1 - Pda[a])
        pca = Pca[a] if samples.get("c") else (1 - Pca[a])
        neg_a_num = (1 - pa) * pda * pca

        pa_markov = a_num / (a_num + neg_a_num)
        samples["a"] = 1 if rand() < pa_markov else 0

    elif (sample == "b"):
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
    
    elif (sample == "c"):
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
        samples["d"] = 1 if rand() < pd_markov else 0

    elif (sample == "d"):
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

    elif (sample == "e"):
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
    
    elif (sample == "f"):
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

    elif (sample == "g"):

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
    
    elif (sample == "h"):
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

    elif (sample == "i"):
        f = samples.get("f")
        k = samples.get("k")
        g = samples.get("g")

        # positive case
        i = 1
        pifg = Pifg[f][g]
        pk = Pki[i] if k else (1 - Pki[i])
        k_num = pifg * pk

        # negative case
        i = 0
        pifg = 1 - Pifg[f][g]
        pk = Pki[i] if k else (1 - Pki[i])
        neg_k_num = pifg * pk

        pk_markov = k_num / (k_num + neg_k_num)
        samples["i"] = 1 if rand() < pk_markov else 0

    elif (sample == "j"):
        g = samples.get("g")
        h = samples.get("h")

        pj_markov = Pjgh[g][h]
        samples["j"] = 1 if rand() < pj_markov else 0

    elif (sample == "k"):
        i = samples.get("i")

        pk_markov = Pki[i]
        samples["k"] = 1 if rand() < pk_markov else 0

def gibbs(sample_size):
    prob = 0
    for _ in range(sample_size):
        sample = random.choice(list(evidence))
        while (sample in evidence or sample == None):
            sample = random.choice(list(samples.keys()))
        calc_markov(sample)
        if (samples.get("g")):
            prob += 1/sample_size
    return prob

print(gibbs(1000000))
