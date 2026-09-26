"""Worst-case (endpoint / corner) analysis for Fig. 8-6 metrics.

Uniform tolerance box (not RSS):
    each R in R*(1±r_tol), each C in C*(1±c_tol),
    Vos in [-vos_max, +vos_max],
    Ibp, Ibn independently in [-ib_max, +ib_max].

Because a full 3^8 grid is large, we use:
1. **Axis corners** — each variable at min/max with others nominal
2. **Random extreme samples** on the box vertices / faces (optional)
3. **Targeted fc corners** — all R high/low × all C high/low (dominant for fc)

HOW TO ADAPT FOR ANOTHER NETLIST
--------------------------------
* Analytical WC: change ``metric_vector()`` to call your metric function
  on a parameter dict (or keep using ``summary_metrics`` if H(s) still applies).
* SPICE WC: generate corner netlists via ``netlist.write_netlist`` with
  replaced CircuitParams, or step parameters in your own deck and parse
  ``.meas`` results — see ``spice_wc_corners``.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product
from pathlib import Path
from typing import Callable

import numpy as np

from .analysis import summary_metrics
from .params import CircuitParams


MetricFn = Callable[[CircuitParams, float, float, float], dict[str, float]]


def dc_accuracy(
    p: CircuitParams,
    vin: float,
    vos: float = 0.0,
    ibp: float = 0.0,
    ibn: float = 0.0,
) -> dict[str, float]:
    """DC tracking accuracy for an applied input voltage.

    Ideal unity-gain target: ``Vout_ideal = Vin`` (all non-ideals zero).
    Reported error is ``Vout - Vin`` (same as ``Vout - Vout_ideal``).

    Parameters
    ----------
    vin :
        Applied DC input voltage (V).  Typical mid-rail is ``p.op.v_in_bias``.
    vos, ibp, ibn :
        Op-amp non-ideals (see ``params.OpampParams`` polarity notes).

    Returns
    -------
    dict with vout, dc_error (V), dc_error_ppm (relative to |vin| if vin≠0),
    and ideal_vout.
    """
    from .analysis import dc_vout

    v_ideal = float(vin)  # unity-gain ideal
    v_tot = dc_vout(p, vin=vin, vos=vos, ibp=ibp, ibn=ibn)
    err = v_tot - v_ideal
    ppm = float("nan") if abs(vin) < 1e-30 else 1e6 * err / vin
    return {
        "vin_applied": float(vin),
        "dc_vout": float(v_tot),
        "dc_error": float(err),
        "dc_error_ppm": float(ppm),
        "ideal_vout": v_ideal,
    }


def _metrics(
    p: CircuitParams,
    vos: float,
    ibp: float,
    ibn: float,
    vin_dc: float | None = None,
) -> dict[str, float]:
    """Evaluate standard metrics with non-ideals applied to DC error terms.

    AC shape metrics (fc, gain) use the passive network in ``p`` (Vos/Ib do
    not change the linear Vin→Vout TF shape for this unity-gain ideal model
    when sources are independent; they do add output offset).

    DC accuracy is evaluated at ``vin_dc`` (default: mid-rail bias) as
    ``dc_error = Vout - Vin_applied``.
    """
    from .analysis import find_fc_3db, gain_at, passband_gain

    vin = p.op.v_in_bias if vin_dc is None else float(vin_dc)
    fc = find_fc_3db(p)
    h_pb = passband_gain(p, 100.0)
    h_des = gain_at(p, p.op.f_design_hz, "vin")
    dca = dc_accuracy(p, vin=vin, vos=vos, ibp=ibp, ibn=ibn)
    return {
        "fc_hz": fc,
        "passband_gain": float(np.abs(h_pb)),
        "gain_at_fdesign": float(np.abs(h_des)),
        "phase_at_fdesign_deg": float(np.angle(h_des, deg=True)),
        "vin_applied": dca["vin_applied"],
        "dc_vout": dca["dc_vout"],
        "dc_error": dca["dc_error"],
        "dc_error_ppm": dca["dc_error_ppm"],
        "vos": vos,
        "ibp": ibp,
        "ibn": ibn,
    }


@dataclass
class WorstCaseResult:
    """Aggregated min/typ/max for each metric plus corner rows."""

    nominal: dict[str, float]
    minimum: dict[str, float]
    maximum: dict[str, float]
    rows: list[dict[str, float]]  # each corner sample

    def span(self, key: str) -> float:
        return self.maximum[key] - self.minimum[key]


def analytical_worst_case(
    p: CircuitParams | None = None,
    *,
    include_opamp: bool = True,
    r_c_corners_only: bool = False,
    vin_dc: float | None = None,
) -> WorstCaseResult:
    """Enumerate analytical WC samples and aggregate min/max metrics.

    Metrics include cutoff ``fc_hz`` and DC accuracy ``dc_error`` /
    ``dc_error_ppm`` at the applied DC voltage ``vin_dc`` (default mid-rail).
    """
    if p is None:
        p = CircuitParams()
    vin = p.op.v_in_bias if vin_dc is None else float(vin_dc)

    nom = _metrics(p, 0.0, 0.0, 0.0, vin_dc=vin)
    rows: list[dict[str, float]] = [dict(nom, corner="nominal")]

    r_lo = {n: p.r_tol.bounds(getattr(p, n))[0] for n in p.resistance_names()}
    r_hi = {n: p.r_tol.bounds(getattr(p, n))[1] for n in p.resistance_names()}
    c_lo = {n: p.c_tol.bounds(getattr(p, n))[0] for n in p.capacitance_names()}
    c_hi = {n: p.c_tol.bounds(getattr(p, n))[1] for n in p.capacitance_names()}

    # All R low/high × all C low/high (4 combinations of "all R" × "all C")
    for r_side, c_side in product(("lo", "hi"), repeat=2):
        kwargs = {}
        for n in p.resistance_names():
            kwargs[n] = r_lo[n] if r_side == "lo" else r_hi[n]
        for n in p.capacitance_names():
            kwargs[n] = c_lo[n] if c_side == "lo" else c_hi[n]
        pc = p.with_values(**kwargs)
        m = _metrics(pc, 0.0, 0.0, 0.0, vin_dc=vin)
        m["corner"] = f"R_{r_side}_C_{c_side}"
        rows.append(m)

    # One-at-a-time passive extremes
    for n in list(p.resistance_names()) + list(p.capacitance_names()):
        lo, hi = p.tol_for(n).bounds(getattr(p, n))
        for tag, val in (("lo", lo), ("hi", hi)):
            pc = p.with_values(**{n: val})
            m = _metrics(pc, 0.0, 0.0, 0.0, vin_dc=vin)
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
        # Combined passive+opamp corners that matter for DC (R extremes × Vos × Ibp)
        for r_side, vos, ibp in product(("lo", "hi"), vos_b, ib_b):
            kwargs = {n: (r_lo[n] if r_side == "lo" else r_hi[n]) for n in p.resistance_names()}
            pc = p.with_values(**kwargs)
            m = _metrics(pc, vos, ibp, 0.0, vin_dc=vin)
            m["corner"] = f"R_{r_side}_vos={vos:.3e}_ibp={ibp:.3e}"
            rows.append(m)

    # Aggregate numeric keys
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
    """One-at-a-time half-span contribution of each parameter to each metric.

    For parameter x with extremes x_lo, x_hi (others nominal)::

        delta_x = 0.5 * |m(x_hi) - m(x_lo)|

    (signed span is also available via full WC).  Used to build RSS bounds.

    Returns
    -------
    dict metric → dict parameter → |half-span contribution|
    """
    if p is None:
        p = CircuitParams()
    vin = p.op.v_in_bias if vin_dc is None else float(vin_dc)
    m0 = _metrics(p, 0.0, 0.0, 0.0, vin_dc=vin)
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
    """Root-sum-square tolerance stack-up about the nominal metric value.

    For each metric m::

        delta_rss = sqrt( sum_i delta_i^2 )

    where ``delta_i`` is the OAT half-span from :func:`oat_contributions`.

    Returns
    -------
    dict metric → {nominal, delta_rss, low=nominal-delta_rss, high=nominal+delta_rss,
                   contributions: {param: delta_i}}
    """
    if p is None:
        p = CircuitParams()
    vin = p.op.v_in_bias if vin_dc is None else float(vin_dc)
    m0 = _metrics(p, 0.0, 0.0, 0.0, vin_dc=vin)
    contrib = oat_contributions(
        p, metrics=metrics, vin_dc=vin, include_opamp=include_opamp
    )
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


def dc_accuracy_vs_vin(
    p: CircuitParams | None = None,
    *,
    vins: list[float] | None = None,
    include_opamp_wc: bool = True,
) -> "pd.DataFrame":
    """Nominal and WC DC error vs applied Vin (for accuracy tables/plots).

    At each Vin: nominal error (0 non-ideals) and WC min/max error over
    op-amp extremes (and R series extremes for Ib·R).  C does not affect DC.
    """
    import pandas as pd

    if p is None:
        p = CircuitParams()
    if vins is None:
        # Span usable single-supply range with headroom
        vins = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]

    vos_b = p.opamp.vos_bounds() if include_opamp_wc else (0.0, 0.0)
    ib_b = p.opamp.ib_bounds() if include_opamp_wc else (0.0, 0.0)
    r_lo = {n: p.r_tol.bounds(getattr(p, n))[0] for n in p.resistance_names()}
    r_hi = {n: p.r_tol.bounds(getattr(p, n))[1] for n in p.resistance_names()}

    rows = []
    for vin in vins:
        nom = dc_accuracy(p, vin=vin, vos=0.0, ibp=0.0, ibn=0.0)
        errs = [nom["dc_error"]]
        vouts = [nom["dc_vout"]]
        if include_opamp_wc:
            for r_side, vos, ibp in product(("nom", "lo", "hi"), vos_b, ib_b):
                if r_side == "nom":
                    pc = p
                else:
                    kw = {
                        n: (r_lo[n] if r_side == "lo" else r_hi[n])
                        for n in p.resistance_names()
                    }
                    pc = p.with_values(**kw)
                d = dc_accuracy(pc, vin=vin, vos=vos, ibp=ibp, ibn=0.0)
                errs.append(d["dc_error"])
                vouts.append(d["dc_vout"])
        rows.append(
            {
                "vin_applied": vin,
                "dc_error_nom": nom["dc_error"],
                "dc_vout_nom": nom["dc_vout"],
                "dc_error_wc_min": min(errs),
                "dc_error_wc_max": max(errs),
                "dc_vout_wc_min": min(vouts),
                "dc_vout_wc_max": max(vouts),
                "dc_error_ppm_nom": nom["dc_error_ppm"],
            }
        )
    return pd.DataFrame(rows)


def spice_wc_corners(
    p: CircuitParams | None = None,
    *,
    workdir: Path | str,
    root: Path | str | None = None,
    opamp_model: str = "ideal",
    ngspice=None,
) -> list[dict]:
    """Run ngspice AC at R/C all-low and all-high corners; return fc estimates.

    For a custom netlist: loop your own corner decks with
    ``simulate.run_external_netlist`` instead of this helper.
    """
    from .analysis import find_fc_3db  # analytical fc for the same corner params
    from .simulate import simulate_ac

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
        wd = workdir / tag
        ac = simulate_ac(
            pc,
            opamp_model=opamp_model,
            workdir=wd,
            root=root_p,
        )
        # Estimate fc from SPICE |H|
        mag = np.abs(ac.h)
        dc = mag[0]
        target = dc / np.sqrt(2)
        fc_sp = float("nan")
        for i in range(1, len(mag)):
            if mag[i - 1] >= target > mag[i]:
                f1, f2 = ac.f_hz[i - 1], ac.f_hz[i]
                m1, m2 = mag[i - 1], mag[i]
                g = (np.log(target) - np.log(m1)) / (np.log(m2) - np.log(m1))
                fc_sp = float(f1 * (f2 / f1) ** g)
                break
        results.append(
            {
                "corner": tag,
                "fc_spice_hz": fc_sp,
                "fc_analytical_hz": find_fc_3db(pc),
                "params": kwargs,
            }
        )
    return results
