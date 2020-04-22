from src.random_util import rand_in_range

NUMBER_TESTS = 6
def rand_prime(q_min, q_max):
    p = rand_in_range(q_min, q_max)
    while not miller_rabin_is_prime(p):
        p = rand_in_range(q_min, q_max)
    
    return p

def miller_rabin_is_prime(n, tests = NUMBER_TESTS):
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

