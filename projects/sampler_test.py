import os
from daw.sampler import load_samples, note_span, apply_to_samples, sampler, compose
from daw.effects import adsr
from daw.audio import load_audio, play, stretch, AudioSegment

sid_root = "/daw/samples/Samples From Mars/sid_from_mars/Sid From Mars/WAV"


def main():
    alter_ego = sampler(
        load_samples(
            os.path.join(sid_root, "Leads/AlterEgoMaleVersion/"),
            chromatic=True,
            convert_16=True,
            choose=note_span("A3", "A4"),
        ),
        attack=200,
        decay=400,
        sustain=-5,
        release=400,
        loop_length=3000,
    )

    clip = compose(alter_ego, "0....2345---6----", 500)
    clip += compose(alter_ego, "7....5432---1----", 250)
    clip = (clip + clip.reverse()) * 8
    clip = stretch(clip, 2) + 10

    return clip
