#returns (u, v) such that (2**u) * v = n - 1 and v is odd
def odd_log2_decomp(n):
    v = (n - 1) >> 1

    #bit shifting should be faster than division but maybe I'm dumb
    exponent = 1
    while (v & 1) == 0:
        v = v >> 1
        exponent += 1

    return (1 << exponent, v)

