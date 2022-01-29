import random
import time
import uuid
from daw.audio import load_audio, save_audio, play, stretch
from daw.chop import chop, reduce_slices, sequence
from daw.pattern import flatten

def seq_one(limit):
    s = lambda x: [x*12, x*13] * 2 + [x*14, x*15] * 2
    return [s(i) * 2 for i in range(int(limit/16))]

def seq_two(limit):
    s = lambda x: [x*12, x*15] + [x*15, x*12] + [x,x+1,x+2,x+3] + [x*14, x*13] + [x*13, x*14]
    return [s(i) * 2 for i in range(int(limit/24))]

def seq_three(limit):
    return [[i] for i in range(limit)]

def munge1(slices):
    new_slices = []
    for i,s in enumerate(slices):
        if i % 2 == 0:
            s = s.reverse() if i % 6 == 0 else s
            s = stretch(s, 1 + random.random()*0.05)
        elif i % 15 == 0:
            s = stretch(s, 0.25  + random.random()*0.05) * 8 + stretch(s, 0.75) * 4
        elif i % 7 == 0:
            s = stretch(s, 0.7)
        new_slices.append(s)
    return new_slices

def liar1(audio):
    slices = chop(audio, 120, 4)
    s8 = sequence(slices, [8])
    s8_0, s8_1 = chop(s8, 120, 2)
    s8b = flatten(zip(reversed(chop(s8_0, 120, 1/8)), chop(s8_1*2, 120, 1/8)))
    return reduce_slices([s8_0, reduce_slices(s8b)])

def liar2(audio, i=16):
    slices = chop(audio, 120, 4)
    s8 = sequence(slices, [i])
    s8_0, s8_1 = chop(s8, 120, 2)
    s8b = flatten(zip(reversed(chop(s8_0, 120, 1/8)), reversed(chop(s8_1*2, 120, 1/8))))
    return reduce_slices([s8_0, reduce_slices(s8b)])

def liar3(audio, i=8):
    slices = chop(audio, 120, 4)
    s8 = sequence(slices, [i])
    s8_0, s8_1 = chop(s8, 120, 2)
    s8_0_slow = stretch(reduce_slices([s8_0]), 2)
    return s8_0_slow + s8_0_slow.reverse()

def liar4(audio1, audio2):
    return 

if __name__ == "__main__":
    audio = load_audio("Liar.mp3")
    a = liar3(audio, 7)
    b = reduce_slices([liar2(audio), liar1(audio).reverse(), ])
    c = liar3(audio, 8)
    d = reduce_slices([liar2(audio, 8), liar1(audio).reverse(), ])

    e = reduce_slices([a, b, c, d])
    f = e.pan(-0.5).overlay(e.reverse().pan(+0.5))
    g = stretch(f, 0.7) * 2
    h = g.pan(-0.5).overlay(g.reverse().pan(+0.5))

    new_audio = a
    
    #save_audio(new_audio, "~/Music", "sci-liar")
    play(new_audio)
