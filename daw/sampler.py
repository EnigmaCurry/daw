import re
import os
from .audio import load_audio, play

note_pattern = re.compile('([A-G]#?)(-?[0-9])')
note_names = ['A','A#','B','C','C#','D','D#', 'E','F','F#','G','G#']

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
    print(f"Loading {len(files)} samples from {directory} ... ")
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
    m = note_pattern.search(string)
    if not m:
        raise NoteParseError(f'Could not parse a note value: {string}')
    return (m.groups()[0], int(m.groups()[1]))

def order_names_chromatic(names):
    """
    Order a list of sample names, looking for a chromatic key name (eg. C#3)
    """
    return sorted([{'name': name, 'note': parsed_note[0], 'octave': parsed_note[1]} \
                     for name, parsed_note in [(name, parse_note(name)) for name in names]],
                    key=lambda n: (n['octave'], n['note']))
