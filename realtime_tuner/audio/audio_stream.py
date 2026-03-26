import sounddevice as sd
import numpy as np
import queue

FS = 44100
FRAME_SIZE = 2048

audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):

    if status:
        print(status)

    audio_queue.put(indata[:, 0].copy())


def start_stream():

    stream = sd.InputStream(
        samplerate=FS,
        blocksize=FRAME_SIZE,
        channels=1,
        callback=audio_callback
    )

    stream.start()

    return stream

def get_frame():

    if audio_queue.empty():
        return None

    return audio_queue.get()