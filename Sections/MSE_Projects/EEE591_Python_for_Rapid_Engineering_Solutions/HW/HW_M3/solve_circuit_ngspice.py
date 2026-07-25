import subprocess
import sys
import os
from pathlib import Path
import tempfile

# NOTE TO GRADER: This AI generated code is used only to check my results and NOT FOR CREDIT.
def solve_circuit_ngspice(netlist_file: str):
    """
    Reads your custom netlist file (R, VS*, IS* only), runs ngspice DC operating point,
    and prints node voltages + element currents for easy comparison with your solver.
    """
    # Read the raw netlist (exact format you provided)
    with open(netlist_file, 'r') as f:
        user_lines = [line.strip() for line in f.readlines()
                      if line.strip() and not line.strip().startswith(('*', '.'))]

    # Collect nodes and elements, preserving original casing and order
    nodes = set()
    elements = []           # keep original refdes (e.g. "VS", "R1")
    elem_map = {}           # lowercased -> original (for ngspice output matching)

    for line in user_lines:
        parts = line.split()
        if len(parts) >= 3:
            refdes = parts[0]
            na, nb = parts[1], parts[2]
            nodes.add(na)
            nodes.add(nb)
            elements.append(refdes)
            elem_map[refdes.lower()] = refdes

    # Build complete ngspice netlist
    netlist = ["* Generated netlist for ngspice - DC solve"]
    netlist.extend(user_lines)
    netlist.append(".control")
    netlist.append("op")                     # DC operating point analysis

    # Print voltage at every node
    node_list = sorted(nodes, key=lambda x: (int(x) if str(x).isdigit() else 999, str(x)))
    for node in node_list:
        netlist.append(f"print v({node})")

    # Print current through every element — IMPORTANT FIX:
    #   • Voltage/current sources (V*, I*):   print i(REFDES)
    #   • Resistors (R*):                     print @REFDES[i]
    #   ngspice only supports i() for sources and @elem[i] for passives
    for elem in elements:
        if elem.upper().startswith(('V', 'I')):
            netlist.append(f"print i({elem})")
        else:
            # Resistors and any other passive elements
            netlist.append(f"print @{elem}[i]")

    netlist.append(".endc")
    netlist.append(".end")

    netlist_str = "\n".join(netlist)

    # Write to temporary .cir file and run ngspice
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cir', delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(netlist_str)

    try:
        # -b = batch mode (no interactive prompt)
        result = subprocess.run(
            ["ngspice", "-b", tmp_path],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
    except FileNotFoundError:
        print("ERROR: 'ngspice' command not found.")
        print("Please install ngspice and make sure it is in your PATH.")
        print("   • Linux:   sudo apt install ngspice")
        print("   • macOS:   brew install ngspice")
        print("   • Windows: Download from https://ngspice.sourceforge.io/download.html")
        return None
    except subprocess.CalledProcessError as e:
        print("ngspice failed to run:")
        print(e.stderr)
        return None
    finally:
        # Cleanup temp file
        Path(tmp_path).unlink(missing_ok=True)

    # Parse the output - now handles BOTH formats:
    #   "i(vs) = -2.00000e+00"
    #   "@r1[i] = 2.00000e+00"
    node_voltages = {}
    element_currents = {}   # keys will match your original casing

    for line in output.splitlines():
        line = line.strip()
        if " = " not in line:
            continue
        try:
            var_part, value_part = line.split(" = ", 1)
            var_name = var_part.strip()
            value = float(value_part.strip())

            if var_name.startswith("v(") and var_name.endswith(")"):
                node = var_name[2:-1]
                node_voltages[node] = value

            elif var_name.startswith("i(") and var_name.endswith(")"):
                # Voltage or current source
                elem_lower = var_name[2:-1].lower()
                original_elem = elem_map.get(elem_lower, var_name[2:-1])
                element_currents[original_elem] = value

            elif var_name.startswith("@") and "[i]" in var_name:
                # Resistor (or passive) current: @R1[i]
                start = var_name.find("@") + 1
                end = var_name.find("[i]")
                if start > 0 and end > start:
                    elem_lower = var_name[start:end].lower()
                    original_elem = elem_map.get(elem_lower, var_name[start:end])
                    element_currents[original_elem] = value

        except ValueError:
            continue  # skip any malformed line

    # Pretty output for easy comparison with your own solver
    print("=== NGSPICE DC OPERATING POINT RESULTS ===")
    print("\nNode Voltages (V):")
    for node in node_list:
        v = node_voltages.get(node, 0.0)
        print(f"  V({node:>3}) = {v:12.6f} V")

    print("\nElement Currents (A):")
    print("  (positive = current flowing from first node to second node in your netlist)")
    for elem in elements:  # preserve exact order and original casing
        i_val = element_currents.get(elem)
        if i_val is not None:
            print(f"  I({elem:>4}) = {i_val:12.6f} A")
        else:
            print(f"  I({elem:>4}) = [not found]")

    # Return data if you want to use it programmatically
    return {
        "node_voltages": node_voltages,
        "element_currents": element_currents,
        "raw_output": output,
        "netlist_used": netlist_str
    }

# NOTE TO GRADER: This AI generated code is used only to check my results and NOT FOR CREDIT.
def pretty_print_results(results: dict):
    """
    Pretty-prints the dictionary returned by solve_circuit()
    in a clean, human-readable, aligned table format.

    Example usage:
        results = solve_circuit("my_netlist.txt")
        pretty_print_results(results)
    """
    if not results or not isinstance(results, dict):
        print("ERROR: Invalid or empty results dictionary.")
        return

    node_voltages = results.get("node_voltages", {})
    element_currents = results.get("element_currents", {})
    raw_output = results.get("raw_output", "")
    netlist_used = results.get("netlist_used", "")

    # === HEADER ===
    print("═" * 60)
    print("          NGSPICE DC OPERATING POINT RESULTS")
    print("═" * 60)

    # === NODE VOLTAGES ===
    if node_voltages:
        print("\n NODE VOLTAGES")
        print("─" * 40)
        # Sort nodes numerically when possible
        node_list = sorted(
            node_voltages.keys(),
            key=lambda x: (int(x) if str(x).isdigit() else 999, str(x))
        )
        max_node_width = max((len(n) for n in node_list), default=3)
        for node in node_list:
            v = node_voltages.get(node, 0.0)
            print(f"  V({node:>{max_node_width}}) = {v:12.6f} V")
    else:
        print("\n(No node voltages available)")

    # === ELEMENT CURRENTS ===
    if element_currents:
        print("\n⚡ ELEMENT CURRENTS")
        print("─" * 40)
        print("  (positive = current flowing from first node → second node)")
        # Preserve original order from the netlist (if possible)
        # Fall back to sorted if we don't have the original order
        elements = list(element_currents.keys())
        max_elem_width = max((len(e) for e in elements), default=4)

        for elem in elements:
            i_val = element_currents.get(elem)
            print(f"  I({elem:>{max_elem_width}}) = {i_val:12.6f} A")
    else:
        print("\n(No element currents available)")

    # === OPTIONAL: Show raw ngspice output (uncomment if you want it) ===
    # print("\n RAW NGSPICE OUTPUT")
    # print("─" * 40)
    # print(raw_output.strip())

    # === OPTIONAL: Show the exact netlist that was used ===
    # print("\n NETLIST USED")
    # print("─" * 40)
    # print(netlist_used)

    print("\n" + "═" * 60)
    print("Results ready for comparison with your solver!")
    print("═" * 60)
