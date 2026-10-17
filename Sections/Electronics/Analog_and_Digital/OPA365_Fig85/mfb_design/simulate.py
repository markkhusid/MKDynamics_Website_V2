"""Run ngspice and parse AC, OP, and transient results."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .netlist import NetlistOptions, write_netlist
from .params import CircuitParams


def scrub_text(text: str) -> str:
    """Drop a home-directory prefix so a message can be shown."""
    home = str(Path.home())
    return text.replace(home, "~")


@dataclass
class AcResult:
    f_hz: np.ndarray
    vout: np.ndarray
    vin: np.ndarray

    @property
    def h(self) -> np.ndarray:
        vin = np.where(np.abs(self.vin) < 1e-30, 1e-30, self.vin)
        return self.vout / vin

    @property
    def mag_db(self) -> np.ndarray:
        return 20.0 * np.log10(np.maximum(np.abs(self.h), 1e-30))

    @property
    def phase_deg(self) -> np.ndarray:
        return np.angle(self.h, deg=True)

    @property
    def phase_unwrapped_deg(self) -> np.ndarray:
        return np.rad2deg(np.unwrap(np.angle(self.h)))


@dataclass
class OpResult:
    nodes: dict[str, float]


@dataclass
class TranResult:
    time: np.ndarray
    vout: np.ndarray
    vin: np.ndarray


def find_ngspice(explicit: str | Path | None = None) -> Path:
    if explicit is not None:
        p = Path(explicit)
        if p.is_file():
            return p
        raise FileNotFoundError("ngspice path is not a file")
    env = os.environ.get("NGSPICE_EXE")
    if env and Path(env).is_file():
        return Path(env)
    which = shutil.which("ngspice")
    if which:
        return Path(which)
    raise FileNotFoundError("ngspice not found. Install it or set NGSPICE_EXE.")


def run_ngspice(
    cir_path: Path,
    workdir: Path | None = None,
    ngspice: Path | str | None = None,
    timeout_s: float = 120.0,
) -> subprocess.CompletedProcess:
    cir_path = Path(cir_path).resolve()
    workdir = Path(workdir).resolve() if workdir is not None else cir_path.parent
    workdir.mkdir(parents=True, exist_ok=True)
    exe = find_ngspice(ngspice)
    log_path = workdir / "ngspice.log"
    cmd = [str(exe), "-b", "-o", str(log_path), str(cir_path)]
    proc = subprocess.run(
        cmd,
        cwd=str(workdir),
        capture_output=True,
        text=True,
        timeout=timeout_s,
    )
    if proc.stdout or proc.stderr:
        with log_path.open("a", encoding="utf-8", errors="replace") as fh:
            fh.write("\n--- stdout ---\n")
            fh.write(proc.stdout or "")
            fh.write("\n--- stderr ---\n")
            fh.write(proc.stderr or "")
    return proc


def parse_ac_complex_wrdata(path: Path) -> AcResult:
    """ngspice wrdata repeats the frequency column for every printed value."""
    path = Path(path)
    candidates = [path]
    if path.suffix == "":
        candidates.append(Path(str(path) + ".data"))
    else:
        candidates.append(path.with_suffix(path.suffix + ".data"))
        candidates.append(path.with_suffix(".data"))
    data_path = next((c for c in candidates if c.is_file()), None)
    if data_path is None:
        parent = path.parent if path.parent.exists() else Path.cwd()
        hits = list(parent.glob("vout_complex*"))
        if not hits:
            raise FileNotFoundError("AC wrdata was not written")
        data_path = hits[0]
    raw = np.loadtxt(data_path)
    if raw.ndim == 1:
        raw = raw.reshape(1, -1)
    if raw.shape[1] >= 8:
        f = raw[:, 0]
        vout = raw[:, 1] + 1j * raw[:, 3]
        vin = raw[:, 5] + 1j * raw[:, 7]
    elif raw.shape[1] >= 4:
        f = raw[:, 0]
        vout = raw[:, 1] + 1j * raw[:, 3]
        vin = np.ones_like(f, dtype=complex)
    else:
        raise ValueError(f"Unexpected wrdata shape {raw.shape}")
    return AcResult(f_hz=f, vout=vout, vin=vin)


def parse_op_log(log_path: Path) -> OpResult:
    import re

    text = Path(log_path).read_text(encoding="utf-8", errors="replace")
    nodes: dict[str, float] = {}
    for m in re.finditer(
        r"v\(([a-zA-Z0-9_]+)\)\s*=\s*([+-]?[0-9eE.+-]+)", text, flags=re.I
    ):
        nodes[m.group(1).lower()] = float(m.group(2))
    return OpResult(nodes=nodes)


def parse_tran_wrdata(path: Path) -> TranResult:
    path = Path(path)
    candidates = [path]
    if path.suffix == "":
        candidates.append(Path(str(path) + ".data"))
    hits = [c for c in candidates if c.is_file()]
    if not hits:
        hits = list(path.parent.glob("vout_tran*")) if path.parent.exists() else []
    if not hits:
        raise FileNotFoundError("transient wrdata was not written")
    raw = np.loadtxt(hits[0])
    if raw.ndim == 1:
        raw = raw.reshape(1, -1)
    t = raw[:, 0]
    vout = raw[:, 1]
    vin = raw[:, 3] if raw.shape[1] >= 4 else raw[:, 1]
    return TranResult(time=t, vout=vout, vin=vin)


def simulate_tran(
    p: CircuitParams | None = None,
    *,
    opamp_model: str = "ideal",
    workdir: Path | str,
    root: Path | str | None = None,
    ngspice: Path | str | None = None,
    freq_hz: float = 250e3,
    amp_v: float = 1.0,
    tstep_s: float = 40e-9,
    tstop_s: float = 100e-6,
    temp_c: float = 25.0,
    lib_path: Path | None = None,
    timeout_s: float = 180.0,
) -> TranResult:
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    root_p = Path(root) if root is not None else _guess_root(workdir)
    opt = NetlistOptions(
        opamp_model=opamp_model,
        analysis="tran",
        temp_c=temp_c,
        tran_freq_hz=freq_hz,
        tran_amp_v=amp_v,
        tran_tstep_s=tstep_s,
        tran_tstop_s=tstop_s,
        lib_path=lib_path,
    )
    cir = workdir / "fig85_tran.cir"
    write_netlist(cir, p=p, opt=opt, root=root_p)
    proc = run_ngspice(cir, workdir=workdir, ngspice=ngspice, timeout_s=timeout_s)
    if proc.returncode not in (0, None) and not list(workdir.glob("vout_tran*")):
        raise RuntimeError(f"ngspice transient failed (code {proc.returncode})")
    return parse_tran_wrdata(workdir / "vout_tran")


def simulate_ac(
    p: CircuitParams | None = None,
    *,
    opamp_model: str = "ideal",
    workdir: Path | str,
    root: Path | str | None = None,
    mirror: Path | str | None = None,
    opt: NetlistOptions | None = None,
    ngspice: Path | str | None = None,
    timeout_s: float = 180.0,
) -> AcResult:
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    root_p = Path(root) if root is not None else _guess_root(workdir)
    if opt is None:
        opt = NetlistOptions(opamp_model=opamp_model, analysis="ac")
    else:
        opt.opamp_model = opamp_model
        opt.analysis = "ac"
    cir = workdir / "fig85_ac.cir"
    write_netlist(cir, p=p, opt=opt, root=root_p, mirror=mirror)
    proc = run_ngspice(cir, workdir=workdir, ngspice=ngspice, timeout_s=timeout_s)
    if proc.returncode not in (0, None) and not list(workdir.glob("vout_complex*")):
        raise RuntimeError(f"ngspice AC failed (code {proc.returncode})")
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
    cir = workdir / "fig85_op.cir"
    write_netlist(cir, p=p, opt=opt, root=root_p)
    run_ngspice(cir, workdir=workdir, ngspice=ngspice)
    return parse_op_log(workdir / "ngspice.log")


def run_external_netlist(
    cir_path: Path | str,
    workdir: Path | str | None = None,
    ngspice: Path | str | None = None,
    timeout_s: float = 300.0,
) -> Path:
    cir_path = Path(cir_path)
    workdir = Path(workdir) if workdir is not None else cir_path.parent
    run_ngspice(cir_path, workdir=workdir, ngspice=ngspice, timeout_s=timeout_s)
    return workdir


def _guess_root(start: Path) -> Path:
    cur = Path(start).resolve()
    for _ in range(8):
        if (cur / "mfb_design").is_dir() or (cur / "models" / "opa365").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return Path.cwd()


def compare_ac_to_analytical(ac: AcResult, h_analytical: np.ndarray) -> dict[str, float]:
    h_s = ac.h
    h_a = np.asarray(h_analytical, dtype=complex)
    db_s = 20 * np.log10(np.maximum(np.abs(h_s), 1e-30))
    db_a = 20 * np.log10(np.maximum(np.abs(h_a), 1e-30))
    err_db = db_s - db_a
    phase_err = np.angle(h_s / np.where(np.abs(h_a) < 1e-30, 1e-30, h_a), deg=True)
    return {
        "max_abs_err_db": float(np.max(np.abs(err_db))),
        "rms_err_db": float(np.sqrt(np.mean(err_db**2))),
        "max_abs_phase_err_deg": float(np.max(np.abs(phase_err))),
    }


def fc_from_mag(f_hz: np.ndarray, mag: np.ndarray) -> float:
    """−3 dB frequency by log interpolation of |H| against |H| at the first point."""
    dc = float(mag[0])
    target = dc / np.sqrt(2.0)
    for i in range(1, len(mag)):
        if mag[i - 1] >= target > mag[i]:
            f1, f2 = float(f_hz[i - 1]), float(f_hz[i])
            m1, m2 = float(mag[i - 1]), float(mag[i])
            if m1 == m2:
                return f1
            g = (np.log(target) - np.log(m1)) / (np.log(m2) - np.log(m1))
            return float(f1 * (f2 / f1) ** g)
    return float("nan")
