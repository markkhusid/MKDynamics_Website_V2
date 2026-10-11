# CAELinux with Salome-Meca and Elmer

Created with Grok Build

CAELinux is an Ubuntu-based distribution loaded with applications for engineering work. In this session Salome-Meca builds the geometry and the mesh, and ElmerGUI solves the model. CAELinux is published at [caelinux.com](https://caelinux.com/).

```{figure} ../images/CAELinux_desktop.jpeg
:width: 900
:align: center
:class: clickable-figure

The CAELinux desktop
```

## Salome-Meca

The geometry window is Salome-Meca 2015.2, running in the CAELinux virtual machine. The object browser holds the sketch, the face built from that sketch, and the extrusion. Salome-Meca also meshes the solid and can hand the mesh to a solver. Salome-Meca is distributed with Code_Aster from [code-aster.org](https://code-aster.org/). The Salome platform itself is documented at [salome-platform.org](https://www.salome-platform.org/).

```{figure} ../images/Salome_elmer1.jpeg
:width: 900
:align: center
:class: clickable-figure

Sketch_1, the profile that becomes the solid
```

The sketch is an upright segment joined to a base segment. That profile is the cross-section of the beam in the later figures.

## Extrusion

The sketch is turned into a face, and the face is extruded into the solid named Extrusion_1.

```{figure} ../images/Salome_elmer2.jpeg
:width: 900
:align: center
:class: clickable-figure

Extrusion_1, the face pulled into a solid beam
```

## The mesh

Mesh_1 is generated from that solid. The view is colored by Aspect Ratio 3D. The scale runs from 1.05 to 4.70. This mesh is the input ElmerGUI reads.

```{figure} ../images/Salome_elmer3.jpeg
:width: 900
:align: center
:class: clickable-figure

Mesh_1 colored by aspect ratio
```

## ElmerGUI

Elmer is the open-source multiphysics finite-element package from CSC, the Finnish IT Center for Science. The same beam is open in ElmerGUI, with the surface mesh drawn on the solid. The project site is [elmerfem.org](https://www.elmerfem.org/).

```{figure} ../images/Salome_elmer4.jpeg
:width: 900
:align: center
:class: clickable-figure

The beam mesh in ElmerGUI
```

## Displacement

The ElmerGUI postprocessor draws the field Displacement_y on that mesh. The color bar runs from -0.000526 to 0.000520. The web sits near the middle of the scale. Along the flange the colors run from the blue end of the bar to the red end.

```{figure} ../images/Salome_elmer5.jpeg
:width: 900
:align: center
:class: clickable-figure

Displacement_y on the beam
```
