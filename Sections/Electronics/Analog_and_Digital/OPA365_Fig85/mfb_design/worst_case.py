"""Worst-case corners for the Figure 8-5 filter.

DC error is Vout minus the ideal passive Vout (Vos = Ib = 0) at the same
Vin. The design gain is −R3/R1. With the published 549 Ω parts that target
is −1. The DC probe is 1 V when the bias is 0 V, so a resistor-ratio error
is visible. Offset and bias current are reported on top of that.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Callable

import numpy as np

from .params import CircuitParams


MetricFn = Callable[[CircuitParams, float, float, float], dict[str, float]]


def dc_probe(p: CircuitParams, vin_dc: float | None) -> float:
    if vin_dc is not None:
        return float(vin_dc)
    if abs(p.op.v_in_bias) > 1e-12:
        return float(p.op.v_in_bias)
    return float(p.op.v_in_peak)


def dc_accuracy(
    p: CircuitParams,
    vin: float,
    vos: float = 0.0,
    ibp: float = 0.0,
    ibn: float = 0.0,
) -> dict[str, float]:
    """DC error against the same network with Vos = Ib = 0."""
    from .analysis import dc_vout

    v_ideal = dc_vout(p, vin=vin, vos=0.0, ibp=0.0, ibn=0.0)
    v_tot = dc_vout(p, vin=vin, vos=vos, ibp=ibp, ibn=ibn)
    err = v_tot - v_ideal
    ppm = float("nan") if abs(vin) < 1e-30 else 1e6 * err / vin
    return {
        "vin_applied": float(vin),
        "dc_vout": float(v_tot),
        "dc_error": float(err),
        "dc_error_ppm": float(ppm),
        "ideal_vout": float(v_ideal),
        "design_vout": float(-vin),
        "gain_error": float(v_tot - (-vin)),
    }


def _metrics(
    p: CircuitParams,
    vos: float,
    ibp: float,
    ibn: float,
    vin_dc: float | None = None,
) -> dict[str, float]:
    from .analysis import find_fc_3db, gain_at, passband_gain

    vin = dc_probe(p, vin_dc)
    fc = find_fc_3db(p)
    h_pb = passband_gain(p, 100.0)
    h_des = gain_at(p, p.op.f_design_hz, "vin")
    h_tone = gain_at(p, p.op.f_passband_hz, "vin")
    dca = dc_accuracy(p, vin=vin, vos=vos, ibp=ibp, ibn=ibn)
    return {
        "fc_hz": fc,
        "passband_gain": float(np.abs(h_pb)),
        "gain_at_fdesign": float(np.abs(h_des)),
        "phase_at_fdesign_deg": float(np.angle(h_des, deg=True)),
        "gain_at_passband": float(np.abs(h_tone)),
        "phase_at_passband_deg": float(np.angle(h_tone, deg=True)),
        "vin_applied": dca["vin_applied"],
        "dc_vout": dca["dc_vout"],
        "dc_error": dca["dc_error"],
        "dc_error_ppm": dca["dc_error_ppm"],
        "gain_error": dca["gain_error"],
        "vos": vos,
        "ibp": ibp,
        "ibn": ibn,
    }


@dataclass
class WorstCaseResult:
    nominal: dict[str, float]
    minimum: dict[str, float]
    maximum: dict[str, float]
    rows: list[dict]

    def span(self, key: str) -> float:
        return self.maximum[key] - self.minimum[key]


def analytical_worst_case(
    p: CircuitParams | None = None,
    *,
    include_opamp: bool = True,
    r_c_corners_only: bool = False,
    vin_dc: float | None = None,
) -> WorstCaseResult:
    if p is None:
        p = CircuitParams()
    vin = dc_probe(p, vin_dc)
    nom = _metrics(p, 0.0, 0.0, 0.0, vin_dc=vin)
    rows: list[dict] = [dict(nom, corner="nominal")]

    r_lo = {n: p.r_tol.bounds(getattr(p, n))[0] for n in p.resistance_names()}
    r_hi = {n: p.r_tol.bounds(getattr(p, n))[1] for n in p.resistance_names()}
    c_lo = {n: p.c_tol.bounds(getattr(p, n))[0] for n in p.capacitance_names()}
    c_hi = {n: p.c_tol.bounds(getattr(p, n))[1] for n in p.capacitance_names()}

    for r_side, c_side in product(("lo", "hi"), repeat=2):
        kwargs = {}
        for n in p.resistance_names():
            kwargs[n] = r_lo[n] if r_side == "lo" else r_hi[n]
        for n in p.capacitance_names():
            kwargs[n] = c_lo[n] if c_side == "lo" else c_hi[n]
        m = _metrics(p.with_values(**kwargs), 0.0, 0.0, 0.0, vin_dc=vin)
        m["corner"] = f"R_{r_side}_C_{c_side}"
        rows.append(m)

    for n in list(p.resistance_names()) + list(p.capacitance_names()):
        lo, hi = p.tol_for(n).bounds(getattr(p, n))
        for tag, val in (("lo", lo), ("hi", hi)):
            m = _metrics(p.with_values(**{n: val}), 0.0, 0.0, 0.0, vin_dc=vin)
            m["corner"] = f"{n}_{tag}"
            rows.append(m)

    if include_opamp and not r_c_corners_only:
        vos_b = p.opamp.vos_bounds()
        ib_b = p.opamp.ib_bounds()
        for vos in vos_b:
            for ibp in ib_b:
                for ibn in ib_b:
                    m = _metrics(p, vos, ibp, ibn, vin_dc=vin)
                    m["corner"] = f"op_vos={vos:.3e}_ibp={ibp:.3e}_ibn={ibn:.3e}"
                    rows.append(m)

    keys = [k for k in nom if k not in ("vos", "ibp", "ibn")]
    minimum = {k: min(r[k] for r in rows) for k in keys}
    maximum = {k: max(r[k] for r in rows) for k in keys}
    return WorstCaseResult(nominal=nom, minimum=minimum, maximum=maximum, rows=rows)


def oat_contributions(
    p: CircuitParams | None = None,
    *,
    metrics: tuple[str, ...] = ("fc_hz", "dc_error"),
    vin_dc: float | None = None,
    include_opamp: bool = True,
) -> dict[str, dict[str, float]]:
    if p is None:
        p = CircuitParams()
    vin = dc_probe(p, vin_dc)
    contrib: dict[str, dict[str, float]] = {m: {} for m in metrics}
    for n in list(p.resistance_names()) + list(p.capacitance_names()):
        lo, hi = p.tol_for(n).bounds(getattr(p, n))
        m_lo = _metrics(p.with_values(**{n: lo}), 0.0, 0.0, 0.0, vin_dc=vin)
        m_hi = _metrics(p.with_values(**{n: hi}), 0.0, 0.0, 0.0, vin_dc=vin)
        for met in metrics:
            contrib[met][n] = 0.5 * abs(m_hi[met] - m_lo[met])
    if include_opamp:
        for pname, bounds, apply in (
            ("vos", p.opamp.vos_bounds(), lambda v: _metrics(p, v, 0.0, 0.0, vin_dc=vin)),
            ("ibp", p.opamp.ib_bounds(), lambda v: _metrics(p, 0.0, v, 0.0, vin_dc=vin)),
            ("ibn", p.opamp.ib_bounds(), lambda v: _metrics(p, 0.0, 0.0, v, vin_dc=vin)),
        ):
            m_lo = apply(bounds[0])
            m_hi = apply(bounds[1])
            for met in metrics:
                contrib[met][pname] = 0.5 * abs(m_hi[met] - m_lo[met])
    return contrib


def rss_bounds(
    p: CircuitParams | None = None,
    *,
    metrics: tuple[str, ...] = ("fc_hz", "dc_error"),
    vin_dc: float | None = None,
    include_opamp: bool = True,
) -> dict[str, dict[str, float]]:
    if p is None:
        p = CircuitParams()
    vin = dc_probe(p, vin_dc)
    m0 = _metrics(p, 0.0, 0.0, 0.0, vin_dc=vin)
    contrib = oat_contributions(p, metrics=metrics, vin_dc=vin, include_opamp=include_opamp)
    out: dict[str, dict[str, float]] = {}
    for met in metrics:
        deltas = contrib[met]
        rss = float(np.sqrt(sum(d * d for d in deltas.values())))
        nom = float(m0[met])
        out[met] = {
            "nominal": nom,
            "delta_rss": rss,
            "low": nom - rss,
            "high": nom + rss,
            **{f"d_{k}": v for k, v in deltas.items()},
        }
    return out


def spice_wc_corners(
    p: CircuitParams | None = None,
    *,
    workdir: Path | str,
    root: Path | str | None = None,
    opamp_model: str = "ideal",
    ngspice=None,
) -> list[dict]:
    from .analysis import find_fc_3db
    from .simulate import fc_from_mag, simulate_ac

    if p is None:
        p = CircuitParams()
    workdir = Path(workdir)
    root_p = Path(root) if root is not None else None
    results = []
    for r_side, c_side in product(("lo", "hi"), repeat=2):
        kwargs = {}
        for n in p.resistance_names():
            lo, hi = p.r_tol.bounds(getattr(p, n))
            kwargs[n] = lo if r_side == "lo" else hi
        for n in p.capacitance_names():
            lo, hi = p.c_tol.bounds(getattr(p, n))
            kwargs[n] = lo if c_side == "lo" else hi
        pc = p.with_values(**kwargs)
        tag = f"R_{r_side}_C_{c_side}"
        ac = simulate_ac(pc, opamp_model=opamp_model, workdir=workdir / tag, root=root_p, ngspice=ngspice)
        results.append(
            {
                "corner": tag,
                "fc_spice_hz": fc_from_mag(ac.f_hz, np.abs(ac.h)),
                "fc_analytical_hz": find_fc_3db(pc),
                "params": kwargs,
            }
        )
    return results
