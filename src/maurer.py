import src.random_util
import secrets
import math

M_BITS = 20
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]

def trial_prime(bits):
    return PRIMES[src.random_util.rand_in_range(0, len(PRIMES))]
    """while True:
        p = src.random_util.rand_in_range(1 << (bits - 1), 1 << bits)
        sqrt = p ** 0.5
        for i in range(0, len(PRIMES)):
            if PRIMES[i] > sqrt:
                return p
            elif p == 0 % PRIMES[i]:
                break"""

def random_prime(bits):
    if bits <= 6:
        return trial_prime(bits) 
    
    r = 0.5
    if bits > 2 * M_BITS:
        r = relative_size(bits)
    
    q = random_prime(math.floor(r * bits) + 1)
    interval = (1 << (bits - 1)) // (2 * q)

    fail_count = interval * 2
    attempts = 0
    while attempts < fail_count:
        rand_scale = src.random_util.rand_in_range(interval + 1, 2 * interval + 1)
        n = 2 * rand_scale * q + 1

        #test by pocklington
        a = src.random_util.rand_in_range(2, n-1)
        b = pow(a, n-1, n)
        if b == 1:
            test = pow(a, 2 * rand_scale, n) - 1
            if math.gcd(test, q) == 1:
                return n
        
        attempts += 1
    
    #try again if it fails
    return random_prime(bits)
        
def relative_size(bits):
    s = secrets.randbelow((1 << 100) + 1) / (1 << 100)
    r = 2**(s-1)
    while bits - bits * r > M_BITS:
        s = secrets.randbelow((1 << 100) + 1) / (1 << 100)
        r = 2**(s-1)
    
    return r
