from collections import Counter



def main():
    prob2_1 = 50
    prob1_3 = -50
    #change these values to for starting utilities
    prob2_2 = 0
    prob3_2 = -3
    prob2_3 = -1
    prob3_3 = -10
    prob2_4 = -3
    prob3_4 = -2
    #rewards for each block
    rprob2_1 = 50
    rprob1_3 = -50
    rprob2_2 = 0
    rprob3_2 = -3
    rprob2_3 = -1
    rprob3_3 = -10
    rprob2_4 = -3
    rprob3_4 = -2
    gamma = .80
    iteration = 17
    for i in range(0,iteration):    
        tprob2_2 = rprob2_2 + gamma * max(
            (prob2_1 * .7 + prob2_2 * .15 + prob3_2 * .15), #up
            (prob2_2 * .7 + prob2_1 * .15 + prob2_3 * .15), #left
            (prob2_3 * .7 + prob2_2 * .15 + prob3_2 * .15), #down
            (prob3_2 * .7 + prob2_1 * .15 + prob2_3 * .15)) #right
        tprob3_2 = rprob3_2 + gamma * max(
            (prob3_2 * .7 + prob3_2 * .15 + prob2_2 * .15),
            (prob2_2 * .7 + prob3_2 * .15 + prob3_3 * .15),
            (prob3_3 * .7 + prob2_2 * .15 + prob3_2 * .15),
            (prob3_2 * .7 + prob3_3 * .15 + prob3_2 * .15))
        tprob2_3 = rprob2_3 + gamma * max(
            (prob2_2 * .7 + prob3_3 * .15 + prob1_3 * .15),
            (prob1_3 * .7 + prob2_4 * .15 + prob2_2 * .15),
            (prob2_4 * .7 + prob1_3 * .15 + prob3_3 * .15),
            (prob3_3 * .7 + prob2_4 * .15 + prob2_2 * .15))
        tprob3_3 = rprob3_3 + gamma * max(
            (prob3_2 * .7 + prob2_3 * .15 + prob3_3 * .15),
            (prob2_3 * .7 + prob3_2 * .15 + prob3_4 * .15),
            (prob3_4 * .7 + prob2_3 * .15 + prob3_3 * .15),
            (prob3_3 * .7 + prob3_2 * .15 + prob3_4 * .15))
        tprob2_4 = rprob2_4 + gamma * max(
            (prob2_3 * .7 + prob2_4 * .15 + prob3_4 * .15),
            (prob2_4 * .7 + prob2_3 * .15 + prob2_4 * .15),
            (prob2_4 * .7 + prob2_4 * .15 + prob3_4 * .15),
            (prob3_4 * .7 + prob2_3 * .15 + prob2_4 * .15))
        tprob3_4 = rprob3_4 + gamma * max(
            (prob3_3 * .7 + prob2_4 * .15 + prob3_4 * .15),
            (prob2_4 * .7 + prob3_3 * .15 + prob3_4 * .15),
            (prob3_4 * .7 + prob2_4 * .15 + prob3_4 * .15),
            (prob3_4 * .7 + prob3_3 * .15 + prob3_4 * .15))

        prob2_2 = tprob2_2;
        prob3_2 = tprob3_2;
        prob2_3 = tprob2_3;
        prob3_3 = tprob3_3;
        prob2_4 = tprob2_4;
        prob3_4 = tprob3_4;

        print('b      {}     {}'.format(round(prob2_1,3), 'b'))
        print('b      {}   {}'.format(round(prob2_2,3), round(prob3_2,3)))
        print('{}  {}   {}'.format(round(prob1_3,3), round(prob2_3,3), round(prob3_3,3)))
        print('b      {}    {}'.format(round(prob2_4,3), round(prob3_4,3)))
        print('\n')
        print('\n')
    
    print("Number of iterations: {}".format(iteration))
    return 0

if __name__ == '__main__':
    main()

