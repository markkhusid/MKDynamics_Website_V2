"""Run ngspice and parse AC / OP / TRAN results.

HOW TO USE YOUR OWN NETLIST
---------------------------
>>> from opamp_design.simulate import run_external_netlist, parse_ac_wrdata
>>> run_external_netlist(Path("my_filter.cir"), workdir=Path("results/custom"))
>>> # If you used wrdata like the generated decks:
>>> ac = parse_ac_complex_wrdata(workdir / "vout_complex.data")

If your deck uses different ``wrdata`` columns, write a thin adapter that
returns an ``AcResult`` (f_hz, vout complex, vin complex) — notebooks only
need that struct for plotting against analytical H(s).

Environment
-----------
* ``NGSPICE_EXE`` — full path to ngspice if not on PATH
* Search also covers common conda/miniforge Windows locations.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .netlist import NetlistOptions, write_netlist
from .params import CircuitParams


@dataclass
class AcResult:
    """AC sweep: complex Vout and Vin vs frequency."""

    f_hz: np.ndarray
    vout: np.ndarray  # complex
    vin: np.ndarray  # complex

    @property
    def h(self) -> np.ndarray:
        """Vout/Vin transfer (handles vin≈0 safely)."""
        vin = np.where(np.abs(self.vin) < 1e-30, 1e-30, self.vin)
        return self.vout / vin

    @property
    def mag_db(self) -> np.ndarray:
        return 20.0 * np.log10(np.maximum(np.abs(self.h), 1e-30))

    @property
    def phase_deg(self) -> np.ndarray:
        return np.angle(self.h, deg=True)


@dataclass
class OpResult:
    """DC operating-point node voltages."""

    nodes: dict[str, float]


@dataclass
class TranResult:
    time: np.ndarray
    vout: np.ndarray
    vin: np.ndarray


def find_ngspice(explicit: str | Path | None = None) -> Path:
    """Locate ngspice executable (same search idea as typical EE setups)."""
    if explicit is not None:
        p = Path(explicit)
        if p.is_file():
            return p
        raise FileNotFoundError(f"ngspice not found at {p}")

    env = os.environ.get("NGSPICE_EXE")
    if env:
        p = Path(env)
        if p.is_file():
            return p

    which = shutil.which("ngspice")
    if which:
        return Path(which)

    for base in (
        Path(os.environ.get("CONDA_PREFIX", "")),
        Path.home() / "miniforge3",
        Path.home() / "mambaforge",
        Path.home() / "anaconda3",
        Path.home() / "miniconda3",
    ):
        if not base or not str(base) or not base.exists():
            continue
        for cand in (
            base / "Library" / "bin" / "ngspice_con.exe",
            base / "Library" / "bin" / "ngspice.exe",
            base / "bin" / "ngspice",
        ):
            if cand.is_file():
                return cand
    raise FileNotFoundError(
        "ngspice not found. Install via conda-forge or set NGSPICE_EXE."
    )


def run_ngspice(
    cir_path: Path,
    workdir: Path | None = None,
    ngspice: Path | str | None = None,
    timeout_s: float = 120.0,
) -> subprocess.CompletedProcess:
    """Batch-run a deck; log written to ``workdir/ngspice.log``."""
    cir_path = Path(cir_path).resolve()
    workdir = Path(workdir) if workdir is not None else cir_path.parent
    workdir.mkdir(parents=True, exist_ok=True)
    exe = find_ngspice(ngspice)
    log_path = workdir / "ngspice.log"
    # -b batch, -o log; run with cwd=workdir so wrdata lands there
    cmd = [str(exe), "-b", "-o", str(log_path), str(cir_path)]
    proc = subprocess.run(
        cmd,
        cwd=str(workdir),
        capture_output=True,
        text=True,
        timeout=timeout_s,
    )
    # Append stderr to log for debugging
    if proc.stdout or proc.stderr:
        with log_path.open("a", encoding="utf-8", errors="replace") as fh:
            fh.write("\n--- stdout ---\n")
            fh.write(proc.stdout or "")
            fh.write("\n--- stderr ---\n")
            fh.write(proc.stderr or "")
    return proc


def parse_ac_complex_wrdata(path: Path) -> AcResult:
    """Parse ``wrdata vout_complex real(v(vout)) imag(v(vout)) real(v(vin)) imag(v(vin))``.

    ngspice wrdata writes:  freq  col1  freq  col2  freq  col3  ...
    so for 4 values we get columns [f, re_out, f, im_out, f, re_in, f, im_in].
    """
    path = Path(path)
    # ngspice may write .data suffix or the bare name
    candidates = [path]
    if path.suffix == "":
        candidates.append(Path(str(path) + ".data"))
    else:
        candidates.append(path.with_suffix(path.suffix + ".data"))
        candidates.append(path.with_suffix(".data"))
    # Also try workdir default names
    for c in list(candidates):
        if c.parent.joinpath(c.name + ".data").exists():
            candidates.append(c.parent / (c.name + ".data"))

    data_path = next((c for c in candidates if c.is_file()), None)
    if data_path is None:
        # search for vout_complex*
        parent = path.parent if path.parent.exists() else Path.cwd()
        hits = list(parent.glob("vout_complex*"))
        if not hits:
            raise FileNotFoundError(f"AC wrdata not found near {path}")
        data_path = hits[0]

    raw = np.loadtxt(data_path)
    if raw.ndim == 1:
        raw = raw.reshape(1, -1)
    # Expected 8 columns
    if raw.shape[1] >= 8:
        f = raw[:, 0]
        vout = raw[:, 1] + 1j * raw[:, 3]
        vin = raw[:, 5] + 1j * raw[:, 7]
    elif raw.shape[1] >= 4:
        f = raw[:, 0]
        vout = raw[:, 1] + 1j * raw[:, 3]
        vin = np.ones_like(f, dtype=complex)
    else:
        raise ValueError(f"Unexpected wrdata shape {raw.shape} in {data_path}")
    return AcResult(f_hz=f, vout=vout, vin=vin)


def parse_op_log(log_path: Path) -> OpResult:
    """Best-effort parse of ``print v(vout)`` style lines from the log."""
    text = Path(log_path).read_text(encoding="utf-8", errors="replace")
    nodes: dict[str, float] = {}
    import re

    # ngspice: v(vout) = 2.50000e+00
    for m in re.finditer(
        r"v\(([a-zA-Z0-9_]+)\)\s*=\s*([+-]?[0-9eE.+-]+)", text, flags=re.I
    ):
        nodes[m.group(1).lower()] = float(m.group(2))
    return OpResult(nodes=nodes)


def parse_tran_wrdata(path: Path) -> TranResult:
    path = Path(path)
    hits = list(path.parent.glob("vout_tran*")) if not path.is_file() else [path]
    if not path.is_file():
        if not hits:
            raise FileNotFoundError(path)
        path = hits[0]
    raw = np.loadtxt(path)
    if raw.ndim == 1:
        raw = raw.reshape(1, -1)
    # time vout time vin
    t = raw[:, 0]
    vout = raw[:, 1]
    vin = raw[:, 3] if raw.shape[1] >= 4 else raw[:, 1]
    return TranResult(time=t, vout=vout, vin=vin)


def simulate_ac(
    p: CircuitParams | None = None,
    *,
    opamp_model: str = "ideal",
    workdir: Path | str,
    root: Path | str | None = None,
    mirror: Path | str | None = None,
    opt: NetlistOptions | None = None,
    ngspice: Path | str | None = None,
) -> AcResult:
    """Build Fig. 8-6 AC deck, run ngspice, return parsed transfer data."""
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    root_p = Path(root) if root is not None else _guess_root(workdir)
    if opt is None:
        opt = NetlistOptions(opamp_model=opamp_model, analysis="ac")
    else:
        opt.opamp_model = opamp_model
        opt.analysis = "ac"
    cir = workdir / "fig86_ac.cir"
    write_netlist(cir, p=p, opt=opt, root=root_p, mirror=mirror)
    proc = run_ngspice(cir, workdir=workdir, ngspice=ngspice)
    if proc.returncode not in (0, None) and not list(workdir.glob("vout_complex*")):
        raise RuntimeError(
            f"ngspice failed (code {proc.returncode}). See {workdir / 'ngspice.log'}"
        )
    return parse_ac_complex_wrdata(workdir / "vout_complex")


def simulate_op(
    p: CircuitParams | None = None,
    *,
    opamp_model: str = "ideal",
    workdir: Path | str,
    root: Path | str | None = None,
    ngspice: Path | str | None = None,
) -> OpResult:
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    root_p = Path(root) if root is not None else _guess_root(workdir)
    opt = NetlistOptions(opamp_model=opamp_model, analysis="dc_op")
    cir = workdir / "fig86_op.cir"
    write_netlist(cir, p=p, opt=opt, root=root_p)
    run_ngspice(cir, workdir=workdir, ngspice=ngspice)
    return parse_op_log(workdir / "ngspice.log")


def run_external_netlist(
    cir_path: Path | str,
    workdir: Path | str | None = None,
    ngspice: Path | str | None = None,
    timeout_s: float = 300.0,
) -> Path:
    """Run any user-supplied .cir; return workdir containing logs/data.

    This is the primary extension point for a custom netlist.  Put your
    ``wrdata`` / print statements in the deck, then parse with the helpers
    above or your own reader.
    """
    cir_path = Path(cir_path)
    workdir = Path(workdir) if workdir is not None else cir_path.parent
    run_ngspice(cir_path, workdir=workdir, ngspice=ngspice, timeout_s=timeout_s)
    return workdir


def _guess_root(start: Path) -> Path:
    """Walk parents until we find models/opa365 or opamp_design."""
    cur = Path(start).resolve()
    for _ in range(8):
        if (cur / "opamp_design").is_dir() or (cur / "models" / "opa365").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return Path.cwd()


def compare_ac_to_analytical(
    ac: AcResult,
    h_analytical: np.ndarray,
) -> dict[str, float]:
    """Error metrics between SPICE H and analytical H on the same frequency grid.

    ``h_analytical`` must be complex and same length as ``ac.f_hz``.
    """
    h_s = ac.h
    h_a = np.asarray(h_analytical, dtype=complex)
    db_s = 20 * np.log10(np.maximum(np.abs(h_s), 1e-30))
    db_a = 20 * np.log10(np.maximum(np.abs(h_a), 1e-30))
    err_db = db_s - db_a
    # Restrict to passband-ish for a friendlier metric if needed — full band here
    return {
        "max_abs_err_db": float(np.max(np.abs(err_db))),
        "rms_err_db": float(np.sqrt(np.mean(err_db**2))),
        "max_abs_phase_err_deg": float(
            np.max(np.abs(np.angle(h_s, deg=True) - np.angle(h_a, deg=True)))
        ),
    }
