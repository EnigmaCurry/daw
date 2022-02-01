import random


def flatten(t):
    """Flatten nested lists and/or tuples
    >>> flatten(zip([1,2,3],[4,5,6]))
    (1, 4, 2, 5, 3, 6)
    >>> flatten((1, (2,3)))
    (1, 2, 3)
    """
    return tuple(
        [
            item
            for sublist in t
            for item in (sublist if isinstance(sublist, (tuple, list)) else [sublist])
        ]
    )


def flat_tokens(t):
    """
    Flatten nested iterables, splitting encounted strings into chars
    >>> flat_tokens((1, ("two", "three")))
    [1, 't', 'w', 'o', 't', 'h', 'r', 'e', 'e']
    """
    flat = []
    for i in flatten(t):
        if type(i) == str:
            [flat.append(j) for j in i]
        else:
            flat.append(i)
    return flat


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
