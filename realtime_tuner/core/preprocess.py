import numpy as np
from scipy.signal import butter, sosfilt

def pre_emphasis(signal, coeff=0.95):
    """Tăng cường tần số cao để giữ độ chi tiết của giọng nói"""
    return np.append(signal[0], signal[1:] - coeff * signal[:-1])

def get_bandpass_sos(fs=44100, low=80, high=1200):
    """Tạo bộ lọc Second-Order Sections (SOS) - ổn định hơn lfilter"""
    nyquist = fs / 2
    # Sử dụng bậc 5 hoặc 6 để cắt sắc hơn nếu cần
    sos = butter(5, [low/nyquist, high/nyquist], btype='band', output='sos')
    return sos

def noise_gate_professional(frame, threshold=0.02, attack=0.1):
    """
    Lọc nhiễu nền dựa trên năng lượng RMS.
    Nếu năng lượng thấp hơn ngưỡng, sẽ làm mờ dần (fade) thay vì cắt xoẹt.
    """
    rms = np.sqrt(np.mean(frame**2))
    if rms < threshold:
        return frame * attack # Giảm âm lượng thay vì trả về None để tránh mất frame
    return frame

def apply_hanning(frame):
    """Áp dụng cửa sổ Hanning để giảm nhiễu rò rỉ phổ"""
    return frame * np.hanning(len(frame))

def normalize(frame):
    """Đảm bảo biên độ không vượt quá giới hạn âm thanh số"""
    max_val = np.max(np.abs(frame))
    if max_val > 0:
        return frame / max_val
    return frame

# Khởi tạo bộ lọc một lần duy nhất để tiết kiệm tài nguyên
SOS_FILTER = get_bandpass_sos()

def preprocess(frame, fs=44100):
    if frame is None or len(frame) == 0:
        return None

    # 1. Pre-emphasis: Làm "sáng" giọng nói
    frame = pre_emphasis(frame)

    # 2. Noise Gate: Loại bỏ đoạn tĩnh (nhiễu nền cực thấp)
    frame = noise_gate_professional(frame, threshold=0.01)

    # 3. Bandpass Filter: Chỉ giữ lại dải tần giọng người (80Hz - 1200Hz)
    # Dùng sosfilt để tránh méo tín hiệu
    frame = sosfilt(SOS_FILTER, frame)

    # 4. Windowing: Hanning window (nên dùng nếu bạn chuẩn bị đưa vào mô hình AI/FFT)
    frame = apply_hanning(frame)

    # 5. Normalization: Chuẩn hóa lại âm lượng
    frame = normalize(frame)

    return frame