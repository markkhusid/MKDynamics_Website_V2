"""LTspice batch execution and raw / .meas parsing.

Batch jobs run one at a time. Several solver processes sharing one
prefix stall, so a lock surrounds every launch. Success is a log file
next to the deck. The process status is not the pass/fail test.

The deck is launched with its directory as the working directory and
only the file name as the argument, so the log does not record an
absolute path.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from .netlist import write_ltspice_ac_deck
from .params import CircuitParams

_LT_LOCK = threading.Lock()


@dataclass
class LtspiceAcSweep:
    f_hz: np.ndarray
    h: np.ndarray
    variables: dict[str, np.ndarray]
    raw_path: Path

    @property
    def mag(self) -> np.ndarray:
        return np.abs(self.h)

    @property
    def mag_db(self) -> np.ndarray:
        return 20.0 * np.log10(np.maximum(self.mag, 1e-30))

    @property
    def phase_deg(self) -> np.ndarray:
        return np.angle(self.h, deg=True)

    @property
    def phase_unwrapped_deg(self) -> np.ndarray:
        return np.rad2deg(np.unwrap(np.angle(self.h)))


DEFAULT_MEAS_KEYS = (
    "gain_100hz",
    "gain_250k",
    "gain_500k",
    "re_500k",
    "im_500k",
    "phase_500k",
    "fc_3db",
)


def find_ltspice(explicit: str | Path | None = None) -> Path:
    if explicit is not None:
        p = Path(explicit)
        if p.is_file():
            return p
        raise FileNotFoundError("LTspice path is not a file")
    env = os.environ.get("LTSPICE_EXE")
    if env and Path(env).is_file():
        return Path(env)
    local = os.environ.get("LOCALAPPDATA", "")
    candidates = [
        Path(local) / "Programs" / "ADI" / "LTspice" / "LTspice.exe",
        Path(r"C:\Program Files\ADI\LTspice\LTspice.exe"),
        Path(r"C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe"),
        Path(shutil.which("LTspice") or ""),
    ]
    prefix = Path.home() / ".wine" / "drive_c"
    if prefix.is_dir():
        candidates.extend(prefix.glob("users/*/AppData/Local/Programs/ADI/LTspice/LTspice.exe"))
        candidates.extend(prefix.glob("Program Files/ADI/LTspice/LTspice.exe"))
    for c in candidates:
        if c and c.is_file():
            return c
    raise FileNotFoundError("LTspice executable not found. Set LTSPICE_EXE.")


def run_ltspice_deck(
    cir_or_asc: Path | str,
    *,
    exe: Path | str | None = None,
    timeout_s: float = 600.0,
) -> Path:
    """Batch-run a deck. Return the log path. A missing log is the failure."""
    deck = Path(cir_or_asc).resolve()
    if not deck.is_file():
        raise FileNotFoundError(deck.name)
    lt = find_ltspice(exe)
    log = deck.with_suffix(".log")
    if log.is_file():
        try:
            log.unlink()
        except OSError:
            pass
    env = os.environ.copy()
    if lt.suffix.lower() == ".exe" and sys.platform != "win32":
        env["WINEDEBUG"] = "-all"
        cmd = ["wine", str(lt), "-b", deck.name]
    else:
        cmd = [str(lt), "-b", "-Run", deck.name]
    with _LT_LOCK:
        subprocess.run(
            cmd,
            cwd=str(deck.parent),
            capture_output=True,
            text=True,
            timeout=timeout_s,
            env=env,
        )
    if log.is_file():
        return log
    alt = deck.with_suffix(".LOG")
    if alt.is_file():
        return alt
    raise FileNotFoundError(f"LTspice did not write a log for {deck.name}")


def parse_meas_log(
    log_path: Path | str,
    keys: Iterable[str] | None = None,
) -> dict[str, float]:
    """Extract .meas results. dB polar values become linear magnitudes."""
    import math

    text = Path(log_path).read_text(encoding="utf-8", errors="replace")
    keys_l = {k.lower() for k in keys} if keys is not None else None
    found: dict[str, float] = {}
    num = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"

    def _want(name: str) -> bool:
        return keys_l is None or name in keys_l

    for m in re.finditer(
        rf"(?im)^\s*([A-Za-z0-9_]+)\s*:.*?=\s*\(\s*{num}\s*dB\s*,\s*{num}",
        text,
    ):
        name = m.group(1).lower()
        if not _want(name):
            continue
        db = float(m.group(2))
        phase_deg = float(m.group(3))
        mag = 10 ** (db / 20.0) if math.isfinite(db) else 0.0
        signed = mag * math.cos(math.radians(phase_deg))
        found[f"{name}_db"] = db
        found[f"{name}_polar_phase_deg"] = phase_deg
        if name.startswith("gain") or name.startswith("mag"):
            found[name] = mag
        else:
            found[name] = signed

    for m in re.finditer(
        rf"(?im)^\s*([A-Za-z0-9_]+)\s*:.*?=\s*{num}(?!\s*dB)",
        text,
    ):
        name = m.group(1).lower()
        if not _want(name):
            continue
        if name in found:
            continue
        found[name] = float(m.group(2))

    for m in re.finditer(
        rf"(?im)^\s*([A-Za-z0-9_]+)\s*:.*?AT\s+{num}",
        text,
    ):
        name = m.group(1).lower()
        if not _want(name):
            continue
        if name.endswith("3db") or name.startswith("fc") or "freq" in name:
            found[name] = float(m.group(2))
        else:
            found.setdefault(f"{name}_at_hz", float(m.group(2)))

    for suffix in ("500k", "250k", "20k"):
        re_k, im_k = f"re_{suffix}", f"im_{suffix}"
        if re_k in found and im_k in found:
            found[f"phase_{suffix}"] = math.degrees(math.atan2(found[im_k], found[re_k]))
    return found


def _forward_mask(time: np.ndarray) -> np.ndarray:
    """Keep the first sample and every later sample that moves time forward."""
    keep = np.empty(time.shape, dtype=bool)
    last = -np.inf
    for i, t in enumerate(time):
        ok = float(t) > last
        keep[i] = ok
        if ok:
            last = float(t)
    return keep


def parse_ltspice_raw_tran(
    raw_path: Path | str,
) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Parse a real transient raw file and drop solver backsteps.

    ``time`` is float64. Other traces are float32 when Flags contains real.
    Names are lower-case, for example ``v(vout)``.
    """
    raw_path = Path(raw_path)
    data = raw_path.read_bytes()
    marker = "Binary:\n".encode("utf-16-le")
    idx = data.find(marker)
    if idx < 0:
        raise ValueError("No UTF-16 Binary marker in the transient raw file")
    data_start = idx + len(marker)
    header = data[:idx].decode("utf-16-le", errors="replace")
    n_vars = n_pts = None
    flags = ""
    var_names: list[str] = []
    in_vars = False
    for line in header.splitlines():
        ls = line.strip()
        if ls.lower().startswith("no. variables:"):
            n_vars = int(ls.split(":")[1].strip())
        elif ls.lower().startswith("no. points:"):
            n_pts = int(ls.split(":")[1].strip())
        elif ls.lower().startswith("flags:"):
            flags = ls.split(":", 1)[1].strip().lower()
        elif ls.lower().startswith("variables:"):
            in_vars = True
        elif in_vars:
            parts = re.split(r"\t+", ls)
            if len(parts) >= 2 and parts[0].strip().isdigit():
                var_names.append(parts[1].strip().lower())
    if n_vars is None or n_pts is None or len(var_names) != n_vars:
        raise ValueError("Could not parse the transient raw header")
    if "complex" in flags:
        raise ValueError("This raw file is an AC sweep, not a transient")
    point_bytes = 8 + 4 * (n_vars - 1)
    blob = data[data_start : data_start + n_pts * point_bytes]
    if len(blob) < n_pts * point_bytes:
        raise ValueError("Transient raw file is short")
    time = np.empty(n_pts, dtype=float)
    bufs = {name: np.empty(n_pts, dtype=float) for name in var_names[1:]}
    off = 0
    for i in range(n_pts):
        time[i] = np.frombuffer(blob, dtype="<f8", count=1, offset=off)[0]
        off += 8
        vals = np.frombuffer(blob, dtype="<f4", count=n_vars - 1, offset=off)
        off += 4 * (n_vars - 1)
        for name, val in zip(var_names[1:], vals):
            bufs[name][i] = float(val)
    keep = _forward_mask(time)
    time = time[keep]
    bufs = {name: arr[keep] for name, arr in bufs.items()}
    return time, bufs


def parse_ltspice_raw_ac(
    raw_path: Path | str,
    *,
    vout_name: str = "v(vout)",
    vin_name: str = "v(vin)",
) -> LtspiceAcSweep:
    raw_path = Path(raw_path)
    data = raw_path.read_bytes()
    if data[1:2] == b"\x00" or data[:2] == b"\xff\xfe":
        enc = "utf-16-le"
        header_bytes = data
        for nl in ("Binary:\n", "Binary:\r\n", "Binary:\r"):
            marker = nl.encode(enc)
            idx = header_bytes.find(marker)
            if idx >= 0:
                data_start = idx + len(marker)
                header_text = header_bytes[:idx].decode(enc, errors="replace")
                break
        else:
            raise ValueError("No Binary marker in the raw file")
    else:
        for nl in (b"Binary:\n", b"Binary:\r\n", b"Values:\n", b"Values:\r\n"):
            idx = data.find(nl)
            if idx >= 0:
                data_start = idx + len(nl)
                header_text = data[:idx].decode("utf-8", errors="replace")
                break
        else:
            raise ValueError("No Binary marker in the raw file")

    n_vars = None
    n_pts = None
    flags = ""
    var_names: list[str] = []
    in_vars = False
    for line in header_text.splitlines():
        ls = line.strip()
        if ls.lower().startswith("no. variables:"):
            n_vars = int(ls.split(":")[1].strip())
        elif ls.lower().startswith("no. points:"):
            n_pts = int(ls.split(":")[1].strip())
        elif ls.lower().startswith("flags:"):
            flags = ls.split(":", 1)[1].strip().lower()
        elif ls.lower().startswith("variables:"):
            in_vars = True
        elif in_vars:
            if not ls or ls.lower().startswith("binary") or ls.lower().startswith("values"):
                in_vars = False
                continue
            parts = re.split(r"\t+", ls)
            if len(parts) >= 2 and parts[0].strip().isdigit():
                var_names.append(parts[1].strip().lower())
            else:
                m = re.match(r"^\s*(\d+)\s*(\S+)", ls)
                if m:
                    var_names.append(m.group(2).lower())
    if n_vars is None or n_pts is None:
        raise ValueError("Could not read variable or point counts from the raw file")
    if len(var_names) != n_vars:
        cleaned = []
        for v in var_names:
            for suf in ("frequency", "voltage", "device_current", "current"):
                if v.endswith(suf) and len(v) > len(suf):
                    head = v[: -len(suf)]
                    if head:
                        v = head
                    break
            cleaned.append(v)
        var_names = cleaned
    if len(var_names) != n_vars:
        raise ValueError("Variable count does not match the raw header")

    is_complex = "complex" in flags
    width = 16 if is_complex else 8
    expect = n_pts * n_vars * width
    blob = data[data_start : data_start + expect]
    if len(blob) < expect:
        raise ValueError("Raw file is shorter than the header claims")
    if is_complex:
        doubles = np.frombuffer(blob, dtype="<f8").reshape(n_pts, n_vars, 2)
        variables = {
            name: doubles[:, i, 0] + 1j * doubles[:, i, 1]
            for i, name in enumerate(var_names)
        }
    else:
        doubles = np.frombuffer(blob, dtype="<f8").reshape(n_pts, n_vars)
        variables = {name: doubles[:, i].astype(complex) for i, name in enumerate(var_names)}

    f_hz = np.abs(np.real(variables[var_names[0]]))

    def _lookup(name: str) -> np.ndarray:
        key = name.lower()
        if key in variables:
            return variables[key]
        alt = f"v({key})"
        if alt in variables:
            return variables[alt]
        raise KeyError(f"Variable {name!r} is not in the raw file")

    vout = _lookup(vout_name)
    vin = _lookup(vin_name)
    vin_safe = np.where(np.abs(vin) < 1e-30, 1.0 + 0j, vin)
    return LtspiceAcSweep(
        f_hz=np.asarray(f_hz, dtype=float),
        h=np.asarray(vout / vin_safe, dtype=complex),
        variables=variables,
        raw_path=raw_path,
    )


def simulate_ltspice_ac(
    p: CircuitParams | None = None,
    *,
    workdir: Path | str,
    root: Path | str | None = None,
    opamp_model: str = "ideal",
    temp_c: float = 25.0,
    exe: Path | str | None = None,
) -> dict[str, float]:
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    root_p = Path(root) if root is not None else _guess_root(workdir)
    cir = workdir / "fig85_ltspice_ac.cir"
    write_ltspice_ac_deck(cir, p=p, opamp_model=opamp_model, root=root_p, temp_c=temp_c)
    log = run_ltspice_deck(cir, exe=exe)
    return parse_meas_log(log)


def simulate_ltspice_ac_bode(
    p: CircuitParams | None = None,
    *,
    workdir: Path | str,
    root: Path | str | None = None,
    opamp_model: str = "ideal",
    temp_c: float = 25.0,
    exe: Path | str | None = None,
    vout_name: str = "v(vout)",
    vin_name: str = "v(vin)",
) -> tuple[dict[str, float], LtspiceAcSweep]:
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    root_p = Path(root) if root is not None else _guess_root(workdir)
    cir = workdir / "fig85_ltspice_ac.cir"
    write_ltspice_ac_deck(cir, p=p, opamp_model=opamp_model, root=root_p, temp_c=temp_c)
    log = run_ltspice_deck(cir, exe=exe)
    meas = parse_meas_log(log)
    raw = cir.with_suffix(".raw")
    if not raw.is_file():
        alt = cir.with_suffix(".RAW")
        raw = alt if alt.is_file() else raw
    sweep = parse_ltspice_raw_ac(raw, vout_name=vout_name, vin_name=vin_name)
    return meas, sweep


def run_ltspice_wc_mc_batch(
    decks: list[Path],
    *,
    exe: Path | str | None = None,
) -> pd.DataFrame:
    rows = []
    for d in decks:
        d = Path(d)
        try:
            log = run_ltspice_deck(d, exe=exe)
            meas = parse_meas_log(log)
            meas["deck"] = d.name
            rows.append(meas)
        except Exception as exc:
            rows.append({"deck": d.name, "error": type(exc).__name__})
    return pd.DataFrame(rows)


def _guess_root(start: Path) -> Path:
    cur = Path(start).resolve()
    for _ in range(8):
        if (cur / "mfb_design").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return Path.cwd()
