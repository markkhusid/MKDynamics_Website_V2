"""Passband transient analysis for Fig. 8-6.

The AC source (1 V) is replaced by a sine about the DC bias::

    Vin(t) = V_bias + A sin(2 π f t)

Default tone: f = 10 kHz (an octave below the 20 kHz design edge, so the
filter is operating in its passband) and A = 1 V (the same amplitude as
the AC source).  The measurement window is the last 0.5 ms of a 1.5 ms
run, which is five cycles after the third-order transient has died.

Steady-state gain and phase are fit with least squares on that window so
ngspice, LTspice, and the analytical solution are reduced the same way.
"""

from __future__ import annotations

import json
import os
import shutil
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

from .analysis import _nodal_matrices, dc_vout, gain_at
from .params import CircuitParams

# Passband probe. 10 kHz is below the ~20 kHz cutoff. 1 V peak matches AC mag.
F_PASSBAND_HZ = 10_000.0
TRAN_AMP_V = 1.0
TRAN_TSTEP_S = 1.0e-6
TRAN_TSTOP_S = 1.5e-3
TRAN_MEAS_FROM_S = 1.0e-3


@dataclass
class ToneMetrics:
    """Steady-state sine fit of one transient."""

    gain: float
    phase_deg: float
    vin_amp: float
    vout_amp: float
    vin_dc: float
    vout_dc: float

    def as_dict(self) -> dict[str, float]:
        return {
            "gain": self.gain,
            "phase_deg": self.phase_deg,
            "vin_amp": self.vin_amp,
            "vout_amp": self.vout_amp,
            "vin_dc": self.vin_dc,
            "vout_dc": self.vout_dc,
        }


def resolve_opa365_lib(root: Path | str) -> Path | None:
    """Return a local OPA365.lib if one is present. Do not copy the model.

    The redistributable path is ``models/opa365/OPA365.lib``.  A TI PSpice
    download unpacked under ``models/opa365/sboc133a/`` is also accepted for
    a local run.  Neither file is written by this package.
    """
    root = Path(root)
    candidates = [
        root / "models" / "opa365" / "OPA365.lib",
        root
        / "models"
        / "opa365"
        / "sboc133a"
        / "OPA365-PSpiceFiles"
        / "SCHEMATIC1"
        / "TransientAnalysis"
        / "OPA365.lib",
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def analytical_tone(
    p: CircuitParams,
    *,
    freq_hz: float = F_PASSBAND_HZ,
    amp_v: float = TRAN_AMP_V,
) -> ToneMetrics:
    """Steady-state gain and phase from H(j 2 π f). DC is the bias solution."""
    h = gain_at(p, freq_hz, "vin")
    vdc = dc_vout(p, vin=p.op.v_in_bias, vos=0.0, ibp=0.0, ibn=0.0)
    return ToneMetrics(
        gain=float(abs(h)),
        phase_deg=float(np.angle(h, deg=True)),
        vin_amp=float(amp_v),
        vout_amp=float(amp_v * abs(h)),
        vin_dc=float(p.op.v_in_bias),
        vout_dc=float(vdc),
    )


def analytical_waveform(
    p: CircuitParams,
    t: np.ndarray,
    *,
    freq_hz: float = F_PASSBAND_HZ,
    amp_v: float = TRAN_AMP_V,
) -> tuple[np.ndarray, np.ndarray]:
    """Vin(t), Vout(t) for the linear network, including startup.

    State equation from the nodal pencil ``(G + s C) v = vin * b``.
    Initial state is the DC solution at the bias, which is what SPICE uses
    when the sine source starts at phase 0.
    """
    from scipy.integrate import solve_ivp

    t = np.asarray(t, dtype=float)
    A0, b_vin, *_ = _nodal_matrices(0.0, p)
    A1, *_ = _nodal_matrices(1.0, p)
    G = np.real(A0)
    Cmat = np.real(A1 - A0)
    b_vin = np.real(b_vin)
    bias = float(p.op.v_in_bias)
    w = 2.0 * np.pi * float(freq_hz)

    def ode(tt, x):
        vin = bias + amp_v * np.sin(w * tt)
        return np.linalg.solve(Cmat, vin * b_vin - G @ x)

    x0 = np.linalg.solve(G, bias * b_vin)
    # max_step keeps the 10 kHz drive from being stepped over. The pencil is
    # stiff, and a loose BDF step can sit on the DC solution.
    sol = solve_ivp(
        ode,
        (float(t[0]), float(t[-1])),
        np.real(x0),
        t_eval=t,
        method="RK45",
        rtol=1e-6,
        atol=1e-8,
        max_step=min(1e-6, 0.02 / float(freq_hz)),
    )
    if not sol.success or sol.y.shape[1] != t.size:
        raise RuntimeError(f"analytical transient failed: {sol.message}")
    vin = bias + amp_v * np.sin(w * t)
    vout = sol.y[2]
    return vin, vout


def measure_tone(
    time: np.ndarray,
    vin: np.ndarray,
    vout: np.ndarray,
    *,
    freq_hz: float = F_PASSBAND_HZ,
    t_min: float = TRAN_MEAS_FROM_S,
) -> ToneMetrics:
    """Least-squares sine fit on ``time >= t_min``.

    Model: ``a sin(ωt) + b cos(ωt) + c``.  Amplitude is hypot(a, b).
    Phase is atan2(b, a), and the reported phase is Vout minus Vin.
    """
    time = np.asarray(time, dtype=float)
    vin = np.asarray(vin, dtype=float)
    vout = np.asarray(vout, dtype=float)
    m = time >= t_min
    if int(np.count_nonzero(m)) < 16:
        raise ValueError("measurement window has too few samples")
    tw = time[m]
    w = 2.0 * np.pi * float(freq_hz)
    S = np.column_stack([np.sin(w * tw), np.cos(w * tw), np.ones_like(tw)])
    av, *_ = np.linalg.lstsq(S, vin[m], rcond=None)
    ao, *_ = np.linalg.lstsq(S, vout[m], rcond=None)
    ain = float(np.hypot(av[0], av[1]))
    aout = float(np.hypot(ao[0], ao[1]))
    if ain < 1e-15:
        raise ValueError("fitted Vin amplitude is ~0")
    ph_in = float(np.arctan2(av[1], av[0]))
    ph_out = float(np.arctan2(ao[1], ao[0]))
    phase = float(np.rad2deg(np.angle(np.exp(1j * (ph_out - ph_in)))))
    return ToneMetrics(
        gain=aout / ain,
        phase_deg=phase,
        vin_amp=ain,
        vout_amp=aout,
        vin_dc=float(av[2]),
        vout_dc=float(ao[2]),
    )


def tone_from_peaks(
    vin_max: float,
    vin_min: float,
    vout_max: float,
    vout_min: float,
    t_vin: float | None = None,
    t_vout: float | None = None,
    *,
    freq_hz: float = F_PASSBAND_HZ,
) -> ToneMetrics:
    """Gain from peak-to-peak, phase from rising-crossing delay."""
    vin_pp = float(vin_max - vin_min)
    vout_pp = float(vout_max - vout_min)
    gain = vout_pp / vin_pp if abs(vin_pp) > 1e-15 else float("nan")
    phase = float("nan")
    if t_vin is not None and t_vout is not None and np.isfinite(t_vin) and np.isfinite(t_vout):
        delay = float(t_vout - t_vin)
        # A negative delay larger than half a period is the previous cycle.
        period = 1.0 / float(freq_hz)
        while delay > 0.5 * period:
            delay -= period
        while delay < -0.5 * period:
            delay += period
        phase = -360.0 * float(freq_hz) * delay
    return ToneMetrics(
        gain=gain,
        phase_deg=phase,
        vin_amp=0.5 * vin_pp,
        vout_amp=0.5 * vout_pp,
        vin_dc=0.5 * float(vin_max + vin_min),
        vout_dc=0.5 * float(vout_max + vout_min),
    )


def _passive_names(p: CircuitParams) -> list[str]:
    return list(p.resistance_names()) + list(p.capacitance_names())


def hypercube_corners(p: CircuitParams) -> list[dict]:
    """Every vertex of the R/C tolerance hypercube.

    Six passives, each at its low or high tolerance endpoint: 64 corners.
    Sign ``-`` is the low endpoint and ``+`` is the high endpoint.
    """
    names = _passive_names(p)
    rows = []
    for bits in product((0, 1), repeat=len(names)):
        values = {}
        signs = []
        for name, bit in zip(names, bits):
            lo, hi = p.tol_for(name).bounds(getattr(p, name))
            values[name] = lo if bit == 0 else hi
            signs.append(f"{name}{'-' if bit == 0 else '+'}")
        rows.append({"corner": " ".join(signs), **values})
    return rows


def _worker_ngspice(task: dict) -> dict:
    """Run one ngspice transient. Top-level so it can be pickled."""
    from .params import CircuitParams
    from .simulate import simulate_tran

    p = CircuitParams(**{k: task["nom"][k] for k in ("R1", "R2", "R3", "C1", "C2", "C3")})
    # Tolerances are unused for the solve; keep defaults.
    p = p.with_values(**task["values"])
    wd = Path(task["workdir"])
    try:
        tr = simulate_tran(
            p,
            opamp_model=task.get("opamp_model", "ideal"),
            workdir=wd,
            root=task["root"],
            freq_hz=task["freq_hz"],
            amp_v=task["amp_v"],
            temp_c=task.get("temp_c", 25.0),
            lib_path=task.get("lib_path"),
            timeout_s=task.get("timeout_s", 120.0),
        )
        m = measure_tone(
            tr.time, tr.vin, tr.vout, freq_hz=task["freq_hz"], t_min=task["t_min"]
        )
        out = {"ok": True, **m.as_dict()}
        if task.get("return_wave"):
            # Downsample for the notebook plot.
            step = max(1, len(tr.time) // 800)
            out["time"] = tr.time[::step].tolist()
            out["vin"] = tr.vin[::step].tolist()
            out["vout"] = tr.vout[::step].tolist()
    except Exception as exc:  # one corner must not kill the batch
        out = {"ok": False, "error": str(exc)}
    if not task.get("keep_runs", False):
        shutil.rmtree(wd, ignore_errors=True)
    return out


def run_ngspice_cases(
    p: CircuitParams,
    cases: list[dict],
    *,
    workdir: Path | str,
    root: Path | str,
    freq_hz: float = F_PASSBAND_HZ,
    amp_v: float = TRAN_AMP_V,
    t_min: float = TRAN_MEAS_FROM_S,
    workers: int = 4,
    opamp_model: str = "ideal",
    temp_c: float = 25.0,
    lib_path: Path | None = None,
    keep_runs: bool = False,
) -> list[dict]:
    """Transient sine-fit for each case. ``cases`` items hold R/C overrides."""
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    nom = p.passive_dict()
    tasks = []
    for i, case in enumerate(cases):
        values = {k: float(case[k]) for k in nom}
        tasks.append(
            {
                "nom": nom,
                "values": values,
                "workdir": str(workdir / f"run_{i:04d}"),
                "root": str(root),
                "freq_hz": freq_hz,
                "amp_v": amp_v,
                "t_min": t_min,
                "opamp_model": opamp_model,
                "temp_c": temp_c,
                "lib_path": str(lib_path) if lib_path else None,
                "keep_runs": keep_runs,
            }
        )
    if workers <= 1 or len(tasks) == 1:
        return [_worker_ngspice(t) for t in tasks]
    # Process pool. ngspice is a separate executable, so processes are safe.
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(_worker_ngspice, tasks))


def _wrap_phase_deg(delay_s: float, freq_hz: float) -> float:
    period = 1.0 / float(freq_hz)
    delay = float(delay_s)
    while delay > 0.5 * period:
        delay -= period
    while delay < -0.5 * period:
        delay += period
    return -360.0 * float(freq_hz) * delay


def write_ltspice_stepped_tran(
    path: Path | str,
    p: CircuitParams,
    cases: list[dict],
    *,
    freq_hz: float = F_PASSBAND_HZ,
    amp_v: float = TRAN_AMP_V,
    tstep_s: float = 2.0e-7,
    tstop_s: float = TRAN_TSTOP_S,
    tmeas_from_s: float = TRAN_MEAS_FROM_S,
) -> Path:
    """One LTspice deck that steps every case with ``table(idx, ...)``.

    Component values are the only thing that changes.  The source is the
    same 10 kHz sine on every step.  Continuation lines keep each table
    under a few kilobytes.
    """
    names = _passive_names(p)
    n = len(cases)
    if n < 1:
        raise ValueError("no cases")

    def table_lines(comp: str) -> str:
        """``.param R1=table(idx, 1, v1, 2, v2, ...)`` with '+' continuations."""
        current = f".param {comp}=table(idx"
        out: list[str] = []
        for i, case in enumerate(cases, start=1):
            piece = f", {i}, {float(case[comp]):.12g}"
            if len(current) + len(piece) > 240:
                out.append(current)
                current = "+" + piece
            else:
                current += piece
        out.append(current + ")")
        return "\n".join(out)

    tables = "\n".join(table_lines(comp) for comp in names)
    sp = p.as_spice_params()
    # R/C come from the tables, not the nominal .param lines.
    fixed = "\n".join(
        f".param {k}={v:.12g}"
        for k, v in sp.items()
        if k not in names
    )
    text = "\n".join(
        [
            "* Fig. 8-6 stepped passband transient. Source is a sine, not AC.",
            f"* {n} cases, f={freq_hz:.12g} Hz, amp={amp_v:.12g} V",
            ".param idx=1",
            f".step param idx 1 {n} 1",
            fixed,
            tables,
            "VOS n3 vplus DC {VOS}",
            "IBP n3 0 DC {IBP}",
            "IBN vout 0 DC {IBN}",
            "EAMP vout 0 vplus vout 1e6",
            "R1 vin n1 {R1}",
            "C1 n1 0 {C1}",
            "R2 n1 n2 {R2}",
            "R3 n2 n3 {R3}",
            "C2 n3 0 {C2}",
            "C3 n2 vout {C3}",
            "Rload vout 0 {RLOAD}",
            "Rbleed vcc 0 10Meg",
            f"Vin vin 0 SINE({{VINBIAS}} {amp_v:.12g} {freq_hz:.12g})",
            "Vcc vcc 0 {VSUP}",
            ".temp 25",
            f".tran 0 {tstop_s:.12g} 0 {tstep_s:.12g}",
            f".four {freq_hz:.12g} 1 5 V(vin) V(vout)",
            ".end",
            "",
        ]
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def parse_four_log(log_path: Path | str) -> pd.DataFrame:
    """Gain and phase from LTspice ``.four`` blocks, one row per ``.step``.

    LTspice reports the cosine-series phase with the opposite sign of the
    engineering phasor (a sine is listed at +90°, not −90°).  The transfer
    phase is ``phase_column(Vin) − phase_column(Vout)``, which matches
    ``angle(Vout/Vin)``.
    """
    import re

    text = Path(log_path).read_text(encoding="utf-8", errors="replace")
    blocks = re.findall(
        r"(?is)Fourier components of V\((\w+)\).*?DC component:\s*"
        r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
        r".*?^\s*1\s+[0-9eE.+\-]+\s+"
        r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s+"
        r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\s+"
        r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)",
        text,
        flags=re.M,
    )
    if len(blocks) < 2 or len(blocks) % 2:
        raise RuntimeError(
            f"Expected Vin/Vout .four pairs in {log_path}, found {len(blocks)} blocks"
        )
    rows = []
    for i in range(0, len(blocks), 2):
        n1, dc1, mag1, ph1 = blocks[i]
        n2, dc2, mag2, ph2 = blocks[i + 1]
        if n1.lower() != "vin" or n2.lower() != "vout":
            raise RuntimeError(f"Unexpected .four order {n1}, {n2} in {log_path}")
        mag_in = float(mag1)
        mag_out = float(mag2)
        phase = float(ph1) - float(ph2)
        rows.append(
            {
                "gain": mag_out / mag_in,
                "phase_deg": phase,
                "vin_amp": mag_in,
                "vout_amp": mag_out,
                "vin_dc": float(dc1),
                "vout_dc": float(dc2),
            }
        )
    return pd.DataFrame(rows)


def parse_stepped_meas(log_path: Path | str) -> dict[str, np.ndarray]:
    """Parse an LTspice log of stepped ``.meas TRAN`` results.

    Accepts both the single-step ``name: ... = value`` form and the
    stepped table::

        Measurement: vin_max
          step    vin_max
             1    3.5
    """
    import re

    text = Path(log_path).read_text(encoding="utf-8", errors="replace")
    found: dict[str, list[tuple[int, float]]] = {}
    # Stepped tables.
    blocks = re.split(r"(?im)^Measurement:\s*", text)
    for block in blocks[1:]:
        lines = block.splitlines()
        name = lines[0].strip().lower()
        rows = []
        for line in lines[1:]:
            m = re.match(
                r"^\s*(\d+)\s+([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)",
                line,
            )
            if m:
                rows.append((int(m.group(1)), float(m.group(2))))
            elif rows and line.strip() and not line.strip().lower().startswith("step"):
                # End of this measurement table.
                if not re.match(r"^\s*\d+", line):
                    break
        if rows:
            found[name] = rows
    if found:
        out = {}
        for name, rows in found.items():
            rows = sorted(rows, key=lambda r: r[0])
            out[name] = np.array([v for _, v in rows], dtype=float)
        return out

    # Single step: fall back to the AC meas parser.
    from .ltspice_io import parse_meas_log

    meas = parse_meas_log(log_path)
    out = {}
    for key in ("vin_max", "vin_min", "vout_max", "vout_min", "t_vin", "t_vout"):
        if key in meas:
            out[key] = np.array([meas[key]], dtype=float)
        elif f"{key}_at_hz" in meas:
            out[key] = np.array([meas[f"{key}_at_hz"]], dtype=float)
    return out


def stepped_metrics_frame(
    meas: dict[str, np.ndarray],
    *,
    freq_hz: float = F_PASSBAND_HZ,
) -> pd.DataFrame:
    """Turn stepped peak/crossing measurements into gain and phase."""
    n = len(meas["vin_max"])
    rows = []
    t_vin = meas.get("t_vin")
    t_vout = meas.get("t_vout")
    for i in range(n):
        tv = float(t_vin[i]) if t_vin is not None and i < len(t_vin) else None
        to = float(t_vout[i]) if t_vout is not None and i < len(t_vout) else None
        m = tone_from_peaks(
            meas["vin_max"][i],
            meas["vin_min"][i],
            meas["vout_max"][i],
            meas["vout_min"][i],
            tv,
            to,
            freq_hz=freq_hz,
        )
        rows.append(m.as_dict())
    return pd.DataFrame(rows)


def draw_mc_samples(
    p: CircuitParams,
    *,
    n: int = 500,
    seed: int = 42,
) -> list[dict]:
    """Uniform R/C draws. Same generator as the analytical Monte Carlo."""
    from .monte_carlo import _draw_passives

    rng = np.random.default_rng(seed)
    rows = []
    for i in range(int(n)):
        rows.append({"sample": i, **_draw_passives(p, rng)})
    return rows


def _cache_ok(path: Path, meta: dict) -> bool:
    meta_path = path.with_suffix(".meta.json")
    if not path.is_file() or not meta_path.is_file():
        return False
    have = json.loads(meta_path.read_text(encoding="utf-8"))
    return all(have.get(k) == v for k, v in meta.items())


def _write_cache(path: Path, frame: pd.DataFrame, meta: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    path.with_suffix(".meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


def load_or_run_hypercube(
    p: CircuitParams,
    *,
    root: Path | str,
    cache_csv: Path | str,
    workers: int = 4,
    run_ltspice: bool = True,
) -> pd.DataFrame:
    """64-corner transient hypercube: analytical, ngspice, and LTspice."""
    root = Path(root)
    cache_csv = Path(cache_csv)
    meta = {"kind": "hypercube", "n": 64, "freq_hz": F_PASSBAND_HZ, "amp_v": TRAN_AMP_V}
    if _cache_ok(cache_csv, meta):
        return pd.read_csv(cache_csv)

    corners = hypercube_corners(p)
    an_rows = []
    for case in corners:
        pc = p.with_values(**{k: case[k] for k in p.passive_dict()})
        m = analytical_tone(pc)
        an_rows.append({"corner": case["corner"], **{f"an_{k}": v for k, v in m.as_dict().items()}})
    an = pd.DataFrame(an_rows)

    ng = run_ngspice_cases(
        p,
        corners,
        workdir=cache_csv.parent / "_ng_wc",
        root=root,
        workers=workers,
    )
    ng_df = pd.DataFrame(
        [
            {f"ng_{k}": r.get(k, np.nan) for k in ("gain", "phase_deg", "vout_amp", "error")}
            | {"ng_ok": r.get("ok", False)}
            for r in ng
        ]
    )

    lt_df = pd.DataFrame({"lt_gain": np.nan, "lt_phase_deg": np.nan, "lt_ok": False}, index=range(64))
    if run_ltspice:
        from .ltspice_io import run_ltspice_deck

        deck = cache_csv.parent / "wc_tran_step.cir"
        write_ltspice_stepped_tran(deck, p, corners)
        log = run_ltspice_deck(deck, timeout_s=600)
        stepped = parse_four_log(log)
        if len(stepped) != len(corners):
            raise RuntimeError(
                f"LTspice hypercube returned {len(stepped)} steps, expected {len(corners)}"
            )
        lt_df = pd.DataFrame(
            {
                "lt_gain": stepped["gain"].to_numpy(),
                "lt_phase_deg": stepped["phase_deg"].to_numpy(),
                "lt_vout_amp": stepped["vout_amp"].to_numpy(),
                "lt_ok": True,
            }
        )

    frame = pd.concat([an, ng_df, lt_df], axis=1)
    # Component values beside the corner label.
    vals = pd.DataFrame([{k: c[k] for k in p.passive_dict()} for c in corners])
    frame = pd.concat([frame, vals], axis=1)
    _write_cache(cache_csv, frame, meta)
    shutil.rmtree(cache_csv.parent / "_ng_wc", ignore_errors=True)
    return frame


def load_or_run_mc(
    p: CircuitParams,
    *,
    root: Path | str,
    cache_csv: Path | str,
    n: int = 500,
    seed: int = 42,
    workers: int = 4,
    run_ltspice: bool = True,
) -> pd.DataFrame:
    """Uniform Monte Carlo of the 10 kHz transient gain. Same draws for all three."""
    root = Path(root)
    cache_csv = Path(cache_csv)
    meta = {
        "kind": "mc",
        "n": int(n),
        "seed": int(seed),
        "freq_hz": F_PASSBAND_HZ,
        "amp_v": TRAN_AMP_V,
    }
    if _cache_ok(cache_csv, meta):
        return pd.read_csv(cache_csv)

    cases = draw_mc_samples(p, n=n, seed=seed)
    an_rows = []
    for case in cases:
        pc = p.with_values(**{k: case[k] for k in p.passive_dict()})
        m = analytical_tone(pc)
        an_rows.append({"sample": case["sample"], **{f"an_{k}": v for k, v in m.as_dict().items()}})
    an = pd.DataFrame(an_rows)

    ng = run_ngspice_cases(
        p,
        cases,
        workdir=cache_csv.parent / "_ng_mc",
        root=root,
        workers=workers,
    )
    ng_df = pd.DataFrame(
        [
            {f"ng_{k}": r.get(k, np.nan) for k in ("gain", "phase_deg")}
            | {"ng_ok": r.get("ok", False)}
            for r in ng
        ]
    )

    lt_df = pd.DataFrame({"lt_gain": np.nan, "lt_phase_deg": np.nan}, index=range(n))
    if run_ltspice:
        from .ltspice_io import run_ltspice_deck

        deck = cache_csv.parent / "mc_tran_step.cir"
        write_ltspice_stepped_tran(deck, p, cases)
        log = run_ltspice_deck(deck, timeout_s=1800)
        stepped = parse_four_log(log)
        if len(stepped) != n:
            raise RuntimeError(f"LTspice MC returned {len(stepped)} steps, expected {n}")
        lt_df = pd.DataFrame(
            {"lt_gain": stepped["gain"].to_numpy(), "lt_phase_deg": stepped["phase_deg"].to_numpy()}
        )

    vals = pd.DataFrame(cases)
    frame = pd.concat([vals, an.drop(columns=["sample"]), ng_df, lt_df], axis=1)
    _write_cache(cache_csv, frame, meta)
    shutil.rmtree(cache_csv.parent / "_ng_mc", ignore_errors=True)
    return frame


def load_or_run_temperature(
    p: CircuitParams,
    *,
    root: Path | str,
    cache_csv: Path | str,
    temps_c: list[float] | None = None,
    workers: int = 4,
    run_ltspice: bool = True,
) -> pd.DataFrame:
    """10 kHz transient gain versus temperature.

    Passives follow the linear TCR/TCC in ``CircuitParams.tempco``.  The
    ideal VCVS has no semiconductor temperature law, so ngspice and LTspice
    see the same scaled R and C as the analytical model.
    """
    root = Path(root)
    cache_csv = Path(cache_csv)
    if temps_c is None:
        temps_c = [float(t) for t in p.tempco.grid()]
    meta = {
        "kind": "temperature",
        "n": len(temps_c),
        "t_min": float(min(temps_c)),
        "t_max": float(max(temps_c)),
        "freq_hz": F_PASSBAND_HZ,
    }
    if _cache_ok(cache_csv, meta):
        return pd.read_csv(cache_csv)

    cases = []
    for T in temps_c:
        pt = p.scaled_at_temp(float(T))
        cases.append({"temp_c": float(T), **pt.passive_dict()})
    an_rows = []
    for case in cases:
        pc = p.with_values(**{k: case[k] for k in p.passive_dict()})
        m = analytical_tone(pc)
        an_rows.append({"temp_c": case["temp_c"], **{f"an_{k}": v for k, v in m.as_dict().items()}})
    an = pd.DataFrame(an_rows)
    ng = run_ngspice_cases(p, cases, workdir=cache_csv.parent / "_ng_temp", root=root, workers=workers)
    ng_df = pd.DataFrame([{f"ng_{k}": r.get(k, np.nan) for k in ("gain", "phase_deg")} for r in ng])
    lt_df = pd.DataFrame({"lt_gain": np.nan, "lt_phase_deg": np.nan}, index=range(len(cases)))
    if run_ltspice:
        from .ltspice_io import run_ltspice_deck

        deck = cache_csv.parent / "temp_tran_step.cir"
        write_ltspice_stepped_tran(deck, p, cases)
        log = run_ltspice_deck(deck, timeout_s=600)
        stepped = parse_four_log(log)
        if len(stepped) != len(cases):
            raise RuntimeError(f"LTspice temperature run returned {len(stepped)} steps")
        lt_df = pd.DataFrame(
            {"lt_gain": stepped["gain"].to_numpy(), "lt_phase_deg": stepped["phase_deg"].to_numpy()}
        )
    frame = pd.concat([an, ng_df, lt_df], axis=1)
    _write_cache(cache_csv, frame, meta)
    shutil.rmtree(cache_csv.parent / "_ng_temp", ignore_errors=True)
    return frame


def summary_table(frame: pd.DataFrame, cols: list[tuple[str, str]]) -> pd.DataFrame:
    """Mean / std / min / max / p05 / p95 for named columns."""
    rows = []
    for label, col in cols:
        s = frame[col].dropna()
        rows.append(
            {
                "result": label,
                "mean": float(s.mean()),
                "std": float(s.std()),
                "min": float(s.min()),
                "p05": float(s.quantile(0.05)),
                "p95": float(s.quantile(0.95)),
                "max": float(s.max()),
            }
        )
    return pd.DataFrame(rows)
