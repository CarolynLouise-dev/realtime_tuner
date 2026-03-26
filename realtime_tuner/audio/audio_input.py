import sounddevice as sd
import numpy as np

FS = 44100
FRAME_SIZE = 2048


def get_audio_frame():

    audio = sd.rec(FRAME_SIZE, samplerate=FS, channels=1, dtype='float32')
    sd.wait()

    return audio.flatten()

