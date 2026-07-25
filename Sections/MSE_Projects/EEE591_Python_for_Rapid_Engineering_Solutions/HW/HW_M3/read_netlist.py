################################################################################
# read netlist file and create a list of lists...                              #
################################################################################

import comp_constants as COMP    # get the constants needed for lists
from sys import exit             # needed to exit on error

# Set debug state
DEBUG = False

################################################################################
# Read a netlist from a spice-like text file                                   #
# Input:                                                                       #
#   none                                                                       #
# Outputs:                                                                     #
#   netlist: a list of components, each component as a list                    #
#                                                                              #
# this is the list structure that we'll use to hold components:                #
# [ Type, Name, i, j, Value ]                                                  #
################################################################################

def read_netlist():              # read a netlist - no input argument!
    filename = input("enter netlist text file name: ")      # ask for the netlist
    #print(filename)                                      # debug statement
    #filename = 'voltage_source_netlist.txt'                            # for debug, hardcode the filename
    #filename = 'current_source_netlist.txt'                            # for debug, hardcode the filename
    if DEBUG:
        print(f"Reading netlist from file: {filename}") # debug statement
    
    fh = open(filename,"r")                               # open the file
    
    if DEBUG:
        print(f"File {filename} opened successfully.") # debug statement
    
    lines = fh.readlines()                                # read the file
    
    if DEBUG:
        print(f"Read {len(lines)} lines from the file.") # debug statement
    
    fh.close()                                            # close the file
    
    if DEBUG:
        print(f"File {filename} closed successfully.") # debug statement

    netlist = []                                          # initialize our list
    for line in lines:                                    # for each component
        line=line.strip()                                 # strip CR/LF
        
        if DEBUG:
            print(f"Processing line: '{line}'") # debug statement to check the line being processed
            print(f"Line split into: {line.split(' ')}") # debug statement to check the split line
        
        if line:                                          # skip empty lines

            # reads: name, from, to, value
            # so we need to insert the node type at the start of the list
            # parse properties delimited by spaces
            props = line.split(" ")

            if ( props[COMP.TYPE][0] == COMP.RESIS ):     # is it a resistor?
                if DEBUG:
                    print(f"Identified resistor: {props[COMP.NAME]}") # debug statement to check resistor identification
                props.insert(COMP.TYPE,COMP.R)            # insert type
                props[COMP.I]   = int(props[COMP.I])      # convert from string
                props[COMP.J]   = int(props[COMP.J])      # convert from string
                props[COMP.VAL] = float(props[COMP.VAL])  # convert from string
                if DEBUG:
                    print(f"Parsed resistor properties: {props}") # debug statement to check parsed properties
                netlist.append(props)                     # add to our netlist

            elif ( props[COMP.TYPE][0:2] == COMP.V_SRC ): # a voltage source?
                if DEBUG:
                    print(f"Identified voltage source: {props[COMP.NAME]}") # debug statement to check voltage source identification
                props.insert(COMP.TYPE,COMP.VS)           # insert type
                props[COMP.I]   = int(props[COMP.I])      # convert from string
                props[COMP.J]   = int(props[COMP.J])      # convert from string
                props[COMP.VAL] = float(props[COMP.VAL])  # convert from string
                if DEBUG:
                    print(f"Parsed voltage source properties: {props}") # debug statement to check parsed properties
                netlist.append(props)                     # add to our netlist

            elif ( props[COMP.TYPE][0:2] == COMP.I_SRC ): # a current source?
                if DEBUG:
                    print(f"Identified current source: {props[COMP.NAME]}") # debug statement to check current source identification
                props.insert(COMP.TYPE,COMP.IS)           # insert type
                props[COMP.I]   = int(props[COMP.I])      # convert from string
                props[COMP.J]   = int(props[COMP.J])      # convert from string
                props[COMP.VAL] = float(props[COMP.VAL])  # convert from string
                if DEBUG:
                    print(f"Parsed current source properties: {props}") # debug statement to check parsed properties
                netlist.append(props)                     # add to our netlist

            else:                                         # unknown component!
                print("Unknown component type:\n",line)   # bad data!
                exit()                                    # bail!

    return netlist
