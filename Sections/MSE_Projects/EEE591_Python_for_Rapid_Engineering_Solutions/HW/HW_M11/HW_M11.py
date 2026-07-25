#!/usr/bin/env python
# coding: utf-8

# # Homework Module 11

# In[1]:


##########################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - HW_M11: HW_M11.py
# Mark Khusid
##########################################################################################

##########################################################################################
# MW_M11
#                    
##########################################################################################


# ## Import Libraries

# In[2]:


import numpy as np
from random import random


# ## Create Debug Flags

# In[3]:


debug = False
debug_lvl_2 = False


# ## Define Maxiumum Number of Attempts

# In[4]:


MAX_NUM_ATTEMPTS = 100


# ## Define Maximum Number of Points

# In[5]:


MAX_NUM_POINTS = 10_000


# ## Define Precisions List

# In[6]:


precisions_list = [10**(-power) for power in range(1, 8)] # 10^-1 to 10^-7


# In[7]:


if debug:
    print(precisions_list)


# ## Define Estimate_Pi_Attempt() Function

# In[8]:


if debug:
    print(random())
    print(type(np.pi))
    print(f"{np.pi:.50f}")
    print(np.finfo(float))


# In[9]:


################################################################################
# Function to estimate pi using the Monte Carlo method.  Returns the estimate  #
# if successful and returns None if not successfull.                           #
#                                                                              #
# Inputs:                                                                      #
#    precision - the desired precision of the estimate                         #
#                                                                              #
# Outputs:                                                                     #
#    returns the estimate of pi at precision and None if not successful        #
################################################################################

def estimate_pi_attempt(precision):

    # Initialize the counter that holds the number of points that are
    # inside the circle.
    num_points_inside = 0

    # Start estimation loop
    for total_points in range(1, MAX_NUM_POINTS + 1):

        # Generate random values for x and y
        x = random() # Number is between 0 and 1
        y = random() # Number is between 0 and 1

        # Check whether generated points are inside the circle
        # The condition is if the distance from the origin is <= 1
        if (x**2 + y**2) <= 1.0:
            # increment number of points inside circle counter
            num_points_inside += 1

        # Estimate pi up till now
        estimated_pi = 4.0 * num_points_inside / total_points

        # Check whether precision criteria is met
        # if the estimated pi - built in pi is <= precision
        # then return the estimated pi, otherwise return None
        if abs(estimated_pi - np.pi) <= precision:
            return(estimated_pi)

    # Else always return a None for safety
    return None   


# In[10]:


if debug:
    print(estimate_pi_attempt(0.001))
    print(estimate_pi_attempt(1e-20))


# ## Define Main() Function

# In[11]:


def main():

    # Loop through all required precisions in precision_list
    for precision in precisions_list:

        # Create a list of successful pi estimates at the current 
        # precision iteration.  
        successful_values = []

        # Initialize success counter
        success_count = 0

        # Loop for MAX_NUM_ATTEMPTS times to estimate pi.
        for attempt in range(MAX_NUM_ATTEMPTS):
            # Try to estimate pi using the estimate_pi_attempt() function
            pi_value = estimate_pi_attempt(precision=precision)

            # If successful, add the pi_value to the successful_values list
            # and increment success counter
            if pi_value is not None:
                successful_values.append(pi_value)
                success_count += 1

                # Get level 2 debug info
                if debug_lvl_2:
                    print(f"[*] Hit at {pi_value:.7f}, success_count = {success_count}")

        # Get the average pi value for this precision iteration only if there are successes
        # Print out results per HW requirements
        if success_count > 0:
            average_pi = sum(successful_values) / success_count
            print(f"{precision}, success, {success_count}, times, {average_pi}")
        else:
            print(f"{precision}, no success")

if __name__ == "__main__":
    main()

