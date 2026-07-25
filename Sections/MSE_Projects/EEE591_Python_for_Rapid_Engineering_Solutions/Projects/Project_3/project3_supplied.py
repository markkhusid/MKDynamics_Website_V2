# Problem 1:
# YOUR CODE GOES HERE


# PROBLEM 2:
# YOUR CODE GOES HERE

def opt_n(...):
################################################################################
# This function calculates the error corresponding to the passed inputs.       #
# Inputs:                                                                      #
#    n_value   - value of the ideality (n)                                     #
#    R         - value of the resistor                                         #
#    phi_value - value of phi                                                  #
#    area      - area of the diode                                             #
#    temp      - temperature                                                   #
#    src_v     - source voltage                                                #
#    meas_i    - measured current                                              #
# Outputs:                                                                     #
#    err_array - array of normalized error measurements                        #
################################################################################
    
    return err_array


################################################################################
# This is how leastsq calls opt_n                                              #
################################################################################

n_opt_array = optimize.leastsq(opt_n,n_init,
                             args=(R,phi,P2_AREA,P2_T,
                                   source_v,meas_diode_i))
n_opt = n_opt_array[0][0]

# DO NOT FORGET TO OUTPUT THE PROJECT DELIVERABLES
