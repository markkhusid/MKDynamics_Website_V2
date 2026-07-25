# Sine Wave at 50 Hz

*Built with Grok Build*

## Introduction

This example demonstrates the computation of the Discretized Fourier Transform of a sine wave at **50 Hz** using the FFTW3 library in Fortran. Unlike the [10 Hz example](../Sine_Wave_10_Hz/sine_wave_10_hz.md), which generates the test signal in SciLAB, this example generates the time-domain data with **Python + NumPy** (originally in a Jupyter Notebook), then feeds that data into the Fortran 2003 DFFT program. Time- and frequency-domain results are plotted with GNUPlot (and, for the Python stage, Matplotlib).

We create a pure 50 Hz sine wave for 10 periods, sampled at 44,100 Hz. After plotting the time domain and a Python-side FFT, the raw samples are written to a text file and used as input to the Fortran DFFT code.

## Python Code to Generate a 50 Hz Sine Wave

The following script generates a 50 Hz sine wave sampled at 44,100 Hz for 10 periods, writes a WAV file and a raw text data file, and plots the waveform:

```{literalinclude} code/sine50Hz_text.py
---
language: python
---
```

### Run the Python Script

```bash
python3 sine50Hz_text.py
```

This produces:

- `sine50Hz.wav` — audio file of the tone
- `sine50Hz.dat` — one sample per line (input for the Fortran DFFT program)
- a Matplotlib time-domain plot of the waveform

### Time Domain Plot (Python / GNUPlot)

```{image} images/sine_wv_50Hz.png
:alt: 50 Hz sine wave time domain
:width: 600px
```

### Frequency Domain Plot (Python-side FFT)

```{image} images/sine_wv_50Hz_freq_domain.png
:alt: FFT of 50 Hz sine wave from Python
:width: 600px
```

## Obtaining the DFFT of the Raw Data File

The text file written by the Python script is the input to the Fortran 2003 FFTW3 program used throughout the DFFT section. The shared source is:

```{literalinclude} ../code/dfft_fftw3.f08
---
language: fortran
---
```

## Compile the Fortran 2003 Code

```bash
gfortran -o dfft_fftw3 ../code/dfft_fftw3.f08 -lfftw3
```

(Or, with the original V1-style filename and flags:)

```bash
gfortran -o a.out data_file_FFTW_ver6.F03 -lfftw3
```

## Execute the Fortran 2003 Code

```bash
./dfft_fftw3 sine50Hz.dat DFFT_mag_file.dat DFFT_phase_file.dat 44100 10
```

Arguments:

| Argument | Meaning |
|----------|---------|
| `sine50Hz.dat` | Time-domain samples from the Python script |
| `DFFT_mag_file.dat` | Output magnitude spectrum |
| `DFFT_phase_file.dat` | Output phase spectrum |
| `44100` | Sample rate (Hz) |
| `10` | Number of periods of data in the input file |

Obtain the line count of the input with:

```bash
wc -l sine50Hz.dat
```

## Visualize the DFFT Results with GNUPlot

A GNUPlot script used for this example is:

```{literalinclude} code/sine_wv_50Hz_DFFT_gnuplot_macro.txt
---
language: gnuplot
---
```

Run it with:

```bash
gnuplot -persist sine_wv_50Hz_DFFT_gnuplot_macro.txt
```

or start GNUPlot and load the script:

```bash
load 'sine_wv_50Hz_DFFT_gnuplot_macro.txt'
```

Adjust the data file name in the script if you used `DFFT_mag_file.dat` instead of `DFFT_mag_50Hz.dat`.

### DFFT Magnitude Plot (Fortran / FFTW3)

```{image} images/DFFT_sine_wv_50Hz.png
:alt: DFFT magnitude of 50 Hz sine wave
:width: 600px
```

## Discussion

There appears to be a slight decrease in the peak of the magnitude of the DFFT plot. It appears to show a peak of around 8 units, rather than purely 10 units. Since other raw data inputs into the Fortran program produced results as expected, the skew may be related to the way the data were generated in Python+NumPy or the way they were saved into a text file.

There also appear to be some secondary peaks that rapidly roll off on both sides of the main peak. This is most likely due to the FFTW3 algorithm responding to the discontinuities of the input data (finite-length window / non-integer number of cycles relative to the FFT length after zero-padding to the next power of two). More research is needed to fully characterize these effects.

## Conclusion

The Discretized Fourier Transform of a 50 Hz sine wave was computed by generating samples in Python, transforming them with a Fortran 2003 FFTW3 program, and plotting the magnitude spectrum with GNUPlot. This example complements the SciLAB-based 10 Hz case and the multi-tone / switched-sine notebooks elsewhere in this section.
