# Square Wave at 1Hz

## Introduction
This example demonstrates the computation of the Discretized Fourier Transform of a square wave at 11 Hz using the FFTW3 library in Fortran. The square wave is generated using SciLAB and the DFFT is computed using the Fortran 2003 code. The time domain and frequency domain plots are generated using GNUPlot.

## SciLAB Code
The SciLAB code to generate the square wave is as follows:
```scilab
//Frequency components of a signal
//----------------------------------
// build a square wave signal sampled at 1000hz  containing at frequency 1Hz
// and 50% duty cycle

// Set the sample rate and frequency
sample_rate=1000;
frequency=1;
t = 0:1/sample_rate:1;

// number of samples
N=size(t,'*'); //number of samples

// generate the square wave signal
s = squarewave(2*%pi*frequency*t,50)

// compute the fft of the signal
y=fft(s);

//s is real so the fft response is conjugate symmetric and we retain only the first N/2 points
f=sample_rate*(0:(N/2))/N; //associated frequency vector
n=size(f,'*')
clf()

// plot the fft
plot(f,abs(y(1:n)))
```

## Execute the SciLAB Code
To execute the SciLAB code, copy and paste the code into the SciLAB console and press Enter.  The time domain and frequency domain plots will be displayed.  The results are shown below:

### Time Domain Plot
```{image} images/scilab_sq_wave_1Hz_50pct.jpeg

:height: 200
```

### Frequency Domain Plot
```{image} images/scilab_sq_wave_1Hz_50pct_DFFT.jpeg

:height: 200
```

## Saving The Time Domain Data
The time-domain data is selected in SciLAB and saved into a CSV file. 

## Processing of CSV File into a Format Suitable for Input into the Fortran 2003 DFFT Code
Since the output of SciLAB is a comma separated value (CSV) file, a method is needed that will process that file into another file, where the commas are removed and each data element is on a separate line.
Additionally, a the data elements need to be reformatted into fixed floating point, since the "e"
floating point format was noticed to possibly cause errors when input into the FFTW3 algorithm.
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
gfortran -o dfft_fftw3 dfft_fftw3.f08 -lfftw3
```

## Execute the Fortran 2003 Code
To execute the Fortran 2003 code, type the following command:

```bash
./dfft_fftw3 outfile.dat DFFT_mag_file.dat DFFT_phase_file.dat
```

where outfile.dat is the output of the Python script, DFFT_mag_file.dat is the DFFT magnitude
DFFT_phase_file.dat is the DFFT phase (if applicable).

## Visualize the DFFT Results
The DFFT results are visualized using GNUPlot.  The GNUPlot script is as follows:

```bash
set term wxt 0
set xrange [0:50]
set title "DFFT Magnitude of 1Hz 50% Duty Cycle Square Wave"
set xlabel "Frequency [Hz]"
set ylabel "Arbitrary Units [Arb]"
plot "DFFT_mag_sq_wv_1Hz.dat" using 1 with lines

set term wxt 1
set xrange [0:200]
set title "DFFT Phase of 1Hz 50% Duty Cycle Square Wave"
set xlabel "Frequency [Hz]"
set ylabel "Phase [degrees]"
plot "DFFT_phase_sq_wv_1Hz.dat" using 1 with lines
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
```{image} images/DFFT_mag_sq_wv2_1Hz_50pct.jpeg

:height: 200
```

### DFFT Phase Plot
```{image} images/DFFT_phase_sq_wv2_1Hz_50pct.jpeg

:height: 200
```

## Discussion
There appears to be good correlation between the DFFT magnitude plot generated by SciLAB and
the DFFT magnitude plot generated by the Fortran 2003 code. Of note are is the anomalous
phase results in the output of the Fortran 2003 code. It is unknown at this time what is causing it.
It would be interesting to see the results on a signal with known phase shift. 

## Conclusion
The Discretized Fourier Transform of a square wave at 1 Hz and 50% duty cycle was successfully computed using the FFTW3 library in Fortran. The results were visualized using GNUPlot. The magnitude and phase plots are shown above.







