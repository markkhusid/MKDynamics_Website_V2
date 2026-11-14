# LT3010-5 — 5 V Supply with Shutdown

## Introduction

These notebooks analyze the typical application on page 1 of the LT3010/LT3010-5 datasheet (Rev. J), figure TA01, "5V Supply with Shutdown".

| Item | Value on the figure |
|------|---------------------|
| Part | LT3010-5, SENSE tied to OUT |
| VIN | 5.4 V to 80 V |
| VOUT | 5 V |
| Load | 50 mA |
| Capacitors | 1 µF input, 1 µF output |

Single-point calculations use 12 V, which is inside the printed input range. The page-3 electrical table supplies the min/typ/max limits. The schematic below is redrawn from those published values. The datasheet PDF and the vendor SPICE macromodel are not included.

The Python package the notebooks import is `p5v_design/` in this folder. The same study is in the public repository [LT3010_5V_Supply](https://github.com/markkhusid/LT3010_5V_Supply).

```{figure} images/schematic.png
:class: clickable-figure

Redrawn schematic of the LT3010-5 datasheet example.
```

## Notebooks

::::{grid} 2 2 2 2

:::{grid-item-card}
:link: 01_analytical_setpoint

01 — Analytical Setpoint
^^^
```{image} images/01_vout.png
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
:link: 03_worst_case

03 — Worst Case
^^^
```{image} images/03_worst_case.png
:height: 200
```
:::

:::{grid-item-card}
:link: 04_monte_carlo

04 — Monte Carlo
^^^
```{image} images/04_monte_carlo.png
:height: 200
```
:::

:::{grid-item-card}
:link: 05_ltspice_nominal_mc_wc

05 — Analytical and ngspice Corners
^^^
```{image} images/05_engines.png
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
:link: 08_derating_thermal

08 — Derating and Thermal
^^^
```{image} images/08_derating.png
:height: 200
```
:::

:::{grid-item-card}
:link: 09_supply_budget

09 — Input Current and Efficiency
^^^
```{image} images/09_efficiency.png
:height: 200
```
:::

:::{grid-item-card}
:link: 10_time_domain

10 — Time Domain
^^^
```{image} images/10_time.png
:height: 200
```
:::

::::
