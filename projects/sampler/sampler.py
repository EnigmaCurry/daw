import os
from daw.sampler import load_samples, adsr
from daw.audio import load_audio, play

sample_root = '/daw/samples/Samples From Mars/extracted/Wasp From Mars'
#samples = load_samples(os.path.join(sample_root, '2SAWS'), chromatic=True)

c1 = load_audio(os.path.join(sample_root, '2SAWS', '36 2SAWS WASP C1.wav'), convert_16=True)
clip = adsr(c1, 2000, 2000, -12, 3000, hold=30000, loop_length=3000)
quiet = clip.apply_gain(0)

play(quiet)
