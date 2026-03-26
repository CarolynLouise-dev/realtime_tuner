from audio.audio_input import get_audio_frame
from core.preprocess import preprocess
from core.pitch import detect_pitch
from core.comparator import compare_pitch
from core.note_mapper import freq_to_note
from audio.audio_stream import start_stream, get_frame

stream = start_stream()

while True:

    frame = get_frame()

    if frame is None:
        continue

    pitch = detect_pitch(frame)
    if pitch is None:
        continue

    if pitch:

        note, cents = freq_to_note(pitch)

        print(f"{note}  {float(cents):+.2f} cents  {pitch:.2f} Hz")
        print("-----------")