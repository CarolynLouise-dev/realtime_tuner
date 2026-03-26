

# Realtime Tuner

Realtime Tuner is a Python-based application designed for real-time audio signal processing and pitch detection. It includes features such as pre-emphasis, noise gating, bandpass filtering, and pitch comparison to help users tune their instruments or analyze audio signals.

## Features

- **Pre-emphasis**: Enhances high frequencies to preserve voice details.
- **Noise Gate**: Reduces background noise dynamically based on RMS energy.
- **Bandpass Filtering**: Isolates human voice frequency range (80Hz - 1200Hz).
- **Hanning Windowing**: Reduces spectral leakage for better signal analysis.
- **Normalization**: Ensures audio amplitude stays within digital limits.
- **Pitch Detection**: Converts frequency to musical notes with cent deviation.
- **Pitch Comparison**: Compares detected pitch with a target note and provides tuning suggestions.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/realtime_tuner.git
   cd realtime_tuner
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   uvicorn realtime_tuner.api.server:app --reload --host 0.0.0.0 --port 8051
   ```

## Usage

### Preprocessing Audio
The `preprocess` function in `realtime_tuner/core/preprocess.py` applies a series of audio processing steps to prepare the signal for analysis.

### Frequency to Note Mapping
The `freq_to_note` function in `realtime_tuner/core/note_mapper.py` converts a frequency to its corresponding musical note and cent deviation.

### Pitch Comparison
The `compare_pitch` function in `realtime_tuner/core/comparator.py` compares a detected pitch with a target note and provides tuning feedback.

## API Endpoints

The application includes an API server for real-time interaction. Example endpoints:
- `/process_audio`: Accepts audio frames and returns processed data.
- `/detect_pitch`: Detects pitch and maps it to a musical note.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Built with Python, NumPy, and SciPy.
- Inspired by real-time audio processing and tuning applications.
