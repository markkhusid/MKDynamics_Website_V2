# 50V to 12V 5A Buck Converter

Created with Grok Build

This buck converter takes a 50 VDC input down to 12 VDC at a maximum load of 5 A. It is meant for household use and can also run outdoors.

## Requirements

* Voltage input
    * 50 V nominal
    * 40 V maximum
    * 60 V minimum
* Input current available
    * 10 A maximum
* Voltage output
    * Nominal output voltage: 12 V
    * Allowable ripple voltage: 50 mV peak to peak
* Current output
    * Minimum load: 0 A
    * Maximum load: 5 A
* Environment
    * Interfaces to household wiring
    * Outdoor use
    * Exposed to lightning
    * Must survive a reversed input
    * Must survive overvoltage and undervoltage transients
    * Must provide 20 ms of output holdup at maximum load
* Efficiency
    * Greater than 90%

## Design analysis

The design screens are from LTpowerCAD II, in the project file for this 50 V to 12 V, 5 A converter. The power-stage screen is dated March 29, 2015.

```{figure} images/LTC3891_efficiency.jpeg
:width: 900
:align: center
:class: clickable-figure

Efficiency simulation
```

The loss-estimate screen plots efficiency and power loss against load current, and it breaks the full-load loss into the MOSFET, inductor, sense-resistor, and input-capacitor terms. The inductor entry on this screen is 22 µH.

```{figure} images/LTC3891_loop_compensation.jpeg
:width: 900
:align: center
:class: clickable-figure

Transient response simulation
```

The loop screen shows the gain and phase of the 11.99 V rail and a load step between 0 A and 5 A. The compensation network on the screen is 49.9 kΩ, 100 pF, and 22 pF, which is the same network drawn on the LTspice schematic below.

```{figure} images/LTC3891_power_stage.jpeg
:width: 900
:align: center
:class: clickable-figure

Power stage design
```

The power-stage screen is the LTC3891 with a 22 µH inductor. LTpowerCAD lists that inductor as a Coilcraft SER2918H-22 and the two MOSFETs as Infineon BSZ150N10L.

## Schematic

```{figure} images/LTC3891_schematic.jpeg
:width: 900
:align: center
:class: clickable-figure

LTspice schematic, 50 V to 12 V at 5 A
```

The LTspice schematic is titled "50V to 12V 5A Buck Converter Design / Mark Khusid 2015". The controller is the LTC3891. The power stage uses two IRL530NS MOSFETs, a 22 µH inductor, a 3.5 mΩ sense resistor, and a 2.4 Ω load. Three 470 µF capacitors and a 0.1 µF capacitor sit on the output. The feedback divider is 60.4 kΩ over 4.32 kΩ. The frequency-setting resistor is 37.4 kΩ. The ITH pin uses 49.9 kΩ, 100 pF, and 22 pF. The run is `.tran 0 15m 0 1m startup`, from a 50 V pulse source.

## Discussion

The power supply control IC is the Linear Technology LTC3891.

## Simulation

```{figure} images/LTC3891_sim.jpeg
:width: 900
:align: center
:class: clickable-figure

50V to 12V 5A buck simulation
```

The capture is a few switching cycles from the LTspice run. The traces are the top and bottom gate currents, a pulsed voltage, the inductor current stepping upward through the window, and the switch node.

## Design calculations

The inductor is sized in a wxMaxima 15.08.2 worksheet, "Inductor Core Requirements and Calculations". The sheet sets the switching frequency to 250 kHz and selects 22 µH.

[Inductor core requirements and calculations](inductor_core_calculations.md)

```{figure} images/DCDCconverter_50Vto12V_calcs.jpeg
:width: 700
:align: center
:class: clickable-figure

Worksheet thumbnail for the inductor calculations
```
