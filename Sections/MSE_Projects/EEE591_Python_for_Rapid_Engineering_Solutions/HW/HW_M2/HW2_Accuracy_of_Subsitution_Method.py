################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - HW2.py
# Mark Khusid
################################################################################

# State the integration problem to be solved
# I_2 = integral from 0 to infinity of dx/(1+x^2) dx = pi/2
# Since the upper limit is infinity, we will use a change of variables as taught in video lecture 2.6 at min ~3:45.
#
# Let x = tan(theta)
# Then dx = sec^2(theta) dtheta
# When x = 0, theta = 0
# When x = infinity, theta = pi/2
# Therefore, the integral becomes:  
# I_2 = integral from 0 to pi/2 of sec^2(theta)/(1+tan^2(theta)) dtheta
# Using the trig identity 1 + tan^2(theta) = sec^2(theta), the integral simplifies to:
# I_2 = integral from 0 to pi/2 of sec^2(theta)/sec^2(theta) dtheta = integral from 0 to pi/2 of dtheta = pi/2

# Import libraries
import numpy as np
from scipy.integrate import quad

# Define the know result for the integral
KNOWN_RESULT = np.pi / 2

# Define precision for printing results
PRINT_PRECISION = 12
DIFF_PRECISION = 16

################################################################################
# Method 1: Compute the integral using scipy's quad function with the 
# transformed integrand and limits
################################################################################

# Perform change of integration limits in code
ORIG_LOWER_LIMIT = 0
ORIG_UPPER_LIMIT = np.inf

# Calculate the new limits after the change of variables
new_lower_limit = np.arctan(ORIG_LOWER_LIMIT) # arctan(0) = 0
new_upper_limit = np.arctan(ORIG_UPPER_LIMIT) # arctan(infinity) = pi/2

# Define the new integrand function after the change of variables
################################################################################
# Function to be integrated: I_2(theta) = 1                                    #
# input:                                                                       #
#    theta: the variable to integrate                                          #
# output:                                                                      #
#    returns the value of the function at theta                                #
################################################################################
def new_integrand(theta):
    return 1 # since sec^2(theta)/sec^2(theta) = 1

# Perform the integration with the new limits and integrand
result_method_1, error_method_1 = quad(new_integrand, new_lower_limit, new_upper_limit)
#print(f"Integral value using scipy's quad function with change of variables: {result_method_1: .{PRINT_PRECISION}f}") # for debug
#print(f"Integral error using scipy's quad function with change of variables: {error_method_1: .{PRINT_PRECISION}f}") # for debug
#print(f"Known result: {KNOWN_RESULT: .{PRINT_PRECISION}f}") # for debug

# Calculate the difference between the computed result and the known result
diff_method_1 = abs(result_method_1 - KNOWN_RESULT)
#print(f"Difference between computed result and known result for method 1: {diff_method_1: .{DIFF_PRECISION}f}") # for debug

#print() # for debug

################################################################################
# Method 2: Compute the integral using a package that can handle ininite 
# limits directly.
################################################################################

# Define the original integrand function
################################################################################
# Function to be integrated: I_2(x) = 1/(1+x^2)                                #
# input:                                                                       #
#    x: the variable to integrate                                              #
# output:                                                                      #
#    returns the value of the function at x                                    #
################################################################################
def original_integrand(x):
    return 1/(1+x**2)

# Perform the integration with the original limits and integrand
result_method_2, error_method_2 = quad(original_integrand, ORIG_LOWER_LIMIT, ORIG_UPPER_LIMIT)
#print(f"Integral value using scipy's quad function with original integrand and limits: {result_method_2: .{PRINT_PRECISION}f}") # for debug
#print(f"Integral error using scipy's quad function with original integrand and limits: {error_method_2: .{PRINT_PRECISION}f}") # for debug
#print(f"Known result: {KNOWN_RESULT: .{PRINT_PRECISION}f}") # for debug

# Calculate the difference between the computed result and the known result
diff_method_2 = abs(result_method_2 - KNOWN_RESULT)
#print(f"Difference between computed result and known result for method 2: {diff_method_2: .{DIFF_PRECISION}f}") # for debug

# Print results for credit
print(f"{result_method_1: .{PRINT_PRECISION}f}                             # I2 Method 1")
print(f"{result_method_2: .{PRINT_PRECISION}f}                             # I2 Method 2")
print(f"{diff_method_1: .{DIFF_PRECISION}f}                         # Difference Method 1")
print(f"{diff_method_2: .{DIFF_PRECISION}f}                         # Difference Method 2")
