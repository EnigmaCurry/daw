import random
import time
import uuid
from daw.audio import load_audio, save_audio, play, stretch
from daw.chop import chop, sequence

def seq_one(limit):
    s = lambda x: [x*12, x*13] * 2 + [x*14, x*15] * 2
    return [s(i) * 2 for i in range(int(limit/16))]

def seq_two(limit):
    s = lambda x: [x*12, x*15] + [x*15, x*12] + [x,x+1,x+2,x+3] + [x*14, x*13] + [x*13, x*14]
    return [s(i) * 2 for i in range(int(limit/24))]

def seq_three(limit):
    return [[i] for i in range(limit)]

def munge_slices(slices):
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

def liar(audio_file, bpm, pattern_func):
    audio = load_audio(audio_file)
    bars = 1/16
    slices = chop(audio, bpm, bars, fade_in=0, fade_out=0)
    slices = munge_slices(slices)

    pat = pattern_func(len(slices))
    flattened = [item for sublist in pat for item in sublist][8:]
    seq = sequence(slices, flattened)
    return seq

def save(seq):
    date = time.strftime("%y-%m-%d")
    rnd_str = str(uuid.uuid1())[:5]
    print("Length: ",time.strftime('%H:%M:%S', time.gmtime(seq.duration_seconds)))
    save_audio(seq, f"~/Music/{date}-sci-liar-{rnd_str}.wav")

if __name__ == "__main__":
    seq = liar(audio_file="Liar.mp3", bpm=120, pattern_func=seq_two)
    seq = stretch(seq, 1.7)
    play(seq)
