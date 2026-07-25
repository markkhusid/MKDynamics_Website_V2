################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - HW1_591.py
# Mark Khusid
################################################################################

################################################################################
# PROBLEM 1: Compute DFT of a hardcoded time rray
################################################################################

# Import numpy
import numpy as np

# Define number of terms
#N = 8
N = 512
#N = 2048

################################################################################
# Define a random hardcoded time array of length N
################################################################################
# Define random seed
np.random.seed(0) # for reproducibility
# Generate random time array of length N
x_time = np.random.rand(N) # random time array of length N

################################################################################
# Compute the DFT of the time array using nested for loops
################################################################################
# Initialize DFT array with zeros
x_freq_loops = np.zeros(N, dtype=complex) # DFT array of length N.  Needs to be complex to store mag and phase information

# Compute DFT using nested for loops
for k in range(N): # loop over frequency bins
    for n in range(N): # loop over time samples
        x_freq_loops[k] += x_time[n] * np.exp(-(2j * np.pi * k * n) / N) # Definition of DFT

################################################################################
# Compute the DFT of the time array using matrix multiplication
################################################################################

# Create the DFT matrix
n = np.arange(N) # row vector of time indices
k = n.reshape((N, 1)) # column vector of frequency indices

# Compute the DFT matrix using the outer product of k and n
W = np.exp(-(2j * np.pi * k * n) / N) # DFT matrix of size NxN
# Compute the DFT by multiplying the DFT matrix with the time array
x_freq_matrix = np.dot(W, x_time) # DFT computed using matrix multiplication

################################################################################
# Compute the DFT using np.fft.fft()
################################################################################
x_freq_fft = np.fft.fft(x_time) # DFT computed using numpy's built-in FFT function

################################################################################
# Calculate the errors between the DFT computed using loops and numpy's FFT function
################################################################################
#print(type(x_freq_loops)) # for debug
#print(type(x_freq_matrix)) # for debug
#print(type(x_freq_fft)) # for debug

#print("x_freq_loops (first few): ", x_freq_loops[:5]) # for debug
#print("x_freq_matrix (first few): ", x_freq_matrix[:5]) # for debug
#print("x_freq_fft (first few): ", x_freq_fft[:5]) # for debug

# Calculate the magnitude of the DFTs
x_freq_loops_mag = np.abs(x_freq_loops) # magnitude of DFT computed using loops
x_freq_matrix_mag = np.abs(x_freq_matrix) # magnitude of DFT computed using matrix
x_freq_fft_mag = np.abs(x_freq_fft) # magnitude of DFT computed using numpy's FFT function

#print("x_freq_loops_mag (first few): ", x_freq_loops_mag[:5]) # for debug
#print("x_freq_matrix_mag (first few): ", x_freq_matrix_mag[:5]) # for debug
#print("x_freq_fft_mag (first few): ", x_freq_fft_mag[:5]) # for debug

# Calculate the errors between the DFTs
#print("Calculating errors between DFT computed using loops and numpy's FFT function...") # for debug
error_loops_fft = np.sum(x_freq_loops_mag - x_freq_fft_mag)/N # error between DFT computed using loops and numpy's FFT function
error_matrix_fft = np.sum(x_freq_matrix_mag - x_freq_fft_mag)/N # error between DFT computed using matrix multiplication and numpy's FFT function

# Print the errors
print(f"Max error (loop   vs FFT): {error_loops_fft:.2e}")
print(f"Max error (matrix vs FFT): {error_matrix_fft:.2e}")
