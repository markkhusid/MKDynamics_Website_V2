# OPA365 Figure 8-6 — Three-Pole Sallen–Key Low-Pass Filter

## Introduction

These notebooks analyze the filter published as **Figure 8-6** in the Texas Instruments OPAx365 datasheet (literature number **SBOS365G**): a three-pole, 20 kHz, unity-gain Sallen–Key low-pass filter.

The published values are R1 = 1.8 kΩ, R2 = 19.5 kΩ, R3 = 150 kΩ, C1 = 3.3 nF, C2 = 47 pF, and C3 = 220 pF. The schematic below is redrawn from those values. The datasheet PDF and the TI SPICE macromodel are not included here. Datasheet: [OPAx365 (SBOS365)](https://www.ti.com/lit/gpn/OPA365).

The ±0.1 % resistor tolerance, ±1 % capacitor tolerance, 0805 resistor rating, and 50 V capacitor rating are assumptions of this study. They are not printed on Figure 8-6.

The Python package that the notebooks import is `opamp_design/` in this folder. Netlists, simulation logs, and PDF exports of the same study are in the public repository [OPA365_Fig86_Sallen_Key](https://github.com/markkhusid/OPA365_Fig86_Sallen_Key).

```{figure} images/fig86_schematic.png
:class: clickable-figure

Redrawn schematic of the Figure 8-6 filter, labeled with the datasheet values.
```

## Notebooks

::::{grid} 2 2 2 2

:::{grid-item-card}
:link: 01_analytical_transfer

01 — Analytical Transfer Function
^^^
```{image} images/01_bode.png
:height: 200
```
:::

:::{grid-item-card}
:link: 02_ngspice_vs_analytical

02 — ngspice vs Analytical
^^^
```{image} images/02_ngspice.png
:height: 200
```
:::

:::{grid-item-card}
:link: 03_ltspice_vs_analytical

03 — LTspice vs Analytical
^^^
```{image} images/03_ltspice.png
:height: 200
```
:::

:::{grid-item-card}
:link: 04_worst_case

04 — Worst Case
^^^
```{image} images/04_worst_case.png
:height: 200
```
:::

:::{grid-item-card}
:link: 05_monte_carlo

05 — Monte Carlo
^^^
```{image} images/05_monte_carlo.png
:height: 200
```
:::

:::{grid-item-card}
:link: 06_temperature_sweep

06 — Temperature Sweep
^^^
```{image} images/06_temperature.png
:height: 200
```
:::

:::{grid-item-card}
:link: 07_sensitivity

07 — Sensitivity
^^^
```{image} images/07_sensitivity.png
:height: 200
```
:::

:::{grid-item-card}
:link: 08_derating

08 — Derating
^^^
```{image} images/08_derating.png
:height: 200
```
:::

::::
