import random


def flatten(t):
    """Flatten nested iterables
    >>> flatten(zip([1,2,3],[4,5,6]))
    [1, 4, 2, 5, 3, 6]
    """
    return [item for sublist in t for item in sublist]


def sliding(limit):
    for i in range(limit):
        yield (0 + i, 1 + i, 2 + i, 3 + i)


def random_twiddle(limit, max):
    for i in range(limit):
        yield (
            random.randint(0, max),
            random.randint(0, max),
            random.randint(0, max),
            random.randint(0, max),
        ) * random.choice((2, 4))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
