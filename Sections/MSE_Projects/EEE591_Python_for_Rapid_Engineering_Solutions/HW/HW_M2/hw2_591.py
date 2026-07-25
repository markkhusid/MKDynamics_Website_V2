################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - HW2_591.py
# Mark Khusid
################################################################################

################################################################################
# Problem 3: Energy Calculation
################################################################################

# Import libraries
import numpy as np
from scipy.integrate import quad

# Define the integrand function for the energy calculation
################################################################################
# Function to be integrated: x(t) = exp(-t)*sin(2*pi*f*t)                      #
# input:                                                                       #
#    t: the variable to integrate                                              #
#    f: the frequency of the sinusoidal component                              #
# output:                                                                      #
#    returns the value of the function at t                                    #
################################################################################
def x(t, f):
    return np.exp(-t) * np.sin(2 * np.pi * f * t)

# Define the integrand for energy calculation: E(f) = integral of |x(t)|^2 dt from 0 to infinity
################################################################################
# Function to be integrated: u(t) = |x(t, f)|^2                                #
# input:                                                                       #
#    t: the time variable                                                      # 
#    f: the frequency of the sinusoidal component                              #
#    x(t, f): function to calculate the energy of at time t and frequency f    #
# output:                                                                      #
#    returns the energy of the function x(t) at time t and frequency f         #
################################################################################
def energy_integrand(t, f):
    return np.abs(x(t, f))**2

# Define the frequency list to evaluate the energy at
FREQUENCIES_LIST = [10, 20, 1E6] # in Hz

# Define the limits of integration for energy calculation
LOWER_LIMIT = 0 # since the time variable t starts at 0
UPPER_LIMIT = 30 # Based on AI suggestion for a tolerance of about 10^-8.  Choosing less than 30 results in a warning.  

# Create a list to store the energy results for each frequency
energy_results = []

# Perform the energy calculation for each frequency in the list
for f in FREQUENCIES_LIST:
    # Compute the energy using scipy's quad function
    # the limit parameter is increased to allow for more subdivisions in the integration.
    # This eliminates the warning.
    energy, energy_error = \
        quad(
            energy_integrand, 
            LOWER_LIMIT, 
            UPPER_LIMIT, 
            args=(f,),    # inform quad to pass additional arguments (namely f), and not just t
            limit=100_000 # increase the limit for better accuracy and avoiding the warnings.
        ) 
    energy_results.append(energy)
    
    # Print the results for debug
    #print(f"Energy at frequency {f} Hz: {energy:.12f} with error estimate {energy_error:.12e}") # for debug

# Create a dictionary to store the energy results for each frequency
answer_dict = {'10 Hz': energy_results[0], '20 Hz': energy_results[1], '1 MHz': energy_results[2]}

# Print the final results
for freq, energy in answer_dict.items():
    print(f"Energy at {freq}: {energy:.5f}")
