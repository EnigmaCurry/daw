import os
import math
import random
from pydub import AudioSegment
from pydub.playback import play

import calc

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
    track = load_audio("~/Music/pablo-reflective-perc.wav")
    bpm = 160
    bars = 0.5
    slices = chop(track, bpm, bars)
    parts = sum((
        ((67, 66) * 3 + (67, 67)) * 2,
        ((29, 90) * 3 + (29, 91)) * 2,
        ((67, 93) * 3 + (67, 94)) * 4,
    ), ()) * 1
    new_track = sequence(slices, parts)
    new_track.export("perc.wav", format="wav")

if __name__ == "__main__":
    test()
