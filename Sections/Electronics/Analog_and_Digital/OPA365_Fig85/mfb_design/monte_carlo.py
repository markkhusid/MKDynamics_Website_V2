"""Uniform Monte Carlo of the analytical Figure 8-5 metrics.

This AC Monte Carlo is separate from the 500-run transient Monte Carlo.
The two files are not interchangeable: this one draws passives and the
op-amp DC limits and records cutoff and DC error.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .params import CircuitParams


@dataclass
class MCResult:
    frame: pd.DataFrame
    summary: pd.DataFrame

    def save(self, dir_path: Path | str) -> None:
        d = Path(dir_path)
        d.mkdir(parents=True, exist_ok=True)
        self.frame.to_csv(d / "mc_samples.csv", index=False)
        self.summary.to_csv(d / "mc_summary.csv")
        meta = {"n": len(self.frame), "columns": list(self.frame.columns)}
        (d / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


def _draw_passives(p: CircuitParams, rng: np.random.Generator) -> dict[str, float]:
    out = {}
    for n, nom in p.passive_dict().items():
        out[n] = p.tol_for(n).scale(nom, float(rng.uniform(0.0, 1.0)))
    return out


def _draw_opamp(p: CircuitParams, rng: np.random.Generator) -> dict[str, float]:
    vlo, vhi = p.opamp.vos_bounds()
    ilo, ihi = p.opamp.ib_bounds()
    return {
        "vos": float(rng.uniform(vlo, vhi)),
        "ibp": float(rng.uniform(ilo, ihi)),
        "ibn": float(rng.uniform(ilo, ihi)),
    }


def _summary(frame: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    summary = frame[cols].agg(["mean", "std", "min", "max"]).T
    for q, name in ((0.01, "p01"), (0.05, "p05"), (0.50, "p50"), (0.95, "p95"), (0.99, "p99")):
        summary[name] = frame[cols].quantile(q).values
    return summary


def sample_metrics(
    p: CircuitParams,
    *,
    n: int = 2000,
    seed: int = 42,
    include_opamp: bool = True,
    vin_dc: float | None = None,
) -> MCResult:
    """Analytical uniform MC. Default 2000 draws, seed 42.

    Transient Monte Carlo uses its own 500-draw generator. Do not overwrite
    that cache with this frame.
    """
    from .analysis import find_fc_3db, gain_at, passband_gain
    from .worst_case import dc_accuracy, dc_probe

    vin = dc_probe(p, vin_dc)
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(int(n)):
        pas = _draw_passives(p, rng)
        pc = p.with_values(**pas)
        op = _draw_opamp(p, rng) if include_opamp else {"vos": 0.0, "ibp": 0.0, "ibn": 0.0}
        h_des = gain_at(pc, p.op.f_design_hz, "vin")
        h_tone = gain_at(pc, p.op.f_passband_hz, "vin")
        dca = dc_accuracy(pc, vin=vin, vos=op["vos"], ibp=op["ibp"], ibn=op["ibn"])
        rows.append(
            {
                "sample": i,
                **pas,
                **op,
                "fc_hz": find_fc_3db(pc),
                "passband_gain": float(abs(passband_gain(pc, 100.0))),
                "gain_at_fdesign": float(abs(h_des)),
                "phase_at_fdesign_deg": float(np.angle(h_des, deg=True)),
                "gain_at_passband": float(abs(h_tone)),
                "phase_at_passband_deg": float(np.angle(h_tone, deg=True)),
                "vin_applied": dca["vin_applied"],
                "dc_vout": dca["dc_vout"],
                "dc_error": dca["dc_error"],
                "dc_error_ppm": dca["dc_error_ppm"],
                "gain_error": dca["gain_error"],
            }
        )
    frame = pd.DataFrame(rows)
    cols = [
        "fc_hz",
        "passband_gain",
        "gain_at_fdesign",
        "phase_at_fdesign_deg",
        "gain_at_passband",
        "phase_at_passband_deg",
        "dc_vout",
        "dc_error",
        "gain_error",
    ]
    return MCResult(frame=frame, summary=_summary(frame, cols))


def annotate_wc_rss_on_axis(
    ax,
    *,
    wc_low: float | None,
    wc_high: float | None,
    rss_low: float | None,
    rss_high: float | None,
    nominal: float | None = None,
) -> None:
    if nominal is not None and np.isfinite(nominal):
        ax.axvline(nominal, color="k", ls="-", lw=1.2, label="nominal", zorder=4)
    if wc_low is not None and np.isfinite(wc_low):
        ax.axvline(wc_low, color="C3", ls="--", lw=1.4, label="WC min/max", zorder=5)
    if wc_high is not None and np.isfinite(wc_high):
        ax.axvline(wc_high, color="C3", ls="--", lw=1.4, zorder=5)
    if rss_low is not None and np.isfinite(rss_low):
        ax.axvline(rss_low, color="C2", ls="-.", lw=1.4, label="RSS", zorder=5)
    if rss_high is not None and np.isfinite(rss_high):
        ax.axvline(rss_high, color="C2", ls="-.", lw=1.4, zorder=5)
