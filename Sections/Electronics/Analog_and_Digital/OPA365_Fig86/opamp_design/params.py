"""Circuit parameters, op-amp non-ideals, tolerances, temperature, derating.

All R and C values used by notebooks and SPICE generators live here as
dataclasses so you can override them without editing analysis math.

HOW TO ADAPT FOR ANOTHER NETLIST
--------------------------------
1. Add or rename fields on ``CircuitParams`` for every passive you care about.
2. Update ``as_spice_params()`` so generated decks get matching ``.param`` names.
3. Update ``component_names()`` / tolerance maps used by WC, MC, and sensitivity.
4. If your circuit has no op-amp offsets, you can still keep ``OpampParams`` and
   set limits to 0.0 so non-ideal sources vanish.
5. Derating fields (package power, cap VR) are independent of topology — change
   them to match your BOM (e.g. 0603, 100 V ceramics).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from typing import Any, Iterable


@dataclass(frozen=True)
class ToleranceSpec:
    """Relative tolerance as a fraction (0.001 = 0.1%), not percent.

    Used for worst-case corners and uniform Monte Carlo draws:
        x ~ Uniform(x_nom * (1 - tol), x_nom * (1 + tol))
    """

    rel_tol: float = 0.001  # default 0.1%

    def __post_init__(self) -> None:
        if self.rel_tol < 0:
            raise ValueError("rel_tol must be >= 0")
        if self.rel_tol >= 1:
            raise ValueError("rel_tol must be < 1 (use fraction, e.g. 0.001 for 0.1%)")

    @property
    def percent(self) -> float:
        """Tolerance in percent for display (0.1 for rel_tol=0.001)."""
        return 100.0 * self.rel_tol

    def bounds(self, nom: float) -> tuple[float, float]:
        """Return (min, max) absolute value for a nominal component."""
        return nom * (1.0 - self.rel_tol), nom * (1.0 + self.rel_tol)

    def scale(self, nom: float, u: float) -> float:
        """Map a uniform [0, 1] draw ``u`` onto the tolerance interval."""
        lo, hi = self.bounds(nom)
        return lo + (hi - lo) * float(u)


@dataclass(frozen=True)
class OpampParams:
    """OPA365 (or substitute) DC input non-ideals and temp coefficients.

    Polarity conventions (used by ``analysis.py`` and SPICE sources)
    ----------------------------------------------------------------
    vos
        Differential input offset. Ideal infinite-gain constraint:
            V(+) - V(-) = vos
        With unity-gain feedback V(-)=Vout => Vout = V(+) - vos.
        Range for WC/MC: [-vos_max, +vos_max].

    ib_p, ib_n
        Bias currents **into** the + and - pins (amperes). Positive means
        conventional current entering the IC pin from the external net.
        At DC, ib_p flows through the series input resistors and creates a
        drop. ib_n is supplied by the op-amp output stage in a voltage-mode
        model, so H_ibn(s)=0 for an ideal VCVS (still carried for bookkeeping).

    ios, ib
        ios = ib_p - ib_n,  ib = (ib_p + ib_n)/2  (standard definitions).

    Temperature
    -----------
    vos(T) ≈ vos_nom + vos_drift * (T - T0)
    ib magnitude grows with temperature; see ``ib_at_temp``.

    To use another op-amp: construct OpampParams(name=..., vos_max=..., ...)
    from that device's datasheet and pass it into analysis / netlist helpers.
    """

    name: str = "OPA365"
    # Datasheet 25 °C electrical characteristics (SBOS365G)
    vos_typ: float = 100e-6  # V
    vos_max: float = 200e-6  # V
    vos_nom: float = 0.0  # used as the "nominal" sim value (0 unless injected)
    vos_drift_typ: float = 1e-6  # V/°C typical dVOS/dT
    ib_typ: float = 0.2e-12  # A (±0.2 pA typ)
    ib_max: float = 10e-12  # A (±10 pA max at 25 °C)
    ios_typ: float = 0.2e-12  # A
    ios_max: float = 10e-12  # A
    ib_p_nom: float = 0.0
    ib_n_nom: float = 0.0
    # Open-loop / AC (informational; macromodel provides dynamics in SPICE)
    gb_w: float = 50e6  # Hz
    t0_c: float = 25.0  # reference temperature °C

    def vos_bounds(self) -> tuple[float, float]:
        return -self.vos_max, self.vos_max

    def ib_bounds(self) -> tuple[float, float]:
        """Each of ib_p, ib_n independently over ±ib_max for WC/MC."""
        return -self.ib_max, self.ib_max

    def vos_at_temp(self, temp_c: float, vos_25: float | None = None) -> float:
        """Offset at temperature using linear drift from 25 °C.

        Parameters
        ----------
        temp_c : float
            Ambient / junction temperature in °C.
        vos_25 : float or None
            Offset at 25 °C. None => use vos_nom.
        """
        v0 = self.vos_nom if vos_25 is None else vos_25
        return v0 + self.vos_drift_typ * (temp_c - self.t0_c)

    def ib_scale_vs_temp(self, temp_c: float) -> float:
        """Multiplicative scale for |Ib| vs temperature.

        CMOS Ib is tiny near room temp and rises strongly at high T.
        This smooth empirical fit is anchored to the datasheet qualitative
        curve (Fig. 7-5): near 1× at 25 °C, tens–hundreds of pA class toward
        125 °C. Override or replace for a different process family.

        Returns a scale factor applied to the 25 °C Ib value (typ or max).
        """
        # Piecewise-log-ish growth: ~1 at 25 °C, ~50 at 85 °C, ~500 at 125 °C
        # (order-of-magnitude model for analysis — not a fit guarantee).
        dT = temp_c - self.t0_c
        # scale = exp(k * dT) with k chosen so 125 °C ~ 500×
        # exp(k*100)=500 => k = ln(500)/100 ≈ 0.062
        import math

        return math.exp(0.062 * dT)

    def ib_max_at_temp(self, temp_c: float) -> float:
        """Temperature-adjusted |Ib| max bound (A)."""
        return self.ib_max * self.ib_scale_vs_temp(temp_c)

    def summary_rows(self) -> list[tuple[str, str]]:
        return [
            ("Device", self.name),
            ("Vos max (25 °C)", f"±{self.vos_max * 1e6:.0f} µV"),
            ("Vos drift typ", f"{self.vos_drift_typ * 1e6:.1f} µV/°C"),
            ("Ib max (25 °C)", f"±{self.ib_max * 1e12:.0f} pA"),
            ("Ios max (25 °C)", f"±{self.ios_max * 1e12:.0f} pA"),
            ("GBW typ", f"{self.gb_w / 1e6:.0f} MHz"),
        ]


@dataclass(frozen=True)
class OperatingPoint:
    """Supply and stimulus for the Fig. 8-6 evaluation.

    Single +5 V supply; input biased at mid-rail with large-signal swing
    used for derating / transient. Small-signal AC uses the same bias as
    the DC operating point (SPICE AC is linearized about the bias).
    """

    v_supply: float = 5.0  # V (V+ rail; V- = 0)
    v_in_bias: float = 2.5  # V
    v_in_peak: float = 2.5  # V peak about bias (full 0..5 V envelope)
    r_load: float = 10e3  # optional load on Vout (ohms); set 1e12 for open
    f_design_hz: float = 20e3  # datasheet design target (annotation)

    @property
    def v_in_min(self) -> float:
        return self.v_in_bias - self.v_in_peak

    @property
    def v_in_max(self) -> float:
        return self.v_in_bias + self.v_in_peak


@dataclass(frozen=True)
class TempcoParams:
    """Passive temperature coefficients (ppm/°C) and sweep grid.

    Defaults assume precision thin-film resistors and C0G/NP0 NPO ceramics
    typical of analog filters. Override for X7R "what-if" studies.
    """

    tcr_ppm_per_c: float = 50.0  # resistor TCR magnitude (use ± in WC)
    tcc_ppm_per_c: float = 30.0  # capacitor TCC magnitude (C0G-ish)
    temp_min_c: float = -40.0
    temp_max_c: float = 125.0
    temp_step_c: float = 10.0
    t_ref_c: float = 25.0

    def grid(self) -> list[float]:
        """Inclusive temperature grid from min to max (always includes t_ref_c)."""
        vals: list[float] = []
        t = self.temp_min_c
        # Guard against float drift
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
        """Linear tempco: x(T) = x0 * (1 + ppm*1e-6 * (T - Tref))."""
        return nom * (1.0 + ppm * 1e-6 * (temp_c - self.t_ref_c))


@dataclass(frozen=True)
class DeratingParams:
    """Package / voltage derating rules for reliability checks.

    Resistors: 0805 thick/thin film, default 0.125 W full rating to 70 °C,
    linear derate to 0 W at t_zero_power_c (common vendor curve shape).

    Capacitors: voltage rating 50 V; recommended operating fraction of VR
    (default 50% => 25 V max) for ceramic long-term reliability.
    """

    resistor_package: str = "0805"
    resistor_power_rated_w: float = 0.125
    resistor_full_power_to_c: float = 70.0
    resistor_zero_power_c: float = 155.0
    # Soft guideline: operate below this fraction of *derated* power
    resistor_power_use_fraction: float = 0.5
    capacitor_v_rated: float = 50.0
    capacitor_v_use_fraction: float = 0.5  # 50% of VR

    def derated_power_w(self, temp_c: float) -> float:
        """Max recommended resistor dissipation at ambient temp_c."""
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
    """Fig. 8-6 passive network (all values are variables for notebooks).

    Topology (unity-gain three-pole Sallen–Key LPF)::

        VIN -- R1 -- n1 -- R2 -- n2 -- R3 -- n3 --(+) OPA365 -- VOUT
                |           |            |          |
               C1          C3           C2         (-)
               gnd      (to VOUT)       gnd      tied to VOUT

    To re-use this project for another filter:
    - Change the numeric fields below (or ``replace(params, R1=...)``).
    - If the *topology* changes, update ``analysis.nodal_system`` and
      ``netlist.build_fig86_netlist`` to match your node graph; keep the
      same field names where possible so notebooks keep working.
    """

    R1: float = 1.8e3  # ohms
    R2: float = 19.5e3
    R3: float = 150e3
    C1: float = 3.3e-9  # farads
    C2: float = 47e-12
    C3: float = 220e-12

    r_tol: ToleranceSpec = field(default_factory=lambda: ToleranceSpec(0.001))  # 0.1%
    c_tol: ToleranceSpec = field(default_factory=lambda: ToleranceSpec(0.01))  # 1%

    opamp: OpampParams = field(default_factory=OpampParams)
    op: OperatingPoint = field(default_factory=OperatingPoint)
    tempco: TempcoParams = field(default_factory=TempcoParams)
    derating: DeratingParams = field(default_factory=DeratingParams)

    def with_values(self, **kwargs: float) -> "CircuitParams":
        """Return a copy with selected R/C overrides, e.g. with_values(R1=2e3)."""
        return replace(self, **kwargs)

    def passive_dict(self) -> dict[str, float]:
        """Name → nominal value for R1..C3 (used by MC/sensitivity)."""
        return {
            "R1": self.R1,
            "R2": self.R2,
            "R3": self.R3,
            "C1": self.C1,
            "C2": self.C2,
            "C3": self.C3,
        }

    def resistance_names(self) -> tuple[str, ...]:
        return ("R1", "R2", "R3")

    def capacitance_names(self) -> tuple[str, ...]:
        return ("C1", "C2", "C3")

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
        """Apply linear TCR/TCC to all R and C; return new CircuitParams.

        tcr_sign / tcc_sign: +1 or -1 to pick the tempco polarity corner.
        """
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
            C3=tc.scale_passive(self.C3, temp_c, ppm_c),
        )

    def as_spice_params(self) -> dict[str, float]:
        """Flat dict of SPICE .param names used by generated decks.

        If you author a custom netlist by hand, either use these names
        (R1, R2, R3, C1, C2, C3, VSUP, VINBIAS, ...) or change the generator
        in netlist.py to emit your names.
        """
        return {
            "R1": self.R1,
            "R2": self.R2,
            "R3": self.R3,
            "C1": self.C1,
            "C2": self.C2,
            "C3": self.C3,
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
    """Factory for the datasheet Figure 8-6 nominal design."""
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
