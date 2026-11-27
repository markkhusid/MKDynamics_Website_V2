# PCB trace current and Joule heating

Created with Grok Build

This page follows the open-source path in Jarrett's note on [thermal simulation of PCBs](https://jrainimo.com/build/2024/11/oss-thermal-simulation-of-pcbs/). The worked example there is static current conduction in the copper, with Joule heating computed from that current. The board dielectric and the air are not in this model. This page does not solve a temperature field.

The tools are [KiCad](https://www.kicad.org/), [Salome](https://www.salome-platform.org/), [Elmer](https://www.elmerfem.org/), and [ParaView](https://www.paraview.org/). KiCad 9 writes the copper. Salome 9.16 meshes it. ElmerSolver 26.2 solves the current problem. ParaView 5.10 draws the fields.

## The copper

The board is a one-net part drawn for this page. The net is `TRACE`.

The outline is a 12 mm by 8 mm rectangle on `Edge.Cuts`. That outline is not in the copper export. Pad A is a 2 mm by 2 mm rectangle on `F.Cu`, centered at (3 mm, 4 mm). A 0.4 mm track on `F.Cu` runs from that pad to a through via at (6 mm, 4 mm). The via drill is 0.3 mm and the via pad is 0.6 mm. A 0.4 mm track on `B.Cu` runs from the via to pad B, a 2 mm by 2 mm rectangle on `B.Cu` centered at (9 mm, 4 mm).

The stackup uses 0.035 mm of copper on each side, which is 1 oz, and a 1.53 mm core. The XAO export keeps the tracks, pads, and vias, fuses them into one solid, and filters on the net `TRACE`. The board body and the component models stay out.

KiCad names the two pad faces `Pad_F_J1_A_TRACE` and `Pad_B_J1_B_TRACE`. Each face has area 4.00 mm², which is $4.00\times 10^{-6}\,\mathrm{m}^2$. In the exported solid those faces span $x$ from 2 mm to 10 mm, $y$ from −5 mm to −3 mm, and $z$ from −0.04 mm to 1.57 mm. The Y axis in the XAO points the other way from the board file, so the pads sit at negative $y$.

## The mesh

`mesh_trace.py` imports the XAO in Salome, names the front pad face `input` and the back pad face `output`, and meshes the solid with Netgen 1D-2D-3D. The hypothesis that produced a volume mesh is a maximum size of 0.2 mm and a minimum size of 0.08 mm. That minimum is thicker than the 0.035 mm foil. Netgen still built the volume mesh, so those are the sizes recorded here. The mesh has 2313 nodes and 6180 tetrahedra. The input group has 692 faces and the output group has 623.

ElmerGrid reads `trace.unv` and scales every coordinate by 0.001, so the mesh Elmer solves is in metres. The output face is then $4.00\times 10^{-6}\,\mathrm{m}^2$.

## Static current

The copper conductivity is $47.00\times 10^{6}\,\mathrm{S/m}$. The input face is held at 12 V. The current is 0.5 A, and it leaves through the output face, so the current density on that face is

$$
J = -\frac{0.5}{4.00\times 10^{-6}} = -1.25\times 10^{5}\,\mathrm{A/m}^2.
$$

The solver is `StatCurrentSolve` / `StatCurrentSolver`, with Joule heating and volume current turned on. The linear solver is BiCGStab with ILU1. The tolerance is $1.0\times 10^{-10}$. The residual reached $3.75\times 10^{-11}$ at iteration 27, and Elmer wrote `case_t0001.vtu`.

The potential on the copper runs from 11.99665 V to 12.00000 V. The drop along this short path is 3.35 mV. The color bar is stretched across that drop.

```{figure} images/potential.png
:width: 900
:align: center
:class: clickable-figure

Electric potential on the copper. The color bar runs from 11.99665 V to 12.00000 V. The input pad is the 12 V end.
```

Joule heating on the nodes runs from about 0 to $3.318\times 10^{7}\,\mathrm{W/m}^3$. It sits in the 0.4 mm tracks. The pads are wide, so they stay at the bottom of the scale. The volume-current magnitude reaches $3.918\times 10^{7}\,\mathrm{A/m}^2$. A 0.5 A current through a 0.4 mm by 0.035 mm section is $3.57\times 10^{7}\,\mathrm{A/m}^2$, which is the same order as that peak.

```{figure} images/joule_heating.png
:width: 900
:align: center
:class: clickable-figure

Joule heating on the copper. The color bar runs from about 0 to $3.318\times 10^{7}\,\mathrm{W/m}^3$.
```

## Files

These files are the scripted path from a board to a current solution. `make_trace_board.py` stands in for a layout drawn by hand. A later board can start as a KiCad schematic and a routed layout, then use the same XAO export. `mesh_trace.py` meshes the copper. `case.sif` is the Elmer case. `render_views.py` draws the two figures. The comments in each file say what that step does.

This case stops at current and Joule heating. It does not solve a temperature. A thermal analysis would be a later Elmer heat case, using this heating as its source, and the geometry for that case has to include the board dielectric. `trace.unv` is the mesh Salome wrote, and `elmer.log` is the solver log.

From this directory, after the KiCad export:

```
salome shell -- python3 mesh_trace.py
ElmerGrid 8 2 trace.unv -scale 1.0e-3 1.0e-3 1.0e-3 -out mesh
ElmerSolver case.sif
```

The Salome line needs the Salome environment. ElmerGrid writes the mesh directory that `case.sif` reads.

## Board script

`make_trace_board.py` draws the one-net board and writes the 0.035 mm copper stackup into the file.

```{literalinclude} make_trace_board.py
:language: python
```

### Board terminal

This is the script, then the XAO export it names.

```{literalinclude} make_trace_board.log
:language: text
```

```{literalinclude} kicad_xao.log
:language: text
```

## Mesh script

`mesh_trace.py` imports the XAO, prints the pad areas, and writes `trace.unv`.

```{literalinclude} mesh_trace.py
:language: python
```

### Mesh terminal

```{literalinclude} mesh_trace.log
:language: text
```

## Elmer case

`case.sif` is the static-current case. The mesh coordinates are metres, and the output current density is $-1.25\times 10^{5}\,\mathrm{A/m}^2$.

```{literalinclude} case.sif
:language: text
```

### Solver terminal

`ElmerGrid` scaled the mesh, then `ElmerSolver` ran `case.sif`.

```{literalinclude} elmer.log
:language: text
```

## ParaView script

`render_views.py` draws the potential and Joule-heating figures. It uses the ParaView build on the host display.

```{literalinclude} render_views.py
:language: python
```

### ParaView terminal

```{literalinclude} render_views.log
:language: text
```
