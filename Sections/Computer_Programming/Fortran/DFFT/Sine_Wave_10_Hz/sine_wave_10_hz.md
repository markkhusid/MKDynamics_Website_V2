# Sine Wave at 10Hz

## Introduction
This example demonstrates the computation of the Discretized Fourier Transform of a sine wave at 10 Hz using the FFTW3 library in Fortran. The sine wave is generated using SciLAB and the DFFT is computed using the Fortran 2003 code. The time domain and frequency domain plots are generated using GNUPlot.

## SciLAB Code
The SciLAB code to generate the sine wave is as follows:
```scilab
// Generate a sine wave at 10 Hz
// Frequency components of a signal
//----------------------------------
// build a signal sampled at 1000hz  containing a pure frequency
// at 10Hz
sample_rate=1000;
frequency=10;

// time vector which goes from 0 to 1 with a step of 1/sample_rate
t = 0:1/sample_rate:1;

// number of samples
N=size(t,'*'); //number of samples

// generate the signal
s=sin(2*%pi*frequency*t);

// compute the fft of the signal
y=fft(s);

//s is real so the fft response is conjugate symmetric and we retain only the first N/2 points
f=sample_rate*(0:(N/2))/N; //associated frequency vector

// number of samples
n=size(f,'*')

// plot the fft
h=0;
scf(h);
xset('window',h);
xtitle('DFFT of 10Hz Sine Wave in SciLAB', 'Freq [Hz]', 'Amplitude [Arb]');
plot(f,abs(y(1:n)))

// plot the time domain signal
h=1;
scf(h);
xset('window',h);
xtitle('s(t)', 'Time [s]', 'Amplitude [Arb]');
plot(t, s);
```

## Execute the SciLAB Code
To execute the SciLAB code, copy and paste the code into the SciLAB console and press Enter.  The time domain and frequency domain plots will be displayed.  The results are shown below:

### Time Domain Plot
```{figure} images/scilab_sine_wave2_10Hz.jpeg
:class: clickable-figure

scilab sine wave2 10Hz
```

### Frequency Domain Plot
```{figure} images/scilab_sine_wave2_10Hz_FFT.jpg
:class: clickable-figure

scilab sine wave2 10Hz FFT
```

## Saving The Time Domain Data
The time-domain data is selected in SciLAB and saved into a CSV file. 

## Processing of CSV File into a Format Suitable for Input into the Fortran 2003 DFFT Code
Since the output of SciLAB is a comma separated value (CSV) file, a method is needed that will process that file into another file, where the commas are removed and each data element is on a separate line.

Additionally, a the data elements need to be reformatted into fixed floating point, since the "e" floating point format was noticed to possibly cause errors when input into the FFTW3 algorithm.

These operations were done using a Python script, with its powerful object-oriented file techniques and its included CSV library. The Python script is shown below: 

```python
#!/usr/bin/python3
import sys
import csv
import os

# Assign constants for better code readability
first_arg = 1
second_arg = 2

# Call the system to get the command line arguments and pull out items from the list
input_file = sys.argv[first_arg]
intermediate_file = 'intermediate.dat'
output_file = sys.argv[second_arg]

# Simple string manipulation that traverses text file until EOF 
# and calls method to replace commas with newline characters
with open(input_file) as infile, open(intermediate_file, "w") as outfile:
  for line in infile:
      outfile.write(line.replace(",", "\n"))

# Close the input file, as it is no longer needed.
infile.close()
      
# Now go through the intermediate file (the file that contains one data element per line)
# and reformat all of the data elements into fixed floating point with 20 decimal precision.
with open(intermediate_file) as infile, open(output_file, "w") as outfile:
  for line in infile:
      outfile.write('%20.20f\n' % float(line))
            
# Close the intermediate file and final output file.
infile.close()
outfile.close()

# Clean away the intermediate file.  The next line may be commented out if the intermediate 
# file is required.
os.remove(intermediate_file)
```

## Execute the Python Script
Run by typing: 
```bash
./convert_csv.py infile.csv outfile.dat
```

where infile.csv is the data file in CSV format, and outfile.dat is the processed file
Obtain the line count of the processed file by typing: 

```bash
wc -l outfile.dat
```

## Fortran 2003 Code
The Fortran 2003 code to compute the Discretized Fourier Transform of the sine wave at 10 Hz is as follows:

```{literalinclude} ../code/dfft_fftw3.f08
---
language: fortran
---
```

## Compile the Fortran 2003 Code
To compile the Fortran 2003 code, type the following command:

```bash
gfortran -o dfft_fftw3 dfft_fftw3.f08 -I/usr/include -lfftw3
```

## Execute the Fortran 2003 Code
To execute the Fortran 2003 code, type the following command:

```bash
./dfft_fftw3 outfile.dat DFFT_mag_file.dat DFFT_phase_file.dat 1000 10
```

where outfile.dat is the output of the Python script, DFFT_mag_file.dat is the DFFT magnitude,
DFFT_phase_file.dat is the DFFT phase, 1000 is the sample rate in Hz, and 10 is the number of
periods in the file. The program requires these five arguments. The sample rate and the number
of periods match the SciLAB listing above: 1000 Hz, and one second of the 10 Hz wave.

## Visualize the DFFT Results
The DFFT results are visualized using GNUPlot.  The GNUPlot script is as follows.

`using 1` plots the first column against the record number. That record number is the FFT bin index, counted from 1. It is not a frequency in Hz. The second column of each file is the frequency in Hz. The figures below are the original plots, and the title baked into those images still says Frequency [Hz]. The numbers on that axis are the bin index. The script here names the axis for what it actually is.

```bash
set term wxt 0
set xrange [0:50]
set title "DFFT Magnitude of 10Hz Sine Wave"
set xlabel "FFT bin index"
set ylabel "Arbitrary Units [Arb]"
plot "DFFT_mag_file.dat" using 1 with lines

set term wxt 1
set xrange [0:50]
set title "DFFT Phase of 10Hz Sine Wave"
set xlabel "FFT bin index"
set ylabel "Phase [degrees]"
plot "DFFT_phase_file.dat" using 1 with lines
```

To execute the GNUPlot script, type the following command:

```bash
gnuplot -persist plot_dfft.gnu
```
or start GNUPlot and type the following to load the script:

```bash
load 'plot_dfft.gnu'
```

## Results


The magnitude and phase plots are shown below:

### DFFT Magnitude Plot
```{figure} images/DFFT_mag_sine_wave2_10Hz.jpeg
:class: clickable-figure

DFFT mag sine wave2 10Hz
```

### DFFT Phase Plot
```{figure} images/DFFT_phase_sine_wave2_10Hz.jpeg
:class: clickable-figure

DFFT phase sine wave2 10Hz
```

## Discussion
The DFFT of the sine wave at 10 Hz was successfully computed using the FFTW3 library in Fortran. The results were visualized using GNUPlot. The magnitude and phase plots are shown above.

The phase plot above displays overall quantization noise and computation noise of FFTW3, since
pure frequency sine wave with zero phase should have been a straight line at 0 degrees.
This plot gives a feel for the accuracy of the computational engine. 

There appears to be good correlation between the DFFT magnitude plot generated by SciLAB and
the DFFT magnitude plot generated by the Fortran 2003 code. Of note are the anomalous
phase results in the output of the Fortran 2003 code. SciLAB's `t = 0:1/1000:1` is 1001 samples,
and the Fortran code zero-pads that array to 1024. The bins are then 1000/1024 Hz apart, about
0.977 Hz, so the 10 Hz tone falls between bins. A bin that holds essentially no energy still
gets a phase from `atan2`, and that phase is just numerical noise.
It would be interesting to see the results on a signal with known phase shift. 

## Conclusion
The Discretized Fourier Transform of a sine wave at 10 Hz was successfully computed using the FFTW3 library in Fortran. The results were visualized using GNUPlot. The magnitude and phase plots are shown above.







