import os
from functools import cache

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


@cache
def load_scales():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "scales.yaml")
    ) as f:
        scales = load(f, Loader=Loader)
    return {i["name"].lower(): i for i in scales}


def get_scale(scale):
    scales = load_scales()
    return scales[scale.lower()]


def in_scale(i, scale):
    """
    >>> major = get_scale("major")
    >>> in_scale(0, major)
    True
    >>> in_scale(1, major)
    False
    >>> in_scale(23, major)
    True
    >>> in_scale(24, major)
    True
    >>> in_scale(25, major)
    False
    """
    for note in scale["notes"]:
        if i % 12 == note:
            return True
    else:
        return False
