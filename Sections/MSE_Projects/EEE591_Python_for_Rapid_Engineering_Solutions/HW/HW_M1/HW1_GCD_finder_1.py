################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - HW1.py
# Mark Khusid
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

        int_div = a // b # for dubug
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

# Split the stripped string into a list of strings using the comma as a delimiter, and then strip each item in the list of leading and trailing whitespace 
split_stripped_str_list_1 = stripped_str.split(",")
#print(split_stripped_str_list_1) # for debug

split_stripped_str_list_2 = [item.strip() for item in split_stripped_str_list_1]
#print(split_stripped_str_list_2) # for debug

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
