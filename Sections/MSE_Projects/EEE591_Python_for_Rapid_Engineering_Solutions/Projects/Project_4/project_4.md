# Project 4 — CMOS Inverter Chain Optimization

*Built with Grok Build*

## Overview

Project 4 uses **Python to drive HSPICE** for a classic VLSI / digital circuits design problem:
sizing a chain of CMOS inverters to drive a large capacitive load with minimal delay.

Course: **EEE591 / EEE419 Python for Rapid Engineering Solutions**.

## Problem statement (summary)

Given a **30 pF** load, automatically:

1. Generate HSPICE netlists for an inverter chain (`InvChain.sp`) parameterized by:
   - `fan` — stage sizing ratio
   - `N` — number of inverter stages (odd, to preserve logic inversion)
2. Run HSPICE from Python (`subprocess`)
3. Extract propagation delay metrics from simulator output
4. Search the design space to **minimize high-to-low propagation delay** (`tphl`) from the first
   inverter input to the final inverter output

Supporting files in this folder include the CMOS library (`cmoslibrary.lib`) and generated
netlists such as `InvChain.sp`.

## Solution script

```{literalinclude} project4.py
:language: python
:linenos:
```

## How to run

Requires a working **HSPICE** installation on the host and a compatible Python 3 environment:

```bash
python3 project4.py
```

The script writes netlists, invokes the simulator, and reports the best `(fan, N)` configuration
found for the delay objective.
