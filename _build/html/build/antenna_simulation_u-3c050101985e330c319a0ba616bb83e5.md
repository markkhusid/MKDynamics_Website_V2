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

## Matched model

The matched antenna keeps the 14.300 MHz design frequency and the 10 m support, and it is solved with NEC-2. The deck is `20m_inverted_v.nec`.

A straight AWG 14 copper dipole at 10 m, lengthened to 10.25 m, resonates at 72.9 + j0 ohm. The 50 ohm SWR of that flat wire is 1.46. Over average ground the resonant resistance of a straight dipole stays near 60 ohm or higher at heights from 3 m to 15 m, so trimming the length alone leaves the SWR above 1.2.

Dropping the ends into an inverted V lowers the feed resistance to 50 ohm. The apex is at 10.00 m. Each sloping leg is 5.135 m. The included angle at the apex is 93.0°. The tips are 6.47 m above the ground and 7.58 m apart. The source sits on a 12.8 cm horizontal segment at the apex. The wire is AWG 14 copper, radius 0.814 mm, conductivity 5.8001×10⁷ S/m. The ground is a Sommerfeld average ground, relative permittivity 13 and conductivity 0.005 S/m. Each leg has 40 segments.

At 14.300 MHz the feed is 50.0 + j0.0 ohm and the 50 ohm SWR is 1.00. Wire efficiency is 97.9%. The maximum gain is 5.92 dBi at theta 57°, broadside to the wire, which is 33° above the horizon. Halving the segment length moves the feed to 49.7 + j0.2 ohm and the SWR to 1.01.

| MHz | R (ohm) | X (ohm) | SWR |
|---:|---:|---:|---:|
| 14.000 | 47.4 | −31.4 | 1.89 |
| 14.150 | 48.7 | −15.7 | 1.38 |
| 14.300 | 50.0 | 0.0 | 1.00 |
| 14.350 | 50.5 | +5.3 | 1.11 |

The SWR stays under 1.5 from 14.11 MHz to 14.50 MHz, and under 2 from 13.97 MHz to 14.65 MHz.

```{figure} images/20m_inverted_v_match.png
:width: 900
:align: center
:class: clickable-figure

The matched inverted V, and its 50 ohm SWR around 14.300 MHz
```

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
