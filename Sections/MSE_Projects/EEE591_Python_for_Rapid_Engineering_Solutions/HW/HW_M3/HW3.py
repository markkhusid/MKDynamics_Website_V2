#!/usr/bin/env python
# coding: utf-8

# ## Import Libraries

# In[1]:


import numpy as np                     # needed for arrays
from numpy.linalg import solve         # needed for matrices
from read_netlist import read_netlist  # supplied function to read the netlist
import comp_constants as COMP          # needed for the common constants

# My ngspice circuit solver
from solve_circuit_ngspice import solve_circuit_ngspice
from solve_circuit_ngspice import pretty_print_results


# # HW3

# In[2]:


################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - HW3.py
# Mark Khusid
################################################################################

################################################################################
# Problem Modified Nodel Analysis Circuit Simulator: 
################################################################################


# ## Set Debug State

# In[3]:


#DEBUG = True
DEBUG = False


# ### Define Functions

# ### Define get_dimensions() Function

# In[4]:


################################################################################
# How large a matrix is needed for netlist? This could have been calculated    #
# at the same time as the netlist was read in but we'll do it here             #
# Input:                                                                       #
#   netlist: list of component lists                                           #
# Outputs:                                                                     #
#   node_cnt: number of nodes in the netlist                                   #
#   volt_cnt: number of voltage sources in the netlist                         #
################################################################################
def get_dimensions(netlist):
    # Initialize lists to hold node numbers and voltage sources
    i_nodes = []    # collect the left nodes (I) of all components  
    j_nodes = []    # collect the right nodes (J) of all components
    vs_list = []    # collect all of the voltage sources

    # go through the netlist line by line to parse each component
    # get the left node number and put into left_node
    # get the right node number and put into right_node
    # append the numbers to their respective lists
    # handle voltage sources by adding to voltage sources list
    for comp in netlist:
        left_node = comp[COMP.I]      # left node = I
        right_node = comp[COMP.J]     # right node = J

        i_nodes.append(left_node)
        j_nodes.append(right_node)

        # check if this component is a voltage source
        if comp[COMP.TYPE] == COMP.VS:
            vs_list.append(comp)      # add the voltage source to the list

    # find the highest node number
    max_i = max(i_nodes)    # highest left node
    max_j = max(j_nodes)    # highest right node
    node_cnt = max(max_i, max_j)      # highest node number overall between left and right

    volt_cnt = len(vs_list)           # number of voltage sources

    return node_cnt, volt_cnt


# ### Read Netlist (print for debug)

# In[5]:


netlist = read_netlist()   # read the netlist
if DEBUG:
    print(netlist)           # debug statement to check the netlist


# ### Get Number of Nodes and Voltage Sources

# In[6]:


node_count, voltage_source_count = get_dimensions(netlist)
if DEBUG:
    print(f"Number of nodes: {node_count}") # debug statement to check node count
    print(f"Number of voltage sources: {voltage_source_count}") # debug statement to check


# ### Define stamper() Function

# In[7]:


################################################################################
# Function to stamp the components into the netlist                            #
# Input:                                                                       #
#   y_add:    the admittance matrix                                            #
#   netlist:  list of component lists                                          #
#   currents: the matrix of currents                                           #
#   node_cnt: the number of nodes in the netlist                               #
# Outputs:                                                                     #
#   node_cnt: the number of rows in the admittance matrix                      #
################################################################################


# In[8]:


def stamper(y_add,netlist,currents,node_cnt):
    # return the total number of rows in the matrix for
    # error checking purposes
    # add 1 for each voltage source...

    # Initialize the voltage source counter variable
    voltage_source_count = 0 

    # Initialize the extra dimension variable for voltage sources
    extra_dimension = 0

    for comp in netlist:                  # for each component...
        #print(' comp ', comp)            # which one are we handling...

        # extract the i,j and fill in the matrix...
        # subtract 1 since node 0 is GND and it isn't included in the matrix
        i = comp[COMP.I] - 1
        j = comp[COMP.J] - 1


        # Handle resistors
        if ( comp[COMP.TYPE] == COMP.R ):           # a resistor
            if DEBUG:
                print(f"Stamping resistor: {comp[COMP.NAME]}") # debug statement to check resistor stamping
                # Print out the resistors value, and the nodes it connects to for debugging
                print(f"Resistor {comp[COMP.NAME]} connects nodes {comp[COMP.I]} and {comp[COMP.J]} with value {comp[COMP.VAL]}")
                print(f"Admittance of resistor {comp[COMP.NAME]}: {1.0/comp[COMP.VAL]}") # debug statement to check admittance calculation
                print(f"Admittance matrix before stamping resistor: \n{y_add}") # debug statement to check admittance matrix before stamping resistor

            admittance = 1.0/comp[COMP.VAL]             # calculate the admittance

            if (i >= 0):                            # add on the diagonal
                if DEBUG:
                    print(f"Adding admittance {admittance} to diagonal element y[{i},{i}]")
                y_add[i,i] += admittance

            if (j >= 0):                            # add on the diagonal
                if DEBUG:
                    print(f"Adding admittance {admittance} to diagonal element y[{j},{j}]")
                y_add[j,j] += admittance

            if (i >= 0 and j >= 0):                 # add on the off-diagonal
                if DEBUG:
                    print(f"Subtracting admittance {admittance} from off-diagonal elements y[{i},{j}] and y[{j},{i}]")
                y_add[i,j] -= admittance
                y_add[j,i] -= admittance

            if DEBUG:
                print(f"Updated admittance matrix after stamping resistor: \n{y_add}") # debug statement to check admittance matrix after stamping resistor

        # Handle current sources
        elif ( comp[COMP.TYPE] == COMP.IS ):       # a current source
            if DEBUG:
                print(f"Stamping current source: {comp[COMP.NAME]}") # debug statement to check current source stamping
                # Print current vector before stamping current source for debugging
                print(f"Current vector before stamping current source: \n{currents}") # debug statement to check currents vector before stamping current source
                # Print out the current source's value, and the nodes it connects to for debugging
                print(f"Current source {comp[COMP.NAME]} connects nodes {comp[COMP.I]} and {comp[COMP.J]} with value {comp[COMP.VAL]}")

            if (i >= 0):                            # add on the current to the currents vector
                if DEBUG:
                    print(f"Subtracting current {comp[COMP.VAL]} from currents[{i}]")
                currents[i] -= comp[COMP.VAL]

            if (j >= 0):
                if DEBUG:
                    print(f"Adding current {comp[COMP.VAL]} to currents[{j}]")
                currents[j] += comp[COMP.VAL]

            if DEBUG:
                print(f"Updated currents vector after stamping current source: \n{currents}") # debug statement to check currents vector after stamping current source

        # Handle voltage sources
        elif ( comp[COMP.TYPE] == COMP.VS ):       # a voltage source
            if DEBUG:
                print(f"Stamping voltage source: {comp[COMP.NAME]}") # debug statement to check voltage source stamping
                # Print out the voltage source's value, and the nodes it connects to for debugging
                print(f"Voltage source {comp[COMP.NAME]} connects nodes {comp[COMP.I]} and {comp[COMP.J]} with value {comp[COMP.VAL]}")

            extra_dimension = node_cnt + voltage_source_count  # calculate the extra dimension for the voltage source
            voltage_source_count += 1  # increment the voltage source counter

            if ( i >= 0 ):
                if DEBUG:
                    print(f"Adding 1.0 to admittance matrix elements y[{i},{extra_dimension}] and y[{extra_dimension},{i}] for voltage source {comp[COMP.NAME]}")
                y_add[i, extra_dimension] += 1.0
                y_add[extra_dimension, i] += 1.0

            if ( j >= 0 ):
                if DEBUG:
                    print(f"Subtracting 1.0 from admittance matrix elements y[{j},{extra_dimension}] and y[{extra_dimension},{j}] for voltage source {comp[COMP.NAME]}")
                y_add[j, extra_dimension] -= 1.0
                y_add[extra_dimension, j] -= 1.0

            if DEBUG:
                print(f"Adding voltage source value {comp[COMP.VAL]} to currents vector at index {extra_dimension} for voltage source {comp[COMP.NAME]}")
            currents[extra_dimension] = comp[COMP.VAL]  # add the voltage source value to the currents vector at the extra dimension

            if DEBUG:
                print(f"Updated admittance matrix after stamping voltage source: \n{y_add}") # debug statement to check admittance matrix after stamping voltage source
                print(f"Updated currents vector after stamping voltage source: \n{currents}") # debug statement to check currents vector after stamping voltage source

    return node_cnt  # should be same as number of rows!


# ### Define Size of Circuit Matrix

# In[9]:


matrix_size = node_count + voltage_source_count  # total size of the matrix including extra dimensions for voltage sources
if DEBUG:
    print(f"Total matrix size (including extra dimensions for voltage sources): {matrix_size}") # debug statement to check total matrix size


# ### Create Circuit Matrix and Current Vector

# In[10]:


# Create the admittance matrix and currents vector with the appropriate size
y_add = np.zeros((matrix_size, matrix_size))  # initialize the admittance matrix
currents = np.zeros(matrix_size)              # initialize the currents vector


# ## Process the Circuit with Stamper

# In[11]:


# Test the stamper function with the netlist, admittance matrix, currents vector, and node count
final_node_count = stamper(y_add, netlist, currents, node_count)


# ## Solve the Circuit!

# In[12]:


# Solve the system of equations to find the node voltages
voltages_result = np.linalg.solve(y_add, currents)

# Print out the voltages for debugging
if DEBUG:
    print(f"Node voltages: \n{voltages_result}")


# ## Use NGSpice to Verify Results

# In[13]:


# Solve the circuit using ngpsice function for comparison
if DEBUG:
    ngspice_voltages = solve_circuit_ngspice("voltage_source_netlist.txt") # pass the filename of the netlist to the ngspice solver
    #print(f"Node voltages from ngspice: \n{ngspice_voltages}")


# ## Obtain Average Voltage and Print Appropriate Message

# In[14]:


# Analyze the results and print out the average voltage for the nodes
if voltage_source_count == 0:
    voltages = voltages_result
    avg = np.mean(voltages)
    print(f"Vector is {voltages}")
    print(f"Node voltages’ average is {avg} Volts. There are no voltage sources in the circuit")
else:
    voltages = voltages_result[0:node_count]          # only the first node_count entries are voltages, the rest are the currents in the voltage sources.
    avg = np.mean(voltages)
    print(f"Vector is {voltages_result}")
    print(f"Voltages average is {avg} Volts")

