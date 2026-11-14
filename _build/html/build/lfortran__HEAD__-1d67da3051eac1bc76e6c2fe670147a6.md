# LFortran

Created with Grok Build

This section recomputes the five discrete Fourier transform examples with the LFortran kernel. The FFTW3 pages stay as they are. Those pages build a waveform in SciLAB or Python, turn it into a text file, and hand it to a Fortran 2003 program. Here each notebook builds the samples and transforms them.

Every example lasts one second. The sample rate equals the number of samples, and that number is a power of two, so each frequency bin is one hertz. A sine of amplitude 1 then peaks at magnitude 1: the DC and Nyquist bins are scaled by $1/N$, and every other bin by $2/N$. The notebook prints each bin whose magnitude is at least 0.05. The columns are frequency in hertz, magnitude, and phase in degrees.

The transform is a radix-2 FFT. While these pages were built, the same samples were checked against NumPy's real FFT with that scaling.

```{literalinclude} code/signals.f90
:language: fortran
```

```{literalinclude} code/spectrum.f90
:language: fortran
```

## Examples

::::{grid} 2 2 2 2

:::{grid-item-card}
:link: sine_10_hz.ipynb

10 Hz Sine Wave
^^^
```{image} images/sine_10_hz_time.png
```
```{image} images/sine_10_hz_spectrum.png
```
:::

:::{grid-item-card}
:link: sine_50_hz.ipynb

50 Hz Sine Wave
^^^
```{image} images/sine_50_hz_time.png
```
```{image} images/sine_50_hz_spectrum.png
```
:::

:::{grid-item-card}
:link: square_1_hz.ipynb

1 Hz Square Wave, 50% Duty
^^^
```{image} images/square_1_hz_time.png
```
```{image} images/square_1_hz_spectrum.png
```
:::

:::{grid-item-card}
:link: two_sines.ipynb

50 Hz and 100 Hz Sines
^^^
```{image} images/two_sines_time.png
```
```{image} images/two_sines_spectrum.png
```
:::

:::{grid-item-card}
:link: switched_sine_1_khz.ipynb

1 kHz Sine Gated at 500 Hz
^^^
```{image} images/switched_sine_1_khz_time.png
```
```{image} images/switched_sine_1_khz_spectrum.png
```
:::

::::
