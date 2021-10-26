import random

def sliding(limit):
    for i in range(limit):
        yield (0+i, 1+i, 2+i, 3+i)

def random_twiddle(limit, max):
    for i in range(limit):
        yield (random.randint(0, max), random.randint(0, max)) * 4

