# OpenFOAM propulsor demo

Created with Grok Build

The [openfoam-propulsor-demo](https://github.com/markkhusid/openfoam-propulsor-demo) repository holds a coarse-mesh transient run of the OpenFOAM tutorial propeller, and a pipeline that starts from a watertight STL. OpenFOAM is GPL. The propeller geometry is from the OpenFOAM Foundation. The pipeline, this demo run, the movie, and the efficiency plots are by Mark Khusid.

## The tutorial propeller

The figures on this page come from the tutorial case at the root of the repository. `Allmesh` copies the tutorial propeller surfaces, runs `blockMesh` and `snappyHexMesh`, and creates the non-conformal couples `nonCouple1` and `nonCouple2`. `Allrun` decomposes that mesh and runs the solver. `make_movie.py` renders the saved surfaces.

The solver is `foamRun` with `incompressibleFluid`. The turbulence model is k-epsilon. The kinematic viscosity is $10^{-6}\,\mathrm{m}^2/\mathrm{s}$.

The inlet velocity is $(0, -5, 0)$ m/s, so the advance speed is 5 m/s in the $-y$ direction. The outer cylinder is a no-slip wall. The propeller patches use `movingWallVelocity`.

The rotor is a `solidBody` motion of the `innerCylinder` cell zone. The origin is $(0, 0, 0)$ and the axis is $(0, 1, 0)$. The speed is 1500 rpm, so one revolution takes 0.04 s. The run stops at 0.08 s, which is two revolutions. The first time step is $10^{-5}$ s. The step can adjust, and the Courant number is limited to 2. Fields are written every 0.02 s, and four time directories are kept.

## Flow movie

`make_movie.py` renders the saved surfaces in ParaView at 1280 by 720. The clip on this page is 10 seconds at 16 frames per second. The mid-plane is colored by velocity magnitude, from 0 to 5 m/s, and the propeller surface is drawn with it. The rotation axis is $y$, and the inflow is along $-y$.

:::{figure} propeller_flow_10s.mp4
:align: center

Mid-plane velocity magnitude on the tutorial propeller. The color bar runs from 0 to 5 m/s.
:::

## Open-water efficiency

Open-water efficiency is

$$
\eta_0 = \frac{T V_a}{Q \omega}
$$

$T$ is thrust along the advance direction, $V_a$ is the advance speed, $Q$ is the moment about the rotation axis, and $\omega = 2\pi n$. At 1500 rpm, $\omega = 157.08$ rad/s.

`plot_efficiency.py` reads the forces history and draws the panels below. The incompressible solver reports force and moment per unit density. The axes take $\rho_\mathrm{inf} = 1$, so the plotted thrust is in newtons and the torque is in newton-metres only for that reference density.

The dashed lines are the post-startup means printed on the figure. The mean open-water efficiency is 0.564, the median is 0.568, and the last sample is 0.570. Mean thrust is 0.3841 and mean torque is $-0.02166$. The repository README states the same result as $\eta_0 \approx 0.56$ and marks it illustrative. The mesh is coarse and the run covers two revolutions.

```{figure} images/propulsor_efficiency.png
:width: 900
:align: center
:class: clickable-figure

Efficiency, thrust, and torque for the tutorial propeller at 1500 rpm and an advance speed of 5 m/s
```

The companion figure keeps thrust and torque. The means match the three-panel plot.

```{figure} images/propulsor_thrust_torque.png
:width: 900
:align: center
:class: clickable-figure

Thrust and torque over the two revolutions, with the same post-startup means
```

## An STL pipeline

The rest of the repository builds a case from a watertight rotor STL, with an optional duct or stator. The manual is [docs/PIPELINE.md](https://github.com/markkhusid/openfoam-propulsor-demo/blob/main/docs/PIPELINE.md). A run starts from the example environment:

```bash
cp pipeline/config.env.example pipeline/config.env
./pipeline/00_check_deps.sh
./pipeline/run_all.sh pipeline/config.env
```

The default rotation mode is MRF. The mesh stays fixed, and the solver adds rotational source terms in the `rotatingZone` cell zone. Sliding mesh motion is available as a separate mode. It uses `solidBody` motion and non-conformal couples, and it needs its own mesh. The tutorial case on this page is that sliding setup.

Mesh presets are `demo`, `engineering`, and `fine`, plus a custom preset. The README pairs the demo preset and a 10 s movie with an 8-core, 16 GB machine, the engineering preset and a 30 s movie with a 16-core machine that has 32 to 64 GB, and the fine preset and a 60 s movie with a 32- to 64-vCPU machine. OpenFOAM 11 can run in Docker from `openfoam/openfoam11-paraview510:latest`, or from a native install.

A pumpjet example lives under `design/`, with `pipeline/config.pumpjet.example.env`. The MRF notes are in [docs/MRF_MODE.md](https://github.com/markkhusid/openfoam-propulsor-demo/blob/main/docs/MRF_MODE.md).
