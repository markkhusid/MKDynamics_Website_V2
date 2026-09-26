"""Temperature sweep of passives, Vos, and Ib for Fig. 8-6.

Models (documented defaults; all overridable via CircuitParams.tempco / opamp):
* R(T) = R0 * (1 + TCR_ppm*1e-6 * (T - 25))
* C(T) = C0 * (1 + TCC_ppm*1e-6 * (T - 25))
* Vos(T) = Vos25 + alpha * (T - 25)
* |Ib|(T) scaled by OpampParams.ib_scale_vs_temp

HOW TO ADAPT FOR ANOTHER NETLIST
--------------------------------
For SPICE-only temp sweeps on a custom deck, put ``.step temp`` / ``.temp``
in your netlist and parse measurements — you do not need this module's
analytical path.  For analytical metrics on a different topology, keep
``sweep_analytical`` but point ``metric_fn`` at your own function of
``CircuitParams``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .params import CircuitParams


@dataclass
class TempSweepResult:
    frame: pd.DataFrame  # one row per temperature

    def save(self, path: Path | str) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.frame.to_csv(path, index=False)


def sweep_analytical(
    p: CircuitParams | None = None,
    *,
    temps_c: list[float] | None = None,
    tcr_sign: float = 1.0,
    tcc_sign: float = 1.0,
    vos_25: float = 0.0,
    use_ib_max_at_temp: bool = True,
) -> TempSweepResult:
    """Analytical metrics vs temperature.

    Parameters
    ----------
    tcr_sign, tcc_sign :
        +1 or -1 polarity of tempco (WC corners of drift direction).
    vos_25 :
        Offset at 25 °C before drift (0 for ideal mid-point).
    use_ib_max_at_temp :
        If True, inject Ib+ = +ib_max(T) as a pessimistic bias error term.
    """
    from .analysis import dc_vout, find_fc_3db, gain_at, passband_gain

    if p is None:
        p = CircuitParams()
    if temps_c is None:
        temps_c = p.tempco.grid()

    rows = []
    for T in temps_c:
        pt = p.scaled_at_temp(T, tcr_sign=tcr_sign, tcc_sign=tcc_sign)
        vos = p.opamp.vos_at_temp(T, vos_25=vos_25)
        if use_ib_max_at_temp:
            ib = p.opamp.ib_max_at_temp(T)
            ibp, ibn = ib, ib  # same sign worst-ish for drop on + side
        else:
            ibp = ibn = 0.0
        fc = find_fc_3db(pt)
        h_pb = abs(passband_gain(pt, 100.0))
        h_des = gain_at(pt, p.op.f_design_hz, "vin")
        v_id = dc_vout(pt, vin=p.op.v_in_bias, vos=0.0, ibp=0.0, ibn=0.0)
        v_tot = dc_vout(pt, vin=p.op.v_in_bias, vos=vos, ibp=ibp, ibn=ibn)
        rows.append(
            {
                "temp_c": T,
                "R1": pt.R1,
                "R2": pt.R2,
                "R3": pt.R3,
                "C1": pt.C1,
                "C2": pt.C2,
                "C3": pt.C3,
                "vos": vos,
                "ibp": ibp,
                "fc_hz": fc,
                "passband_gain": h_pb,
                "gain_at_fdesign": abs(h_des),
                "phase_at_fdesign_deg": float(np.angle(h_des, deg=True)),
                "dc_error": v_tot - v_id,
            }
        )
    return TempSweepResult(frame=pd.DataFrame(rows))


def spice_temp_sweep(
    p: CircuitParams | None = None,
    *,
    temps_c: list[float] | None = None,
    workdir: Path | str,
    root: Path | str | None = None,
    opamp_model: str = "ideal",
    apply_passive_tempco: bool = True,
    tcr_sign: float = 1.0,
    tcc_sign: float = 1.0,
    ngspice=None,
) -> TempSweepResult:
    """ngspice AC at each temperature (scaled passives + .temp).

    Note: the TI macromodel does not perfectly track all datasheet temp
    curves; ideal model + explicit tempco is the fair analytical match.
    """
    from .simulate import simulate_ac

    if p is None:
        p = CircuitParams()
    if temps_c is None:
        temps_c = p.tempco.grid()
    workdir = Path(workdir)
    rows = []
    for T in temps_c:
        pt = (
            p.scaled_at_temp(T, tcr_sign=tcr_sign, tcc_sign=tcc_sign)
            if apply_passive_tempco
            else p
        )
        from .netlist import NetlistOptions

        opt = NetlistOptions(opamp_model=opamp_model, analysis="ac", temp_c=T)
        wd = workdir / f"T_{T:.0f}"
        ac = simulate_ac(pt, opamp_model=opamp_model, workdir=wd, root=root, opt=opt, ngspice=ngspice)
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
        rows.append({"temp_c": T, "fc_spice_hz": fc_sp, "passband_gain_spice": float(dc)})
    return TempSweepResult(frame=pd.DataFrame(rows))
