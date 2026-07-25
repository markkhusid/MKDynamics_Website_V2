
input_str = input("Input a list of integers: ")
#input_str = "[31.0, 17, 81.4, 28]" # hard code for debug

#print("Input string: ", input_str) # for debug
#print("Type of input string: ", type(input_str)) # for debug

stripped_str = input_str.strip("[]")
#print("Stripped string: ", stripped_str) # for debug

split_stripped_str_list_1 = stripped_str.split(",")
#print("Split string: ", split_stripped_str_list_1) # for debug

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

# Loop through the list of strings, and check if the number is an integer and if so, check if it is prime
# Otherswise, print that the number is not an integer and skip the primality check
working_list = []
working_list = list.copy(split_stripped_str_list_2)
#print("Working list: ", working_list) # for debug

for item in working_list:
    #print()
    #print("Got string item: ", item) # for debug
    float_item = float(item) # First safely convert to float
    #print("Item as float: ", float_item) # for debug

    # Check if the float number is an integer using is_integer() because maybe its fractional part is 0,
    # and if so, convert to integer. Otherwise, print that the number is not an integer and skip the primality check
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
