import secrets

def rand_in_range(min, max):
    return min + secrets.randbelow(max - min)