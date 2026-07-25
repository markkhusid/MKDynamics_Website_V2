
input_str = input("Input an integer: ")
#input_str = "2" # hard code for debug

#print("Input string: ", input_str) # for debug
#print("Type of input string: ", type(input_str)) # for debug

stripped_str = input_str.strip()
#print("Stripped string: ", stripped_str) # for debug

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


