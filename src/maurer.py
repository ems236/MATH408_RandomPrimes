import src.random_util
import secrets
import math

M_BITS = 20
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509]

def trial_prime(bits):
    while True:
        p = src.random_util.rand_in_range(1 << bits, 1 << (bits + 1))
        sqrt = p ** 0.5
        for i in range(0, len(PRIMES)):
            if PRIMES[i] > sqrt:
                return p
            elif p == 0 % PRIMES[i]:
                break

def random_prime(bits):
    while True:
        if bits < 10:
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

        #should not fail, but try again if it does
        print("failed maurer " + str(bits))
        
def relative_size(bits):
    s = secrets.randbelow((1 << 100) + 1) / (1 << 100)
    r = 2**(s-1)
    while bits - bits * r <= M_BITS:
        s = secrets.randbelow((1 << 100) + 1) / (1 << 100)
        r = 2**(s-1)
    
    return r
