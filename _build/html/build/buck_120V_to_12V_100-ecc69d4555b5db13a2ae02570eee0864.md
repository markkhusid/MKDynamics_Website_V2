# 120V to 12V 100mA Buck Converter

Created with Grok Build

This buck converter takes a 120 VDC input down to 12 VDC. The load requirement written for the supply is 20 mA maximum. The page heading follows the original writeup, which names the converter for the 100 mA rating of the LTC3639. The supply is meant for household use and can also run outdoors.

## Requirements

* Voltage input
    * 120 V nominal
    * 130 V maximum
    * 110 V minimum
* Current available
    * 10 A maximum
* Voltage output
    * Nominal output voltage: 12 V
    * Allowable ripple voltage: 50 mV peak to peak
* Current output
    * Minimum load: 0 A
    * Maximum load: 20 mA
* Environment
    * Interfaces to household wiring
    * Outdoor use
    * Exposed to lightning
    * Must survive a reversed input
    * Must survive overvoltage and undervoltage transients
    * Must provide 20 ms of output holdup at maximum load
* Efficiency
    * Greater than 90%

## Control IC

The controller is the Linear Technology LTC3639, a high-efficiency, 150 V, 100 mA synchronous step-down regulator. The high-side and low-side MOSFETs are inside the IC, and so is the compensation. The feedback divider sets the voltage the IC regulates. At light load the LTC3639 enters Burst Mode, Linear Technology's light-load mode, and skips as many cycles as it needs. It then fires a burst of pulses to hold the output at the set voltage.

## Schematic

```{figure} images/LTC3639.jpeg
:width: 900
:align: center
:class: clickable-figure

LTspice schematic of the 120 V to 12 V buck
```

The LTspice drawing is the 120 V to 12 V converter. The load resistor is 600 Ω and is labeled for 20 mA. The power inductor is 500 µH, the input filter inductor is 100 µH, the input capacitor is 1 µF, and the soft-start capacitor is 680 nF. Those are the values chosen in the [design calculations](design_calculations.ipynb).

## Simulation

```{figure} images/LTC3639_sim2.jpeg
:width: 900
:align: center
:class: clickable-figure

120V to 12V 100mA buck simulation
```

The output sits near 12 V and the load current sits near 20 mA. The inductor current runs in bursts, and the switch node pulses up toward the input during each burst. That is the Burst Mode operation described above, at the 20 mA load.

## Design calculations

The passives are worked out in a notebook that evaluates the wxMaxima 13.04.2 worksheet. The input used in that sheet is the 130 V maximum, which is why the original file is named for 130 V. The sheet covers the peak-current resistor, the input and output capacitors, the input filter, the feedback divider, the undervoltage and overvoltage lockout string, and the soft-start capacitor.

[Design calculations](design_calculations.ipynb)

```{figure} images/DCDCconverter_130Vto12V_calcs.jpeg
:width: 700
:align: center
:class: clickable-figure

Worksheet thumbnail for the 120 V buck calculations
```
