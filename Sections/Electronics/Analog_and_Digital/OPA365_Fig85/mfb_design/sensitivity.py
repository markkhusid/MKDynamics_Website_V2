"""Sensitivity of cutoff frequency and DC output voltage.

Normalized sensitivity is (x / m) dm/dx from a central difference.
The DC table uses Vin = 1 V so the −R3/R1 gain is visible. At the 0 V
bias, and with Ib = 0, every passive has a zero DC output.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
import pandas as pd

from .params import CircuitParams

MetricFn = Callable[[CircuitParams], dict[str, float]]


def default_metrics(p: CircuitParams) -> dict[str, float]:
    from .analysis import dc_vout, find_fc_3db, gain_at, passband_gain

    h_des = gain_at(p, p.op.f_design_hz, "vin")
    h_tone = gain_at(p, p.op.f_passband_hz, "vin")
    return {
        "fc_hz": find_fc_3db(p),
        "passband_gain": float(abs(passband_gain(p, 100.0))),
        "gain_at_fdesign": float(abs(h_des)),
        "phase_at_fdesign_deg": float(np.angle(h_des, deg=True)),
        "gain_at_passband": float(abs(h_tone)),
        "dc_vout": float(dc_vout(p, vin=p.op.v_in_peak)),
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
        from .analysis import dc_vout

        vin = p.op.v_in_peak

        def with_sources(vos=0.0, ibp=0.0, ibn=0.0):
            base = dict(metric_fn(p))
            base["dc_vout"] = dc_vout(p, vin=vin, vos=vos, ibp=ibp, ibn=ibn)
            base["dc_error"] = base["dc_vout"] - dc_vout(p, vin=vin)
            return base

        m0dc = with_sources()
        for pname, bounds, apply in (
            ("vos", p.opamp.vos_bounds(), lambda v: with_sources(vos=v)),
            ("ibp", p.opamp.ib_bounds(), lambda v: with_sources(ibp=v)),
            ("ibn", p.opamp.ib_bounds(), lambda v: with_sources(ibn=v)),
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
            s = float("nan") if abs(v0) < 1e-30 else (nom / v0) * dmdx
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


def full_sensitivity(p: CircuitParams | None = None, **kwargs) -> SensitivityResult:
    oat = oat_analysis(p, **kwargs)
    kw2 = {k: v for k, v in kwargs.items() if k != "include_opamp"}
    return SensitivityResult(oat=oat, normalized=normalized_sensitivity(p, **kw2))


def dc_vout_influence(p: CircuitParams | None = None, vin: float | None = None) -> pd.DataFrame:
    """How each parameter moves Vout at a 1 V input.

    Vos gain is −(1 + R3/R1), which is −2 with the published resistors.
    Ibn moves Vout by (R2 + R3 + R2 R3/R1) ohms. Ibp does not, because the
    + pin is grounded.
    """
    from .analysis import dc_vout

    if p is None:
        p = CircuitParams()
    vin_v = p.op.v_in_peak if vin is None else float(vin)
    rows = []
    v_nom = dc_vout(p, vin=vin_v, vos=0.0, ibp=0.0, ibn=0.0)

    def add(parameter, lo_v, hi_v, note):
        rows.append(
            {
                "parameter": parameter,
                "Vout_nominal_V": v_nom,
                "Vout_at_lo_V": lo_v,
                "Vout_at_hi_V": hi_v,
                "span_uV": (hi_v - lo_v) * 1e6,
                "note": note,
            }
        )

    for name, nom in p.passive_dict().items():
        lo, hi = p.tol_for(name).bounds(nom)
        add(
            name,
            dc_vout(p.with_values(**{name: lo}), vin=vin_v),
            dc_vout(p.with_values(**{name: hi}), vin=vin_v),
            "Ib = 0. DC gain depends on R3/R1 only.",
        )

    ib = p.opamp.ib_max
    for name in p.resistance_names():
        nom = getattr(p, name)
        lo, hi = p.tol_for(name).bounds(nom)
        add(
            f"{name} at Ibn = Ib max",
            dc_vout(p.with_values(**{name: lo}), vin=vin_v, ibn=ib),
            dc_vout(p.with_values(**{name: hi}), vin=vin_v, ibn=ib),
            "Ibn = +10 pA. The span is the tolerance piece of that drop.",
        )

    vlo, vhi = p.opamp.vos_bounds()
    add(
        "Vos",
        dc_vout(p, vin=vin_v, vos=vlo),
        dc_vout(p, vin=vin_v, vos=vhi),
        "V(n2) = −Vos, so Vout moves by −(1 + R3/R1) Vos.",
    )
    ilo, ihi = p.opamp.ib_bounds()
    add(
        "Ibp",
        dc_vout(p, vin=vin_v, ibp=ilo),
        dc_vout(p, vin=vin_v, ibp=ihi),
        "+ pin is grounded. Ibp does not enter the signal nodes.",
    )
    add(
        "Ibn",
        dc_vout(p, vin=vin_v, ibn=ilo),
        dc_vout(p, vin=vin_v, ibn=ihi),
        "Ibn leaves n2. DC transresistance is R2 + R3 + R2 R3/R1.",
    )
    return pd.DataFrame(rows)


def sensitivity_vs_frequency(
    p: CircuitParams | None = None,
    f_hz: np.ndarray | None = None,
    rel_step: float = 1e-4,
) -> pd.DataFrame:
    from .analysis import bode, frequency_grid

    if p is None:
        p = CircuitParams()
    if f_hz is None:
        f_hz = frequency_grid(10, 20e6, 161)
    f_hz = np.asarray(f_hz, dtype=float)
    h0 = bode(p, source="vin", f_hz=f_hz).mag
    rows = []
    for name, nom in p.passive_dict().items():
        dx = nom * rel_step
        hp = bode(p.with_values(**{name: nom + dx}), source="vin", f_hz=f_hz).mag
        hm = bode(p.with_values(**{name: nom - dx}), source="vin", f_hz=f_hz).mag
        dhdX = (hp - hm) / (2 * dx)
        with np.errstate(divide="ignore", invalid="ignore"):
            sens = (nom / np.maximum(h0, 1e-30)) * dhdX
        for fi, si, h in zip(f_hz, sens, h0):
            rows.append({"parameter": name, "f_hz": float(fi), "S_mag": float(si), "H_mag": float(h)})
    return pd.DataFrame(rows)
