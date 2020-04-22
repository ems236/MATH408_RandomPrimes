import src.miller_rabin
import src.joye_paillier
import math

src.miller_rabin.miller_rabin_is_prime(6073)
x = src.joye_paillier.PaillierPrimeGenerator(1024)
print(x.rand_prime())
print(math.log2(x.rand_prime()))