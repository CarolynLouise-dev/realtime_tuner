from .yin import *
from collections import deque
import numpy as np

pitch_history = deque(maxlen=7)

def smooth_pitch(pitch):

    pitch_history.append(pitch)

    return np.median(pitch_history)


def detect_pitch(signal, fs=44100):

    d = difference_function(signal)

    cmnd = cumulative_mean_normalized(d)

    tau = absolute_threshold(cmnd)

    if tau is None:
        return None

    tau = parabolic_interpolation(cmnd, tau)

    pitch = fs / tau
    if pitch < 70 or pitch > 1000:
        return None

    pitch = smooth_pitch(pitch)

    return pitch