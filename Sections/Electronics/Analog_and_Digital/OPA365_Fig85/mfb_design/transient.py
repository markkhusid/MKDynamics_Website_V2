"""250 kHz passband transient for Figure 8-5.

Vin(t) = A sin(2 π f t), with A = 1 V and f = 250 kHz. There is no DC
offset. The run is 100 µs. Gain and phase are fit on the last 40 µs.

The analytical waveform is integrated on the same time vector the solver
saved. A compressed waveform is not interpolated onto a new grid.
"""

from __future__ import annotations

import json
import shutil
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

from .analysis import dc_vout, gain_at, state_matrices
from .params import CircuitParams

F_PASSBAND_HZ = 250_000.0
TRAN_AMP_V = 1.0
TRAN_TSTEP_S = 40.0e-9
TRAN_TSTOP_S = 100.0e-6
TRAN_MEAS_FROM_S = 60.0e-6
LT_MAXSTEP_S = 8.0e-9


@dataclass
class ToneMetrics:
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

    Looks in this tree first, then in a sibling Figure 8-6 checkout, so a
    local macromodel can be used without being committed here.
    """
    root = Path(root)
    names = [
        Path("models") / "opa365" / "OPA365.lib",
        Path("models")
        / "opa365"
        / "sboc133a"
        / "OPA365-PSpiceFiles"
        / "SCHEMATIC1"
        / "TransientAnalysis"
        / "OPA365.lib",
    ]
    roots = [root, root.parent / "OPA365_Fig86_Sallen_Key"]
    for base in roots:
        for rel in names:
            cand = base / rel
            if cand.is_file():
                return cand
    return None


def analytical_tone(
    p: CircuitParams,
    *,
    freq_hz: float = F_PASSBAND_HZ,
    amp_v: float = TRAN_AMP_V,
) -> ToneMetrics:
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
    """Vin(t) and Vout(t), including startup from the DC bias state."""
    from scipy.integrate import solve_ivp

    t = np.asarray(t, dtype=float)
    g, cmat, b_vin, _b_vos, _b_ibn = state_matrices(p)
    bias = float(p.op.v_in_bias)
    w = 2.0 * np.pi * float(freq_hz)
    max_step = min(40e-9, 0.02 / float(freq_hz))

    def ode(tt, x):
        vin = bias + amp_v * np.sin(w * tt)
        return np.linalg.solve(cmat, vin * b_vin - g @ x)

    x0 = np.linalg.solve(g, bias * b_vin)
    sol = solve_ivp(
        ode,
        (float(t[0]), float(t[-1])),
        np.real(x0),
        t_eval=t,
        method="RK45",
        rtol=1e-6,
        atol=1e-8,
        max_step=max_step,
    )
    if not sol.success or sol.y.shape[1] != t.size:
        raise RuntimeError(f"analytical transient failed: {sol.message}")
    vin = bias + amp_v * np.sin(w * t)
    return vin, sol.y[1]


def measure_tone(
    time: np.ndarray,
    vin: np.ndarray,
    vout: np.ndarray,
    *,
    freq_hz: float = F_PASSBAND_HZ,
    t_min: float = TRAN_MEAS_FROM_S,
) -> ToneMetrics:
    """Least-squares fit of a sin + b cos + c on time >= t_min.

    Phase is the output phase minus the input phase, in degrees, wrapped
    to (−180, 180].
    """
    time = np.asarray(time, dtype=float)
    vin = np.asarray(vin, dtype=float)
    vout = np.asarray(vout, dtype=float)
    m = time >= t_min
    if int(np.count_nonzero(m)) < 16:
        raise ValueError("measurement window has too few samples")
    tw = time[m]
    w = 2.0 * np.pi * float(freq_hz)
    s = np.column_stack([np.sin(w * tw), np.cos(w * tw), np.ones_like(tw)])
    av, *_ = np.linalg.lstsq(s, vin[m], rcond=None)
    ao, *_ = np.linalg.lstsq(s, vout[m], rcond=None)
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


def waveform_error(
    v_spice: np.ndarray,
    v_ref: np.ndarray,
    time: np.ndarray,
    *,
    t_min: float = TRAN_MEAS_FROM_S,
) -> dict[str, float]:
    """Residual on the solver's own samples. No interpolation."""
    m = np.asarray(time) >= t_min
    err = np.asarray(v_spice)[m] - np.asarray(v_ref)[m]
    return {
        "max_abs_v": float(np.max(np.abs(err))),
        "rms_v": float(np.sqrt(np.mean(err ** 2))),
        "n": int(err.size),
    }


def _passive_names(p: CircuitParams) -> list[str]:
    return list(p.resistance_names()) + list(p.capacitance_names())


def hypercube_corners(p: CircuitParams) -> list[dict]:
    """Every vertex of the R/C tolerance box. Five parts give 32 corners."""
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
    """One ngspice transient. Top-level so a process pool can pickle it."""
    from .params import CircuitParams
    from .simulate import scrub_text, simulate_tran

    p = CircuitParams().with_values(**task["values"])
    wd = Path(task["workdir"])
    try:
        lib = task.get("lib_path")
        tr = simulate_tran(
            p,
            opamp_model=task.get("opamp_model", "ideal"),
            workdir=wd,
            root=task["root"],
            freq_hz=task["freq_hz"],
            amp_v=task["amp_v"],
            temp_c=task.get("temp_c", 25.0),
            lib_path=Path(lib) if lib else None,
            timeout_s=task.get("timeout_s", 180.0),
        )
        m = measure_tone(tr.time, tr.vin, tr.vout, freq_hz=task["freq_hz"], t_min=task["t_min"])
        out = {"ok": True, **m.as_dict()}
        if task.get("return_wave"):
            step = max(1, len(tr.time) // 800)
            out["time"] = tr.time[::step].tolist()
            out["vin"] = tr.vin[::step].tolist()
            out["vout"] = tr.vout[::step].tolist()
    except Exception as exc:
        out = {"ok": False, "error": scrub_text(str(exc))[:300]}
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
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    nom = p.passive_dict()
    tasks = []
    for i, case in enumerate(cases):
        values = {k: float(case[k]) for k in nom}
        tasks.append(
            {
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
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(_worker_ngspice, tasks))


def write_ltspice_stepped_tran(
    path: Path | str,
    p: CircuitParams,
    cases: list[dict],
    *,
    freq_hz: float = F_PASSBAND_HZ,
    amp_v: float = TRAN_AMP_V,
    tstep_s: float = LT_MAXSTEP_S,
    tstop_s: float = TRAN_TSTOP_S,
) -> Path:
    """One deck that steps every case with table(idx, ...).

    Only the passives change. The source is the same 250 kHz sine.
    """
    names = _passive_names(p)
    n = len(cases)
    if n < 1:
        raise ValueError("no cases")

    def table_lines(comp: str) -> str:
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
    fixed = "\n".join(
        f".param {k}={v:.12g}"
        for k, v in p.as_spice_params().items()
        if k not in names
    )
    text = "\n".join(
        [
            "* Fig. 8-5 stepped passband transient. Source is a sine.",
            f"* {n} cases, f={freq_hz:.12g} Hz, amp={amp_v:.12g} V",
            ".param idx=1",
            f".step param idx 1 {n} 1",
            fixed,
            tables,
            "VOS 0 vplus DC {VOS}",
            "IBP vplus 0 DC {IBP}",
            "IBN n2 0 DC {IBN}",
            "EAMP vout 0 vplus n2 1e6",
            "R1 vin n1 {R1}",
            "C1 n1 0 {C1}",
            "R3 n1 vout {R3}",
            "R2 n1 n2 {R2}",
            "C2 n2 vout {C2}",
            "Rload vout 0 {RLOAD}",
            "Rbleed vcc 0 10Meg",
            "Rbleedn vee 0 10Meg",
            f"Vin vin 0 SINE(0 {amp_v:.12g} {freq_hz:.12g})",
            "Vcc vcc 0 {VPOS}",
            "Vee vee 0 {VNEG}",
            ".temp 25",
            ".options plotwinsize=0",
            ".save V(vin) V(vout)",
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
    """Gain and phase from LTspice .four blocks, one row per .step.

    A sine is listed at phase +90°. Transfer phase is the Vin column minus
    the Vout column, which matches angle(Vout/Vin).
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
        raise RuntimeError(f".four parser found {len(blocks)} blocks, expected Vin/Vout pairs")
    rows = []
    for i in range(0, len(blocks), 2):
        n1, dc1, mag1, ph1 = blocks[i]
        n2, dc2, mag2, ph2 = blocks[i + 1]
        if n1.lower() != "vin" or n2.lower() != "vout":
            raise RuntimeError(f"Unexpected .four order {n1}, {n2}")
        mag_in = float(mag1)
        mag_out = float(mag2)
        phase = (float(ph1) - float(ph2) + 180.0) % 360.0 - 180.0
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


def draw_mc_samples(p: CircuitParams, *, n: int = 500, seed: int = 42) -> list[dict]:
    from .monte_carlo import _draw_passives

    rng = np.random.default_rng(seed)
    return [{"sample": i, **_draw_passives(p, rng)} for i in range(int(n))]


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


def _ng_frame(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {f"ng_{k}": r.get(k, np.nan) for k in ("gain", "phase_deg", "vout_amp", "error")}
            | {"ng_ok": bool(r.get("ok", False))}
            for r in rows
        ]
    )


def load_or_run_hypercube(
    p: CircuitParams,
    *,
    root: Path | str,
    cache_csv: Path | str,
    workers: int = 4,
    run_ltspice: bool = True,
) -> pd.DataFrame:
    """32-corner transient hypercube: analytical, ngspice, and LTspice."""
    root = Path(root)
    cache_csv = Path(cache_csv)
    corners = hypercube_corners(p)
    meta = {
        "kind": "hypercube",
        "n": len(corners),
        "freq_hz": F_PASSBAND_HZ,
        "amp_v": TRAN_AMP_V,
    }
    if _cache_ok(cache_csv, meta):
        return pd.read_csv(cache_csv)

    an_rows = []
    for case in corners:
        pc = p.with_values(**{k: case[k] for k in p.passive_dict()})
        m = analytical_tone(pc)
        an_rows.append({"corner": case["corner"], **{f"an_{k}": v for k, v in m.as_dict().items()}})
    an = pd.DataFrame(an_rows)
    ng = run_ngspice_cases(p, corners, workdir=cache_csv.parent / "_ng_wc", root=root, workers=workers)
    ng_df = _ng_frame(ng)

    lt_df = pd.DataFrame(
        {"lt_gain": np.nan, "lt_phase_deg": np.nan, "lt_ok": False},
        index=range(len(corners)),
    )
    if run_ltspice:
        from .ltspice_io import run_ltspice_deck

        deck = cache_csv.parent / "wc_tran_step.cir"
        write_ltspice_stepped_tran(deck, p, corners)
        log = run_ltspice_deck(deck, timeout_s=900)
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
    vals = pd.DataFrame([{k: c[k] for k in p.passive_dict()} for c in corners])
    frame = pd.concat([an, ng_df, lt_df, vals], axis=1)
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
    """Uniform Monte Carlo of the 250 kHz transient. Same draws for all three."""
    root = Path(root)
    cache_csv = Path(cache_csv)
    meta = {
        "kind": "mc_tran",
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
    ng = run_ngspice_cases(p, cases, workdir=cache_csv.parent / "_ng_mc", root=root, workers=workers)
    ng_df = _ng_frame(ng)
    lt_df = pd.DataFrame({"lt_gain": np.nan, "lt_phase_deg": np.nan}, index=range(n))
    if run_ltspice:
        from .ltspice_io import run_ltspice_deck

        deck = cache_csv.parent / "mc_tran_step.cir"
        write_ltspice_stepped_tran(deck, p, cases)
        log = run_ltspice_deck(deck, timeout_s=2400)
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
    """250 kHz transient gain versus temperature.

    Passives follow the linear TCR/TCC. The ideal VCVS has no semiconductor
    temperature law, so ngspice and LTspice see the same scaled R and C.
    """
    root = Path(root)
    cache_csv = Path(cache_csv)
    if temps_c is None:
        temps_c = [float(t) for t in p.tempco.grid()]
    meta = {
        "kind": "temperature_tran",
        "n": len(temps_c),
        "t_min": float(min(temps_c)),
        "t_max": float(max(temps_c)),
        "freq_hz": F_PASSBAND_HZ,
    }
    if _cache_ok(cache_csv, meta):
        return pd.read_csv(cache_csv)

    cases = []
    for temp in temps_c:
        pt = p.scaled_at_temp(float(temp))
        cases.append({"temp_c": float(temp), **pt.passive_dict()})
    an_rows = []
    for case in cases:
        pc = p.with_values(**{k: case[k] for k in p.passive_dict()})
        m = analytical_tone(pc)
        an_rows.append({"temp_c": case["temp_c"], **{f"an_{k}": v for k, v in m.as_dict().items()}})
    an = pd.DataFrame(an_rows)
    ng = run_ngspice_cases(p, cases, workdir=cache_csv.parent / "_ng_temp", root=root, workers=workers)
    ng_df = pd.DataFrame(
        [{f"ng_{k}": r.get(k, np.nan) for k in ("gain", "phase_deg")} | {"ng_ok": bool(r.get("ok", False))} for r in ng]
    )
    lt_df = pd.DataFrame({"lt_gain": np.nan, "lt_phase_deg": np.nan}, index=range(len(cases)))
    if run_ltspice:
        from .ltspice_io import run_ltspice_deck

        deck = cache_csv.parent / "temp_tran_step.cir"
        write_ltspice_stepped_tran(deck, p, cases)
        log = run_ltspice_deck(deck, timeout_s=900)
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
