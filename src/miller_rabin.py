from src.random_util import rand_in_range

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]
NUMBER_TESTS = 6
def rand_prime(bits):
    q_min = 1 << bits
    q_max = 1 << (bits + 1)
    p = rand_in_range(q_min, q_max)
    while not miller_rabin_is_prime(p):
        p = rand_in_range(q_min, q_max)
    
    return p

def miller_rabin_is_prime(n, tests = NUMBER_TESTS):
    for p in PRIMES:
        if n % p == 0:
            return n == p

    (exponet, v) = odd_log2_decomp(n)
    for i in range(0, tests):
        #should be fine not to check this
        base = rand_in_range(2, n - 2)
        if is_composite_witness(base, exponet, v, n):
            return False
    
    return True

#returns (u, v) such that (2**u) * v = n - 1 and v is odd
def odd_log2_decomp(n):
    v = (n - 1) >> 1

    #bit shifting should be faster than division but maybe I'm dumb
    exponent = 1
    while (v & 1) == 0:
        v = v >> 1
        exponent += 1

    return (exponent, v)

#witness is some b in [2, n-1]
#returns true if composite
#false if pseudoprime
def is_composite_witness(witness, exponent, v, n):
    test_val = pow(witness, v, n)
    if abs(test_val) == 1:
        return False

    #go from 1 to u-1
    for i in range(0, exponent - 1):
        test_val = pow(test_val, 2, n)
        if test_val == n - 1:
            return False
        if test_val == 1:
            #n is composite, sqrt(1) != +- 1
            return True
    
    #n is composite.  Either witness ** n -1 mod n != 1 or sqrt(1) mod n != +- 1 
    return True

