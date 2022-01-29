import os
from daw.sampler import load_samples

sample_root = '/app/samples/Samples From Mars/extracted/Wasp From Mars'
samples = load_samples(os.path.join(sample_root, '2SAWS'), chromatic=True)
print(samples)
