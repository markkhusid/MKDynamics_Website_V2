"""Stress and derating analysis for Fig. 8-6 passives + op-amp rails.

Resistors: 0805 package, power vs temperature derating curve.
Capacitors: 50 V rated, recommended use fraction of VR.

Stress estimates use worst-case large-signal mid-rail swing
(Vin = 2.5 ± 2.5 V).  For this unity-gain LPF in the passband,
node voltages closely follow Vin, so resistor voltages are small
differences along the ladder; we bound conservatively.

HOW TO ADAPT FOR ANOTHER NETLIST
--------------------------------
Replace ``estimate_stresses`` with currents/voltages from your SPICE ``.op``
or ``.tran`` measurements (preferred for complex networks).  Keep the
``DeratingParams`` rules and ``evaluate_derating`` so the pass/fail table
format stays the same for notebooks.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .params import CircuitParams


@dataclass
class StressEstimate:
    """Electrical stress on one component."""

    name: str
    kind: str  # 'R' or 'C' or 'U'
    v_peak: float
    i_rms_est: float
    p_est: float
    notes: str = ""


def estimate_stresses(p: CircuitParams | None = None) -> list[StressEstimate]:
    """Conservative analytical stress bounds for Fig. 8-6.

    Approach
    --------
    In the deep passband, Vn1≈Vn2≈Vn3≈Vout≈Vin.  Resistor currents are then
    dominated by residual drops from offset/bias and by high-frequency
    capacitor currents.  For derating we use a **bound**:
    * Max differential across any series R ≤ full input span (5 V) as an
      absolute ceiling (pessimistic).
    * More realistic passband bound: simulate DC at Vin max/min and take
      |I| through each R from nodal DC solution with ideal unity gain.

    We use the nodal DC solution at Vin = vmin and vmax for realistic
    currents, then take the max |I| and |V| over those points.
    """
    from .analysis import solve_frequency

    if p is None:
        p = CircuitParams()

    vins = [p.op.v_in_min, p.op.v_in_bias, p.op.v_in_max]
    # Collect peak |V| and |I| per element
    r_names = [("R1", "vin", "V1"), ("R2", "V1", "V2"), ("R3", "V2", "V3")]
    peaks_v = {n: 0.0 for n, _, _ in r_names}
    peaks_i = {n: 0.0 for n, _, _ in r_names}
    c_peaks = {"C1": 0.0, "C2": 0.0, "C3": 0.0}

    for vin in vins:
        sol = solve_frequency(0.0, p, vin=vin, vos=0.0, ibp=0.0, ibn=0.0)
        # map
        vals = {
            "vin": vin,
            "V1": sol["V1"].real,
            "V2": sol["V2"].real,
            "V3": sol["V3"].real,
            "Vout": sol["Vout"].real,
        }
        for n, a, b in r_names:
            vr = abs(vals[a] - vals[b])
            peaks_v[n] = max(peaks_v[n], vr)
            R = getattr(p, n)
            peaks_i[n] = max(peaks_i[n], vr / R if R > 0 else 0.0)
        # Capacitor DC voltage = node-to-ref (C3: n2 to vout → ~0 in passband)
        c_peaks["C1"] = max(c_peaks["C1"], abs(vals["V1"]))
        c_peaks["C2"] = max(c_peaks["C2"], abs(vals["V3"]))
        c_peaks["C3"] = max(c_peaks["C3"], abs(vals["V2"] - vals["Vout"]))

    # Add a small AC current allowance for caps at design freq with full-scale Vin
    # I_c ≈ 2π f C Vpk  (order-of-magnitude for RMS stress discussion)
    f = p.op.f_design_hz
    vpk = p.op.v_in_peak
    # Not added to voltage stress; voltage remains DC-like bound above.

    out: list[StressEstimate] = []
    for n, _, _ in r_names:
        R = getattr(p, n)
        i = peaks_i[n]
        # If ideal DC equal voltages, I≈0 — use a floor from Ib through chain
        i_floor = abs(p.opamp.ib_max)  # tiny
        i_use = max(i, i_floor)
        # Also consider transient charging: bound I by C dV/dt ~ C * (2π f Vpk)
        # reflected through nearby R — keep simple: power from VR^2/R with a
        # minimum VR of 1 mV for numerical display when nearly zero.
        vr = max(peaks_v[n], 1e-6)
        pwr = vr**2 / R
        out.append(
            StressEstimate(
                name=n,
                kind="R",
                v_peak=vr,
                i_rms_est=i_use,
                p_est=pwr,
                notes="from DC nodal extremes; passband |VR| often near 0",
            )
        )

    # Capacitor AC voltage bound: up to Vin peak about bias on shunt caps
    # C1 sees ~Vin, C2 sees ~Vin, C3 sees small residual
    # Use max of DC nodal and Vbias+Vpeak for shunt caps (conservative)
    v_abs_max = max(abs(p.op.v_in_max), abs(p.op.v_in_min), p.op.v_supply)
    for cn, v_est in c_peaks.items():
        # shunt caps: allow full rail as absolute ceiling annotation
        v_use = max(v_est, v_abs_max if cn != "C3" else v_est)
        if cn == "C3":
            # feedback cap: differential; bound by small SK error — use at least peak AC estimate
            v_use = max(v_est, 0.1)  # 0.1 V placeholder floor for display if ~0
        out.append(
            StressEstimate(
                name=cn,
                kind="C",
                v_peak=v_use,
                i_rms_est=2 * np.pi * f * getattr(p, cn) * vpk,
                p_est=0.0,
                notes="voltage bound from bias/swing; I~2πfCV for AC",
            )
        )

    # Op-amp rails
    out.append(
        StressEstimate(
            name=p.opamp.name,
            kind="U",
            v_peak=p.op.v_supply,
            i_rms_est=4.6e-3,  # Iq typ from datasheet
            p_est=p.op.v_supply * 4.6e-3,
            notes="Iq typ 4.6 mA; supply within 2.2–5.5 V",
        )
    )
    return out


def evaluate_derating(
    p: CircuitParams | None = None,
    *,
    temp_c: float = 25.0,
    stresses: list[StressEstimate] | None = None,
) -> pd.DataFrame:
    """Build pass/fail derating table at ambient ``temp_c``."""
    if p is None:
        p = CircuitParams()
    if stresses is None:
        stresses = estimate_stresses(p)
    d = p.derating
    p_der = d.derated_power_w(temp_c)
    p_allow = p_der * d.resistor_power_use_fraction
    v_cap_allow = d.capacitor_v_max_recommended

    rows = []
    for s in stresses:
        if s.kind == "R":
            limit = p_allow
            stress_val = s.p_est
            limit_name = f"P_allow ({d.resistor_package} @{temp_c:.0f}°C)"
            margin = (limit - stress_val) / limit * 100 if limit > 0 else float("nan")
            ok = stress_val <= limit
            rows.append(
                {
                    "component": s.name,
                    "package_or_rating": d.resistor_package,
                    "stress_type": "power",
                    "stress_value": stress_val,
                    "stress_unit": "W",
                    "limit_value": limit,
                    "derated_full_W": p_der,
                    "rated_W": d.resistor_power_rated_w,
                    "margin_percent": margin,
                    "pass": ok,
                    "notes": s.notes,
                }
            )
            # Also voltage (use 150 V typical 0805 working voltage as soft limit)
            v_lim = 150.0
            rows.append(
                {
                    "component": s.name,
                    "package_or_rating": d.resistor_package,
                    "stress_type": "voltage",
                    "stress_value": s.v_peak,
                    "stress_unit": "V",
                    "limit_value": v_lim,
                    "derated_full_W": p_der,
                    "rated_W": d.resistor_power_rated_w,
                    "margin_percent": (v_lim - s.v_peak) / v_lim * 100,
                    "pass": s.v_peak <= v_lim,
                    "notes": "soft 0805 working-voltage guideline 150 V",
                }
            )
        elif s.kind == "C":
            rows.append(
                {
                    "component": s.name,
                    "package_or_rating": f"{d.capacitor_v_rated:.0f} V",
                    "stress_type": "voltage",
                    "stress_value": s.v_peak,
                    "stress_unit": "V",
                    "limit_value": v_cap_allow,
                    "derated_full_W": float("nan"),
                    "rated_W": float("nan"),
                    "margin_percent": (v_cap_allow - s.v_peak) / v_cap_allow * 100,
                    "pass": s.v_peak <= v_cap_allow,
                    "notes": s.notes
                    + f"; rule: ≤{d.capacitor_v_use_fraction*100:.0f}% of VR",
                }
            )
        else:
            # Op-amp supply window
            rows.append(
                {
                    "component": s.name,
                    "package_or_rating": "2.2–5.5 V",
                    "stress_type": "supply",
                    "stress_value": s.v_peak,
                    "stress_unit": "V",
                    "limit_value": 5.5,
                    "derated_full_W": float("nan"),
                    "rated_W": float("nan"),
                    "margin_percent": (5.5 - s.v_peak) / 5.5 * 100,
                    "pass": 2.2 <= s.v_peak <= 5.5,
                    "notes": s.notes,
                }
            )
            rows.append(
                {
                    "component": s.name,
                    "package_or_rating": "Iq / Pd",
                    "stress_type": "power",
                    "stress_value": s.p_est,
                    "stress_unit": "W",
                    "limit_value": 0.5,  # generous package-level placeholder
                    "derated_full_W": float("nan"),
                    "rated_W": float("nan"),
                    "margin_percent": (0.5 - s.p_est) / 0.5 * 100,
                    "pass": s.p_est <= 0.5,
                    "notes": s.notes,
                }
            )
    return pd.DataFrame(rows)


def power_derating_curve(
    p: CircuitParams | None = None,
    temps: np.ndarray | None = None,
) -> pd.DataFrame:
    """Full vs derated allowable resistor power vs ambient temperature."""
    if p is None:
        p = CircuitParams()
    if temps is None:
        temps = np.linspace(-40, 160, 41)
    d = p.derating
    rows = []
    for T in temps:
        p_full = d.derated_power_w(float(T))
        rows.append(
            {
                "temp_c": float(T),
                "p_rated_curve_W": p_full,
                "p_allow_W": p_full * d.resistor_power_use_fraction,
            }
        )
    return pd.DataFrame(rows)
