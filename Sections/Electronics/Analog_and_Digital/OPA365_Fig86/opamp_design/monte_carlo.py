"""Uniform Monte Carlo for analytical metrics and optional SPICE subset.

Distribution (as specified):
    each parameter independent Uniform on its tolerance / limit interval.

HOW TO ADAPT FOR ANOTHER NETLIST
--------------------------------
* Analytical MC: replace ``sample_metrics`` body with your metric function
  of a parameter dict.
* SPICE MC: either use ``spice_monte_carlo`` (generates Fig. 8-6 decks) or
  write your own loop that patches ``.param`` lines in a template netlist
  and calls ``simulate.run_external_netlist``.  Cache results as NPZ/CSV
  the same way for notebook re-runs.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .params import CircuitParams


@dataclass
class MCResult:
    """Monte Carlo sample table + summary statistics."""

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
        u = rng.uniform(0.0, 1.0)
        out[n] = p.tol_for(n).scale(nom, u)
    return out


def _draw_opamp(p: CircuitParams, rng: np.random.Generator) -> dict[str, float]:
    vlo, vhi = p.opamp.vos_bounds()
    ilo, ihi = p.opamp.ib_bounds()
    return {
        "vos": float(rng.uniform(vlo, vhi)),
        "ibp": float(rng.uniform(ilo, ihi)),
        "ibn": float(rng.uniform(ilo, ihi)),
    }


def sample_metrics(
    p: CircuitParams,
    *,
    n: int = 2000,
    seed: int = 42,
    include_opamp: bool = True,
    vin_dc: float | None = None,
) -> MCResult:
    """Analytical uniform MC of fc, gains, and DC accuracy at ``vin_dc``.

    DC accuracy: ``dc_error = Vout - Vin_applied`` (ideal unity-gain target).
    Also stores ``dc_vout`` and ``dc_error_ppm``.
    """
    from .analysis import find_fc_3db, gain_at, passband_gain
    from .worst_case import dc_accuracy

    vin = p.op.v_in_bias if vin_dc is None else float(vin_dc)
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(int(n)):
        pas = _draw_passives(p, rng)
        pc = p.with_values(**pas)
        if include_opamp:
            op = _draw_opamp(p, rng)
        else:
            op = {"vos": 0.0, "ibp": 0.0, "ibn": 0.0}
        fc = find_fc_3db(pc)
        h_pb = abs(passband_gain(pc, 100.0))
        h_des = gain_at(pc, p.op.f_design_hz, "vin")
        dca = dc_accuracy(
            pc, vin=vin, vos=op["vos"], ibp=op["ibp"], ibn=op["ibn"]
        )
        rows.append(
            {
                "sample": i,
                **pas,
                **op,
                "fc_hz": fc,
                "passband_gain": h_pb,
                "gain_at_fdesign": abs(h_des),
                "phase_at_fdesign_deg": float(np.angle(h_des, deg=True)),
                "vin_applied": dca["vin_applied"],
                "dc_vout": dca["dc_vout"],
                "dc_error": dca["dc_error"],
                "dc_error_ppm": dca["dc_error_ppm"],
            }
        )
    frame = pd.DataFrame(rows)
    metric_cols = [
        "fc_hz",
        "passband_gain",
        "gain_at_fdesign",
        "phase_at_fdesign_deg",
        "dc_vout",
        "dc_error",
        "dc_error_ppm",
    ]
    summary = frame[metric_cols].agg(["mean", "std", "min", "max"]).T
    # percentiles
    for q, name in ((0.01, "p01"), (0.05, "p05"), (0.50, "p50"), (0.95, "p95"), (0.99, "p99")):
        summary[name] = frame[metric_cols].quantile(q).values
    return MCResult(frame=frame, summary=summary)


def annotate_wc_rss_on_axis(
    ax,
    *,
    wc_low: float | None,
    wc_high: float | None,
    rss_low: float | None,
    rss_high: float | None,
    nominal: float | None = None,
) -> None:
    """Draw WC (red dashed) and RSS (green dash-dot) vertical bands on a histogram.

    Call after plotting the MC histogram so the reference lines sit on top.
    """
    if nominal is not None and np.isfinite(nominal):
        ax.axvline(nominal, color="k", ls="-", lw=1.2, label="nominal", zorder=4)
    if wc_low is not None and np.isfinite(wc_low):
        ax.axvline(wc_low, color="C3", ls="--", lw=1.4, label="WC min/max", zorder=5)
    if wc_high is not None and np.isfinite(wc_high):
        ax.axvline(wc_high, color="C3", ls="--", lw=1.4, zorder=5)
    if rss_low is not None and np.isfinite(rss_low):
        ax.axvline(rss_low, color="C2", ls="-.", lw=1.4, label="RSS ±", zorder=5)
    if rss_high is not None and np.isfinite(rss_high):
        ax.axvline(rss_high, color="C2", ls="-.", lw=1.4, zorder=5)


def spice_monte_carlo(
    p: CircuitParams | None = None,
    *,
    n: int = 50,
    seed: int = 42,
    workdir: Path | str,
    root: Path | str | None = None,
    opamp_model: str = "ideal",
    cache: bool = True,
    ngspice=None,
) -> MCResult:
    """Run ``n`` ngspice AC decks with uniform passive draws; estimate fc.

    Caching: if ``workdir/mc_cache/frame.csv`` exists and n matches meta, reload.
    """
    from .simulate import simulate_ac

    if p is None:
        p = CircuitParams()
    workdir = Path(workdir)
    cache_dir = workdir / "mc_cache"
    if cache and (cache_dir / "frame.csv").is_file() and (cache_dir / "meta.json").is_file():
        meta = json.loads((cache_dir / "meta.json").read_text(encoding="utf-8"))
        if meta.get("n") == n and meta.get("seed") == seed:
            frame = pd.read_csv(cache_dir / "frame.csv")
            summary = pd.read_csv(cache_dir / "mc_summary.csv", index_col=0)
            return MCResult(frame=frame, summary=summary)

    rng = np.random.default_rng(seed)
    rows = []
    for i in range(int(n)):
        pas = _draw_passives(p, rng)
        pc = p.with_values(**pas)
        wd = workdir / f"mc_{i:04d}"
        ac = simulate_ac(pc, opamp_model=opamp_model, workdir=wd, root=root, ngspice=ngspice)
        mag = np.abs(ac.h)
        dc = mag[0]
        target = dc / np.sqrt(2)
        fc_sp = float("nan")
        for j in range(1, len(mag)):
            if mag[j - 1] >= target > mag[j]:
                f1, f2 = ac.f_hz[j - 1], ac.f_hz[j]
                m1, m2 = mag[j - 1], mag[j]
                g = (np.log(target) - np.log(m1)) / (np.log(m2) - np.log(m1))
                fc_sp = float(f1 * (f2 / f1) ** g)
                break
        rows.append({"sample": i, **pas, "fc_spice_hz": fc_sp, "passband_gain_spice": float(dc)})

    frame = pd.DataFrame(rows)
    metric_cols = ["fc_spice_hz", "passband_gain_spice"]
    summary = frame[metric_cols].agg(["mean", "std", "min", "max"]).T
    for q, name in ((0.05, "p05"), (0.50, "p50"), (0.95, "p95")):
        summary[name] = frame[metric_cols].quantile(q).values
    result = MCResult(frame=frame, summary=summary)
    if cache:
        result.save(cache_dir)
        meta = {"n": n, "seed": seed}
        (cache_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return result
