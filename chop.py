import os
import math
import random
import itertools
from pydub import AudioSegment
from pydub.playback import play

import calc
import pattern

def load_audio(path):
    path_parts = path.split(".")
    if len(path_parts) > 1:
        format = path_parts[-1]
    else:
        format = "wav"
    track = AudioSegment.from_file(
        os.path.expanduser(path), format=format)
    return track

def chop(audio, bpm, bars, beats=4):
    bar_ms = calc.bpm(bpm).beat_ms * beats
    total_bars = calc.count_bars(audio.duration_seconds*1000, bpm, beats)
    sections = []
    for i in range(math.ceil(total_bars / bars)):
        sections.append(audio[i * bars * bar_ms:
                              i * bars * bar_ms + bars * bar_ms])
    return sections

def sequence(slices, seq):
    return sum([slices[s] for s in seq])

def test():
    # https://soundcloud.com/pablomoretti/percussion-mantra-open-collab
    track = load_audio("~/Music/pablo-reflective-perc.wav")
    bpm = 160
    bars = 0.5
    slices = chop(track, bpm, bars)
    # parts = sum((
    #     ((67, 66) * 3 + (67, 67)) * 2,
    #     ((29, 90) * 3 + (29, 91)) * 2,
    #     ((67, 93) * 3 + (67, 94)) * 4,
    # ), ()) * 1
    #pat = list(itertools.chain(*pattern.random_twiddle(20, len(slices))))
    pat=[64, 108, 64, 108, 64, 108, 64, 108, 172, 130, 172, 130, 172, 130, 172, 130, 83, 28, 83, 28, 83, 28, 83, 28, 144, 92, 144, 92, 144, 92, 144, 92, 10, 183, 10, 183, 10, 183, 10, 183, 61, 168, 61, 168, 61, 168, 61, 168, 63, 6, 63, 6, 63, 6, 63, 6, 103, 89, 103, 89, 103, 89, 103, 89, 130, 22, 130, 22, 130, 22, 130, 22, 81, 91, 81, 91, 81, 91, 81, 91, 126, 73, 126, 73, 126, 73, 126, 73, 31, 66, 31, 66, 31, 66, 31, 66, 145, 74, 145, 74, 145, 74, 145, 74, 105, 90, 105, 90, 105, 90, 105, 90, 187, 148, 187, 148, 187, 148, 187, 148, 77, 41, 77, 41, 77, 41, 77, 41, 119, 100, 119, 100, 119, 100, 119, 100, 146, 118, 146, 118, 146, 118, 146, 118, 167, 28, 167, 28, 167, 28, 167, 28, 160, 184, 160, 184, 160, 184, 160, 184]
    print(pat)
    new_track = sequence(slices, pat)
    new_track.export("perc2.wav", format="wav")
    #play(new_track)

if __name__ == "__main__":
    test()
