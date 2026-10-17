"""Analytical transfer of the Figure 8-5 multiple-feedback low-pass filter.

    Vout(s) = H_vin(s) Vin(s) + H_vos(s) Vos + H_ibp(s) Ibp + H_ibn(s) Ibn

Ideal infinite-gain constraint, + pin grounded:

    V(+) − V(−) = Vos  =>  V(n2) = −Vos

Closed form with Vos = Ibp = Ibn = 0:

    H(s) = −(1/R1) / [s² C1 C2 R2 + s C2 R2 (1/R1 + 1/R2 + 1/R3) + 1/R3]

    ω0 = 1 / sqrt(R2 R3 C1 C2)
    Q  = ω0 C1 / (1/R1 + 1/R2 + 1/R3)
    H(0) = −R3/R1

Ibp does not enter the signal nodes because the + pin is grounded.
Ibn leaves n2 and does move Vout. At DC, with R1 = R3,

    Vout = −Vin − (1 + R3/R1) Vos + Ibn (R2 + R3 + R2 R3/R1)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .params import CircuitParams, format_eng


def _conductances(p: CircuitParams) -> tuple[float, float, float]:
    return 1.0 / p.R1, 1.0 / p.R2, 1.0 / p.R3


def nodal_matrices(
    s: complex,
    p: CircuitParams,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """3×3 system for unknowns [V1, V2, Vo].

    Row 0 is KCL at the summing node n1.
    Row 1 is KCL at the inverting node n2.
    Row 2 is the ideal constraint V2 = −Vos.
    """
    g1, g2, g3 = _conductances(p)
    c1, c2 = p.C1, p.C2
    A = np.zeros((3, 3), dtype=complex)

    A[0, 0] = g1 + g2 + g3 + s * c1
    A[0, 1] = -g2
    A[0, 2] = -g3

    A[1, 0] = -g2
    A[1, 1] = g2 + s * c2
    A[1, 2] = -s * c2

    A[2, 1] = 1.0

    b_vin = np.array([g1, 0.0, 0.0], dtype=complex)
    b_vos = np.array([0.0, 0.0, -1.0], dtype=complex)
    b_ibp = np.zeros(3, dtype=complex)
    b_ibn = np.array([0.0, -1.0, 0.0], dtype=complex)
    return A, b_vin, b_vos, b_ibp, b_ibn


def state_matrices(
    p: CircuitParams,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Reduced real pencil for states [V1, Vo], with V2 = −Vos.

    C dx/dt + G x = b_vin vin + b_vos Vos + b_ibn Ibn

    C is diagonal (C1, C2) and invertible. The constraint row of the 3×3
    nodal matrix is not, so the transient integrator uses this reduction.
    """
    g1, g2, g3 = _conductances(p)
    g = np.array(
        [
            [g1 + g2 + g3, -g3],
            [g2, 0.0],
        ],
        dtype=float,
    )
    c = np.array(
        [
            [p.C1, 0.0],
            [0.0, p.C2],
        ],
        dtype=float,
    )
    b_vin = np.array([g1, 0.0], dtype=float)
    b_vos = np.array([-g2, -g2], dtype=float)
    b_ibn = np.array([0.0, 1.0], dtype=float)
    return g, c, b_vin, b_vos, b_ibn


def solve_frequency(
    s: complex,
    p: CircuitParams,
    vin: complex = 0.0,
    vos: complex = 0.0,
    ibp: complex = 0.0,
    ibn: complex = 0.0,
) -> dict[str, complex]:
    """Nodal voltages at one complex frequency."""
    A, b_vin, b_vos, b_ibp, b_ibn = nodal_matrices(s, p)
    b = vin * b_vin + vos * b_vos + ibp * b_ibp + ibn * b_ibn
    try:
        x = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        x = np.linalg.lstsq(A, b, rcond=None)[0]
    v1, v2, vo = complex(x[0]), complex(x[1]), complex(x[2])
    return {"V1": v1, "V2": v2, "Vout": vo}


def closed_form_h(s: complex, p: CircuitParams) -> complex:
    """Ideal Hvin(s). Vos and both bias currents are zero."""
    g1, g2, g3 = _conductances(p)
    num = -g1
    den = (
        (s ** 2) * p.C1 * p.C2 * p.R2
        + s * p.C2 * p.R2 * (g1 + g2 + g3)
        + g3
    )
    return num / den


def dc_gain(p: CircuitParams) -> float:
    return -p.R3 / p.R1


def natural_frequency_hz(p: CircuitParams) -> float:
    w0 = 1.0 / np.sqrt(p.R2 * p.R3 * p.C1 * p.C2)
    return float(w0 / (2.0 * np.pi))


def quality_factor(p: CircuitParams) -> float:
    w0 = 2.0 * np.pi * natural_frequency_hz(p)
    gsum = 1.0 / p.R1 + 1.0 / p.R2 + 1.0 / p.R3
    return float(w0 * p.C1 / gsum)


def transfer_at_s(s: complex, p: CircuitParams, source: str = "vin") -> complex:
    src = source.lower()
    vin = 1.0 if src == "vin" else 0.0
    vos = 1.0 if src == "vos" else 0.0
    ibp = 1.0 if src == "ibp" else 0.0
    ibn = 1.0 if src == "ibn" else 0.0
    return solve_frequency(s, p, vin=vin, vos=vos, ibp=ibp, ibn=ibn)["Vout"]


@dataclass
class BodeResult:
    f_hz: np.ndarray
    h: np.ndarray

    @property
    def mag(self) -> np.ndarray:
        return np.abs(self.h)

    @property
    def mag_db(self) -> np.ndarray:
        mag = np.maximum(self.mag, 1e-30)
        return 20.0 * np.log10(mag)

    @property
    def phase_deg(self) -> np.ndarray:
        return np.angle(self.h, deg=True)

    @property
    def phase_unwrapped_deg(self) -> np.ndarray:
        return np.rad2deg(np.unwrap(np.angle(self.h)))


def frequency_grid(
    f_min: float = 10.0,
    f_max: float = 50e6,
    n_points: int = 501,
) -> np.ndarray:
    return np.logspace(np.log10(f_min), np.log10(f_max), int(n_points))


def bode(
    p: CircuitParams,
    source: str = "vin",
    f_hz: ArrayLike | None = None,
) -> BodeResult:
    f = np.asarray(frequency_grid() if f_hz is None else f_hz, dtype=float)
    h = np.empty(f.shape, dtype=complex)
    for i, fi in enumerate(f):
        h[i] = transfer_at_s(1j * 2.0 * np.pi * fi, p, source=source)
    return BodeResult(f_hz=f, h=h)


def superposition_bode(
    p: CircuitParams,
    f_hz: ArrayLike | None = None,
) -> dict[str, BodeResult]:
    f = np.asarray(frequency_grid() if f_hz is None else f_hz, dtype=float)
    return {name: bode(p, source=name, f_hz=f) for name in ("vin", "vos", "ibp", "ibn")}


def ideal_den_coefficients(p: CircuitParams) -> tuple[float, float, float, float]:
    """Return (a2, a1, a0, h0) for H(s) = h0 a0 / (a2 s² + a1 s + a0).

    a0 is ω0², a1 is ω0/Q, a2 is 1, and h0 is the DC gain −R3/R1.
    """
    w0 = 2.0 * np.pi * natural_frequency_hz(p)
    q = quality_factor(p)
    h0 = dc_gain(p)
    return 1.0, w0 / q, w0 * w0, h0


def latex_transfer_ideal(p: CircuitParams) -> str:
    _, a1, a0, h0 = ideal_den_coefficients(p)
    return (
        r"H(s)=\frac{"
        + f"{h0 * a0:.6e}"
        + r"}{s^{2} + "
        + f"{a1:.6e}"
        + r"\,s + "
        + f"{a0:.6e}"
        + r"}"
    )


def latex_superposition() -> str:
    return (
        r"V_{\mathrm{out}}(s)="
        r"H_{\mathrm{vin}}(s)\,V_{\mathrm{in}}(s)"
        r"+H_{V_{OS}}(s)\,V_{OS}"
        r"+H_{I_{B+}}(s)\,I_{B+}"
        r"+H_{I_{B-}}(s)\,I_{B-}"
    )


def find_fc_3db(p: CircuitParams) -> float:
    """Frequency where |Hvin| is 1/√2 of the DC gain."""
    from scipy.optimize import brentq

    dc = abs(dc_gain(p))
    target = dc / np.sqrt(2.0)

    def err(freq: float) -> float:
        h = transfer_at_s(1j * 2.0 * np.pi * freq, p, source="vin")
        return abs(h) - target

    f0 = natural_frequency_hz(p)
    lo, hi = f0 / 50.0, f0 * 50.0
    if err(lo) < 0 or err(hi) > 0:
        return float("nan")
    return float(brentq(err, lo, hi))


def passband_gain(p: CircuitParams, f_hz: float = 100.0) -> complex:
    return transfer_at_s(1j * 2 * np.pi * f_hz, p, source="vin")


def gain_at(p: CircuitParams, f_hz: float, source: str = "vin") -> complex:
    return transfer_at_s(1j * 2 * np.pi * f_hz, p, source=source)


def dc_vout(
    p: CircuitParams,
    vin: float | None = None,
    vos: float | None = None,
    ibp: float | None = None,
    ibn: float | None = None,
) -> float:
    vin_v = p.op.v_in_bias if vin is None else vin
    vos_v = p.opamp.vos_nom if vos is None else vos
    ibp_v = p.opamp.ib_p_nom if ibp is None else ibp
    ibn_v = p.opamp.ib_n_nom if ibn is None else ibn
    res = solve_frequency(0.0, p, vin=vin_v, vos=vos_v, ibp=ibp_v, ibn=ibn_v)
    return float(res["Vout"].real)


def dc_error_budget(
    p: CircuitParams,
    vin: float | None = None,
    vos: float = 0.0,
    ibp: float = 0.0,
    ibn: float = 0.0,
) -> dict[str, float]:
    """Split DC Vout into the ideal passive response and each non-ideal."""
    vin_v = p.op.v_in_bias if vin is None else vin
    ideal = dc_vout(p, vin=vin_v, vos=0.0, ibp=0.0, ibn=0.0)
    d_vos = dc_vout(p, vin=0.0, vos=vos, ibp=0.0, ibn=0.0)
    d_ibp = dc_vout(p, vin=0.0, vos=0.0, ibp=ibp, ibn=0.0)
    d_ibn = dc_vout(p, vin=0.0, vos=0.0, ibp=0.0, ibn=ibn)
    total = dc_vout(p, vin=vin_v, vos=vos, ibp=ibp, ibn=ibn)
    return {
        "ideal": ideal,
        "due_vos": d_vos,
        "due_ibp": d_ibp,
        "due_ibn": d_ibn,
        "total": total,
        "error": total - ideal,
    }


def summary_metrics(p: CircuitParams, f_design: float | None = None) -> dict[str, float]:
    fd = p.op.f_design_hz if f_design is None else f_design
    fp = p.op.f_passband_hz
    fc = find_fc_3db(p)
    h_pb = passband_gain(p, 100.0)
    h_pass = gain_at(p, fp, "vin")
    h_des = gain_at(p, fd, "vin")
    return {
        "f0_hz": natural_frequency_hz(p),
        "q": quality_factor(p),
        "fc_hz": fc,
        "dc_gain": dc_gain(p),
        "passband_gain": float(np.abs(h_pb)),
        "passband_gain_db": float(20 * np.log10(max(abs(h_pb), 1e-30))),
        "gain_at_passband": float(np.abs(h_pass)),
        "phase_at_passband_deg": float(np.angle(h_pass, deg=True)),
        "gain_at_fdesign": float(np.abs(h_des)),
        "gain_at_fdesign_db": float(20 * np.log10(max(abs(h_des), 1e-30))),
        "phase_at_fdesign_deg": float(np.angle(h_des, deg=True)),
        "dc_vout_bias": dc_vout(p),
    }


def format_metrics_table(m: dict[str, float]) -> list[tuple[str, str]]:
    return [
        ("f0", format_eng(m["f0_hz"], "Hz")),
        ("Q", f"{m['q']:.4f}"),
        ("f_c (−3 dB)", format_eng(m["fc_hz"], "Hz")),
        ("DC gain", f"{m['dc_gain']:.6f}"),
        ("|H| at 100 Hz", f"{m['passband_gain']:.6f}"),
        ("|H| at passband tone", f"{m['gain_at_passband']:.6f}"),
        ("phase at passband tone", f"{m['phase_at_passband_deg']:.2f}°"),
        ("|H| at f_design", f"{m['gain_at_fdesign']:.6f}"),
        ("phase at f_design", f"{m['phase_at_fdesign_deg']:.2f}°"),
        ("DC Vout at bias", f"{m['dc_vout_bias']:.6e} V"),
    ]


def assert_closed_form(p: CircuitParams | None = None, tol: float = 1e-9) -> None:
    """Raise if the nodal solver disagrees with the hand expansion."""
    if p is None:
        p = CircuitParams()
    h_dc = transfer_at_s(0.0, p, "vin")
    if abs(h_dc - dc_gain(p)) > tol:
        raise AssertionError(f"DC gain {h_dc} != {dc_gain(p)}")
    samples = [100.0, 1e3, 100e3, 250e3, 500e3, p.op.f_design_hz, 2e6]
    for f in samples:
        s = 1j * 2.0 * np.pi * f
        h_n = transfer_at_s(s, p, "vin")
        h_c = closed_form_h(s, p)
        scale = max(1.0, abs(h_c))
        if abs(h_n - h_c) / scale > tol:
            raise AssertionError(f"nodal/closed-form mismatch at {f} Hz: {h_n} vs {h_c}")
        g, c, b_vin, _, _ = state_matrices(p)
        x = np.linalg.solve(g + s * c, b_vin)
        if abs(complex(x[1]) - h_c) / scale > tol:
            raise AssertionError(f"state/closed-form mismatch at {f} Hz")
    # DC non-ideals, R1 = R3.
    vos = 200e-6
    ibn = 10e-12
    v_vos = dc_vout(p, vin=0.0, vos=vos)
    expect_vos = -(1.0 + p.R3 / p.R1) * vos
    if abs(v_vos - expect_vos) > 1e-12:
        raise AssertionError(f"Vos DC {v_vos} != {expect_vos}")
    v_ibn = dc_vout(p, vin=0.0, ibn=ibn)
    expect_ibn = ibn * (p.R2 + p.R3 + p.R2 * p.R3 / p.R1)
    if abs(v_ibn - expect_ibn) > 1e-15:
        raise AssertionError(f"Ibn DC {v_ibn} != {expect_ibn}")
    if abs(dc_vout(p, vin=0.0, ibp=10e-12)) > 1e-18:
        raise AssertionError("Ibp should not move Vout when + is grounded")
    if abs(transfer_at_s(1j * 2 * np.pi * 1000.0, p, "ibp")) > 1e-9:
        raise AssertionError("H_ibp is not zero")
