"""OPA365 Figure 8-5 multiple-feedback low-pass filter analysis.

Analytical transfer functions (including op-amp non-ideals), ngspice and
LTspice checks, worst-case, Monte Carlo, temperature, sensitivity, and
derating for the 500 kHz Butterworth filter in datasheet Figure 8-5.
"""

from .params import CircuitParams, OpampParams, ToleranceSpec, OperatingPoint

__all__ = [
    "CircuitParams",
    "OpampParams",
    "ToleranceSpec",
    "OperatingPoint",
]

__version__ = "0.1.0"
