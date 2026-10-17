"""Circuit parameters, op-amp non-ideals, tolerances, temperature, derating.

Figure 8-5 is an inverting multiple-feedback low-pass filter. Published
values are R1 = 549 Ω, R2 = 1.24 kΩ, R3 = 549 Ω, C1 = 1 nF, C2 = 150 pF.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from typing import Any


@dataclass(frozen=True)
class ToleranceSpec:
    """Relative tolerance as a fraction (0.001 = 0.1%), not percent."""

    rel_tol: float = 0.001

    def __post_init__(self) -> None:
        if self.rel_tol < 0:
            raise ValueError("rel_tol must be >= 0")
        if self.rel_tol >= 1:
            raise ValueError("rel_tol must be < 1 (use a fraction, e.g. 0.001)")

    @property
    def percent(self) -> float:
        return 100.0 * self.rel_tol

    def bounds(self, nom: float) -> tuple[float, float]:
        return nom * (1.0 - self.rel_tol), nom * (1.0 + self.rel_tol)

    def scale(self, nom: float, u: float) -> float:
        lo, hi = self.bounds(nom)
        return lo + (hi - lo) * float(u)


@dataclass(frozen=True)
class OpampParams:
    """OPA365 DC input non-ideals used by the linear model.

    Polarity
    --------
    vos
        V(+) − V(−) = vos. On Figure 8-5 the + pin is grounded, so the
        inverting pin sits at −vos.
    ib_p, ib_n
        Current into the + and − pins. The + pin is tied to ground, so
        ib_p does not enter the signal nodes. ib_n leaves the inverting
        node and does move the output.
    """

    name: str = "OPA365"
    vos_typ: float = 100e-6
    vos_max: float = 200e-6
    vos_nom: float = 0.0
    vos_drift_typ: float = 1e-6
    ib_typ: float = 0.2e-12
    ib_max: float = 10e-12
    ios_typ: float = 0.2e-12
    ios_max: float = 10e-12
    ib_p_nom: float = 0.0
    ib_n_nom: float = 0.0
    gb_w: float = 50e6
    t0_c: float = 25.0
    iq_typ: float = 4.6e-3
    package_power_allow_w: float = 0.5
    v_supply_max: float = 5.5
    v_supply_min: float = 2.2
    slew_rate_v_per_s: float = 25e6

    def vos_bounds(self) -> tuple[float, float]:
        return -self.vos_max, self.vos_max

    def ib_bounds(self) -> tuple[float, float]:
        return -self.ib_max, self.ib_max

    def vos_at_temp(self, temp_c: float, vos_25: float | None = None) -> float:
        v0 = self.vos_nom if vos_25 is None else vos_25
        return v0 + self.vos_drift_typ * (temp_c - self.t0_c)

    def ib_scale_vs_temp(self, temp_c: float) -> float:
        """Smooth |Ib| growth used as a study model, not a datasheet fit.

        Anchored near 1× at 25 °C and about 500× at 125 °C.
        """
        import math

        return math.exp(0.062 * (temp_c - self.t0_c))

    def ib_max_at_temp(self, temp_c: float) -> float:
        return self.ib_max * self.ib_scale_vs_temp(temp_c)

    def summary_rows(self) -> list[tuple[str, str]]:
        return [
            ("Device", self.name),
            ("Vos max (25 °C)", f"±{self.vos_max * 1e6:.0f} µV"),
            ("Vos drift typ", f"{self.vos_drift_typ * 1e6:.1f} µV/°C"),
            ("Ib max (25 °C)", f"±{self.ib_max * 1e12:.0f} pA"),
            ("Ios max (25 °C)", f"±{self.ios_max * 1e12:.0f} pA"),
            ("GBW typ", f"{self.gb_w / 1e6:.0f} MHz"),
            ("Iq typ", f"{self.iq_typ * 1e3:.1f} mA"),
            ("Slew rate typ", f"{self.slew_rate_v_per_s / 1e6:.0f} V/µs"),
        ]


@dataclass(frozen=True)
class OperatingPoint:
    """Supplies and stimulus for the Figure 8-5 study.

    The datasheet drawing grounds the + pin and does not print the rails.
    ±2.5 V keeps the inverted output inside a 5 V span. The ideal model
    does not clip; the span is still inside 2.2 V to 5.5 V.
    """

    v_pos: float = 2.5
    v_neg: float = -2.5
    v_in_bias: float = 0.0
    v_in_peak: float = 1.0
    r_load: float = 10e3
    f_design_hz: float = 500e3
    f_passband_hz: float = 250e3

    @property
    def v_supply(self) -> float:
        """Total supply span, V+ minus V−."""
        return self.v_pos - self.v_neg

    @property
    def v_in_min(self) -> float:
        return self.v_in_bias - self.v_in_peak

    @property
    def v_in_max(self) -> float:
        return self.v_in_bias + self.v_in_peak


@dataclass(frozen=True)
class TempcoParams:
    """Passive temperature coefficients and the sweep grid.

    Defaults are a precision thin-film / C0G assumption for this study.
    """

    tcr_ppm_per_c: float = 50.0
    tcc_ppm_per_c: float = 30.0
    temp_min_c: float = -40.0
    temp_max_c: float = 125.0
    temp_step_c: float = 10.0
    t_ref_c: float = 25.0

    def grid(self) -> list[float]:
        vals: list[float] = []
        t = self.temp_min_c
        while t <= self.temp_max_c + 1e-9:
            vals.append(round(t, 6))
            t += self.temp_step_c
        if vals[-1] < self.temp_max_c - 1e-9:
            vals.append(self.temp_max_c)
        if self.t_ref_c not in vals:
            vals.append(self.t_ref_c)
            vals = sorted(set(vals))
        return vals

    def scale_passive(self, nom: float, temp_c: float, ppm: float) -> float:
        return nom * (1.0 + ppm * 1e-6 * (temp_c - self.t_ref_c))


@dataclass(frozen=True)
class DeratingParams:
    """0805 resistor power curve and 50 V capacitor voltage fraction."""

    resistor_package: str = "0805"
    resistor_power_rated_w: float = 0.125
    resistor_full_power_to_c: float = 70.0
    resistor_zero_power_c: float = 155.0
    resistor_power_use_fraction: float = 0.5
    resistor_voltage_guideline: float = 150.0
    capacitor_v_rated: float = 50.0
    capacitor_v_use_fraction: float = 0.5

    def derated_power_w(self, temp_c: float) -> float:
        p = self.resistor_power_rated_w
        t1 = self.resistor_full_power_to_c
        t0 = self.resistor_zero_power_c
        if temp_c <= t1:
            return p
        if temp_c >= t0:
            return 0.0
        return p * (t0 - temp_c) / (t0 - t1)

    @property
    def capacitor_v_max_recommended(self) -> float:
        return self.capacitor_v_rated * self.capacitor_v_use_fraction


@dataclass(frozen=True)
class CircuitParams:
    """Figure 8-5 multiple-feedback low-pass network.

    VIN — R1 — n1 — R2 — n2 (inverting input)
              |         |
             C1        C2 to VOUT
             gnd
              |
             R3 to VOUT

    The non-inverting input is grounded. Ideal constraint: V(n2) = −Vos.
    """

    R1: float = 549.0
    R2: float = 1.24e3
    R3: float = 549.0
    C1: float = 1.0e-9
    C2: float = 150.0e-12

    r_tol: ToleranceSpec = field(default_factory=lambda: ToleranceSpec(0.001))
    c_tol: ToleranceSpec = field(default_factory=lambda: ToleranceSpec(0.01))

    opamp: OpampParams = field(default_factory=OpampParams)
    op: OperatingPoint = field(default_factory=OperatingPoint)
    tempco: TempcoParams = field(default_factory=TempcoParams)
    derating: DeratingParams = field(default_factory=DeratingParams)

    def with_values(self, **kwargs: float) -> "CircuitParams":
        return replace(self, **kwargs)

    def passive_dict(self) -> dict[str, float]:
        return {"R1": self.R1, "R2": self.R2, "R3": self.R3, "C1": self.C1, "C2": self.C2}

    def resistance_names(self) -> tuple[str, ...]:
        return ("R1", "R2", "R3")

    def capacitance_names(self) -> tuple[str, ...]:
        return ("C1", "C2")

    def tol_for(self, name: str) -> ToleranceSpec:
        if name.startswith("R") or name.startswith("r"):
            return self.r_tol
        if name.startswith("C") or name.startswith("c"):
            return self.c_tol
        raise KeyError(f"No tolerance mapping for {name!r}")

    def scaled_at_temp(
        self,
        temp_c: float,
        tcr_sign: float = 1.0,
        tcc_sign: float = 1.0,
    ) -> "CircuitParams":
        tc = self.tempco
        ppm_r = tcr_sign * tc.tcr_ppm_per_c
        ppm_c = tcc_sign * tc.tcc_ppm_per_c
        return replace(
            self,
            R1=tc.scale_passive(self.R1, temp_c, ppm_r),
            R2=tc.scale_passive(self.R2, temp_c, ppm_r),
            R3=tc.scale_passive(self.R3, temp_c, ppm_r),
            C1=tc.scale_passive(self.C1, temp_c, ppm_c),
            C2=tc.scale_passive(self.C2, temp_c, ppm_c),
        )

    def as_spice_params(self) -> dict[str, float]:
        return {
            "R1": self.R1,
            "R2": self.R2,
            "R3": self.R3,
            "C1": self.C1,
            "C2": self.C2,
            "VPOS": self.op.v_pos,
            "VNEG": self.op.v_neg,
            "VSUP": self.op.v_supply,
            "VINBIAS": self.op.v_in_bias,
            "VINPEAK": self.op.v_in_peak,
            "RLOAD": self.op.r_load,
            "VOS": self.opamp.vos_nom,
            "IBP": self.opamp.ib_p_nom,
            "IBN": self.opamp.ib_n_nom,
        }

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_circuit() -> CircuitParams:
    return CircuitParams()


def format_eng(x: float, unit: str = "") -> str:
    """Engineering-string helper for notebook tables."""
    ax = abs(x)
    if ax == 0:
        return f"0 {unit}".strip()
    import math

    exp = int(math.floor(math.log10(ax) / 3) * 3)
    exp = max(min(exp, 12), -15)
    scaled = x / 10**exp
    prefixes = {
        12: "T",
        9: "G",
        6: "M",
        3: "k",
        0: "",
        -3: "m",
        -6: "µ",
        -9: "n",
        -12: "p",
        -15: "f",
    }
    return f"{scaled:.4g} {prefixes.get(exp, f'e{exp}')}{unit}".strip()
