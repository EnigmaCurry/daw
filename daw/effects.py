import math
import logging
from pydub import AudioSegment

logger = logging.getLogger(__name__)


def adsr(
    audio,
    attack,
    decay,
    sustain,
    release,
    loop_length=float("inf"),
    hold=0,
    loop_mode="loop",
    offset=0,
):
    """
    Render audio sample with a linear ADSR envelope applied to the output volume.

    attack, decay, release, loop_length, and hold are in terms of milliseconds.
    sustain is in terms of relative gain in dB. So usually 0 or a negative number.
    loop_length is the length of the sustain portion of the input clip.
    hold is the output length for the attack+decay+sustain in milliseconds.
    (sustain will loop if longer than loop_length).
    """
    if offset > 0:
        audio = audio[offset:]
    if attack == 0:
        attack_part = AudioSegment.empty()
    else:
        attack_part = audio[:attack].fade(from_gain=-120, duration=attack, start=0)
    if decay == 0:
        decay_part = AudioSegment.empty()
    else:
        decay_part = audio[attack : attack + decay].fade(
            from_gain=0, to_gain=sustain, duration=decay, end=float("inf")
        )
    sustain_part = audio[(attack + decay) : (attack + decay + loop_length)] + sustain
    hold = max(hold - attack - decay, 0)

    if hold > sustain_part.duration_seconds * 1000:
        if loop_mode == "ping_pong":
            sustain_part = (
                (sustain_part + sustain_part.reverse())
                * (math.ceil(hold / (sustain_part.duration_seconds * 1000) / 2))
            )[:hold]
        elif loop_mode == "loop":
            sustain_part = (
                sustain_part
                * (math.ceil(hold / (sustain_part.duration_seconds * 1000)))
            )[:hold]
        else:
            raise AssertionError(f"Unknown loop mode: {loop_mode}")
    else:
        sustain_part = sustain_part[:hold]

    if loop_length == 0:
        release_offset = attack + decay
    else:
        release_offset = (hold % loop_length) + attack + decay
    if release == 0:
        release_part = AudioSegment.empty()
    else:
        release_part = audio[release_offset : release_offset + release].fade(
            from_gain=sustain, to_gain=-120, duration=release, end=float("inf")
        )

    logger.debug(
        f"ADSR: attack:{attack_part.duration_seconds:.3f} "
        f"+ decay:{decay_part.duration_seconds:.3f} "
        f"+ sustain:{sustain_part.duration_seconds:.3f}@{sustain}dB "
        f"+ release:{release_part.duration_seconds:.3f}"
    )
    return attack_part + decay_part + sustain_part + release_part
