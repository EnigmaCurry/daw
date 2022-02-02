from collections import namedtuple
import uuid
import time
import os
import io
import wave
from pydub import AudioSegment
from pydub.effects import pan
import simpleaudio
import subprocess
import tempfile

import logging

logger = logging.getLogger(__name__)


class AudioFormatException(Exception):
    pass


def load_audio(path: str, convert_16=False) -> AudioSegment:
    path_parts = path.split(".")
    if len(path_parts) > 1:
        format = path_parts[-1]
    else:
        format = "wav"
        path = os.path.expanduser(path)
    if convert_16:
        ## Convert to 16 bit .wav before trying to load it
        tmp_wav = tempfile.mktemp(prefix="convert_", suffix=".wav")
        try:
            logger.debug("Converting sample to pcm_s16le")
            p = subprocess.run(
                ["ffmpeg", "-i", path, "-acodec", "pcm_s16le", tmp_wav],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            logger.error(p.stdout)
            raise e
        try:
            track = AudioSegment.from_file_using_temporary_files(tmp_wav, format=format)
        finally:
            try:
                os.unlink(tmp_wav)
            except FileNotFoundError:
                pass
    else:
        track = AudioSegment.from_file(path, format=format)
    return track


def play(audio: AudioSegment, stop_flag):
    logger.info(
        f"Playing: {time.strftime('%H:%M:%S', time.gmtime(audio.duration_seconds))}"
        f" ({audio.duration_seconds} seconds)"
    )
    s = simpleaudio.play_buffer(
        audio.raw_data,
        num_channels=audio.channels,
        bytes_per_sample=audio.sample_width,
        sample_rate=audio.frame_rate,
    )
    while not stop_flag.is_set():
        time.sleep(0.5)
        if s.is_playing() == False:
            break
    logger.info("Stopped")
    s.stop()


def save_audio(audio, directory, prefix=""):
    date = time.strftime("%y-%m-%d")
    rnd_str = str(uuid.uuid1())[:5]
    prefix = f"-{prefix}-" if len(prefix) else "-"
    path = os.path.join(directory, f"{date}{prefix}{rnd_str}.wav")
    path_parts = path.split(".")
    if len(path_parts) > 1:
        format = path_parts[-1]
    else:
        raise AudioFormatException("Must specify format in file extension.")
    audio.export(os.path.expanduser(path), format=format)
    logger.info(f"Saved {path}")


def stretch(audio: AudioSegment, factor):
    orig_frame_rate = audio.frame_rate
    b = io.BytesIO()
    audio.export(b, format="wav")
    b.seek(0)
    w = wave.open(b, "rb")
    rate = w.getframerate()
    channels = w.getnchannels()
    sample_width = w.getsampwidth()
    num_frames = w.getnframes()
    audio = w.readframes(num_frames)
    b.close()

    frame_rate = int(rate / factor)
    b2 = io.BytesIO()
    w2 = wave.open(b2, "wb")
    w2.setnchannels(channels)
    w2.setsampwidth(sample_width)
    w2.setframerate(frame_rate)
    w2.writeframes(audio)
    w2.close()
    b2.seek(0)

    a = AudioSegment.from_file(
        b2,
        format="wav",
        frame_rate=frame_rate,
        channels=channels,
        sample_width=sample_width,
    )
    b2.close()
    a = a.set_frame_rate(orig_frame_rate)
    return a


Track = namedtuple(
    "MixArgument", ("audio", "start_pos", "amplify", "pan"), defaults=(0, 0, 0)
)


def mix(*tracks, duration=0):
    if duration == 0:
        for track in tracks:
            t = track.audio.duration_seconds * 1000
            duration = t if t > duration else duration
    mixed = AudioSegment.silent(duration=duration)
    for track in tracks:
        mixed = mixed.overlay(
            pan(track.audio + track.amplify, track.pan), position=track.start_pos
        )
    return mixed
