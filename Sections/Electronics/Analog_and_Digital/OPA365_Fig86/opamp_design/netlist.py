"""Generate ngspice / LTspice-compatible netlists for Fig. 8-6.

Two op-amp models are supported in the *same* passive network:

* ``ideal`` — voltage-controlled voltage source (VCVS) with explicit
  Vos, Ibp, Ibn sources so analytical non-ideals match SPICE 1:1.
* ``opa365`` — TI macromodel subcircuit from ``models/opa365/OPA365.lib``.

HOW TO USE YOUR OWN NETLIST
---------------------------
You do **not** have to use this generator.  For a custom circuit:

1. Write a ``.cir`` (ngspice) or ``.asc``/``.cir`` (LTspice) by hand.
2. Call ``simulate.run_external_netlist(path, workdir=...)`` or
   ``ltspice_io.run_ltspice_deck(path)``.
3. Ensure your deck prints / measures the same signals the parsers expect,
   **or** update the parser key map:
   - ngspice: vectors ``frequency``, ``v(vout)``, ``v(vin)`` (AC)
   - LTspice: ``.meas`` names documented in ``ltspice_io.py``

If you only change passive values, prefer editing ``CircuitParams`` and
keeping this generator — all notebooks stay consistent.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

from .params import CircuitParams


# Repository-root relative default model location (resolved at write time).
DEFAULT_OPA365_LIB = Path("models") / "opa365" / "OPA365.lib"


@dataclass
class NetlistOptions:
    """Switches that control how the deck is built.

    Attributes
    ----------
    opamp_model :
        ``\"ideal\"`` or ``\"opa365\"``.
    analysis :
        ``\"ac\"`` | ``\"dc_op\"`` | ``\"tran\"`` | ``\"ac_temp\"``.
    lib_path :
        Absolute or relative path to OPA365.lib (only for opa365 model).
    include_nonideals :
        When True, emit Vos / Ibp / Ibn sources (mainly for ideal model).
    ac_fstart, ac_fstop, ac_points :
        AC decade sweep controls.
    temp_c :
        Operating temperature for ``.temp`` / ``.options TEMP``.
    mirror_path :
        Optional second write location (e.g. netlists/ tree).
    """

    opamp_model: str = "ideal"
    analysis: str = "ac"
    lib_path: Path | None = None
    include_nonideals: bool = True
    ac_fstart: float = 10.0
    ac_fstop: float = 10e6
    ac_points: int = 40  # points per decade
    temp_c: float = 25.0
    title: str = "OPA365 Fig8-6 Sallen-Key LPF"


def _param_block(p: CircuitParams) -> str:
    """Emit .param lines for every variable R/C and bias source.

    When adapting names for a hand-written netlist, either rename here or
    replace values in the deck after generation.
    """
    sp = p.as_spice_params()
    lines = [f".param {k}={v:.12g}" for k, v in sp.items()]
    return "\n".join(lines)


def _passive_network() -> str:
    """Shared R/C ladder + feedback C3. Node names are the contract.

    Nodes
    -----
    vin, n1, n2, n3, vout, vcc, 0

    Change this string (and analysis.py together) if you alter topology.
    """
    return dedent(
        """\
        * --- Passive network (Fig. 8-6) ---
        R1 vin n1 {R1}
        C1 n1 0 {C1}
        R2 n1 n2 {R2}
        R3 n2 n3 {R3}
        C2 n3 0 {C2}
        C3 n2 vout {C3}
        """
    )


def _ideal_opamp(include_nonideals: bool) -> str:
    """Unity-gain ideal op-amp with optional Vos and bias currents.

    Implementation
    --------------
    * Eamp: VCVS gain 1e6 from (vplus - vminus) to produce vout_int
    * Unity feedback: vminus tied to vout
    * Vos: series DC source between n3 and vplus  (vplus = n3 - Vos
      when Vos source polarity is n3 --(+)Vos(-)-- vplus with value Vos,
      so vplus - n3 = -Vos ... we use: n3 is + of source, vplus is -,
      value={VOS} => n3 - vplus = VOS => vplus = n3 - VOS.
      Constraint Vout ≈ vplus (unity) => Vout ≈ n3 - VOS. Matches analysis.
    * Ibp into n3 (from n3 to 0 would be wrong direction). Current source
      from 0 to n3 with value -Ibp means Ibp enters the pin from external
      view... Standard: Ibp into op-amp pin leaves node n3 into the amp.
      G or I source: ``Ibp n3 0 {IBP}`` draws IBP from n3 to ground, i.e.
      current leaves n3 toward gnd — equivalent to current into the pin
      if the pin is the only other path... Actually the op-amp + pin is
      vplus, not n3, when Vos is in series.

    Cleaner non-ideal placement (matches analysis.py):
    * Op-amp + pin at n3 directly when VOS=0.
    * Vos modeled as ``VOS n3 vplus DC {VOS}`` with ``n3 - vplus = VOS``.
    * Ibp: ``IBP n3 0 DC {IBP}`` — current from n3 to 0, i.e. out of the
      network node into a shunt; analysis places Ibp as leaving n3 into
      the + pin. With + pin = vplus after Vos, Ibp should leave n3 through
      the series Vos source into the amp. For DC resistance of Vos=0,
      putting IBP from n3 to 0 is a good approximation only if amp input
      current is that shunt... 

    Analysis KCL: (V3-V2)/R3 + s*C2*V3 + Ibp = 0  with Ibp into the IC.
    So Ibp leaves node n3. SPICE: ``IBP n3 0 {IBP}`` has current IBP
    flowing n3→0, leaving n3 — correct sign.

    Ibn: ``IBN vout 0 {IBN}`` leaves vout toward gnd (into - pin).
    Ideal VCVS ignores it for Vo; included for completeness / matching.
    """
    vos_bit = ""
    if include_nonideals:
        vos_bit = dedent(
            """\
            * Vos: n3 - vplus = VOS  => vplus = n3 - VOS
            VOS n3 vplus DC {VOS}
            * Bias currents into the IC pins (leave external nodes)
            IBP n3 0 DC {IBP}
            IBN vout 0 DC {IBN}
            """
        )
    else:
        vos_bit = "VOS n3 vplus DC 0\n"

    return vos_bit + dedent(
        """\
        * Ideal high-gain op-amp, unity feedback to vout
        EAMP vout 0 vplus vout 1e6
        """
    )


def _spice_lib_ref(lib: Path, deck_dir: Path | None) -> str:
    """Include path for OPA365.lib, relative to the deck when possible.

    An absolute path would embed a local home directory in generated decks.
    ngspice is started with the deck directory as cwd (see
    ``simulate.run_ngspice``), so a path relative to that directory resolves.
    """
    lib = Path(lib)
    if deck_dir is not None:
        try:
            return Path(os.path.relpath(lib.resolve(), Path(deck_dir).resolve())).as_posix()
        except ValueError:
            return lib.resolve().as_posix()
    try:
        return Path(os.path.relpath(lib.resolve(), Path.cwd().resolve())).as_posix()
    except ValueError:
        return DEFAULT_OPA365_LIB.as_posix()


def _opa365_instance(lib: Path, deck_dir: Path | None = None) -> str:
    """Instance TI OPA365: pins +IN -IN +V -V OUT.

    The macromodel itself is not shipped in this repository. Download TI
    PSpice model SBOC133A and place ``OPA365.lib`` at
    ``models/opa365/OPA365.lib``.
    """
    lib_s = _spice_lib_ref(lib, deck_dir)
    return dedent(
        f"""\
        * TI OPA365 macromodel (pin order: +IN -IN +V -V OUT)
        * Not included in this repo. Download SBOC133A from ti.com and
        * save it as models/opa365/OPA365.lib. Path is relative to this deck.
        .include '{lib_s}'
        XU1 n3 vout vcc 0 vout OPA365
        """
    )


def _analysis_block(opt: NetlistOptions, p: CircuitParams) -> str:
    if opt.analysis == "ac":
        # AC source: magnitude 1 V about the DC bias set on Vin
        return dedent(
            f"""\
            * DC bias on vin; AC magnitude 1 V for transfer V(vout)/V(vin)
            Vin vin 0 DC {{VINBIAS}} AC 1 0
            Vcc vcc 0 DC {{VSUP}}
            .temp {opt.temp_c}
            .ac dec {opt.ac_points} {opt.ac_fstart} {opt.ac_fstop}
            .control
            run
            wrdata vout_ac vdb(vout) vp(vout) vm(vout) vdb(vin) vm(vin)
            wrdata vout_complex real(v(vout)) imag(v(vout)) real(v(vin)) imag(v(vin))
            quit
            .endc
            """
        )
    if opt.analysis == "dc_op":
        return dedent(
            f"""\
            Vin vin 0 DC {{VINBIAS}}
            Vcc vcc 0 DC {{VSUP}}
            .temp {opt.temp_c}
            .op
            .control
            run
            print v(vout) v(vin) v(n1) v(n2) v(n3)
            echo OP_VOUT
            print v(vout)
            quit
            .endc
            """
        )
    if opt.analysis == "tran":
        # Full-scale sine about mid-rail for qualitative check
        return dedent(
            f"""\
            Vin vin 0 DC {{VINBIAS}} SIN({{VINBIAS}} {{VINPEAK}} 1k 0 0 0)
            Vcc vcc 0 DC {{VSUP}}
            .temp {opt.temp_c}
            .tran 1u 5m
            .control
            run
            wrdata vout_tran v(vout) v(vin)
            quit
            .endc
            """
        )
    if opt.analysis == "ac_temp":
        return _analysis_block(
            NetlistOptions(
                opamp_model=opt.opamp_model,
                analysis="ac",
                lib_path=opt.lib_path,
                include_nonideals=opt.include_nonideals,
                ac_fstart=opt.ac_fstart,
                ac_fstop=opt.ac_fstop,
                ac_points=opt.ac_points,
                temp_c=opt.temp_c,
            ),
            p,
        )
    raise ValueError(f"Unknown analysis {opt.analysis!r}")


def build_fig86_netlist(
    p: CircuitParams | None = None,
    opt: NetlistOptions | None = None,
    root: Path | None = None,
    deck_dir: Path | None = None,
) -> str:
    """Return the full deck text for Fig. 8-6.

    Parameters
    ----------
    p :
        Component values / biases.
    opt :
        Model and analysis switches.
    root :
        Project root for resolving relative lib paths.
    deck_dir :
        Directory the deck will be written to. The ``.include`` of
        ``OPA365.lib`` is made relative to this directory.
    """
    if p is None:
        p = CircuitParams()
    if opt is None:
        opt = NetlistOptions()
    root = Path(root) if root is not None else Path.cwd()

    lib = opt.lib_path
    if lib is None:
        lib = root / DEFAULT_OPA365_LIB
    elif not lib.is_absolute():
        lib = root / lib

    parts = [
        f"* {opt.title}",
        f"* opamp_model={opt.opamp_model}  analysis={opt.analysis}  temp={opt.temp_c}",
        ".options savecurrents",
        _param_block(p),
        _passive_network(),
    ]
    if opt.opamp_model.lower() == "ideal":
        parts.append(_ideal_opamp(opt.include_nonideals))
    elif opt.opamp_model.lower() in ("opa365", "opa"):
        parts.append(_opa365_instance(lib, deck_dir=deck_dir))
    else:
        raise ValueError(
            f"Unknown opamp_model={opt.opamp_model!r}. "
            "Use 'ideal' or 'opa365', or supply a fully custom netlist file."
        )

    # Optional light load
    parts.append("Rload vout 0 {RLOAD}")
    parts.append(_analysis_block(opt, p))
    parts.append(".end\n")
    return "\n".join(parts)


def write_netlist(
    path: Path | str,
    p: CircuitParams | None = None,
    opt: NetlistOptions | None = None,
    root: Path | None = None,
    mirror: Path | str | None = None,
) -> Path:
    """Write deck to ``path`` and optionally mirror a browseable copy.

    The mirror is handy for a ``netlists/`` folder that stays free of logs.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = build_fig86_netlist(p=p, opt=opt, root=root, deck_dir=path.parent)
    path.write_text(text, encoding="utf-8")
    if mirror is not None:
        m = Path(mirror)
        m.parent.mkdir(parents=True, exist_ok=True)
        # Rebuild so the .include path is relative to the mirror, not the deck.
        m.write_text(
            build_fig86_netlist(p=p, opt=opt, root=root, deck_dir=m.parent),
            encoding="utf-8",
        )
    return path


def write_ltspice_ac_deck(
    path: Path | str,
    p: CircuitParams | None = None,
    opamp_model: str = "ideal",
    root: Path | None = None,
    temp_c: float = 25.0,
) -> Path:
    """Write an LTspice-oriented .cir (same network, LTspice meas style).

    LTspice uses ``.meas AC`` instead of ngspice ``wrdata``.  The passive
    network and params match the ngspice deck so apples-to-apples compare
    is possible.  For a GUI schematic workflow, open ``LTSpice/*.asc`` and
    export, or point the batch runner at any custom .cir you create.
    """
    if p is None:
        p = CircuitParams()
    root = Path(root) if root is not None else Path.cwd()
    lib = (root / DEFAULT_OPA365_LIB).resolve()
    deck_dir = Path(path).parent
    lib_s = _spice_lib_ref(lib, deck_dir)

    if opamp_model == "ideal":
        amp = dedent(
            """\
            VOS n3 vplus DC {VOS}
            IBP n3 0 DC {IBP}
            IBN vout 0 DC {IBN}
            EAMP vout 0 vplus vout 1e6
            """
        )
    else:
        amp = dedent(
            f"""\
            * OPA365.lib is not in this repo. Download TI SBOC133A into
            * models/opa365/OPA365.lib. Path is relative to this deck.
            .lib '{lib_s}'
            XU1 n3 vout vcc 0 vout OPA365
            """
        )

    sp = p.as_spice_params()
    params = "\n".join(f".param {k}={v:.12g}" for k, v in sp.items())
    text = dedent(
        f"""\
        * OPA365 Fig8-6 LTspice AC deck (generated)
        * To use your own schematic: File→Export netlist, keep .meas names below,
        * or edit ltspice_io.MEAS_KEYS to match your .meas statements.
        {params}
        R1 vin n1 {{R1}}
        C1 n1 0 {{C1}}
        R2 n1 n2 {{R2}}
        R3 n2 n3 {{R3}}
        C2 n3 0 {{C2}}
        C3 n2 vout {{C3}}
        {amp}
        Rload vout 0 {{RLOAD}}
        Vin vin 0 {{VINBIAS}} AC 1 0
        Vcc vcc 0 {{VSUP}}
        .temp {temp_c}
        .ac dec 40 10 10Meg
        .meas AC gain_100Hz FIND mag(V(vout)) AT 100
        .meas AC gain_20k FIND mag(V(vout)) AT 20k
        * Real/imag parts — compute phase in Python (LTspice ph() log format is awkward)
        .meas AC re_20k FIND re(V(vout)) AT 20k
        .meas AC im_20k FIND im(V(vout)) AT 20k
        .meas AC fc_3db WHEN mag(V(vout))=gain_100Hz/sqrt(2) FALL=1
        .end
        """
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path
