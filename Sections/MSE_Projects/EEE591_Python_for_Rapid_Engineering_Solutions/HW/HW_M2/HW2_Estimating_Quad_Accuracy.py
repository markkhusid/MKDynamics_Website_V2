################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - HW2.py
# Mark Khusid
################################################################################

# Import libraries
import numpy as np
from scipy.integrate import quad

# Get the input list of integers from the user as a string
input_str = input("Input a set of 3 numbers between -10 and 10: ")
#input_str = "-2 6 0" # hard code for debug
#print(input_str) # for debug
#print(type(input_str)) # for debug

    # Split the stripped string into a list of strings using the comma as a delimiter
split_stripped_str_list_1 = input_str.split(" ")
#print(split_stripped_str_list_1) # for debug

# Strip each string in the list of leading and trailing whitespace using a list comprehension
split_stripped_str_list_2 = [item.strip() for item in split_stripped_str_list_1]
#print(split_stripped_str_list_2) # for debug

# Extract the three numbers into the variables a, b, and c
a = float(split_stripped_str_list_2[0])
b = float(split_stripped_str_list_2[1])
c = float(split_stripped_str_list_2[2])
#print("a: ", a) # for debug
#print("b: ", b) # for debug
#print("c: ", c) # for debug

# Define the number of points to use in the numerical integration
NUM_POINTS = 1_000_000

# Define the limits of integration
LOWER_LIMIT = -4
UPPER_LIMIT = 5

# Define the integrand function
################################################################################
# Function to be integrated: I_1(x) = a*x^5 + b*x^2 - c)                       #
# input:                                                                       #
#    x: the variable to integrate                                              #
#    a: a constant to be used                                                  #
#    b: a constant to be used                                                  #
#    c: a constant to be used                                                  #
# output:                                                                      #
#    returns the value of the function at x given a, b, and c                  #
################################################################################
def integrand(x):
    return (a * x**5 + b * x**2 - c)

# Compute the value of the integra using scipy's quad function from -4 to 5
integral_value_quad, integral_error_quad = quad(integrand, -4, 5)
#print(f"Integral value using scipy's quad function: {integral_value_quad: .4f}") # for debug
#print("Integral error using scipy's quad function: ", integral_error_quad) # for debug

# Use the trapezoidal rule to compute the integral numerically and manually
subinvterval_width = (UPPER_LIMIT - LOWER_LIMIT) / NUM_POINTS
#print(f"Subinterval width: {subinvterval_width: .6f}") # for debug

# Print the number of points and the limits of integration for debug
#print(f"Number of points: {NUM_POINTS}") # for debug

# Compute the initial result using the trapezoidal rule algorithm
initial_result = 0.5 * (integrand(LOWER_LIMIT) + integrand(UPPER_LIMIT)) 
#print("Initial result before for loop: ", initial_result) # for debug

# Start a running sum to compute the integral using the trapezoidal rule algorithm
running_sum = 0

# Give the runninsg sum the initial result
running_sum += initial_result

# Create a scratchpad variable to store the value of x at each interval
x = 0

# Create a scratchpad variable to store the value of the function at each interval
f_x = 0

# Create a variable to store the final result of the integral computed using the trapezoidal rule algorithm
final_result_numerical = 0

# Loop over the subintervals and compute the value of the function at each point
for i in range(1, NUM_POINTS):
    x = LOWER_LIMIT + i * subinvterval_width # compute the tmp value at the current point
    f_x = integrand(x) # compute the value of the function at the current point
    running_sum += 2 * f_x # add the value of the function at the current point to the running sum
# Multiply the running sum by the subinterval width divided by 2 to get the final result
final_result_numerical = running_sum * (subinvterval_width / 2)

#print(f"Final result using trapezoidal rule: {final_result_numerical: .4f}") # for debug

# Report results for credit
print(f"Method 1: I1 = {integral_value_quad: .4f}")
print(f"Method 2: I1 = {final_result_numerical: .4f}")

# Calculate the error between the two methods
# Percentage error = (|Accurate method - Inaccurate method| / |Accurate method|) * 100
error_percentage = (abs(integral_value_quad - final_result_numerical) / abs(integral_value_quad)) * 100
print(f"Percentage error: {error_percentage: .4f}%")

