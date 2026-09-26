"""LTspice batch execution and .meas log parsing.

Default executable search (Windows)
-----------------------------------
1. ``LTSPICE_EXE`` environment variable
2. ``%LocalAppData%\\Programs\\ADI\\LTspice\\LTspice.exe``
3. ``C:\\Program Files\\ADI\\LTspice\\LTspice.exe``
4. ``LTspice`` on PATH

HOW TO USE YOUR OWN SCHEMATIC / NETLIST
---------------------------------------
1. Draw or open any ``.asc`` in LTspice; add SPICE directives for ``.ac``,
   ``.step``, ``.meas`` as needed.
2. Either:
   a. Run from the GUI, or
   b. Export a ``.cir`` netlist and call ``run_ltspice_deck(path)``.
3. Keep / adapt the ``.meas`` names listed in ``DEFAULT_MEAS_KEYS`` **or**
   pass your own key list to ``parse_meas_log``.
4. Notebooks only need a dict/DataFrame of measured scalars (fc, gains…)
   to compare against analytical results — they do not require Fig. 8-6.

Batch flag: ``-b`` (batch) ``-Run`` as supported by ADI LTspice.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from .netlist import write_ltspice_ac_deck
from .params import CircuitParams


@dataclass
class LtspiceAcSweep:
    """Full AC sweep parsed from an LTspice ``.raw`` file.

    Attributes
    ----------
    f_hz :
        Frequency points (Hz).
    h :
        Complex transfer ``V(vout) / V(vin)`` (or custom node pair).
    variables :
        Name → complex array for every trace in the raw file (for debugging
        or custom nets).  Keys are lower-case, e.g. ``\"v(vout)\"``.
    raw_path :
        Path to the ``.raw`` file that was parsed.
    """

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
    "gain_20k",
    "re_20k",
    "im_20k",
    "phase_20k",
    "fc_3db",
)


def find_ltspice(explicit: str | Path | None = None) -> Path:
    if explicit is not None:
        p = Path(explicit)
        if p.is_file():
            return p
        raise FileNotFoundError(p)

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
    for c in candidates:
        if c and c.is_file():
            return c
    raise FileNotFoundError(
        "LTspice.exe not found. Set LTSPICE_EXE or install ADI LTspice."
    )


def run_ltspice_deck(
    cir_or_asc: Path | str,
    *,
    exe: Path | str | None = None,
    timeout_s: float = 600.0,
) -> Path:
    """Run LTspice in batch on a .cir or .asc; return path to the .log file.

    LTspice writes the log next to the deck (same stem).
    """
    deck = Path(cir_or_asc).resolve()
    if not deck.is_file():
        raise FileNotFoundError(deck)
    lt = find_ltspice(exe)
    # Remove stale log
    log = deck.with_suffix(".log")
    if log.is_file():
        try:
            log.unlink()
        except OSError:
            pass
    cmd = [str(lt), "-b", "-Run", str(deck)]
    subprocess.run(
        cmd,
        cwd=str(deck.parent),
        capture_output=True,
        text=True,
        timeout=timeout_s,
    )
    if not log.is_file():
        # Some versions write uppercase .LOG
        alt = deck.with_suffix(".LOG")
        if alt.is_file():
            return alt
        raise FileNotFoundError(f"LTspice did not produce a log for {deck}")
    return log


def parse_meas_log(
    log_path: Path | str,
    keys: Iterable[str] | None = None,
) -> dict[str, float]:
    """Extract ``.meas`` results from an LTspice log.

    Handles modern ADI LTspice formats such as::

        gain_100hz: mag(V(vout)) =(-6.87e-05dB,0°) at 100
        fc_3db: mag(V(vout))=gain_100Hz/sqrt(2)  AT 19753.4

    For custom nets, keep ``name:`` prefixes on ``.meas`` results, or extend
    the patterns below.  Magnitude reported in dB is converted back to a
    linear ratio and stored as ``<name>``; the dB value is also stored as
    ``<name>_db`` when conversion applies.

    Parameters
    ----------
    keys :
        Optional whitelist (case-insensitive).  ``None`` stores every meas.
    """
    import math

    text = Path(log_path).read_text(encoding="utf-8", errors="replace")
    keys_l = {k.lower() for k in keys} if keys is not None else None
    found: dict[str, float] = {}

    num = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"

    def _want(name: str) -> bool:
        return keys_l is None or name in keys_l

    # Pattern A: polar form  name: ... = ( <dB> dB, <phase> ° )
    # LTspice often reports even real-valued re()/im() this way; a negative
    # real number appears as (XXdB, 180°).
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
        # Signed cartesian value for re()/im() style meas; for mag() this is
        # still the positive magnitude when phase is 0.
        signed = mag * math.cos(math.radians(phase_deg))
        found[f"{name}_db"] = db
        found[f"{name}_polar_phase_deg"] = phase_deg
        # mag(...) measurements: store positive linear gain
        if name.startswith("gain") or name.startswith("mag"):
            found[name] = mag
        else:
            found[name] = signed

    # Pattern B: plain number  name: ... = 1.23e4
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

    # Pattern C: WHEN measurements — frequency after AT
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

    # Phase from rectangular re/im at 20 kHz when available
    if "re_20k" in found and "im_20k" in found:
        found["phase_20k"] = math.degrees(
            math.atan2(found["im_20k"], found["re_20k"])
        )

    return found


def parse_ltspice_raw_ac(
    raw_path: Path | str,
    *,
    vout_name: str = "v(vout)",
    vin_name: str = "v(vin)",
) -> LtspiceAcSweep:
    """Parse an LTspice AC ``.raw`` file into frequency and complex H(f).

    Supports the modern ADI LTspice binary format used on Windows:
    UTF-16-LE header ending with ``Binary:\\n``, then little-endian
    float64 pairs (real, imag) per variable per point when ``Flags``
    contains ``complex``.

    HOW TO ADAPT FOR ANOTHER NETLIST
    --------------------------------
    After running your deck, point this at the produced ``.raw`` and set
    ``vout_name`` / ``vin_name`` to match your node names (case-insensitive),
    e.g. ``vout_name=\"v(out)\"``, ``vin_name=\"v(in)\"``.

    Parameters
    ----------
    raw_path :
        Path to ``*.raw`` next to the deck.
    vout_name, vin_name :
        Variable names as listed in the raw header (``V(vout)`` style).
    """
    raw_path = Path(raw_path)
    data = raw_path.read_bytes()

    # --- Locate UTF-16 header vs binary payload --------------------------------
    # Modern LTspice writes the ASCII header as UTF-16 LE (no BOM).
    if data[1:2] == b"\x00" or data[:2] == b"\xff\xfe":
        enc = "utf-16-le"
        if data[:2] == b"\xff\xfe":
            header_bytes = data
        else:
            header_bytes = data
        # Find Binary: marker in UTF-16
        for nl in ("Binary:\n", "Binary:\r\n", "Binary:\r"):
            marker = nl.encode(enc)
            idx = header_bytes.find(marker)
            if idx >= 0:
                data_start = idx + len(marker)
                header_text = header_bytes[:idx].decode(enc, errors="replace")
                break
        else:
            raise ValueError(f"No Binary: marker in UTF-16 raw file {raw_path}")
    else:
        # Older / ASCII-header raw files
        enc = "utf-8"
        for nl in (b"Binary:\n", b"Binary:\r\n", b"Values:\n", b"Values:\r\n"):
            idx = data.find(nl)
            if idx >= 0:
                data_start = idx + len(nl)
                header_text = data[:idx].decode("utf-8", errors="replace")
                break
        else:
            raise ValueError(f"No Binary:/Values: marker in raw file {raw_path}")

    # --- Parse header fields ---------------------------------------------------
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
            # e.g. "0\tfrequency\tfrequency" or "0frequencyfrequency" (no tabs)
            if not ls or ls.lower().startswith("binary") or ls.lower().startswith("values"):
                in_vars = False
                continue
            # Prefer tab-split; fall back to leading index
            parts = re.split(r"\t+", ls)
            if len(parts) >= 2 and parts[0].strip().isdigit():
                var_names.append(parts[1].strip().lower())
            else:
                m = re.match(r"^\s*(\d+)\s*(\S+)", ls)
                if m:
                    var_names.append(m.group(2).lower())

    if n_vars is None or n_pts is None:
        raise ValueError(f"Could not read No. Variables/Points from {raw_path}")
    if len(var_names) != n_vars:
        # Variable lines sometimes concatenate name+type without tabs
        # (seen: "0frequencyfrequency"). Recover by stripping known suffixes.
        cleaned = []
        for v in var_names:
            for suf in ("frequency", "voltage", "device_current", "current"):
                if v.endswith(suf) and len(v) > len(suf):
                    # "frequencyfrequency" → "frequency"; "v(vout)voltage" → "v(vout)"
                    head = v[: -len(suf)]
                    if head:
                        v = head
                    break
            cleaned.append(v)
        var_names = cleaned
    if len(var_names) != n_vars:
        raise ValueError(
            f"Variable count mismatch in {raw_path}: header {n_vars}, "
            f"parsed {len(var_names)} names {var_names!r}"
        )

    is_complex = "complex" in flags
    width = 16 if is_complex else 8  # bytes per variable per point
    expect = n_pts * n_vars * width
    blob = data[data_start : data_start + expect]
    if len(blob) < expect:
        raise ValueError(
            f"Raw data short in {raw_path}: got {len(blob)} bytes, need {expect}"
        )

    if is_complex:
        doubles = np.frombuffer(blob, dtype="<f8").reshape(n_pts, n_vars, 2)
        variables: dict[str, np.ndarray] = {}
        for i, name in enumerate(var_names):
            variables[name] = doubles[:, i, 0] + 1j * doubles[:, i, 1]
    else:
        doubles = np.frombuffer(blob, dtype="<f8").reshape(n_pts, n_vars)
        variables = {name: doubles[:, i].astype(complex) for i, name in enumerate(var_names)}

    # Frequency is variable 0; take real part / magnitude for log sweeps
    freq_key = var_names[0]
    f_hz = np.real(variables[freq_key])
    # Guard: some writers store frequency with a tiny imag component
    f_hz = np.abs(f_hz)

    def _lookup(name: str) -> np.ndarray:
        key = name.lower()
        if key in variables:
            return variables[key]
        # Allow bare node names → v(node)
        alt = f"v({key})"
        if alt in variables:
            return variables[alt]
        raise KeyError(
            f"Variable {name!r} not in raw file. Available: {list(variables)}"
        )

    vout = _lookup(vout_name)
    vin = _lookup(vin_name)
    # Avoid /0; AC source magnitude should be 1∠0
    vin_safe = np.where(np.abs(vin) < 1e-30, 1.0 + 0j, vin)
    h = vout / vin_safe

    return LtspiceAcSweep(
        f_hz=np.asarray(f_hz, dtype=float),
        h=np.asarray(h, dtype=complex),
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
    """Generate Fig. 8-6 LTspice AC deck, run, parse .meas → dict.

    For a full Bode curve (not just .meas scalars), use
    :func:`simulate_ltspice_ac_bode` instead.
    """
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    root_p = Path(root) if root is not None else _guess_root(workdir)
    cir = workdir / "fig86_ltspice_ac.cir"
    write_ltspice_ac_deck(
        cir, p=p, opamp_model=opamp_model, root=root_p, temp_c=temp_c
    )
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
    """Run LTspice AC and return both ``.meas`` scalars and full Bode H(f).

    Returns
    -------
    meas : dict
        Parsed ``.meas`` results (fc, gains, …).
    sweep : LtspiceAcSweep
        Frequency vector and complex ``Vout/Vin`` from the ``.raw`` file.

    Custom netlist
    --------------
    Call ``run_ltspice_deck`` on your deck, then
    ``parse_ltspice_raw_ac(deck.with_suffix('.raw'), vout_name=..., vin_name=...)``.
    """
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    root_p = Path(root) if root is not None else _guess_root(workdir)
    cir = workdir / "fig86_ltspice_ac.cir"
    write_ltspice_ac_deck(
        cir, p=p, opamp_model=opamp_model, root=root_p, temp_c=temp_c
    )
    log = run_ltspice_deck(cir, exe=exe)
    meas = parse_meas_log(log)
    raw = cir.with_suffix(".raw")
    if not raw.is_file():
        # LTspice sometimes capitalizes the extension
        alt = cir.with_suffix(".RAW")
        raw = alt if alt.is_file() else raw
    sweep = parse_ltspice_raw_ac(raw, vout_name=vout_name, vin_name=vin_name)
    return meas, sweep


def run_ltspice_wc_mc_batch(
    decks: list[Path],
    *,
    exe: Path | str | None = None,
) -> pd.DataFrame:
    """Run many pre-written decks; collect meas rows (custom WC/MC).

    Point this at any list of .cir files produced from your schematic.
    """
    rows = []
    for d in decks:
        d = Path(d)
        try:
            log = run_ltspice_deck(d, exe=exe)
            meas = parse_meas_log(log)
            meas["deck"] = d.name
            rows.append(meas)
        except Exception as exc:  # keep batch going
            rows.append({"deck": d.name, "error": str(exc)})
    return pd.DataFrame(rows)


def _guess_root(start: Path) -> Path:
    cur = Path(start).resolve()
    for _ in range(8):
        if (cur / "opamp_design").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return Path.cwd()
