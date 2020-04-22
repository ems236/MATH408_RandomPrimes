import src.random_util
import math

M_BITS = 20
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]

def trial_prime(bits):
    while True:
        p = src.random_util.rand_in_range(1 << bits, 1 << (bits + 1))
        sqrt = p ** 0.5
        for i in range(0, len(PRIMES)):
            if PRIMES[i] > sqrt:
                return p
            else:
                break

def random_prime(bits):
    if bits <= 6:
        return trial_prime(bits) 
    
    r = 0.5
    if bits > 2 * M_BITS:
        r = relative_size(bits)
    
    q = random_prime(math.floor(r * bits) + 1)
    interval = (1 << (bits - 1)) // (2 * q)

    while True:
        r = src.random_util.rand_in_range(interval + 1, 2 * interval + 1)
        n = 2 * r * q + 1

        #test by pocklington
        a = src.random_util(2, n-1)
        b = pow(a, n-1, n)
        if b == 1:
            test = pow(a, 2*r, n) - 1
            if math.gcd(test, q) == 1:
                return n    
        


def relative_size(bits):
    pass
