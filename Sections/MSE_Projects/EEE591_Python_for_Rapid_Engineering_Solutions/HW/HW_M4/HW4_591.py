#!/usr/bin/env python
# coding: utf-8

# In[1]:


################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - HW4_591.py
# Mark Khusid
################################################################################

################################################################################
# Problem: Classical Bit Demodulator
################################################################################


# In[2]:


import numpy as np                     # need math and arrays
from numpy.linalg import inv           # matrix inversion
import matplotlib.pyplot as plt        # and plotting


# In[3]:


# ================================================
# PARAMETER SETUP FOR CLASSICAL BIT DEMODULATOR
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Number of samples (N) per transmitted bit signal
# The problem requires N = 3 samples per bit
number_of_samples = 3

# Number of bits (N_B) for Monte Carlo simulation
# Large value chosen to obtain statistically accurate BER estimate
number_of_bits = 100000

# Signal-to-Noise Ratio (SNR) in linear scale
# SNR = 1 corresponds to 0 dB as specified in the problem
SNR = 1 # corresponds to 0 dB

# Angular frequency (OMEGA) in rad/sec
# Calculated as: OMEGA = 2 * π / N
# This ensures exactly one full cycle over the N samples
omega = 2 * np.pi / number_of_samples # rad / sec
#print(f"Omega = {omega:.4f} [rad/sec]")

# Frequency in Hz (derived from omega)
# f = OMEGA / (2π) = 1/N Hz (exactly 1 cycle over N samples)
freq = omega / (2 * np.pi )
#print(f"Frequency = {freq:.4f} [Hz]")

# Standard deviation of the additive white Gaussian noise (AWGN)
# sigma = sqrt(0.5 / SNR) as defined in the problem statement
# This scaling ensures the noise power matches the given SNR definition
sigma = np.sqrt(0.5 / SNR) # standard deviation of noise
#print(f"Sigma = {sigma:.4f}")


# In[4]:


# ================================================
# SIGNAL GENERATION (TRANSMISSION) - TIME AXIS & RANDOM BITS
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Create the discrete time index array t for the N samples of each bit
# t = [0, 1, 2] when N = 3 (as required by the problem)
# This time vector is used in the signal equation:
# x_i(t) = cos(OMEGA * t + phase_i)
time_array = np.arange(number_of_samples)

# Generate the array of transmitted bits (N_B random bits)
# Each bit is independently 0 or 1 with equal probability (fair coin flip)
# This creates the ground-truth data for the Monte Carlo simulation
# and will be used later to compute the Bit-Error-Rate (BER)
bits_array = np.random.randint(0, 2, size = number_of_bits)


# In[5]:


#time_array


# In[6]:


#bits_array


# In[7]:


# ================================================
# SIGNAL GENERATION (TRANSMISSION) - PHASE MAPPING
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Map each transmitted bit to its corresponding phase (BPSK modulation)
#   Logic 0 → phase = 0 radians
#   Logic 1 → phase = π radians
# This directly implements the modulation scheme in the problem statement:
#   x_i(t) = cos(OMEGA * t + phase_i)
# The vectorized multiplication (bit * π) is efficient and produces a
# phase_array of the same length as bits_array
phase_array = bits_array * np.pi


# In[8]:


#phase_array


# In[9]:


# ================================================
# SIGNAL GENERATION (TRANSMISSION) - TRANSMITTED SIGNAL MATRIX
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Compute the clean transmitted signal x_i(t) for all N_B bits at once
# Equation from the problem statement:
#   x_i(t) = cos(OMEGA * t + phase_i)
#
# Uses NumPy broadcasting for a fully vectorized (fast) implementation:
#   - time_array.shape          = (N,)          → [0, 1, 2]
#   - phase_array[:, np.newaxis].shape = (N_B, 1)
# Broadcasting automatically expands to shape (N_B, N)
# Result: x_of_t is a matrix of shape (N_B, N) where
# each row contains the N clean samples of one transmitted bit
x_of_t = np.cos(omega * time_array + phase_array[:, np.newaxis])


# In[10]:


#x_of_t


# In[11]:


# ================================================
# SIGNAL GENERATION (TRANSMISSION) - NOISE GENERATION
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Generate the additive white Gaussian noise (AWGN) matrix n_i(t)
# for all N_B bits simultaneously.
#
# Each noise sample is drawn from a normal distribution:
#   mean (loc) = 0.0
#   standard deviation (scale) = sigma = sqrt(0.5 / SNR)
#   (as explicitly required in the problem statement)
#
# The shape (number_of_bits, number_of_samples) = (N_B, N)
# exactly matches the dimensions of the transmitted signal matrix
# x_of_t. This enables clean, vectorized addition later:
#   y_i(t) = x_i(t) + n_i(t)
noise_array = np.random.normal(loc=0.0, scale=sigma, size=(number_of_bits, number_of_samples))


# In[12]:


#noise_array[0:5]


# In[13]:


#x_of_t.shape


# In[14]:


# ================================================
# SIGNAL GENERATION (TRANSMISSION) - RECEIVED SIGNAL MATRIX
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Compute the received noisy signal y_i(t) for every bit
# This implements the wireless channel model exactly as stated in the problem:
#     y_i(t) = x_i(t) + n_i(t)
#
# Both x_of_t and noise_array are matrices of identical shape (N_B, N),
# so NumPy performs element-wise addition. The result y_of_t is the
# complete received-signal matrix that the Classical Demodulator will
# use to estimate the transmitted bits.
y_of_t = x_of_t + noise_array


# In[15]:


#y_of_t[0:5]


# In[16]:


# ================================================
# DECODING (RECEPTION) - DESIGN MATRIX INITIALIZATION
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Initialize the design matrix H (commonly called "h" in the lecture code)
# for the Classical Demodulator's least-squares phase estimation.
#
# Shape: (N, 2) where N = number_of_samples = 3
# This matrix will later be populated with the known basis functions:
#   Column 0: cos(OMEGA * t)
#   Column 1: sin(OMEGA * t)   (or -sin, depending on the exact formulation)
#
# The received signal for each bit will be modeled as:
#   y ≈ h @ theta
# where theta contains the coefficients from which the phase is recovered.
# This is the standard linear algebra setup used in Lecture 4.1,
# now simplified since frequency and amplitude are known.
h = np.zeros((number_of_samples,2))


# In[17]:


#h


# In[18]:


# ================================================
# DECODING (RECEPTION) - DESIGN MATRIX POPULATION
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Populate the two columns of the design matrix `h` (shape N × 2)
# with the known trigonometric basis functions at the fixed frequency.
#
# This implements the linear signal model from Lecture 4.1:
#     y(t) ≈ h[:, 0] * A + h[:, 1] * B
# where:
#   - Column 0 → cos(2π * freq * t)   (in-phase / cosine component)
#   - Column 1 → sin(2π * freq * t)   (quadrature / sine component)
#
# Because frequency (and therefore ω = 2π·freq) is known and fixed,
# we only need to solve for the coefficients A and B via least-squares
# to recover the transmitted phase φ for each bit.
# (Note: 2 * np.pi * freq is exactly equal to omega.)
h[:, 0] = np.cos(2 * np.pi * freq * time_array)
h[:, 1] = np.sin(2 * np.pi * freq * time_array)


# In[19]:


#h


# In[20]:


# ================================================
# DECODING (RECEPTION) - PRECOMPUTE LEAST-SQUARES MATRIX
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Compute the matrix b = (Hᵀ H)⁻¹
# This is the key precomputation step from the Classical Demodulator
# in Lecture 4.1 (normal equations / pseudo-inverse approach).
#
# Because the design matrix `h` (shape N × 2) is identical for every bit
# (fixed frequency and sampling instants), we only need to invert
# (Hᵀ H) once. The result `b` will be reused for all N_B bits when
# solving for the coefficients:
#     theta = b @ (Hᵀ y)
# where theta = [A, B]ᵀ and the phase is recovered from A and B.
#
# This avoids repeating the matrix inversion inside a loop and
# makes the code efficient even for very large N_B.
b = inv(np.dot(h.transpose(), h))


# In[21]:


#b


# In[22]:


# ================================================
# DECODING (RECEPTION) - ESTIMATED BITS INITIALIZATION
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Initialize the array that will hold the demodulator's bit decisions
# (the "hat" notation denotes an estimate).
#
# Shape: (N_B,) with integer dtype (values will be 0 or 1)
# This array is populated later by the phase estimation logic
# for every received signal y_i(t). It serves as the output of
# the Classical Bit Demodulator and will be compared element-wise
# against the true transmitted bits_array to compute the Bit-Error-Rate (BER).
bits_array_hat = np.zeros(number_of_bits, dtype=int)


# In[23]:


#bits_array_hat


# In[24]:


# ================================================
# DECODING (RECEPTION) - CLASSICAL BIT DEMODULATOR (LOOP)
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Main demodulation loop: estimates the transmitted bit for every received
# signal vector y_i(t) using the Classical Demodulator from Lecture 4.1.
#
# For each bit we solve the linear least-squares problem:
#     y ≈ A·cos(ωt) + B·sin(ωt)
# using the precomputed matrix b = (HᵀH)⁻¹.
# Then we make a hard decision on the in-phase coefficient A:
#   A ≥ 0 → bit 0 (phase ≈ 0)
#   A <  0 → bit 1 (phase ≈ π)
# This is sufficient (and optimal) for BPSK because the quadrature
# coefficient B is expected to be near zero.
#
# Note: The loop processes all N_B bits sequentially.
# (The problem encourages vectorization as an optional optimization.)
for i in range(number_of_bits):
    # Extract the i-th received noisy signal vector (N samples)
    # yi now holds y_i(t) for the current bit
    yi = y_of_t[i, :]

    # Compute the projection of yi onto the two basis functions:
    # a = Hᵀ · yi   (shape (2,))
    # This is the first step of the normal equations
    a = np.dot(h.transpose(), yi)

    # Solve for the least-squares coefficients using the precomputed inverse:
    # c = b @ a  →  c = [A, B]ᵀ
    # (equivalent to the pseudo-inverse solution theta = (HᵀH)⁻¹ Hᵀ y)
    c = np.dot(b, a)

    # Extract the in-phase (cosine) coefficient A and quadrature (sine) coefficient B
    A = c[0]
    B = c[1]

    # BPSK hard-decision rule based on the sign of A:
    #   A < 0  → estimated phase ≈ π  → decide bit = 1
    #   A ≥ 0  → estimated phase ≈ 0   → decide bit = 0
    # (We ignore B because it should be approximately zero for pure BPSK)
    bits_array_hat[i] = 1 if A < 0 else 0


# In[25]:


#bits_array


# In[26]:


#bits_array_hat


# In[29]:


# ================================================
# PERFORMANCE EVALUATION - BIT-ERROR-RATE (BER)
# (Based on HW4 specifications - EEE 419/591)
# ================================================

# Compute the Bit-Error-Rate (BER) of the Classical Bit Demodulator.
# This is the final performance metric required by the homework.
#
# BER is defined exactly as stated in the problem:
#     BER = (number of bits in error) / N_B
#
# The comparison `bits_array != bits_array_hat` produces a boolean
# array of length N_B. np.sum() counts how many bits were incorrectly
# decoded (True = error). Dividing by the total number of bits
# gives the error probability (a floating-point number between 0 and 1).
#
# This line is fully vectorized, very fast, and matches the Monte Carlo
# simulation approach described in the assignment.
BER = np.sum(bits_array != bits_array_hat) / number_of_bits

# Print the computed BER value.
print(f"{BER:.6f}")


# In[ ]:


