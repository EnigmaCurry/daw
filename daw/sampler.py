import math
import re
import os
from .audio import load_audio, play

note_pattern = re.compile('([A-G]#?)(-?[0-9])')
note_names = ['A','A#','B','C','C#','D','D#', 'E','F','F#','G','G#']

import logging
logger = logging.getLogger(__name__)

class NoteParseError(Exception):
    pass
class ChromaticGapError(Exception):
    pass

def load_samples(directory, chromatic=False):
    """
    Load all the .wav files in the given directory

    if chromatic==True, assert that files have chromatic key names
    """
    samples={}
    files = sorted([f for f in os.listdir(directory) if f.lower().endswith('.wav')])
    logger.info(f"Loading {len(files)} samples from {directory} ... ")
    if chromatic:
        note_files = order_names_chromatic(files)
        files = [f['name'] for f in note_files]
    for wav in files:
        if chromatic:
            note, octave = parse_note(wav)
            samples[f"{note}{octave}"] = load_audio(os.path.join(directory,wav))
        else:
            samples[wav] = load_audio(os.path.join(directory,wav))

    ## Check for gaps:
    if chromatic:
        for ((note, octave), f) in zip(chromatic_seq((note_files[0]['note'], note_files[0]['octave']),
                                              (note_files[-1]['note'], note_files[-1]['octave'])),
                                note_files):
            if f['note'] != note or f['octave'] != octave:
                #raise ChromaticGapError(f"{directory} - Missing note file: {note}{octave}")
                pass
    return samples

def chromatic_seq(start=('C', 0), end=('C', 6)):
    """
    Generate the full chromatic sequence of notes from start to end.

    >>> list(chromatic_seq(('G', 3), ('A#', 4)))
    [('G', 3), ('G#', 3), ('A', 4), ('A#', 4)]
    """
    note = start
    yield note
    while note_names.index(note[0]) < note_names.index(end[0]) \
          or note[1] < end[1]:
        if note[0] == 'G#':
            note = ('A', note[1]+1)
        else:
           note = (note_names[note_names.index(note[0])+1], note[1])
        yield note

def parse_note(string):
    """
    Parse a note value from a freeform string.

    >>> parse_note('cool sample C#3.wav')
    ('C#', 3)

    Returns a tuple (note: str, octave: int)
    """
    m = note_pattern.search(string)
    if not m:
        raise NoteParseError(f'Could not parse a note value: {string}')
    return (m.groups()[0], int(m.groups()[1]))

def order_names_chromatic(names):
    """
    Order a list of sample names, looking for a chromatic key name (eg. C#3)

    >>> order_names_chromatic(('C#3','D#5','D4','B2'))
    [{'name': 'B2', 'note': 'B', 'octave': 2}, {'name': 'C#3', 'note': 'C#', 'octave': 3}, {'name': 'D4', 'note': 'D', 'octave': 4}, {'name': 'D#5', 'note': 'D#', 'octave': 5}]
    """
    return sorted([{'name': name, 'note': parsed_note[0], 'octave': parsed_note[1]} \
                     for name, parsed_note in [(name, parse_note(name)) for name in names]],
                    key=lambda n: (n['octave'], n['note']))

def adsr(audio, attack, decay, sustain, release, loop_length=float("inf"), hold=0):
    """
    Render audio sample with a linear ADSR applied to the output volume.

    attack, decay, release, loop_length, and hold are in terms of milliseconds.
    sustain is in terms of relative gain in dB. So usually 0 or a negative number.
    loop_length is the length of the sustain portion of the input clip.
    hold is the output length for the attack+decay+sustain in milliseconds.
    (sustain will loop if longer than loop_length).
    """
    
    attack_part = audio[:attack].fade(from_gain=-120, duration=attack, start=0)
    decay_part = audio[attack:attack+decay].fade(from_gain=0, to_gain=sustain, duration=decay, end=float("inf"))
    sustain_part = audio[(attack+decay):(attack+decay+loop_length)] + sustain
    hold -= attack + decay
    if hold > sustain_part.duration_seconds * 1000:
        sustain_part = (sustain_part * math.ceil(hold / (sustain_part.duration_seconds * 1000)))[:hold]
    else:
        sustain_part = sustain_part[:hold]
    if loop_length == 0:
        offset = attack+decay
    else:
        offset = (hold % loop_length) + attack + decay
    release_part = audio[offset:offset+release].fade(from_gain=sustain, to_gain=-120, duration=release, end=float("inf"))
    return attack_part + decay_part + sustain_part + release_part

