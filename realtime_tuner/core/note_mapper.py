import numpy as np

NOTE_NAMES = [
"C","C#","D","D#","E","F",
"F#","G","G#","A","A#","B"
]


def freq_to_note(freq):

    n = 12 * np.log2(freq/440) + 69

    note_number = int(round(n))

    note = NOTE_NAMES[note_number % 12]

    octave = note_number // 12 - 1

    ref_freq = 440 * 2 ** ((note_number - 69)/12)

    cents = 1200 * np.log2(freq / ref_freq)

    return f"{note}{octave}", cents

def cent_to_position(cents):

    cents = max(-50, min(50, cents))

    position = (cents + 50) / 100

    return position

