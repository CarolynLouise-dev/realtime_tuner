import numpy as np

NOTE_NAMES = [
"C","C#","D","D#","E","F",
"F#","G","G#","A","A#","B"
]


def note_to_freq(note):

    name = note[:-1]
    octave = int(note[-1])

    idx = NOTE_NAMES.index(name)

    midi = idx + (octave + 1) * 12

    return 440 * (2 ** ((midi - 69) / 12))


def compare_pitch(pitch, target_note):

    target_freq = note_to_freq(target_note)

    cents = 1200 * np.log2(pitch / target_freq)

    status = "in tune"

    if cents > 5:
        status = "tone down"

    elif cents < -5:
        status = "tone up"

    return cents, status