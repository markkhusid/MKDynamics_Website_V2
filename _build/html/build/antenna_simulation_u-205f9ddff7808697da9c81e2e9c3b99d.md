# Antenna Simulation using 4NEC2

Created with Grok Build

This page follows one 4NEC2 session: a dipole drawn for the 20 meter band and run at 14.300 MHz. The program is 4NEC2 5.8.16, and the file is `20dip.nec`. [4NEC2](https://www.qsl.net/4nec2/) is Arie Voors' front end for NEC2.

## Geometry symbols

The model started from an 80 meter dipole example. The length was replaced with the amateur estimate \(468/f\), with \(f\) in MHz and the result in feet, then converted to meters. At 14.300 MHz that length is 9.975 m. It is the estimate for the whole antenna.

The symbols window stores `len = 9.9752727272` and `hgh = 10`. The comment on that line is "Wire length and height in meters." Scaling is set to meters with a factor of 1.0. The frequency symbol is `freq = 14.300`. The geometry tab is not in this screenshot, so this page does not say which wire card uses `len`.

```{figure} images/20_meter_dipole_data_entry_and_main.jpeg
:width: 900
:align: center
:class: clickable-figure

Symbols for `20dip.nec`, and the 4NEC2 main window after the 14.300 MHz run
```

## Feed point

The main window is one frequency step. The free-space wavelength is 20.97 m. The source is a voltage source, `EX 0`, on tag 2, segment 1. The conductors are copper (`LD 5` on every tag). The pattern uses 39 segments and 65,341 pattern lines. Theta runs from −90° to 90° in 1° steps, and phi runs from 0° to 360° in 1° steps. The calculation took 1.650 s.

The feed result on that window is:

- Voltage: 707 + j0 V
- Current: 141 − j76.5 mA
- Impedance: 3871 + j2095 ohm
- Parallel form: 5004 // j9247
- SWR on 50 ohm: 100
- Efficiency: 99.15%
- Radiation efficiency: 77.76%
- RDF: 10.1 dB
- Input power: 100 W
- Structure loss: 848 mW
- Network loss: 0
- Radiated power: 99.15 W
- Series compensation: 5.313 pF
- Parallel compensation: 1.204 pF

A center-fed half-wave dipole is near 70 ohm. Half a wavelength at 14.300 MHz is about 10.5 m, and the 468/f estimate above is 9.975 m for the whole antenna. The feed impedance on this run is 3871 + j2095 ohm, and the 50 ohm SWR reads 100. This saved model is not a matched half-wave dipole.

## Radiation pattern

The same run is shown three ways. The color scale is total gain in dBic. It runs from −111 to 9.04, with a tick at 7.74. The lobes lie broadside to the wire.

```{figure} images/20_meter_dipole_geometry_and_pattern.jpeg
:width: 900
:align: center
:class: clickable-figure

Total gain at 14.3 MHz, with the wire. This view is theta 36 and phi 36, and the axis scale is 5 m
```

The polar plot is total gain in dBic at 14.3 MHz. The red trace is the horizontal plane and the blue trace is the vertical plane. The plot is taken at theta 60 and phi 90, and the drawn range is −11 to 9.04 dBic. The figure marks the maximum at theta 60. In NEC, theta is measured from the zenith, so theta 60 is 30 degrees above the horizon.

```{figure} images/20_meter_dipole_pattern_polar_plot.jpeg
:width: 900
:align: center
:class: clickable-figure

Horizontal plane in red and vertical plane in blue. The maximum is marked at theta 60
```

The last view draws the same pattern in color with the wire through it. The Ham Radio section card is this picture.

```{figure} images/20_meter_dipole_pattern_multicolor.jpeg
:width: 900
:align: center
:class: clickable-figure

The same total-gain pattern, colored on the dBic scale, with the dipole wire
```
