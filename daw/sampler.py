import time
import math
import re
import sys
import os
from .audio import load_audio, play

note_pattern = re.compile("([A-G]#?)(-?[0-9])")
note_names = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

import logging

logger = logging.getLogger(__name__)


class NoteParseError(Exception):
    pass


class ChromaticGapError(Exception):
    pass


def load_samples(
    directory,
    regex=None,
    chromatic=False,
    convert_16=False,
    limit=sys.maxsize,
    offset=0,
    choose=None,
):
    """
    Load all the .wav files in the given directory

    if chromatic==True, assert that files have chromatic key names
    if convert_16==True, convert input files to pcm_s16le
    limit will limit the number of files loaded
    offset will skip the first n files
    choose is a direct list of note names desired, ignoring limit and offset
    """
    samples = {}
    if regex is not None:
        if getattr(regex, "match", None) is None:
            regex = re.compile(regex)
        files = sorted([f for f in os.listdir(directory) if regex.match(f)])
    else:
        files = sorted([f for f in os.listdir(directory) if f.lower().endswith(".wav")])

    def log_file_details(wav, audio, key=""):
        logger.info(
            f"Loaded sample: '{key}' {time.strftime('%H:%M:%S', time.gmtime(audio.duration_seconds))}"
            f" ({audio.duration_seconds:.3f} seconds) ({os.path.basename(wav)})"
        )

    if choose is not None:
        logger.info(f"Loading {len(choose)} samples from {directory} ... ")
        note_files = {
            k: v
            for k, v in [
                (f'{x["note"]}{x["octave"]}', x) for x in order_names_chromatic(files)
            ]
        }
        for note in choose:
            wav = os.path.join(directory, note_files[note]["name"])
            s = samples[note] = load_audio(wav, convert_16=convert_16)
            log_file_details(wav, s, key=note)
    elif chromatic:
        note_files = order_names_chromatic(files)[offset : offset + limit]
        files = [f["name"] for f in note_files]
        logger.info(f"Loading {len(files)} samples from {directory} ... ")
        for wav in files:
            note, octave = parse_note(wav)
            key = f"{note}{octave}"
            s = samples[key] = load_audio(
                os.path.join(directory, wav), convert_16=convert_16
            )
            log_file_details(wav, s, key)

        ## Check for gaps:
        for ((note, octave), f) in zip(
            chromatic_seq(
                (note_files[0]["note"], note_files[0]["octave"]),
                (note_files[-1]["note"], note_files[-1]["octave"]),
            ),
            note_files,
        ):
            if f["note"] != note or f["octave"] != octave:
                raise ChromaticGapError(
                    f"{directory} - Missing note file: {note}{octave}"
                )
    else:
        files = files[offset : offset + limit]
        logger.info(f"Loading {len(files)} samples from {directory} ... ")
        for wav in files:
            s = samples[wav] = load_audio(
                os.path.join(directory, wav), convert_16=convert_16
            )
            log_file_details(wav, s, key=os.path.basename(wav))

    return samples


def chromatic_seq(start=("C", 0), end=("C", 6)):
    """
    Generate the full chromatic sequence of note tuples from start to end.

    >>> list(chromatic_seq(('G', 3), ('A#', 4)))
    [('G', 3), ('G#', 3), ('A', 4), ('A#', 4)]
    """
    if type(start) == str:
        start = parse_note(start)
    if type(end) == str:
        end = parse_note(end)
    note = start
    yield note
    while note_names.index(note[0]) < note_names.index(end[0]) or note[1] < end[1]:
        if note[0] == "G#":
            note = ("A", note[1] + 1)
        else:
            note = (note_names[note_names.index(note[0]) + 1], note[1])
        yield note


def note_span(start="C0", end="C6"):
    """
    Generate the full chromatic sequence of note names from start to end

    >>> list(chromatic_seq('G3', 'A#4'))
    ['G3', 'G#3', 'A4', 'A#4']
    """
    return [f"{note}{octave}" for note, octave in chromatic_seq(start, end)]


def parse_note(string):
    """
    Parse a note value from a freeform string.

    >>> parse_note('cool sample C#3.wav')
    ('C#', 3)

    Returns a tuple (note: str, octave: int)
    """
    m = note_pattern.search(string)
    if not m:
        raise NoteParseError(f"Could not parse a note value: {string}")
    return (m.groups()[0], int(m.groups()[1]))


def order_names_chromatic(names):
    """
    Order a list of sample names, looking for a chromatic key name (eg. C#3)

    >>> order_names_chromatic(('C#3','D#5','D4','B2'))
    [{'name': 'B2', 'note': 'B', 'octave': 2}, {'name': 'C#3', 'note': 'C#', 'octave': 3}, {'name': 'D4', 'note': 'D', 'octave': 4}, {'name': 'D#5', 'note': 'D#', 'octave': 5}]
    """
    return sorted(
        [
            {"name": name, "note": parsed_note[0], "octave": parsed_note[1]}
            for name, parsed_note in [(name, parse_note(name)) for name in names]
        ],
        key=lambda n: (n["octave"], n["note"]),
    )


def apply_to_samples(samples, func):
    return {key: func(audio, key) for key, audio in samples.items()}
