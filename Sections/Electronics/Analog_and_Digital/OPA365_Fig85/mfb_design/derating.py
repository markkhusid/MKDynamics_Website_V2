"""Applied voltage and power for the Figure 8-5 parts.

Stress comes from the nodal solution at the study bias plus the 250 kHz,
1 V peak tone. Capacitor voltage is |Vdc| + |Vac| of that phasor. Resistor
power is Vdc²/R + |Vac|²/(2R). No extra voltage is invented for a part
that the solution puts near zero.

Op-amp supply stress is the 5 V span. Dissipation is Vs·Iq plus the load
term |Vout_ac|² / (2 Rload). The 0.5 W figure is the package allowance
used in this study, not a computed thermal resistance.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .params import CircuitParams
from .transient import F_PASSBAND_HZ, TRAN_AMP_V


@dataclass
class StressEstimate:
    name: str
    kind: str
    v_peak: float
    i_rms_est: float
    p_est: float
    notes: str = ""


def _node(sol: dict, name: str, vin_value: complex) -> complex:
    if name == "vin":
        return complex(vin_value)
    return complex(sol[name])


def passband_stresses(
    p: CircuitParams | None = None,
    *,
    freq_hz: float = F_PASSBAND_HZ,
    amp_v: float = TRAN_AMP_V,
) -> list[StressEstimate]:
    from .analysis import solve_frequency

    if p is None:
        p = CircuitParams()
    bias = p.op.v_in_bias
    s = 1j * 2.0 * np.pi * float(freq_hz)
    dc = solve_frequency(0.0, p, vin=bias)
    ac = solve_frequency(s, p, vin=amp_v)
    out: list[StressEstimate] = []
    branches = (
        ("R1", "vin", "V1"),
        ("R2", "V1", "V2"),
        ("R3", "V1", "Vout"),
    )
    for name, a, b in branches:
        vd = _node(dc, a, bias) - _node(dc, b, bias)
        va = _node(ac, a, amp_v) - _node(ac, b, amp_v)
        r = getattr(p, name)
        p_avg = (abs(vd) ** 2) / r + (abs(va) ** 2) / (2.0 * r)
        v_peak = abs(vd) + abs(va)
        out.append(
            StressEstimate(
                name=name,
                kind="R",
                v_peak=float(v_peak),
                i_rms_est=float(np.sqrt(p_avg / r)),
                p_est=float(p_avg),
                notes=f"{freq_hz:.0f} Hz, {amp_v:g} V peak about {bias:g} V",
            )
        )
    caps = (("C1", "V1", None), ("C2", "V2", "Vout"))
    for name, a, b in caps:
        if b is None:
            vd = _node(dc, a, bias)
            va = _node(ac, a, amp_v)
        else:
            vd = _node(dc, a, bias) - _node(dc, b, bias)
            va = _node(ac, a, amp_v) - _node(ac, b, amp_v)
        i_rms = 2.0 * np.pi * freq_hz * getattr(p, name) * abs(va) / np.sqrt(2.0)
        out.append(
            StressEstimate(
                name=name,
                kind="C",
                v_peak=float(abs(vd) + abs(va)),
                i_rms_est=float(i_rms),
                p_est=0.0,
                notes=f"peak |Vdc|+|Vac| at {freq_hz:.0f} Hz",
            )
        )
    vo_ac = _node(ac, "Vout", amp_v)
    p_load = (abs(vo_ac) ** 2) / (2.0 * p.op.r_load)
    iq = p.opamp.iq_typ
    out.append(
        StressEstimate(
            name=p.opamp.name,
            kind="U",
            v_peak=float(p.op.v_supply),
            i_rms_est=float(iq),
            p_est=float(p.op.v_supply * iq + p_load),
            notes=f"supply span; Iq typ plus load ({p_load * 1e6:.2f} µW)",
        )
    )
    return out


def estimate_stresses(p: CircuitParams | None = None) -> list[StressEstimate]:
    """Same operating stress the bar charts use."""
    return passband_stresses(p)


def evaluate_derating(
    p: CircuitParams | None = None,
    *,
    temp_c: float = 25.0,
    stresses: list[StressEstimate] | None = None,
) -> pd.DataFrame:
    if p is None:
        p = CircuitParams()
    if stresses is None:
        stresses = passband_stresses(p)
    d = p.derating
    p_der = d.derated_power_w(temp_c)
    p_allow = p_der * d.resistor_power_use_fraction
    v_cap = d.capacitor_v_max_recommended
    rows = []
    for s in stresses:
        if s.kind == "R":
            rows.append(
                {
                    "component": s.name,
                    "package_or_rating": d.resistor_package,
                    "stress_type": "power",
                    "stress_value": s.p_est,
                    "stress_unit": "W",
                    "limit_value": p_allow,
                    "derated_full_W": p_der,
                    "rated_W": d.resistor_power_rated_w,
                    "margin_percent": (p_allow - s.p_est) / p_allow * 100 if p_allow else float("nan"),
                    "pass": s.p_est <= p_allow,
                    "notes": s.notes,
                }
            )
            v_lim = d.resistor_voltage_guideline
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
                    "notes": "0805 working-voltage guideline, 150 V",
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
                    "limit_value": v_cap,
                    "derated_full_W": float("nan"),
                    "rated_W": float("nan"),
                    "margin_percent": (v_cap - s.v_peak) / v_cap * 100,
                    "pass": s.v_peak <= v_cap,
                    "notes": s.notes + f"; rule is ≤{d.capacitor_v_use_fraction * 100:.0f}% of VR",
                }
            )
        else:
            vmax = p.opamp.v_supply_max
            vmin = p.opamp.v_supply_min
            rows.append(
                {
                    "component": s.name,
                    "package_or_rating": f"{vmin:.1f}–{vmax:.1f} V",
                    "stress_type": "supply",
                    "stress_value": s.v_peak,
                    "stress_unit": "V",
                    "limit_value": vmax,
                    "derated_full_W": float("nan"),
                    "rated_W": float("nan"),
                    "margin_percent": (vmax - s.v_peak) / vmax * 100,
                    "pass": vmin <= s.v_peak <= vmax,
                    "notes": s.notes,
                }
            )
            p_lim = p.opamp.package_power_allow_w
            rows.append(
                {
                    "component": s.name,
                    "package_or_rating": "package allowance",
                    "stress_type": "power",
                    "stress_value": s.p_est,
                    "stress_unit": "W",
                    "limit_value": p_lim,
                    "derated_full_W": float("nan"),
                    "rated_W": float("nan"),
                    "margin_percent": (p_lim - s.p_est) / p_lim * 100,
                    "pass": s.p_est <= p_lim,
                    "notes": s.notes,
                }
            )
    return pd.DataFrame(rows)


def stress_vs_limits(
    p: CircuitParams | None = None,
    *,
    temp_c: float = 25.0,
    stresses: list[StressEstimate] | None = None,
) -> pd.DataFrame:
    if p is None:
        p = CircuitParams()
    if stresses is None:
        stresses = passband_stresses(p)
    d = p.derating
    p_allow = d.derated_power_w(temp_c) * d.resistor_power_use_fraction
    rows = []
    for s in stresses:
        if s.kind == "R":
            rows.append(
                {
                    "component": s.name,
                    "quantity": "voltage",
                    "unit": "V",
                    "applied": s.v_peak,
                    "derated_limit": d.resistor_voltage_guideline,
                    "rated_limit": d.resistor_voltage_guideline,
                    "notes": "0805 working-voltage guideline",
                }
            )
            rows.append(
                {
                    "component": s.name,
                    "quantity": "power",
                    "unit": "W",
                    "applied": s.p_est,
                    "derated_limit": p_allow,
                    "rated_limit": d.resistor_power_rated_w,
                    "notes": f"derated limit is {d.resistor_power_use_fraction:.0%} of the {temp_c:.0f} °C curve",
                }
            )
        elif s.kind == "C":
            rows.append(
                {
                    "component": s.name,
                    "quantity": "voltage",
                    "unit": "V",
                    "applied": s.v_peak,
                    "derated_limit": d.capacitor_v_max_recommended,
                    "rated_limit": d.capacitor_v_rated,
                    "notes": f"≤{d.capacitor_v_use_fraction:.0%} of VR",
                }
            )
        else:
            rows.append(
                {
                    "component": s.name,
                    "quantity": "voltage",
                    "unit": "V",
                    "applied": s.v_peak,
                    "derated_limit": p.opamp.v_supply_max,
                    "rated_limit": p.opamp.v_supply_max,
                    "notes": "recommended operating maximum",
                }
            )
            rows.append(
                {
                    "component": s.name,
                    "quantity": "power",
                    "unit": "W",
                    "applied": s.p_est,
                    "derated_limit": p.opamp.package_power_allow_w,
                    "rated_limit": p.opamp.package_power_allow_w,
                    "notes": "package allowance used in this study",
                }
            )
    frame = pd.DataFrame(rows)
    frame["utilization_of_derated"] = frame["applied"] / frame["derated_limit"]
    frame["utilization_of_rated"] = frame["applied"] / frame["rated_limit"]
    return frame


def power_derating_curve(p: CircuitParams | None = None, temps: np.ndarray | None = None) -> pd.DataFrame:
    if p is None:
        p = CircuitParams()
    if temps is None:
        temps = np.linspace(-40, 160, 41)
    d = p.derating
    rows = []
    for temp in temps:
        full = d.derated_power_w(float(temp))
        rows.append(
            {
                "temp_c": float(temp),
                "p_rated_curve_W": full,
                "p_allow_W": full * d.resistor_power_use_fraction,
            }
        )
    return pd.DataFrame(rows)
