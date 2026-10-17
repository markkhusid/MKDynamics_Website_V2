"""Temperature sweep of the Figure 8-5 passives, offset, and bias current.

R(T) = R0 (1 + TCR_ppm * 1e-6 * (T − 25))
C(T) = C0 (1 + TCC_ppm * 1e-6 * (T − 25))
Vos(T) = Vos25 + drift * (T − 25)
|Ib|(T) follows the smooth scale in OpampParams.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .params import CircuitParams


@dataclass
class TempSweepResult:
    frame: pd.DataFrame

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
    from .analysis import dc_vout, find_fc_3db, gain_at, passband_gain

    if p is None:
        p = CircuitParams()
    if temps_c is None:
        temps_c = p.tempco.grid()
    rows = []
    for temp in temps_c:
        pt = p.scaled_at_temp(temp, tcr_sign=tcr_sign, tcc_sign=tcc_sign)
        vos = p.opamp.vos_at_temp(temp, vos_25=vos_25)
        if use_ib_max_at_temp:
            ib = p.opamp.ib_max_at_temp(temp)
            ibp, ibn = ib, ib
        else:
            ibp = ibn = 0.0
        h_des = gain_at(pt, p.op.f_design_hz, "vin")
        h_tone = gain_at(pt, p.op.f_passband_hz, "vin")
        v_id = dc_vout(pt, vin=1.0, vos=0.0, ibp=0.0, ibn=0.0)
        v_tot = dc_vout(pt, vin=1.0, vos=vos, ibp=ibp, ibn=ibn)
        rows.append(
            {
                "temp_c": temp,
                "R1": pt.R1,
                "R2": pt.R2,
                "R3": pt.R3,
                "C1": pt.C1,
                "C2": pt.C2,
                "vos": vos,
                "ibp": ibp,
                "ibn": ibn,
                "fc_hz": find_fc_3db(pt),
                "passband_gain": float(abs(passband_gain(pt, 100.0))),
                "gain_at_fdesign": float(abs(h_des)),
                "phase_at_fdesign_deg": float(np.angle(h_des, deg=True)),
                "gain_at_passband": float(abs(h_tone)),
                "phase_at_passband_deg": float(np.angle(h_tone, deg=True)),
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
    from .netlist import NetlistOptions
    from .simulate import fc_from_mag, simulate_ac

    if p is None:
        p = CircuitParams()
    if temps_c is None:
        temps_c = p.tempco.grid()
    workdir = Path(workdir)
    rows = []
    for temp in temps_c:
        pt = p.scaled_at_temp(temp, tcr_sign=tcr_sign, tcc_sign=tcc_sign) if apply_passive_tempco else p
        opt = NetlistOptions(opamp_model=opamp_model, analysis="ac", temp_c=float(temp))
        ac = simulate_ac(
            pt,
            opamp_model=opamp_model,
            workdir=workdir / f"T_{float(temp):.0f}",
            root=root,
            opt=opt,
            ngspice=ngspice,
        )
        mag = np.abs(ac.h)
        rows.append(
            {
                "temp_c": float(temp),
                "fc_spice_hz": fc_from_mag(ac.f_hz, mag),
                "passband_gain_spice": float(mag[0]),
            }
        )
    return TempSweepResult(frame=pd.DataFrame(rows))
