import src.miller_rabin
import src.joye_paillier
import src.maurer
import math

src.miller_rabin.miller_rabin_is_prime(6073)
x = src.joye_paillier.PaillierPrimeGenerator(1024)
print(x.rand_prime())
print(math.log2(x.rand_prime()))

for _ in range(0, 10):
    p = src.maurer.random_prime(10)
    print(p)