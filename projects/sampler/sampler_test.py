import os
from daw.sampler import load_samples, note_span, apply_to_samples
from daw.effects import adsr
from daw.audio import load_audio, play, stretch, AudioSegment

wasp_root = "/daw/samples/Samples From Mars/Wasp From Mars/WAV"
sid_root = "/daw/samples/Samples From Mars/sid_from_mars/Sid From Mars/WAV"

# saws_samples = load_samples(os.path.join(wasp_root, '2SAWS'), chromatic=True, convert_16=True, limit=12, offset=12)
# saws_samples = load_samples(os.path.join(wasp_root, '2SAWS'), convert_16=True,
#                             choose=note_span("C1","C2"))

# hold =240000

# saws_C1 = adsr(saws_samples['C1'], attack=1646, decay=5317-1646, sustain=-10, release=3000, hold=hold, loop_length=3698)

# saws_C2 = adsr(saws_samples['C2'], attack=2000, decay=3795-2000, sustain=-10, release=3000, hold=hold, loop_length=9002-3795)


# clip = AudioSegment.silent(duration=hold)
# clip = clip.overlay(saws_C1)
# clip = clip.overlay(saws_C2, position=9000)
# clip += 5
# play(clip)

###########
# hold = 2050
# bards_tale = load_samples(
#     os.path.join(sid_root, "Leads/Bard'sTale"),
#     regex=".*_Bard'sTale_Sid_[A-G]#?[0-9].wav",
#     convert_16=True,
#     choose=note_span("A5", "G#5"),
# )
# bards_tale_b = apply_to_samples(
#     bards_tale,
#     lambda a: adsr(
#         a, attack=92, decay=0, sustain=0, release=2000, loop_length=300 - 92, hold=hold
#     ),
# )
# clip = stretch(bards_tale_b["G5"], 4) + 20
# clip = clip
# play(clip)


alter_ego = load_samples(
    os.path.join(sid_root, "Leads/AlterEgoMaleVersion/"),
    chromatic=True,
    convert_16=True,
    choose=note_span("C4", "C5"),
)

alter_ego_b = apply_to_samples(
    alter_ego,
    lambda audio, note: adsr(
        audio,
        attack=269,
        decay=2000,
        sustain=-12,
        release=3000,
        loop_length=3000,
        hold=6000,
    ),
)


play(alter_ego_b["C4"])
