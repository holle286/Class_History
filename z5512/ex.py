import math

def gradientDescent(initial, alpha):
    
    weights = initial
    
    for i in range(100000):
        
        a,b,c,d = weights

        # partial derivatives 
        derA = 4 * a * c**4 - b
        derB = -a + 4 * b * d**2
        derC = 8 * a**2 * c**3 - 9 * c**2 * d
        derD = math.exp(d + math.sin(d)) * (math.cos(d) + 1) + 4 * b**2 * d - 3 * c**3

        # calc new weights
        newWeights = [a - alpha * derA, b - alpha * derB, c - alpha * derC, d - alpha * derD]
        weights = newWeights
        
    return weights

def main():
    print(gradientDescent([0,0,0,0],.01))

if __name__ == '__main__':
    main()



