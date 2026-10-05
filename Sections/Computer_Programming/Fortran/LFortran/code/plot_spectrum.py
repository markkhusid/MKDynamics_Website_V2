"""Draw the LFortran DFFT figures and check them against NumPy.

Reads the time and spectrum files written by the notebooks, compares the
Fortran magnitude and phase with numpy.fft.rfft, and writes the PNG files
the pages show. The text files are authoring scratch and are removed after
the check.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
IMAGES = ROOT / "images"
TOLERANCE = 1e-6
PHASE_TOLERANCE = 1e-3
PEAK_THRESHOLD = 0.05

CASES = (
    {
        "stem": "sine_10_hz",
        "sample_rate": 1024.0,
        "time_span": 0.2,
        "frequency_max": 40.0,
        "time_title": "10 Hz sine",
        "spectrum_title": "Magnitude spectrum of a 10 Hz sine",
        "phase_title": "Phase spectrum of a 10 Hz sine",
    },
    {
        "stem": "sine_50_hz",
        "sample_rate": 4096.0,
        "time_span": 0.06,
        "frequency_max": 150.0,
        "time_title": "50 Hz sine",
        "spectrum_title": "Magnitude spectrum of a 50 Hz sine",
        "phase_title": "Phase spectrum of a 50 Hz sine",
    },
    {
        "stem": "square_1_hz",
        "sample_rate": 1024.0,
        "time_span": 1.0,
        "frequency_max": 40.0,
        "time_title": "1 Hz square wave",
        "spectrum_title": "Magnitude spectrum of a 1 Hz square wave",
        "phase_title": "Phase spectrum of a 1 Hz square wave",
    },
    {
        "stem": "two_sines",
        "sample_rate": 2048.0,
        "time_span": 0.04,
        "frequency_max": 200.0,
        "time_title": "50 Hz and 100 Hz sines",
        "spectrum_title": "Magnitude spectrum of two sines",
        "phase_title": "Phase spectrum of two sines",
    },
    {
        "stem": "switched_sine_1_khz",
        "sample_rate": 16384.0,
        "time_span": 0.004,
        "frequency_max": 3000.0,
        "time_title": "1 kHz sine gated at 500 Hz",
        "spectrum_title": "Magnitude spectrum of a gated 1 kHz sine",
        "phase_title": "Phase spectrum of a gated 1 kHz sine",
    },
)


def load_columns(path):
    data = np.loadtxt(path)
    if data.ndim == 1:
        data = data.reshape(1, -1)
    return data


def numpy_spectrum(samples, sample_rate):
    count = samples.size
    transformed = np.fft.rfft(samples)
    magnitude = np.abs(transformed) / count
    if magnitude.size > 2:
        magnitude[1:-1] *= 2.0
    phase = np.degrees(np.angle(transformed))
    frequency = np.fft.rfftfreq(count, d=1.0 / sample_rate)
    return frequency, magnitude, phase


def wrapped_degrees(difference):
    return (difference + 180.0) % 360.0 - 180.0


def check_case(case):
    time_path = ROOT / f"{case['stem']}_time.dat"
    spectrum_path = ROOT / f"{case['stem']}_spectrum.dat"
    time = load_columns(time_path)
    spectrum = load_columns(spectrum_path)
    samples = time[:, 1]
    sample_rate = case["sample_rate"]
    expected_time = np.arange(samples.size) / sample_rate
    if not np.allclose(time[:, 0], expected_time, atol=TOLERANCE, rtol=0.0):
        raise SystemExit(f"{case['stem']}: time axis does not match the sample rate")

    if spectrum.shape[1] < 3:
        raise SystemExit(f"{case['stem']}: spectrum file needs frequency, magnitude, and phase")
    frequency, magnitude, phase = numpy_spectrum(samples, sample_rate)
    if spectrum.shape[0] != magnitude.size:
        raise SystemExit(f"{case['stem']}: spectrum length {spectrum.shape[0]} != {magnitude.size}")
    if not np.allclose(spectrum[:, 0], frequency, atol=TOLERANCE, rtol=0.0):
        raise SystemExit(f"{case['stem']}: frequency axis disagrees with NumPy")
    if not np.allclose(spectrum[:, 1], magnitude, atol=TOLERANCE, rtol=0.0):
        worst = np.max(np.abs(spectrum[:, 1] - magnitude))
        raise SystemExit(f"{case['stem']}: magnitude disagrees with NumPy by {worst}")
    peaks = magnitude >= PEAK_THRESHOLD
    if np.any(peaks):
        phase_error = np.max(np.abs(wrapped_degrees(spectrum[peaks, 2] - phase[peaks])))
        if phase_error > PHASE_TOLERANCE:
            raise SystemExit(f"{case['stem']}: phase disagrees with NumPy by {phase_error} degrees")
    return time, spectrum


def draw_case(case, time, spectrum):
    IMAGES.mkdir(parents=True, exist_ok=True)
    time_mask = time[:, 0] <= case["time_span"]
    frequency_mask = spectrum[:, 0] <= case["frequency_max"]

    figure, axis = plt.subplots(figsize=(7.2, 3.4))
    axis.plot(time[time_mask, 0], time[time_mask, 1], color="#1f4e79", linewidth=1.1)
    axis.set_title(case["time_title"])
    axis.set_xlabel("Time [s]")
    axis.set_ylabel("Amplitude")
    axis.grid(True, color="#d0d7de", linewidth=0.6)
    figure.tight_layout()
    figure.savefig(IMAGES / f"{case['stem']}_time.png", dpi=140)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7.2, 3.4))
    axis.plot(
        spectrum[frequency_mask, 0],
        spectrum[frequency_mask, 1],
        color="#9a3412",
        linewidth=1.1,
    )
    axis.set_title(case["spectrum_title"])
    axis.set_xlabel("Frequency [Hz]")
    axis.set_ylabel("Magnitude")
    axis.grid(True, color="#d0d7de", linewidth=0.6)
    figure.tight_layout()
    spectrum_path = IMAGES / f"{case['stem']}_spectrum.png"
    figure.savefig(spectrum_path, dpi=140)
    plt.close(figure)

    phase_mask = frequency_mask & (spectrum[:, 1] >= PEAK_THRESHOLD)
    figure, axis = plt.subplots(figsize=(7.2, 3.4))
    axis.axhline(0.0, color="#d0d7de", linewidth=0.8)
    axis.plot(
        spectrum[phase_mask, 0],
        spectrum[phase_mask, 2],
        color="#0f766e",
        marker="o",
        linestyle="none",
        markersize=5,
    )
    axis.set_xlim(0.0, case["frequency_max"])
    axis.set_ylim(-190.0, 190.0)
    axis.set_title(case["phase_title"])
    axis.set_xlabel("Frequency [Hz]")
    axis.set_ylabel("Phase [deg]")
    axis.grid(True, color="#d0d7de", linewidth=0.6)
    figure.tight_layout()
    figure.savefig(IMAGES / f"{case['stem']}_phase.png", dpi=140)
    plt.close(figure)

    if case["stem"] == "sine_10_hz":
        figure_copy = IMAGES / "lfortran_dfft.png"
        figure_copy.write_bytes(spectrum_path.read_bytes())


def main():
    for case in CASES:
        time, spectrum = check_case(case)
        draw_case(case, time, spectrum)
        (ROOT / f"{case['stem']}_time.dat").unlink()
        (ROOT / f"{case['stem']}_spectrum.dat").unlink()
        print(f"checked {case['stem']}")


if __name__ == "__main__":
    sys.exit(main())
