import os
import math
import random
import itertools
import time
import uuid
from pydub import AudioSegment
from pydub.playback import play as pydub_play
from pydub.exceptions import TooManyMissingFrames

import calc
import pattern

class AudioFormatException(Exception):
    pass

def load_audio(path):
    path_parts = path.split(".")
    if len(path_parts) > 1:
        format = path_parts[-1]
    else:
        format = "wav"
    track = AudioSegment.from_file(
        os.path.expanduser(path), format=format)
    return track

def save_audio(audio, path):
    path_parts = path.split(".")
    if len(path_parts) > 1:
        format = path_parts[-1]
    else:
        raise AudioFormatException('Must specify format in file extension.')
    audio.export(os.path.expanduser(path), format=format)
    print(f"Saved {path}")

def play(audio):
    print("playing ... ")
    pydub_play(audio)

def chop(audio, bpm, bars, beats=4, fade_in=0, fade_out=0):
    segment_ms = round(calc.bpm(bpm).beat_ms * beats * bars)
    total_bars = calc.count_bars(audio.duration_seconds*1000, bpm, beats)
    total_segments = math.ceil(total_bars / bars)
    print(f"Chopping audio: {segment_ms}ms * {total_segments}, fade_in={fade_in}")
    sections = []
    for i in range(total_segments):
        offset = fade_in if i > 0 else 0
        sections.append(audio[(i * segment_ms) - offset:
                              (i * segment_ms + segment_ms)])
        if fade_out != 0:
            sections[i] = sections[i].fade_out(fade_out)
    return sections

def reduce_slices(slices):
    def chunks(lst, n):
        for i in range(0,len(lst), n):
            yield lst[i:i+n]
    def reduce(slices):
        new_slices = []
        for slice_pair in chunks(slices, 2):
            if len(slice_pair) > 1:
                new_slices.append(slice_pair[0] + slice_pair[1])
            else:
                new_slices.append(slice_pair[0])
        if len(new_slices) == 1:
            return new_slices
        else:
            return reduce(new_slices)
    print(f"Reducing {len(slices)} slices into one audio segment ...")
    return reduce(slices)[0]

def sequence(slices, seq, fade_in=0):
    print(f"Sequencing {len(seq)} segments ...")
    # Overlay the segments:
    last_slice = slices[0]
    seq_slices = [slices[i] for i in seq]
    mix_slices = []
    for i, (s, s2) in enumerate(zip(seq_slices, seq_slices[1:-1] + [seq_slices[0]])):
        if fade_in > 0 and i > 0:
            pos = len(s) - fade_in
            if len(s) > 0:
                try:
                    s = s.overlay(s2, position=pos)
                except TooManyMissingFrames:
                    break
        mix_slices.append(s)
        last_slice = s
    new_audio = reduce_slices(mix_slices[:3000])
    return new_audio

def test():
    track = load_audio("~/Music/the city - myrcury.wav")
    bpm = 147
    date = time.strftime("%y-%m-%d")
    rnd_str = str(uuid.uuid1())[:5]
    out_format="mp3"
    out_filename=f"{date}-chop.{rnd_str}.{out_format}"

    bars = 0.0625
    fade_in = 1
    fade_out = int(20 * bpm * bars)
    slices = chop(track, bpm, bars, fade_in=fade_in, fade_out=fade_out)
    num_slices = len(slices)
    pat = list(range(num_slices))
    pat = list(itertools.chain(*pat))
    pat = pat[:-32]
    new_track = sequence(slices, pat, fade_in)
    new_track.overlay(new_track.invert_phase(), position=10)
    #save_audio(new_track, "~/Music/21-11-01.e.the-city.chop.wav")
    play(new_track)

if __name__ == "__main__":
    test()
