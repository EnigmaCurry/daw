import os
from daw.sampler import load_samples, adsr, note_span
from daw.audio import load_audio, play, stretch, AudioSegment

wasp_root = '/daw/samples/Samples From Mars/Wasp From Mars/WAV'
#saws_samples = load_samples(os.path.join(wasp_root, '2SAWS'), chromatic=True, convert_16=True, limit=12, offset=12)
saws_samples = load_samples(os.path.join(wasp_root, '2SAWS'), convert_16=True,
                            choose=note_span("C1","C2"))

hold =240000

wasp_2saws_C1 = adsr(saws_samples['C1'], attack=1646, decay=5317-1646, sustain=-10, release=3000, hold=hold, loop_length=3698)
wasp_2saws_C1_stretch = stretch(wasp_2saws_C1, 1.2)

clip = AudioSegment.silent(duration=hold)
clip = clip.overlay(wasp_2saws_C1)

clip += 5
play(clip)
