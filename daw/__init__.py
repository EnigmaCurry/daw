import logging

import os
from . import chop, audio, sampler, effects

logging.basicConfig(level=os.getenv("DAW_LOG_LEVEL", "INFO").upper())
