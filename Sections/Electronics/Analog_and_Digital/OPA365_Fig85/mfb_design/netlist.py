"""Generate ngspice and LTspice decks for Figure 8-5.

Two op-amp models share the same passive network:

* ``ideal`` — a high-gain VCVS plus explicit Vos, Ibp, and Ibn sources,
  so the linear analytical model and SPICE solve the same circuit.
* ``opa365`` — the TI macromodel. That file is not in this repository.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

from .params import CircuitParams

DEFAULT_OPA365_LIB = Path("models") / "opa365" / "OPA365.lib"


@dataclass
class NetlistOptions:
    opamp_model: str = "ideal"
    analysis: str = "ac"
    lib_path: Path | None = None
    include_nonideals: bool = True
    ac_fstart: float = 10.0
    ac_fstop: float = 50e6
    ac_points: int = 50
    temp_c: float = 25.0
    title: str = "OPA365 Fig 8-5 MFB 500 kHz LPF"
    tran_freq_hz: float = 250e3
    tran_amp_v: float = 1.0
    tran_tstep_s: float = 40e-9
    tran_tstop_s: float = 100e-6


def _param_block(p: CircuitParams) -> str:
    sp = p.as_spice_params()
    return "\n".join(f".param {k}={v:.12g}" for k, v in sp.items())


def _passive_network() -> str:
    """R1, C1, R3, R2, C2. Node names are the contract with the parsers."""
    return dedent(
        """\
        * --- Passive network (Fig. 8-5 multiple feedback) ---
        R1 vin n1 {R1}
        C1 n1 0 {C1}
        R3 n1 vout {R3}
        R2 n1 n2 {R2}
        C2 n2 vout {C2}
        """
    )


def _ideal_opamp(include_nonideals: bool) -> str:
    """Inverting ideal op-amp.

    VOS from ground to vplus with value {VOS} sets vplus = −VOS.
    EAMP nulls (vplus − n2), so n2 = −VOS. That is V(+) − V(−) = VOS
    with the circuit + pin at ground.
    IBP leaves vplus and does not touch n1 or n2.
    IBN leaves n2, matching the analytical KCL.
    """
    if include_nonideals:
        sources = dedent(
            """\
            * vplus = −VOS, so the ideal amp holds n2 = −VOS
            VOS 0 vplus DC {VOS}
            IBP vplus 0 DC {IBP}
            IBN n2 0 DC {IBN}
            """
        )
    else:
        sources = "VOS 0 vplus DC 0\n"
    return sources + dedent(
        """\
        * High-gain VCVS. Output impedance is zero, so Rload does not move Vout.
        EAMP vout 0 vplus n2 1e6
        """
    )


def _spice_lib_ref(lib: Path, deck_dir: Path | None) -> str:
    """Include path relative to the deck. An absolute path is not written."""
    lib = Path(lib)
    base = Path(deck_dir) if deck_dir is not None else Path.cwd()
    try:
        return Path(os.path.relpath(lib.resolve(), base.resolve())).as_posix()
    except ValueError:
        return DEFAULT_OPA365_LIB.as_posix()


def _opa365_instance(lib: Path, deck_dir: Path | None = None) -> str:
    """+IN grounded, −IN at n2, rails vcc/vee, output vout.

    The macromodel is not shipped here. Download SBOC133A and save
    OPA365.lib at models/opa365/OPA365.lib.
    """
    lib_s = _spice_lib_ref(lib, deck_dir)
    return dedent(
        f"""\
        * TI OPA365 macromodel (pin order: +IN -IN +V -V OUT)
        * Not included in this repo. Download SBOC133A from ti.com and
        * save it as models/opa365/OPA365.lib. Path is relative to this deck.
        .include '{lib_s}'
        XU1 0 n2 vcc vee vout OPA365
        """
    )


def _supplies() -> str:
    return dedent(
        """\
        Vcc vcc 0 DC {VPOS}
        Vee vee 0 DC {VNEG}
        * The ideal VCVS does not use the rails. These resistors keep the nodes.
        Rbleed vcc 0 10Meg
        Rbleedn vee 0 10Meg
        Rload vout 0 {RLOAD}
        """
    )


def _analysis_block(opt: NetlistOptions) -> str:
    if opt.analysis in ("ac", "ac_temp"):
        return dedent(
            f"""\
            Vin vin 0 DC {{VINBIAS}} AC 1 0
            .temp {opt.temp_c}
            .ac dec {opt.ac_points} {opt.ac_fstart} {opt.ac_fstop}
            .control
            run
            wrdata vout_complex real(v(vout)) imag(v(vout)) real(v(vin)) imag(v(vin))
            quit
            .endc
            """
        )
    if opt.analysis == "dc_op":
        return dedent(
            f"""\
            Vin vin 0 DC {{VINBIAS}}
            .temp {opt.temp_c}
            .op
            .control
            run
            print v(vout) v(vin) v(n1) v(n2)
            quit
            .endc
            """
        )
    if opt.analysis == "tran":
        return dedent(
            f"""\
            * Passband sine, no DC offset. Amplitude {opt.tran_amp_v:.12g} V at {opt.tran_freq_hz:.12g} Hz.
            Vin vin 0 DC {{VINBIAS}} SIN(0 {opt.tran_amp_v:.12g} {opt.tran_freq_hz:.12g})
            .temp {opt.temp_c}
            .tran {opt.tran_tstep_s:.12g} {opt.tran_tstop_s:.12g}
            .control
            run
            wrdata vout_tran v(vout) v(vin)
            quit
            .endc
            """
        )
    raise ValueError(f"Unknown analysis {opt.analysis!r}")


def build_netlist(
    p: CircuitParams | None = None,
    opt: NetlistOptions | None = None,
    root: Path | None = None,
    deck_dir: Path | None = None,
) -> str:
    if p is None:
        p = CircuitParams()
    if opt is None:
        opt = NetlistOptions()
    root = Path(root) if root is not None else Path.cwd()
    lib = opt.lib_path
    if lib is None:
        lib = root / DEFAULT_OPA365_LIB
    elif not Path(lib).is_absolute():
        lib = root / lib

    parts = [
        f"* {opt.title}",
        f"* opamp_model={opt.opamp_model}  analysis={opt.analysis}  temp={opt.temp_c}",
        ".options savecurrents",
        _param_block(p),
        _passive_network(),
    ]
    model = opt.opamp_model.lower()
    if model == "ideal":
        parts.append(_ideal_opamp(opt.include_nonideals))
    elif model in ("opa365", "opa"):
        parts.append(_opa365_instance(lib, deck_dir=deck_dir))
    else:
        raise ValueError(f"Unknown opamp_model={opt.opamp_model!r}. Use 'ideal' or 'opa365'.")
    parts.append(_supplies())
    parts.append(_analysis_block(opt))
    parts.append(".end\n")
    return "\n".join(parts)


def write_netlist(
    path: Path | str,
    p: CircuitParams | None = None,
    opt: NetlistOptions | None = None,
    root: Path | None = None,
    mirror: Path | str | None = None,
) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_netlist(p=p, opt=opt, root=root, deck_dir=path.parent), encoding="utf-8")
    if mirror is not None:
        m = Path(mirror)
        m.parent.mkdir(parents=True, exist_ok=True)
        m.write_text(build_netlist(p=p, opt=opt, root=root, deck_dir=m.parent), encoding="utf-8")
    return path


def _amp_card_ltspice(
    opamp_model: str,
    lib: Path,
    deck_dir: Path,
) -> str:
    if opamp_model == "ideal":
        return dedent(
            """\
            VOS 0 vplus DC {VOS}
            IBP vplus 0 DC {IBP}
            IBN n2 0 DC {IBN}
            EAMP vout 0 vplus n2 1e6
            """
        )
    lib_s = _spice_lib_ref(lib, deck_dir)
    return dedent(
        f"""\
        * OPA365.lib is not in this repo. Download TI SBOC133A into
        * models/opa365/OPA365.lib. Path is relative to this deck.
        .lib '{lib_s}'
        XU1 0 n2 vcc vee vout OPA365
        """
    )


def _ltspice_body(
    p: CircuitParams,
    opamp_model: str,
    root: Path,
    deck_dir: Path,
    lib_path: Path | None,
) -> str:
    lib = Path(lib_path) if lib_path is not None else (root / DEFAULT_OPA365_LIB)
    amp = _amp_card_ltspice(opamp_model, lib, deck_dir)
    params = "\n".join(f".param {k}={v:.12g}" for k, v in p.as_spice_params().items())
    return dedent(
        f"""\
        {params}
        R1 vin n1 {{R1}}
        C1 n1 0 {{C1}}
        R3 n1 vout {{R3}}
        R2 n1 n2 {{R2}}
        C2 n2 vout {{C2}}
        {amp}
        Rload vout 0 {{RLOAD}}
        Rbleed vcc 0 10Meg
        Rbleedn vee 0 10Meg
        Vcc vcc 0 {{VPOS}}
        Vee vee 0 {{VNEG}}
        """
    )


def write_ltspice_ac_deck(
    path: Path | str,
    p: CircuitParams | None = None,
    opamp_model: str = "ideal",
    root: Path | None = None,
    temp_c: float = 25.0,
    lib_path: Path | None = None,
) -> Path:
    if p is None:
        p = CircuitParams()
    root = Path(root) if root is not None else Path.cwd()
    path = Path(path)
    body = _ltspice_body(p, opamp_model, root, path.parent, lib_path)
    text = (
        "* OPA365 Fig 8-5 LTspice AC deck (generated)\n"
        + body
        + dedent(
            f"""\
            Vin vin 0 {{VINBIAS}} AC 1 0
            .temp {temp_c}
            .ac dec 50 10 50Meg
            .meas AC gain_100Hz FIND mag(V(vout)) AT 100
            .meas AC gain_250k FIND mag(V(vout)) AT 250k
            .meas AC gain_500k FIND mag(V(vout)) AT 500k
            .meas AC re_500k FIND re(V(vout)) AT 500k
            .meas AC im_500k FIND im(V(vout)) AT 500k
            .meas AC fc_3db WHEN mag(V(vout))=gain_100Hz/sqrt(2) FALL=1
            .end
            """
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def write_ltspice_tran_deck(
    path: Path | str,
    p: CircuitParams | None = None,
    opamp_model: str = "ideal",
    root: Path | None = None,
    temp_c: float = 25.0,
    *,
    freq_hz: float = 250e3,
    amp_v: float = 1.0,
    tstep_s: float = 8e-9,
    tstop_s: float = 100e-6,
    tmeas_from_s: float = 60e-6,
    lib_path: Path | None = None,
) -> Path:
    """Transient deck. The source is SINE(0, amp, freq). Max step is tstep_s."""
    if p is None:
        p = CircuitParams()
    root = Path(root) if root is not None else Path.cwd()
    path = Path(path)
    body = _ltspice_body(p, opamp_model, root, path.parent, lib_path)
    text = (
        f"* OPA365 Fig 8-5 LTspice transient deck (generated)\n"
        f"* {freq_hz:.12g} Hz sine, {amp_v:.12g} V peak, no offset.\n"
        + body
        + dedent(
            f"""\
            Vin vin 0 SINE(0 {amp_v:.12g} {freq_hz:.12g})
            .temp {temp_c}
            .options plotwinsize=0
            .tran 0 {tstop_s:.12g} 0 {tstep_s:.12g}
            .meas TRAN vin_max MAX V(vin) FROM {tmeas_from_s:.12g} TO {tstop_s:.12g}
            .meas TRAN vin_min MIN V(vin) FROM {tmeas_from_s:.12g} TO {tstop_s:.12g}
            .meas TRAN vout_max MAX V(vout) FROM {tmeas_from_s:.12g} TO {tstop_s:.12g}
            .meas TRAN vout_min MIN V(vout) FROM {tmeas_from_s:.12g} TO {tstop_s:.12g}
            .four {freq_hz:.12g} 1 5 V(vin) V(vout)
            .end
            """
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path
