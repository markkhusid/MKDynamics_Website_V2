"""Original sketch of the Figure 8-5 multiple-feedback filter.

This drawing is not a copy of the datasheet figure. Notebooks use it until
an LTspice export replaces the PNG.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

from .params import CircuitParams, format_eng


def draw_fig85_schematic(
    path: str | Path | None = None,
    p: CircuitParams | None = None,
    figsize: tuple[float, float] = (11.2, 5.4),
    title: str | None = None,
    vin_label: str | None = None,
) -> Path | None:
    if p is None:
        p = CircuitParams()
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 15.2)
    ax.set_ylim(0, 7.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        title or "Original sketch — OPA365 Figure 8-5 multiple-feedback low-pass",
        fontsize=12,
        pad=8,
    )

    def wire(*pts):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color="k", lw=1.2, solid_capstyle="round")

    def label(x, y, text, **kw):
        kw.setdefault("ha", "center")
        kw.setdefault("va", "center")
        kw.setdefault("fontsize", 8)
        ax.text(x, y, text, **kw)

    def resistor(x, y, w, h):
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                fill=False,
                lw=1.2,
            )
        )

    def capacitor_v(x, y):
        ax.plot([x - 0.28, x + 0.28], [y + 0.08, y + 0.08], "k", lw=1.3)
        ax.plot([x - 0.28, x + 0.28], [y - 0.08, y - 0.08], "k", lw=1.3)

    def capacitor_h(x, y):
        ax.plot([x - 0.08, x - 0.08], [y - 0.28, y + 0.28], "k", lw=1.3)
        ax.plot([x + 0.08, x + 0.08], [y - 0.28, y + 0.28], "k", lw=1.3)

    def ground(x, y):
        ax.plot([x - 0.28, x + 0.28], [y, y], "k", lw=1.2)
        ax.plot([x - 0.18, x + 0.18], [y - 0.1, y - 0.1], "k", lw=1.2)
        ax.plot([x - 0.08, x + 0.08], [y - 0.2, y - 0.2], "k", lw=1.2)

    y = 3.3
    wire((0.7, y), (1.7, y))
    resistor(1.7, y - 0.22, 1.15, 0.44)
    wire((2.85, y), (4.15, y))
    resistor(4.15, y - 0.22, 1.15, 0.44)
    wire((5.3, y), (6.55, y))

    label(2.28, y + 0.55, f"$R_1$ = {format_eng(p.R1, 'Ω')}")
    label(4.72, y + 0.55, f"$R_2$ = {format_eng(p.R2, 'Ω')}")
    label(
        0.55,
        y + 0.7,
        vin_label or "$V_{\\mathrm{IN}}$\n0 V bias",
        fontsize=8,
    )
    label(3.5, y - 0.38, "n1", fontsize=7, color="0.25")

    # C1 to ground
    wire((3.5, y), (3.5, 2.15))
    capacitor_v(3.5, 2.0)
    wire((3.5, 1.85), (3.5, 1.35))
    ground(3.5, 1.35)
    label(4.15, 2.0, f"$C_1$ = {format_eng(p.C1, 'F')}")

    # R3 feedback along the top
    wire((3.5, y), (3.5, 5.35))
    resistor(3.28, 5.35, 0.44, 0.95)
    wire((3.5, 6.3), (3.5, 6.55), (11.15, 6.55), (11.15, y))
    label(2.55, 5.8, f"$R_3$ = {format_eng(p.R3, 'Ω')}")

    # C2 from inverting node up to the feedback rail
    wire((6.15, y), (6.15, 5.55))
    capacitor_v(6.15, 5.7)
    wire((6.15, 5.85), (6.15, 6.55))
    label(6.85, 5.7, f"$C_2$ = {format_eng(p.C2, 'F')}")

    # Op-amp
    tri = Polygon(
        [[7.15, y - 0.95], [7.15, y + 0.95], [8.85, y]],
        closed=True,
        fill=False,
        lw=1.3,
    )
    ax.add_patch(tri)
    label(7.55, y + 0.42, "+", fontsize=11)
    label(7.55, y - 0.42, "−", fontsize=11)
    label(8.15, y + 0.15, "OPA365", fontsize=7)
    wire((6.55, y), (7.15, y - 0.45))
    # + pin to ground
    wire((7.15, y + 0.45), (6.55, y + 0.45), (6.55, 1.35))
    ground(6.55, 1.35)
    label(6.15, 2.15, "+ pin", fontsize=7, color="0.25")

    # Output
    wire((8.85, y), (12.6, y))
    label(13.15, y + 0.35, "$V_{\\mathrm{OUT}}$")
    # load
    wire((12.2, y), (12.2, 2.35))
    resistor(11.98, 1.55, 0.44, 0.8)
    wire((12.2, 1.55), (12.2, 1.15))
    ground(12.2, 1.15)
    label(13.05, 1.95, f"$R_L$ = {format_eng(p.op.r_load, 'Ω')}", fontsize=7)

    # Supplies, drawn as labels on the amplifier rather than a second signal path
    label(8.35, y + 1.25, f"$V+$ = {p.op.v_pos:g} V", fontsize=8)
    label(8.35, y - 1.25, f"$V−$ = {p.op.v_neg:g} V", fontsize=8)

    note = (
        "Original sketch of the published Figure 8-5 values. "
        "Not a copy of the datasheet drawing. "
        f"Study supplies are ±{p.op.v_pos:g} V."
    )
    ax.text(0.4, 0.35, note, fontsize=8, color="0.2")

    fig.tight_layout()
    if path is None:
        return None
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
