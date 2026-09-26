"""OPA365 Figure 8-6 three-pole Sallen–Key filter analysis package.

This package supports analytical transfer functions (including op-amp
non-ideals), ngspice/LTspice simulation, worst-case, Monte Carlo,
temperature, sensitivity, and derating studies.

Extending to another netlist / schematic
----------------------------------------
Most users only need to change *parameters* and *netlist generation*:

1. Edit component values / tolerances in ``params.py`` (or override them
   in a notebook cell — every notebook has an editable parameter block).
2. For a **different topology**, either:
   a. Provide your own SPICE netlist path to ``simulate.run_external_netlist``
      / ``ltspice_io.run_ltspice_deck`` (recommended for arbitrary circuits), or
   b. Modify ``netlist.build_fig86_netlist`` and the nodal model in
      ``analysis.py`` if you still want a closed-form analytical H(s).
3. Keep node names documented in your netlist so ``.meas`` / print statements
   remain valid, or update the parser keys in ``simulate.py`` / ``ltspice_io.py``.

The Figure 8-6 circuit is the *reference case*, not a hard limit of the tooling.
"""

from .params import CircuitParams, OpampParams, ToleranceSpec, OperatingPoint

__all__ = [
    "CircuitParams",
    "OpampParams",
    "ToleranceSpec",
    "OperatingPoint",
]

__version__ = "0.1.0"
