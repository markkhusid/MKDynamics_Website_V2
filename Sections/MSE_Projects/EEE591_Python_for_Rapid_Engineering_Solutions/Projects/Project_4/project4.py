#!/usr/bin/env python3.7

##########################################################################################
# EEE591_419 Python for Rapid Engineering Solutions - Project 4: project4.py
# Mark Khusid
##########################################################################################

##########################################################################################
# Project 3
##########################################################################################

###############################################################################
#
# Uses Python to automatically generate HSPICE netlists, run HSPICE,
# extract propagation delay measurements, and determine the optimal
# inverter chain configuration.
#
# Optimization Variables:
#   fan = stage sizing ratio
#   N   = total number of inverters (odd to preserve inversion)
#
# Objective:
#   Minimize tphl delay from the input of the first inverter to the
#   output of the final inverter driving a 30 pF load.
###############################################################################

import os
# Import the os module to interact with the operating system, primarily for file existence checks.

import subprocess
# Import subprocess to run external commands (HSPICE simulator) from within Python.

import numpy as np
# Import NumPy for efficient handling of numerical data from HSPICE output CSV files.


def write_netlist(fan, N, filename="InvChain.sp"):
    """
    Create an HSPICE netlist for an odd-numbered inverter chain.
    fan controls the size ratio between stages.
    N is the total number of inverters.
    """
    # Function to generate an HSPICE-compatible netlist file (.sp) for a chain of inverters.
    # Parameters:
    #   - fan: Fanout factor (sizing multiplier between consecutive stages).
    #   - N: Number of inverter stages (must be odd for this lab setup).
    #   - filename: Output netlist filename (default: InvChain.sp).

    netlist = """Lab 1 Problem 1A
* Bring in the library
.lib 'cmoslibrary.lib' nominal
* My VCC is
.param pvcc = 3
* Sizing Variables
.param alpha = 1.7
.param fan = {fan}
* Set Power and Ground as Global
.global vcc! gnd!
.subckt inv A Z
  m1 Z A gnd! gnd! nmos w=1.4u l=0.35u AD=0.7p
  m2 Z A vcc! vcc! pmos w=(1.4u*alpha) l=0.35u AD=0.7p*alpha
.ends
Cload z gnd! 30pF
Vin a gnd! 0V PWL 0 0NS 1NS 3 20NS 3
* Power Supplies
Vgnd gnd! 0 DC = 0
Vvcc vcc! 0 DC = 3V
* Analysis
.tran 1NS 100NS
.print tran v(a) v(z)
.OPTION MEASFORM=3
.OPTION POST
.TEMP 25
.measure TRAN tphl_inv TRIG v(a) VAL=1.5 RISE=1 TARG v(z) VAL=1.5 FALL=1
""".format(fan=fan)
    # Multi-line string template for the base HSPICE netlist.
    # This includes:
    #   - Library inclusion (cmoslibrary.lib).
    #   - Parameter definitions (Vcc=3V, alpha=1.7 for PMOS/NMOS sizing ratio, fan passed from Python).
    #   - Global power/ground nodes.
    #   - Subcircuit definition for a single inverter (NMOS/PMOS transistors with area/diffusion params).
    #   - Load capacitance (30pF on output).
    #   - Input voltage source (piecewise linear ramp for transient simulation).
    #   - Power supply sources.
    #   - Transient analysis command (.tran).
    #   - Print statement for waveforms.
    #   - Measurement command to extract tphl_inv (high-to-low propagation delay).
    # .format() injects the fan value into the .param line.

    # Generate inverter chain
    for i in range(N):
        # Loop over each inverter stage (0 to N-1).
        stage_number = i + 1
        # Human-readable stage number (starts at 1).

        if i == 0:
            input_node = "a"
        else:
            input_node = "n{}".format(i)
        # Determine input node name: first stage uses primary input 'a'; subsequent stages use intermediate nodes 'nX'.

        if i == N - 1:
            output_node = "z"
        else:
            output_node = "n{}".format(i + 1)
        # Determine output node name: last stage drives 'z' (loaded output); others drive next stage's input.

        netlist += "Xinv{} {} {} inv M=fan**{}\n".format(
            stage_number,
            input_node,
            output_node,
            i
        )
        # Append an instance of the 'inv' subcircuit.
        # M= multiplier scales transistor widths by fan**stage_index (geometric progression in sizing).
    # End of chain generation loop.

    netlist += ".end\n"
    # Final .end statement required by HSPICE to close the netlist.

    with open(filename, "w") as f:
        f.write(netlist)
    # Write the complete netlist string to the specified file (overwrites if exists).
    # This creates the simulation input file for HSPICE.


def run_hspice(filename="InvChain.sp"):
    """
    Run HSPICE on the generated netlist.
    """
    # Function to execute the HSPICE simulator on the netlist file.
    # Returns True on success, False on failure.

    proc = subprocess.Popen(
        ["hspice", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Launch HSPICE as a subprocess, passing the netlist filename as argument.
    # Capture stdout and stderr for error handling/logging.

    output, err = proc.communicate()
    # Wait for the process to complete and retrieve output streams.

    if proc.returncode != 0:
        print("HSPICE failed.")
        print(err.decode("utf-8", errors="ignore"))
        return False
    # Check return code. Non-zero indicates error (e.g., syntax issue in netlist, missing library).
    # Print error details for debugging.

    return True
    # Success case.


def read_delay(filename="InvChain.mt0.csv"):
    """
    Read tphl_inv from the HSPICE measurement output file.
    """
    # Function to parse the measurement results from HSPICE's .mt0.csv output file.
    # Returns the measured tphl_inv delay (in seconds) or None on failure.

    if not os.path.exists(filename):
        return None
    # Safety check: HSPICE may not have produced the measurement file if the run failed.

    data = np.recfromcsv(filename, comments="$", skip_header=3)
    # Use NumPy to read the CSV file.
    # comments="$" skips HSPICE header lines starting with $.
    # skip_header=3 accounts for metadata rows before the actual data table.

    try:
        delay = data["tphl_inv"]
    except Exception:
        return None
    # Extract the column corresponding to the .measure tphl_inv result.
    # Exception handling for cases where the measurement is missing.

    # Handles scalar or array result
    if np.ndim(delay) > 0:
        delay = delay[0]
    # HSPICE sometimes returns arrays even for single measurements; flatten to scalar.

    return float(delay)
    # Convert to Python float and return.


def main():
    # Main driver function: Performs parameter sweep over fan and N values,
    # runs simulations, collects results, and identifies the minimum delay configuration.

    fan_values = range(2, 11)
    # Fanout values to sweep: 2 through 10 (inclusive).

    # Odd number of inverters only
    N_values = range(1, 22, 2)
    # Number of stages: 1, 3, 5, ..., 21 (odd numbers only, as per lab requirements for ring/inverter chain).

    results = []
    # List to store all (fan, N, delay) tuples for potential further analysis.

    best_delay = None
    best_fan = None
    best_N = None
    # Variables to track the configuration with the smallest propagation delay.

    for fan in fan_values:
        for N in N_values:
            # Nested loops: brute-force sweep over all combinations of fan and N.

            write_netlist(fan, N)
            # Generate a fresh netlist for the current parameters.

            success = run_hspice()
            # Execute HSPICE simulation.

            if not success:
                print("fan={}, N={}, delay=FAILED".format(fan, N))
                continue
            # Skip to next iteration on simulation failure.

            delay = read_delay()
            if delay is None:
                print("fan={}, N={}, delay=NO MEASUREMENT".format(fan, N))
                continue
            # Skip if measurement could not be read.

            results.append((fan, N, delay))
            # Record successful result.

            print("fan={}, N={}, delay={:.6e}".format(fan, N, delay))
            # Print progress in scientific notation for readability.

            if best_delay is None or delay < best_delay:
                best_delay = delay
                best_fan = fan
                best_N = N
            # Update best result if this delay is smaller (or first valid result).
    # End of double loop.

    print()
    print("Optimal Result")
    print("--------------")
    print("Best fan = {}".format(best_fan))
    print("Best N = {}".format(best_N))
    print("Best delay = {:.6e}".format(best_delay))
    # Summary output showing the optimal (fan, N) pair that minimizes tphl_inv.


if __name__ == "__main__":
    main()
# Standard Python idiom: Run main() only when the script is executed directly (not imported as a module).
