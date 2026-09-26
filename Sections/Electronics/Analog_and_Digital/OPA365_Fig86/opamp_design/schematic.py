"""Draw an annotated schematic of OPA365 Figure 8-6 for notebooks.

HOW TO ADAPT FOR ANOTHER NETLIST
--------------------------------
Replace ``draw_fig86_schematic`` with a drawing of your topology, or skip
schematic generation entirely and embed a PNG export from LTspice / your CAD.
Notebooks only call this for documentation; nothing in the math depends on it.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

from .params import CircuitParams, format_eng


def draw_fig86_schematic(
    path: str | Path | None = None,
    p: CircuitParams | None = None,
    figsize: tuple[float, float] = (10.5, 4.2),
) -> Path | None:
    """Render a simple annotated schematic; save if path given.

    Labels use values from ``p`` so the figure stays consistent with the
    notebook parameter cell.
    """
    if p is None:
        p = CircuitParams()

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        "OPA365 Fig. 8-6 — Three-Pole 20 kHz Unity-Gain Sallen–Key LPF",
        fontsize=12,
        pad=8,
    )

    def wire(x1, y1, x2, y2, **kw):
        ax.plot([x1, x2], [y1, y2], color="k", lw=1.2, **kw)

    def label(x, y, text, **kw):
        # fontsize may be overridden via kwargs
        kw.setdefault("ha", "center")
        kw.setdefault("va", "center")
        kw.setdefault("fontsize", 8)
        ax.text(x, y, text, **kw)

    # Node y for signal path
    y = 2.4
    # Positions
    x_vin, x_n1, x_n2, x_n3, x_op, x_out = 0.8, 3.0, 5.5, 8.0, 10.2, 12.8

    # Input
    label(x_vin - 0.15, y + 0.35, r"$V_{\mathrm{IN}}$" + f"\n{p.op.v_in_bias:g} V bias")
    wire(x_vin, y, x_n1, y)
    # R1
    ax.add_patch(FancyBboxPatch((1.5, y - 0.18), 1.0, 0.36, boxstyle="round,pad=0.02", fill=False, lw=1.2))
    label(2.0, y, "")
    label(2.0, y + 0.45, f"$R_1$={format_eng(p.R1, 'Ω')}")

    # C1 to gnd
    wire(x_n1, y, x_n1, 1.1)
    ax.plot([x_n1 - 0.25, x_n1 + 0.25], [1.1, 1.1], "k", lw=1.2)
    ax.plot([x_n1 - 0.25, x_n1 + 0.25], [0.95, 0.95], "k", lw=1.2)
    # gnd symbol
    ax.plot([x_n1 - 0.2, x_n1 + 0.2], [0.7, 0.7], "k", lw=1.2)
    ax.plot([x_n1 - 0.12, x_n1 + 0.12], [0.55, 0.55], "k", lw=1.0)
    ax.plot([x_n1 - 0.05, x_n1 + 0.05], [0.42, 0.42], "k", lw=1.0)
    wire(x_n1, 0.95, x_n1, 0.7)
    label(x_n1 + 0.55, 1.05, f"$C_1$={format_eng(p.C1, 'F')}")
    label(x_n1, y + 0.25, r"$n_1$", color="C0")

    # R2
    wire(x_n1, y, x_n2, y)
    ax.add_patch(FancyBboxPatch((3.7, y - 0.18), 1.2, 0.36, boxstyle="round,pad=0.02", fill=False, lw=1.2))
    label(4.3, y + 0.45, f"$R_2$={format_eng(p.R2, 'Ω')}")

    # C3 feedback from n2 to Vout
    wire(x_n2, y, x_n2, 3.6)
    wire(x_n2, 3.6, x_out - 0.3, 3.6)
    wire(x_out - 0.3, 3.6, x_out - 0.3, y)
    # cap symbol on top
    ax.plot([6.3, 6.3], [3.45, 3.75], "k", lw=1.2)
    ax.plot([6.5, 6.5], [3.45, 3.75], "k", lw=1.2)
    label(6.4, 4.05, f"$C_3$={format_eng(p.C3, 'F')} (feedback)")
    label(x_n2, y + 0.25, r"$n_2$", color="C0")

    # R3
    wire(x_n2, y, x_n3, y)
    ax.add_patch(FancyBboxPatch((6.2, y - 0.18), 1.2, 0.36, boxstyle="round,pad=0.02", fill=False, lw=1.2))
    label(6.8, y - 0.45, f"$R_3$={format_eng(p.R3, 'Ω')}")

    # C2 to gnd at n3
    wire(x_n3, y, x_n3, 1.1)
    ax.plot([x_n3 - 0.25, x_n3 + 0.25], [1.1, 1.1], "k", lw=1.2)
    ax.plot([x_n3 - 0.25, x_n3 + 0.25], [0.95, 0.95], "k", lw=1.2)
    wire(x_n3, 0.95, x_n3, 0.7)
    ax.plot([x_n3 - 0.2, x_n3 + 0.2], [0.7, 0.7], "k", lw=1.2)
    ax.plot([x_n3 - 0.12, x_n3 + 0.12], [0.55, 0.55], "k", lw=1.0)
    ax.plot([x_n3 - 0.05, x_n3 + 0.05], [0.42, 0.42], "k", lw=1.0)
    label(x_n3 + 0.55, 1.05, f"$C_2$={format_eng(p.C2, 'F')}")
    label(x_n3, y + 0.25, r"$n_3 = V_{(+)}$", color="C0")

    # Op-amp triangle
    tri_x = [x_op, x_op + 1.6, x_op]
    tri_y = [y + 0.9, y, y - 0.9]
    ax.fill(tri_x, tri_y, facecolor="#e8f0fe", edgecolor="k", lw=1.2)
    label(x_op + 0.55, y + 0.45, "+")
    label(x_op + 0.55, y - 0.45, "−")
    ax.text(x_op + 0.85, y + 0.05, p.opamp.name, ha="center", va="center", fontsize=7)
    # supplies
    wire(x_op + 0.7, y + 0.55, x_op + 0.7, y + 1.35)
    label(x_op + 0.7, y + 1.55, f"+{p.op.v_supply:g} V", fontsize=8)
    wire(x_op + 0.7, y - 0.55, x_op + 0.7, y - 1.2)
    label(x_op + 0.7, y - 1.4, "0 V", fontsize=8)

    wire(x_n3, y, x_op, y + 0.45)  # to +
    # unity feedback from out to -
    wire(x_op + 1.6, y, x_out, y)
    wire(x_out, y, x_out, y - 1.0)
    wire(x_out, y - 1.0, x_op + 0.15, y - 1.0)
    wire(x_op + 0.15, y - 1.0, x_op + 0.15, y - 0.45)
    wire(x_op + 0.15, y - 0.45, x_op, y - 0.45)

    label(x_out + 0.35, y + 0.35, r"$V_{\mathrm{OUT}}$")
    ax.plot(x_out, y, "o", color="k", ms=3)

    # Annotation box
    note = (
        f"R tol ±{p.r_tol.percent:g}%   C tol ±{p.c_tol.percent:g}%\n"
        f"Design target ~{format_eng(p.op.f_design_hz, 'Hz')} LPF\n"
        f"Sources: Vin, Vos, Ib+, Ib− (superposition)"
    )
    ax.text(
        0.3,
        4.5,
        note,
        ha="left",
        va="top",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    fig.tight_layout()
    if path is not None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return path
    return None
