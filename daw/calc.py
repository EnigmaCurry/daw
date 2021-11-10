import math
from collections import namedtuple

def bpm(bpm):
    """
    >>> bpm(120)
    Bpm(bpm=120, beat_ms=500.0, frequency=2.0)
    >>> bpm(160)
    Bpm(bpm=160, beat_ms=375.0, frequency=2.6666666666666665)
    """
    Bpm = namedtuple("Bpm", ['bpm', 'beat_ms', 'frequency'])
    return Bpm(bpm, (1 / (bpm / 60.)) * 1000, bpm / 60)

def count_bars(duration_ms, audio_bpm, beats=4):
    """
    >>> count_bars(2000, 120)
    1
    >>> count_bars(144000, 160)
    96
    >>> count_bars(144001, 160)
    97
    """
    return math.ceil(duration_ms / (bpm(audio_bpm).beat_ms * beats))

def calc_bpm(duration_ms, bars=4, beats=4):
    """
    >>> calc_bpm(6E3)
    Bpm(bpm=160.0, beat_ms=375.0, frequency=2.6666666666666665)
    """
    beat_ms = (duration_ms / bars) / beats
    duration_beats = duration_ms / beat_ms
    return bpm(duration_beats * (60E3 / duration_ms))

if __name__ == "__main__":
    import doctest
    doctest.testmod()

