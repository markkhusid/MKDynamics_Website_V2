# OPA365 Figure 8-5 — Multiple-Feedback 500 kHz Low-Pass Filter

Created with Grok Build

## Introduction

These notebooks analyze the filter published as **Figure 8-5** in the Texas Instruments OPAx365 datasheet (literature number **SBOS365G**): a second-order Butterworth, 500 kHz, multiple-feedback low-pass filter.

The published values are R1 = 549 Ω, R2 = 1.24 kΩ, R3 = 549 Ω, C1 = 1 nF, and C2 = 150 pF. DC gain is −1. The sketch below is an original drawing of those values. The datasheet PDF and the TI SPICE macromodel are not included here. Datasheet: [OPAx365 (SBOS365)](https://www.ti.com/lit/gpn/OPA365).

The ±0.1 % resistor tolerance, ±1 % capacitor tolerance, 0805 resistor rating, and 50 V capacitor rating are assumptions of this study. They are not printed on Figure 8-5. The study uses ±2.5 V supplies so the inverted output is not clipped. The passband transient is a 250 kHz sine, 1 V peak, with no offset.

Notebooks 2 through 6 compare that transient with ngspice and LTspice. Notebook 7 adds the DC sensitivity of the output voltage. Notebook 8 charts the applied voltage and power against the rating and the derating limit.

The Python package that the notebooks import is `mfb_design/` in this folder. Netlists and the LTspice sheets are in the public repository [OPA365_Fig85_MFB](https://github.com/markkhusid/OPA365_Fig85_MFB).

```{figure} images/fig85_schematic.png
:class: clickable-figure

Original sketch of the Figure 8-5 filter, labeled with the datasheet values.
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
