import random
import os
from daw.sampler import (
    load_samples,
    note_span,
    apply_to_samples,
    sampler,
    compose,
    make_scale,
)
from daw.effects import adsr
from daw.audio import Track, load_audio, play, mix, stretch, AudioSegment
from daw.chop import chop, reduce_slices, sequence
from daw.pattern import flatten

sci_root = "/daw/samples/Scilent Symphony/"


def foursix(audio):
    bpm = 120
    bars = 2
    bins = 64
    new_length = bins * 4
    slices = chop(audio, bpm, bars/bins)

    ## random pattern
    #pattern = [random.choice(range(bins)) for x in range(new_length)]

    ## backwards and forward interleaved
    pattern = flatten(zip(range(0, bins, 2), reversed(range(1, bins, 2))))

    ## backwards, but the bins play forward:
    pattern = reversed(range(0, bins))
    print(pattern)

    return reduce_slices([slices[x] for x in pattern])


def tension(audio):
    bpm = 77
    bars = 2
    bins = 64
    slices = chop(audio, bpm, bars/bins)
    pattern = reversed(range(0, bins))
    return reduce_slices([slices[x] for x in pattern])

def slap_house(audio):
    bpm = 77
    bars = 4
    bins = 64
    slices = chop(audio, bpm, bars/bins)
    pattern = flatten(zip(range(0, bins, 2), reversed(range(1, bins, 2))))
    return reduce_slices([slices[x] for x in pattern])



def main():
    #return foursix(load_audio(os.path.join(sci_root, "foursix.b.wav")))
    #return tension(load_audio(os.path.join(sci_root, "sci-tension.wav")))
    return slap_house(load_audio(os.path.join(sci_root, "22-09-02.a sci-slap-house.wav")))
