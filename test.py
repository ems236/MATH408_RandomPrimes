import src.miller_rabin
import src.joye_paillier
import src.maurer
import math
import csv
import timeit

with open('timing.csv', 'w', newline='') as results:
    writer = csv.writer(results)
    writer.writerow(["bits", "Miller-Rabin", "Joye-Paillier", "Maurer"])
    for i in range(3, 12):
        bits = 1 << i
        miller = timeit.timeit(lambda: src.miller_rabin.rand_prime(bits), number=1000)
        paillier_gen = src.joye_paillier.PaillierPrimeGenerator(bits)
        paillier = timeit.timeit(lambda: paillier_gen.rand_prime(), number=1000)
        maurer = timeit.timeit(lambda: src.maurer.random_prime(bits), number=1000)

        data = [bits, miller, paillier, maurer]
        writer.writerow(data)
