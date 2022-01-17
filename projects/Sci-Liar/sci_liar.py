import random
import time
import uuid
from daw.audio import load_audio, save_audio, play, stretch
from daw.chop import chop, sequence

def seq_one():
    s = lambda x: [x*12, x*13] * 2 + [x*14, x*15] * 2
    return [s(i) * 2 for i in range(8)]

def seq_two():
    s = lambda x: [x*12, x*15] + [x*15, x*12] + [x*14, x*13] + [x*13, x*14]
    return [s(i) * 2 for i in range(24)]

def liar(audio_file, bpm, pattern_func):
    audio = load_audio(audio_file)
    bars = 7/16
    slices = chop(audio, bpm, bars, fade_in=2, fade_out=2)
    new_slices = []
    for i,s in enumerate(slices):
        if i % 2 == 0:
            s = s.reverse() if i % 6 == 0 else s
            s = stretch(s, 1.2 + random.random()*0.05)
        elif i % 7 == 0:
            s = stretch(s, 0.5) * 2 + stretch(s, 0.25) * 4
        elif i % 5 == 0:
            s = stretch(s, 0.7)
        new_slices.append(s)

    pat = pattern_func()
    seq = sequence(new_slices, [item for sublist in pat for item in sublist][8:])
    seq = stretch(seq, 0.7)
    date = time.strftime("%y-%m-%d")
    rnd_str = str(uuid.uuid1())[:5]
    save_audio(seq, f"~/Music/{date}-sci-liar-{rnd_str}.wav")
    #play(seq)

if __name__ == "__main__":
    liar(audio_file="Liar.mp3", bpm=120, pattern_func=seq_one)
