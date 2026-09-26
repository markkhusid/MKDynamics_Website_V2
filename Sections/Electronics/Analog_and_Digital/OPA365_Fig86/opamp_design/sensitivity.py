"""Sensitivity and one-at-a-time influence ranking for Fig. 8-6.

Normalized relative sensitivity of metric m to parameter x:
    S_x^m = (x / m) * dm/dx
estimated with central finite differences.

OAT (one-at-a-time) span: metric change when x sweeps its full tolerance
interval with all other parameters nominal — good for tornado charts.

HOW TO ADAPT FOR ANOTHER NETLIST
--------------------------------
Pass a custom ``metric_fn(CircuitParams) -> dict[str, float]`` if your
accuracy metrics differ (e.g. notch depth, differential gain).  For pure
SPICE sensitivity, sweep ``.param`` in your deck and fill the same
DataFrame schema (parameter, metric, span, sensitivity).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
import pandas as pd

from .params import CircuitParams


MetricFn = Callable[[CircuitParams], dict[str, float]]


def default_metrics(p: CircuitParams) -> dict[str, float]:
    from .analysis import find_fc_3db, gain_at, passband_gain

    h_des = gain_at(p, p.op.f_design_hz, "vin")
    return {
        "fc_hz": find_fc_3db(p),
        "passband_gain": float(abs(passband_gain(p, 100.0))),
        "gain_at_fdesign": float(abs(h_des)),
        "phase_at_fdesign_deg": float(np.angle(h_des, deg=True)),
    }


@dataclass
class SensitivityResult:
    oat: pd.DataFrame
    normalized: pd.DataFrame

    def top_drivers(self, metric: str, n: int = 3) -> pd.DataFrame:
        df = self.oat[self.oat["metric"] == metric].copy()
        df["abs_span"] = df["span"].abs()
        return df.sort_values("abs_span", ascending=False).head(n)


def oat_analysis(
    p: CircuitParams | None = None,
    *,
    metric_fn: MetricFn | None = None,
    include_opamp: bool = True,
) -> pd.DataFrame:
    """One-at-a-time tolerance sweeps → span of each metric per parameter."""
    if p is None:
        p = CircuitParams()
    if metric_fn is None:
        metric_fn = default_metrics

    m0 = metric_fn(p)
    rows = []

    for name, nom in p.passive_dict().items():
        lo, hi = p.tol_for(name).bounds(nom)
        m_lo = metric_fn(p.with_values(**{name: lo}))
        m_hi = metric_fn(p.with_values(**{name: hi}))
        for metric, v0 in m0.items():
            rows.append(
                {
                    "parameter": name,
                    "metric": metric,
                    "nominal_metric": v0,
                    "metric_at_lo": m_lo[metric],
                    "metric_at_hi": m_hi[metric],
                    "span": m_hi[metric] - m_lo[metric],
                    "max_abs_delta": max(abs(m_hi[metric] - v0), abs(m_lo[metric] - v0)),
                }
            )

    if include_opamp:
        # Op-amp terms mainly affect DC error — add dc_error metric path
        from .analysis import dc_vout

        def metrics_with_dc(pp: CircuitParams, vos=0.0, ibp=0.0, ibn=0.0):
            base = metric_fn(pp)
            v_id = dc_vout(pp, vin=pp.op.v_in_bias, vos=0.0, ibp=0.0, ibn=0.0)
            v_t = dc_vout(pp, vin=pp.op.v_in_bias, vos=vos, ibp=ibp, ibn=ibn)
            base = dict(base)
            base["dc_error"] = v_t - v_id
            return base

        m0dc = metrics_with_dc(p)
        for pname, bounds, apply in (
            ("vos", p.opamp.vos_bounds(), lambda v: metrics_with_dc(p, vos=v)),
            ("ibp", p.opamp.ib_bounds(), lambda v: metrics_with_dc(p, ibp=v)),
            ("ibn", p.opamp.ib_bounds(), lambda v: metrics_with_dc(p, ibn=v)),
        ):
            m_lo = apply(bounds[0])
            m_hi = apply(bounds[1])
            for metric in m0dc:
                rows.append(
                    {
                        "parameter": pname,
                        "metric": metric,
                        "nominal_metric": m0dc[metric],
                        "metric_at_lo": m_lo[metric],
                        "metric_at_hi": m_hi[metric],
                        "span": m_hi[metric] - m_lo[metric],
                        "max_abs_delta": max(
                            abs(m_hi[metric] - m0dc[metric]),
                            abs(m_lo[metric] - m0dc[metric]),
                        ),
                    }
                )

    return pd.DataFrame(rows)


def normalized_sensitivity(
    p: CircuitParams | None = None,
    *,
    metric_fn: MetricFn | None = None,
    rel_step: float = 1e-4,
) -> pd.DataFrame:
    """Central-difference normalized sensitivity for each R/C."""
    if p is None:
        p = CircuitParams()
    if metric_fn is None:
        metric_fn = default_metrics
    m0 = metric_fn(p)
    rows = []
    for name, nom in p.passive_dict().items():
        dx = nom * rel_step
        m_p = metric_fn(p.with_values(**{name: nom + dx}))
        m_m = metric_fn(p.with_values(**{name: nom - dx}))
        for metric, v0 in m0.items():
            dmdx = (m_p[metric] - m_m[metric]) / (2 * dx)
            # S = (x/m) dm/dx ; guard m≈0
            if abs(v0) < 1e-30:
                s = float("nan")
            else:
                s = (nom / v0) * dmdx
            rows.append(
                {
                    "parameter": name,
                    "metric": metric,
                    "normalized_sensitivity": s,
                    "dm_dx": dmdx,
                    "nominal_metric": v0,
                }
            )
    return pd.DataFrame(rows)


def full_sensitivity(
    p: CircuitParams | None = None,
    **kwargs,
) -> SensitivityResult:
    oat = oat_analysis(p, **kwargs)
    # normalized does not take include_opamp
    kw2 = {k: v for k, v in kwargs.items() if k != "include_opamp"}
    norm = normalized_sensitivity(p, **kw2)
    return SensitivityResult(oat=oat, normalized=norm)


def sensitivity_vs_frequency(
    p: CircuitParams | None = None,
    f_hz: np.ndarray | None = None,
    rel_step: float = 1e-4,
) -> pd.DataFrame:
    """S_x^{|H(f)|} vs frequency for each passive — Bode sensitivity map."""
    from .analysis import bode, frequency_grid

    if p is None:
        p = CircuitParams()
    if f_hz is None:
        f_hz = frequency_grid(10, 1e6, 121)
    f_hz = np.asarray(f_hz, dtype=float)
    h0 = bode(p, source="vin", f_hz=f_hz).mag
    rows = []
    for name, nom in p.passive_dict().items():
        dx = nom * rel_step
        hp = bode(p.with_values(**{name: nom + dx}), source="vin", f_hz=f_hz).mag
        hm = bode(p.with_values(**{name: nom - dx}), source="vin", f_hz=f_hz).mag
        dhdX = (hp - hm) / (2 * dx)
        # S = (x/|H|) d|H|/dx
        with np.errstate(divide="ignore", invalid="ignore"):
            S = (nom / np.maximum(h0, 1e-30)) * dhdX
        for fi, si, h in zip(f_hz, S, h0):
            rows.append(
                {"parameter": name, "f_hz": fi, "S_mag": float(si), "H_mag": float(h)}
            )
    return pd.DataFrame(rows)
