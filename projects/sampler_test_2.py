import os
from daw.sampler import (
    load_samples,
    note_span,
    apply_to_samples,
    sampler,
    compose,
    make_scale,
)
from daw.effects import adsr
from daw.audio import Track, load_audio, play, mix, stretch, AudioSegment

sid_root = "/daw/samples/Samples From Mars/sid_from_mars/Sid From Mars/WAV/"


def main():
    instrument = sampler(
        make_scale(
            load_samples(
                os.path.join(sid_root, "Pads/CelestialHarmony"),
                chromatic=True,
                convert_16=True,
                choose=note_span("C4", "C7"),
            ),
            "Aeolian",
        ),
        offset=2000,
        attack=1000,
        decay=1000,
        sustain=-5,
        release=400,
        loop_length=4600,
        loop_mode="ping_pong",
    )

    a1 = Track(
        compose(instrument, [0, "-" * 120], 1000).fade_out(120000), pan=-1, amplify=-10
    )
    a2 = Track(
        compose(instrument, [3, "-" * 120], 1000).fade_out(120000), pan=0.5, amplify=-1
    )
    a3 = Track(
        compose(instrument, [7, "-" * 120], 1000).fade_out(90000),
        pan=0,
        amplify=-10,
        start_pos=16000,
    )
    a4 = Track(
        compose(instrument, ([9, "-" * 3] + [10, "-" * 3]) * 10, 1000).fade_out(10000),
        pan=-0.5,
        amplify=-10,
        start_pos=32000,
    )
    a5 = Track(
        compose(instrument, [8, "-" * 2] * 15, 1000).fade_out(10000),
        pan=0.5,
        amplify=-10,
        start_pos=0,
    )

    a = mix(a1, a2, a3, a4, a5)
    return a
