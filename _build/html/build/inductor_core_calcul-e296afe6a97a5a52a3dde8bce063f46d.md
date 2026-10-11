# Inductor Core Requirements and Calculations

Created with Grok Build

This is the wxMaxima 15.08.2 worksheet linked from the [50 V to 12 V 5 A buck](buck_50V_to_12V_5A.md). The switching frequency is set to 250 kHz, so the switching period is 4.0 µs. The sheet keeps units on the quantities and prints each result in engineering units. The numbers below are those printed results.

## 1. Inductor core data and requirements

### Output voltage and current

The output is 12 V. The maximum nominal load current is 5 A, and the sheet sets the nominal operating current to that worst-case load until a better figure is available. The minimum nominal load is 0.1 A.

### Short-circuit current

The short-circuit peak is 50% above the 5 A load, which covers the ripple and a margin above it.

$$
I_{sc,peak} = 1.50 \times 5\,\mathrm{A} = 7.5\,\mathrm{A}
$$

### Ripple current, first estimate

The peak-to-peak ripple is guessed at 35% of the 5 A load, and the exact ripple is calculated later.

$$
I_{ripple,pp} = 0.35 \times 5\,\mathrm{A} = 1.75\,\mathrm{A}
$$

Half of that ripple is 0.875 A.

### Input voltage

The sheet uses 56 V maximum, 50 V nominal, and 46 V minimum.

### Duty-ratio ceiling

The control loop is taken to allow a maximum duty ratio of 1, so continuous conduction is acceptable. The operating duty ratios computed in section 2 are smaller than this ceiling, and the sheet stores $V_o / V_{i,min}$ back into the same `D_max` symbol.

### Output power and copper-loss allowance

At 12 V and 5 A the output power is 60 W. The regulation factor $\alpha$ is the copper loss as a fraction of that power, set to 0.01. The inductor loss allowance is then 0.6 W.

### Flux density

The nominal maximum flux density is 0.25 T. During the short circuit the ripple rides on top of that. With the guessed 1.75 A ripple and the 7.5 A short-circuit peak, the sheet prints

$$
\Delta B_{sc,pp} = 0.05833\,\mathrm{T}, \quad \Delta B_{sc,pk} = 0.02917\,\mathrm{T}
$$

$$
B_{sc,pk} = 0.2792\,\mathrm{T}
$$

### Voltage drops in the load-current path

The upper switch is given $R_{DS(on)} = 0.03\,\Omega$, so at 5 A it drops 0.15 V. Two overvoltage-protection switches use the same $R_{DS(on)}$ and drop 0.15 V each. Two sense resistors of 0.01 Ω drop 0.05 V each. The sheet adds the two protection switches and both sense resistors:

$$
V_{drop} = 0.15 + 0.15 + 2 \times 0.05 = 0.4\,\mathrm{V}
$$

## 2. Operating calculations

### Load resistance

At the 5 A load the resistance is 2.4 Ω. At the 0.1 A minimum it is 120 Ω.

### Duty ratios

The steady-state duties are $V_o / V_i$.

$$
D_{min} = \frac{12}{56} = \frac{3}{14} = 0.2143
$$

$$
D_{nom} = \frac{12}{50} = \frac{6}{25} = 0.24
$$

$$
D \text{ at } 46\,\mathrm{V} = \frac{12}{46} = \frac{6}{23} = 0.2609
$$

### Minimum inductance

The application-note form, using the 0.4 V drop and the 4.0 µs period, prints 194.9 µH:

$$
L_{min} = \frac{(V_o + V_{drop})(1 - D_{min}) T_s}{2 I_{o,min}}
$$

The textbook form, using the 120 Ω light-load resistance, prints 188.6 µH:

$$
L_{min} = \frac{(1 - D_{min}) R_{load,min}}{2 f_s}
$$

Continuous conduction at the 0.1 A minimum would need an inductor of that size that can also carry the full load current. The sheet says an inductor like that is not readily available. Page 12 of the LTC3891 datasheet says the controller allows the inductor current to go discontinuous and uses high-efficiency Burst Mode, so the inductor can be chosen for the desired ripple, with the peak flux kept below saturation.

The page 16 estimate, aimed at 30% of the 7.5 A short-circuit peak and the 46 V input, prints 15.77 µH. A 20% margin for tolerance brings that to 18.92 µH. The value selected in the sheet is 22 µH.

## 3. Nominal operating conditions

With the 22 µH inductor, the textbook ripple at nominal duty is 1.658 A peak to peak, and half of that is 0.829 A. The application-note form, using the 56 V input and the minimum duty, prints 1.714 A peak to peak, and half of that is 0.857 A.

The peak current uses that second ripple:

$$
I_{peak,nom} = 5\,\mathrm{A} + \frac{1.714\,\mathrm{A}}{2} = 5.857\,\mathrm{A}
$$

## 4. Short-circuit operating conditions

Page 21 of the LTC3891 datasheet gives a minimum on time of 95 ns. Divided by the 4.0 µs period, the short-circuit duty is 0.02375. The ripple at 56 V and 22 µH is then 0.236 A peak to peak.

The earlier ripple guess was 1.75 A. The sheet's note is that the guess is larger than this calculated short-circuit ripple, so the margin to saturation is enough and no adjustment is needed.

## 5. Core geometry

The energy stored at the nominal peak is

$$
E = \frac{1}{2} L I_{peak,nom}^{2} = 377.4\,\mu\mathrm{J}
$$

The electrical condition $K_e$ for ferrite at the nominal flux prints $5.4375 \times 10^{-5}$:

$$
K_e = 0.145 \, P_o \, B_{max}^{2} \times 10^{-4}
$$

The core geometry $K_g$, which the section heading gives in cm⁵, is $E^{2} / (K_e \alpha)$. The sheet prints 0.2619 for that ratio.

## 6. Winding loss

The last cell in the worksheet assigns the inductor DCR:

$$
L_{DCR} = 0.026\,\Omega
$$

The section has no further calculation after that assignment.
