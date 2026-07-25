################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - HW1.py
# Mark Khusid
################################################################################

################################################################################
# PROBLEM 1: GCD Finder
################################################################################

################################################################################
# Function to find the GCD of two numbers using Euclid's algorithm.            #
# input:                                                                       #
#    a, b: the two numbers for which to find the GCD                           #
# output:                                                                      #
#    returns the GCD of a and b                                                #
################################################################################
def gcd(a, b):
    # Parameter definitions
    # a: the first number for which to find the GCD
    # b: the second number for which to find the GCD

    #print("a: ", a) # for debug
    #print("b: ", b) # for debug

    #int_div = a // b # for dubug
    #print("int_div: ", int_div) # for debug

    mod = a % b # for debug
    #print("mod: ", mod) # for debug

    while mod != 0:
        a = b
        b = mod

        #print("a: ", a) # for debug
        #print("b: ", b) # for debug

        #int_div = a // b # for dubug
        #print("int_div: ", int_div) # for debug

        mod = a % b # for debug
        #print("mod: ", mod) # for debug

    else: # Grab the last value of b when mod is 0, which is the GCD
        #print("GCD inside function: ", b) # for debug
        return b

# Get the input list of integers from the user as a string
input_str = input("Input a list of integers: ")
#input_str = "[24, 60, 120, 30]" # hard code for debug
#input_str = "[48, 18, 30, 12]" # easy numbers for debug
#print(input_str) # for debug
#print(type(input_str)) # for debug

# Strip the input string of leading and trailing whitespace and square brackets
stripped_str = input_str.strip("[]")
#print(stripped_str) # for debug

# Split the stripped string into a list of strings using the comma as a delimiter
split_stripped_str_list_1 = stripped_str.split(",")
#print(split_stripped_str_list_1) # for debug

# Strip each string in the list of leading and trailing whitespace using a list comprehension
split_stripped_str_list_2 = [item.strip() for item in split_stripped_str_list_1]
#print(split_stripped_str_list_2) # for debug

# Convert the list of strings to a list of integers using a list comprehension
int_list = [int(item) for item in split_stripped_str_list_2]
#print(int_list) # for debug
#print(type(int_list[0])) # for debug

# Function testing for debug
#print("GCD = ", gcd(48, 18))
#print()
#print("GCD = ", gcd(12, 2))
#print()
#print("GCD = ", gcd(15, 10))
#print()
#print("GCD = ", gcd(90, 25))

working_list = int_list.copy()      # Create a copy of the input list to work with, so that the original list remains unchanged
len_list = len(working_list)        # Calculate the length of the working list and store it in len_list 
                                    # for later use in the loop to calculate GCD of adjacent pairs of integers.

# Print the input list and its length for debug
#print("Input list: ", working_list) # for debug
#print("Length of input list: ", len_list) # for debug

# Calculate the GCD of the first pair of integers in the working list, which are at index 0 and 1, and store the result in current_gcd.
current_gcd = gcd(working_list[0], working_list[(1)])
#print("GCD of ", working_list[0], " and ", working_list[(1)], " is: ", current_gcd) # for debug

# We now assume that the list has more than 2 integers, so we can loop through the rest of the list 
# to calculate the GCD of adjacent pairs of integers.
for i in range(2, len_list):     
    #print("i: ", i) # for debug
    #print("working_list[i]: ", working_list[i]) # for debug
    #print("GCD of ", current_gcd, " and ", working_list[(i)], " is: ", end="") # for debug
    current_gcd = gcd(current_gcd, working_list[(i)])
    #print(current_gcd) # for debug

# After the loop, current_gcd will contain the GCD of all the integers in the input list, which is the final result.
print("The GCD is: ", current_gcd)

################################################################################
# PROBLEM 2: Prime Finder
################################################################################


# Get the input list of integers from the user as a string
input_str = input("Input a list of integers: ")
#input_str = "[31.0, 17, 81.4, 28]" # hard code for debug

#print("Input string: ", input_str) # for debug
#print("Type of input string: ", type(input_str)) # for debug

# Strip the input string of leading and trailing whitespace and square brackets
stripped_str = input_str.strip("[]")
#print("Stripped string: ", stripped_str) # for debug

# Split the stripped string into a list of strings using the comma as a delimiter
split_stripped_str_list_1 = stripped_str.split(",")
#print("Split string: ", split_stripped_str_list_1) # for debug

# Strip each string in the list of leading and trailing whitespace using a list comprehension
split_stripped_str_list_2 = [item.strip() for item in split_stripped_str_list_1]
#print("Split string (stripped): ", split_stripped_str_list_2) # for debug


################################################################################
# Function to find out whether a number is prime using the optimized trial     #
# division algorithm.                                                          #
# input:                                                                       #
#    n: the number to check for primality                                      #
# output:                                                                      #
#    returns True if n is prime, False otherwise                               #
################################################################################
def is_prime(n):
    # Parameter definitions
    # n: the number to check for primality

    # Initial trivial case checks
    if n <= 1:
        #print("Not prime because n <= 1: ", n) # for debug
        return False
    elif ((n == 2) or (n == 3)):
        #print("Prime because n == 2 or n == 3: ", n) # for debug
        return True
    elif ((n % 2 == 0) or (n % 3 == 0)):
        #print("Not prime because n % 2 == 0 or n % 3 == 0: ", n) # for debug
        return False
    
    # Number is not a trivial case, so we can proceed with the optimized trial division algorithm
    # Set i = 5 per the algorithm
    i = 5
    # Loop until i^2 > n, checking if n is divisible by i or i + 2 per the algorithm
    while (i * i <= n):
        if ((n % i == 0) or (n % (i + 2) == 0)):
            #print("Not prime because n % i == 0 or n % (i + 2) == 0: ", n) # for debug
            return False
        i += 6 # increment i by 6 per the algorithm
    
    # we have a winner!
    #print(n, " is a prime") # for debug
    return True

# Test out the function with the list of integers
#is_prime(100)
#is_prime(101)
#is_prime(2)
#is_prime(3)
#is_prime(4)
#is_prime(5)
#is_prime(99)

# Create a copy of the input list to work with, so that the original list remains unchanged
working_list = []
working_list = list.copy(split_stripped_str_list_2)
#print("Working list: ", working_list) # for debug

# Loop through the list of strings, and check if the number is an integer and if so, check if it is prime
# Otherswise, print that the number is not an integer and skip the primality check
for item in working_list:
    #print() # for debug
    #print("Got string item: ", item) # for debug
    float_item = float(item) # First safely convert to float
    #print("Item as float: ", float_item) # for debug

    # Check if the float number is an integer using is_integer() because maybe its fractional part is 0,
    # and if so, convert to integer. Otherwise, print that the number is not an integer and skip the primality check
    # If the number is an integer, we can then check for primality and print the result.
    if float_item.is_integer():
        int_item = int(float_item) # Convert to integer
        #print("Item as integer: ", int_item) # for debug

        #print("Checking if ", int_item, " is prime...") # for debug
        # Check for primality and print the result
        if is_prime(int_item):
            print(int_item, " is a prime")
        else:
            print(int_item, " is not a prime")
    else:
        print(item, " is not an integer. Skipping...")

################################################################################
# PROBLEM 3: Riemann Zeta Function Calculator 
# (Approximation using the definition of the zeta function as an infinite sum
# but only for 1,000,000 terms).
################################################################################


# Get the input integer from the user as a string
input_str = input("Input an integer: ")
#input_str = "2" # hard code for debug

#print("Input string: ", input_str) # for debug
#print("Type of input string: ", type(input_str)) # for debug

# Strip the input string of leading and trailing whitespace
stripped_str = input_str.strip()
#print("Stripped string: ", stripped_str) # for debug

# Convert the stripped string to an integer
input_int = int(stripped_str)
#print("Input integer: ", input_int) # for debug
#print("Type of input integer: ", type(input_int)) # for debug

################################################################################
# Calculate the Riemann zeta function at the input integer using the definition 
# of the zeta function as an infinite sum.
################################################################################

# Define number of terms to use in the sum for approximation
NUM_TERMS = 1_000_000

# Initialize sum variable
sum = 0

# Loop to calculate the sum based of the definition of the zeta function, 
# which is the sum from n = 1 to infinity of 1 / n^s, where s is the input integer
for n in range(1, NUM_TERMS + 1):
    sum += 1 / (n ** input_int)

# Print the result with 6 decimal places and commas for thousands separator, along with the number of terms used in the approximation
print(f"Zeta({input_int}) = {sum:.6f} based on {NUM_TERMS:,} terms")


