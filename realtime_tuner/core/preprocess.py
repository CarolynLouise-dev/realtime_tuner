import numpy as np
from scipy.signal import butter, sosfilt

# ==============================
# FILTER DESIGN
# ==============================

def design_highpass(fs, cutoff=60, order=3):
    nyquist = fs / 2
    return butter(order, cutoff / nyquist, btype="highpass", output="sos")

def design_bandpass(fs, low=70, high=500, order=4):
    nyquist = fs / 2
    return butter(order, [low/nyquist, high/nyquist], btype="bandpass", output="sos")

# ==============================
# INITIALIZE FILTERS
# ==============================

FS = 44100

HIGHPASS_FILTER = design_highpass(FS, 60)
BANDPASS_FILTER = design_bandpass(FS, 70, 500)

# ==============================
# SIGNAL UTILITIES
# ==============================

def remove_dc(frame):
    """Loại bỏ DC offset"""
    return frame - np.mean(frame)

def energy(frame):
    """Tính năng lượng tín hiệu"""
    return np.mean(frame ** 2)

def rms(frame):
    return np.sqrt(np.mean(frame ** 2))

def adaptive_noise_gate(frame, noise_floor=None, ratio=2.5):
    """
    Noise gate thích ứng theo môi trường
    """
    if noise_floor is None:
        noise_floor = np.median(np.abs(frame))

    threshold = noise_floor * ratio

    if rms(frame) < threshold:
        return None

    return frame

def apply_hanning(frame):
    """Windowing để giảm spectral leakage"""
    return frame * np.hanning(len(frame))

# ==============================
# MAIN PREPROCESSOR
# ==============================

def preprocess(frame, fs=FS):

    if frame is None or len(frame) == 0:
        return None

    # 1. Remove DC offset
    frame = remove_dc(frame)

    # 2. High-pass filter (remove rumble, fan noise)
    frame = sosfilt(HIGHPASS_FILTER, frame)

    # 3. Band-pass filter (focus instrument frequency)
    frame = sosfilt(BANDPASS_FILTER, frame)

    # 4. Energy check (skip silent frames)
    if energy(frame) < 1e-6:
        return None

    # 5. Adaptive noise gate
    frame = adaptive_noise_gate(frame)

    if frame is None:
        return None

    # 6. Windowing before FFT
    frame = apply_hanning(frame)

    return frame