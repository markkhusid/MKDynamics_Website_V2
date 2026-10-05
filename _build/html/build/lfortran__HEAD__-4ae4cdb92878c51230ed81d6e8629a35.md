# LFortran

Created with Grok Build

This section recomputes five discrete Fourier transforms in Jupyter notebooks that run on the LFortran kernel. The [FFTW3 section](../DFFT/DFFT__HEAD__.md) stays as its own set of pages. Those pages build a waveform in SciLAB or Python, write a text file, and pass that file to a Fortran 2003 program. Each notebook here builds the samples and transforms them inside LFortran.

## Kernel

**Kernel:** LFortran. The notebook metadata selects it with this kernelspec:

```yaml
name: fortran
display_name: Fortran
language: fortran
```

Jupyter starts that kernel with `lfortran kernel -f {connection_file}`. A code cell is Fortran source: a module, or top-level statements that call procedures from a module defined earlier in the same notebook. The kernel keeps those modules for the rest of the session. The printed tables on the example pages are the stdout saved from that run. Building this book publishes the saved output and does not start the kernel again.

## What each notebook runs

Each example has two code cells.

The first cell is `code/signals.f90`, a blank line, and `code/spectrum.f90`. It is the same text as the listings below. Executing it defines modules `signals` and `spectrum`.

The second cell calls one function from `signals`, then `spectrum_of`, `write_series`, and `print_peaks`. `write_series` writes `{name}_time.dat` and `{name}_spectrum.dat` next to the notebook. `print_peaks` prints every bin whose magnitude is at least 0.05. That table is the saved output on the page.

Every example lasts one second. The sample rate equals the number of samples, and that number is a power of two, so each frequency bin is one hertz. A sine of amplitude 1 then peaks at magnitude 1. DC and Nyquist are scaled by $1/N$, and every other bin by $2/N$. The columns of the table are frequency in hertz, magnitude, and phase in degrees.

## signals.f90

`signals` is private by default. It publishes `sine_tone`, `square_wave`, `two_sines`, and `switched_sine`. Kinds are `int32` and `real64` from `iso_fortran_env`, and every procedure starts from `implicit none`.

`time_at` is private. Sample `index`, counting from 1, is at time `(index - 1) / sample_rate`.

`sine_tone` writes `amplitude * sin(2π f t)` into each sample. `π` is `acos(-1.0_real64)`.

`square_wave` is a 50% duty square between `+amplitude` and `-amplitude`. The fractional position in the period is `modulo(t * frequency, 1)`. `merge` selects `+amplitude` when that position is below one half, and `-amplitude` otherwise.

`two_sines` adds two sines. Each term has its own frequency and amplitude, and both use the same sample time.

`switched_sine` applies a carrier sine through a gate. For the first half of each gate period the sample is the sine. For the second half the sample is 0. That choice is also a `merge`.

```{literalinclude} code/signals.f90
:language: fortran
```

## spectrum.f90

`spectrum` publishes `spectrum_of`, `write_series`, and `print_peaks`. The FFT, the bit reversal, the power-of-two test, and the per-bin print are private.

`spectrum_of` takes the real samples and the sample rate, and returns magnitude, frequency, and phase. It stops with `error stop` unless the length `N` is a power of two: `N >= 2` and `iand(N, N - 1) == 0`. The samples are copied into a `complex(real64)` array with a zero imaginary part. `fft_inplace` then runs a radix-2 decimation-in-time FFT. It bit-reverses the array by integer division, then combines even and odd halves for block lengths 2, 4, and so on up to `N`. The twiddle angle is `-2π / length`, which is the sign NumPy uses. Bin `k` is placed at frequency `k * sample_rate / N`. Magnitude is `abs(X) / N` at DC and at Nyquist, and `2 * abs(X) / N` on the bins in between. Phase is `atan2` of the imaginary and real parts, converted from radians to degrees.

`write_series` opens each path with `newunit` and writes `es24.16` columns. The time file holds time and sample. The spectrum file holds frequency, magnitude, and phase.

`print_peaks` prints the header `frequency_hz magnitude phase_deg` and calls private `print_one_peak` once per bin. That routine formats the line into a character variable, stores `magnitude >= threshold` in a logical, and returns before the print when the logical is false. A block-`if` whose condition is a real comparison is miscompiled by this LFortran kernel inside a module procedure, which is why the branch is an early return on that logical. The notebooks call the public `print_peaks` only.

```{literalinclude} code/spectrum.f90
:language: fortran
```

## Plots

The example cell writes the two text files and prints the peak table. The figures are drawn from those files by Matplotlib. From `Sections/Computer_Programming/Fortran/LFortran` the command is:

```bash
python3 code/plot_spectrum.py
```

`code/plot_spectrum.py` loads each pair of files. It checks the time column against `(i - 1) / sample_rate` and checks the Fortran magnitude and phase against `numpy.fft.rfft` using the $1/N$ and $2/N$ scaling above. Magnitude must agree to $10^{-6}$. Phase, on bins at or above magnitude 0.05, must agree to $10^{-3}$ degrees. The script then writes three PNGs at 140 dpi: the time series in blue, the magnitude in rust, and the phase as teal markers. The phase markers are only the bins at or above 0.05, on a scale from -180 to 180 degrees, over the same frequency window as the magnitude plot. The [10 Hz sine](sine_10_hz.ipynb) magnitude plot is also copied to `images/lfortran_dfft.png`, the picture on the LFortran card of the [Fortran](../fortran__HEAD__.md) page. After a case passes the check, the script deletes that case's `.dat` files. Those files are scratch and are not part of the site.

```{literalinclude} code/plot_spectrum.py
:language: python
```

The windows in the script are:

| Notebook | Time window | Magnitude through | Phase markers |
| --- | --- | --- | --- |
| [10 Hz sine](sine_10_hz.ipynb) | first 0.2 s | 40 Hz | bins at or above 0.05 |
| [50 Hz sine](sine_50_hz.ipynb) | first 0.06 s | 150 Hz | bins at or above 0.05 |
| [1 Hz square wave](square_1_hz.ipynb) | the whole second | 40 Hz | bins at or above 0.05 |
| [50 Hz and 100 Hz sines](two_sines.ipynb) | first 0.04 s | 200 Hz | bins at or above 0.05 |
| [1 kHz sine gated at 500 Hz](switched_sine_1_khz.ipynb) | first 4 ms | 3000 Hz | bins at or above 0.05 |

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
```{image} images/sine_10_hz_phase.png
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
```{image} images/sine_50_hz_phase.png
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
```{image} images/square_1_hz_phase.png
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
```{image} images/two_sines_phase.png
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
```{image} images/switched_sine_1_khz_phase.png
```
:::

::::
