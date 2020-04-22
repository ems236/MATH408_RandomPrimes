import math
import secrets
import src.random_util
import src.miller_rabin

EPSILON = 0.001
B_MIN = 0
A_VAL = 2

def rand_unit(pi, lamba_pi):
    k = secrets.randbelow(pi)
    while True:
        k_carm = pow(k, lamba_pi, pi)
        if k_carm == 1:
            return k
        k = (k + secrets.randbelow(pi) * (1 - k_carm)) % pi

def carmichael(prime_factors):
    #this is not a good way
    #carmichael(p) = p -1

    carmichaels = [p - 1 for p in prime_factors]

    current_gcd = carmichaels[0]
    current_prod = carmichaels[0]
    for i in range(1, len(carmichaels)):
        current_gcd = math.gcd(current_gcd, carmichaels[i])
        current_prod *= carmichaels[i]
    
    return current_prod // current_gcd



class PaillierPrimeGenerator():
    def __init__(self, bitsize):
        self.bits = bitsize
        self.set_params()

    #creates the first r primes where r is a lot
    def bunch_of_odd_primes(self):
        data = []

        COUNT = 10000
        pos = 0
        while pos < COUNT:
            data.append(True)
            pos += 1
        
        end = math.ceil(COUNT ** 0.5)
        base = 2
        while base <= end:
            if data[base]:
                mult = 2 * base
                while mult < COUNT:
                    data[mult] = False 
                    mult += base
            base += 1

        primes = []
        pos = 3
        while pos < COUNT:
            if data[pos]:
                primes.append(pos)
            pos += 1
        
        return primes

    def can_use_pi(self, pi, q_min, q_max):
        #find delta b
        b = 0
        while (((b + 1) * pi) - 1)/(q_max - q_min) <= 1 - EPSILON:
            b += 1
        
        test = (((b + 1) * pi) - 1)/(q_max - q_min) 
        if test > 1:
            return (False, 0, 0)

        #find v
        # (v + 1 + b_max) pi <= q_max + 1
        v = 0
        while v * pi <= q_min:
            v += 1

        return (True, b, v)

    def set_params(self):
        #q_min = math.ceil(2 ** (self.bits - 0.5))
        q_min = 1 << self.bits
        q_max = 1 << (self.bits + 1)

        upper_bound = (q_max - q_min) + 1
        #0 <= (b_m+1)PI < bound
        # vPI >= q_min
        # vPI + (b_m+1)PI - 1 <= q_max

        primes = self.bunch_of_odd_primes()

        #find pi
        pi_vals = []
        pi = 1
        for i in range(0, len(primes)):
            pi *= primes[i]
            if pi > upper_bound:
                break
            else:
                pi_vals.append(pi)
        
        i = len(pi_vals) - 1
        while i >= 0:
            (pi_works, b, v) = self.can_use_pi(pi_vals[i], q_min, q_max)
            if pi_works:
                self.pi = pi_vals[i]
                self.b_min = B_MIN
                self.b_max = b
                self.v = v
                self.a = A_VAL
                self.pi_carmichael = carmichael(primes[:(i + 1)])
                break
            else:
                i -= 1

    def rand_prime(self):
        while True:
            k = rand_unit(self.pi, self.pi_carmichael)
            b = src.random_util.rand_in_range(self.b_min, self.b_max + 1)
            t = self.pi * b
            l = self.pi * self.v
            q = self.q_value(k, t, l)

            fail_max = 10000
            fails = 0
            while not src.miller_rabin.miller_rabin_is_prime(q) and fails < fail_max:
                k = (k << 1) % self.pi
                q = self.q_value(k, t, l)

                fails += 1

            if fails > fail_max:
                print("failed paillier " + str(self.bits))
                continue
            
            return q

    def q_value(self, k, t, l):
        q = k + t + l
        if 1 & q == 0:
            q = self.pi - k + t + l
        return q
    
    
    

        




