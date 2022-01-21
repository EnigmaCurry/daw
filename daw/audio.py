import uuid
import time
import os
import io
import wave
from pydub import AudioSegment
from pydub.playback import play as pydub_play

class AudioFormatException(Exception):
    pass

def load_audio(path: str) -> AudioSegment:
    path_parts = path.split(".")
    if len(path_parts) > 1:
        format = path_parts[-1]
    else:
        format = "wav"
    track = AudioSegment.from_file(
        os.path.expanduser(path), format=format)
    return track

def play(audio: AudioSegment):
    print("Playing: ",time.strftime('%H:%M:%S', time.gmtime(audio.duration_seconds)))
    pydub_play(audio)

def save_audio(audio, directory, prefix=""):
    date = time.strftime("%y-%m-%d")
    rnd_str = str(uuid.uuid1())[:5]
    prefix = f"-{prefix}-" if len(prefix) else "-"
    path = os.path.join(directory, f"{date}{prefix}{rnd_str}.wav")
    path_parts = path.split(".")
    if len(path_parts) > 1:
        format = path_parts[-1]
    else:
        raise AudioFormatException('Must specify format in file extension.')
    audio.export(os.path.expanduser(path), format=format)
    print(f"Saved {path}")

def stretch(audio: AudioSegment, factor):
    orig_frame_rate = audio.frame_rate
    b = io.BytesIO()
    audio.export(b, format="wav")
    b.seek(0)
    w = wave.open(b, 'rb')
    rate = w.getframerate()
    channels = w.getnchannels()
    sample_width = w.getsampwidth()
    num_frames = w.getnframes()
    audio = w.readframes(num_frames)
    b.close()

    frame_rate = int(rate/factor)
    b2 = io.BytesIO()
    w2 = wave.open(b2, 'wb')
    w2.setnchannels(channels)
    w2.setsampwidth(sample_width)
    w2.setframerate(frame_rate)
    w2.writeframes(audio)
    w2.close()
    b2.seek(0)

    a = AudioSegment.from_file(b2, format="wav", frame_rate=frame_rate,
                                  channels=channels, sample_width=sample_width)
    b2.close()
    a = a.set_frame_rate(orig_frame_rate)
    return a
