# Object-oriented Fortran

Created with Grok Build

These programs are the examples in Jonas Lindemann's [oop_fortran](https://github.com/jonaslindemann/oop_fortran) repository. Each program is copied here once, under `code/`, and the pages below walk through what that source does. The lecture PDF in the repository is not copied onto this site.

The shape classes, the Fortran program that calls C++, and the 2D bar element were built with gfortran 14.2.0 on this machine. The saved text on those pages is the output of those runs. The particle viewer is a Qt Widgets program. Qt Widgets is not installed here, so that window was not built.

## Programs

::::{grid} 2 2 2 2

:::{grid-item-card}
:link: general_oop.md

Shapes, inheritance, and polymorphism
^^^
```{image} images/general_oop.png
:height: 220
```
:::

:::{grid-item-card}
:link: fortran_cpp.md

Fortran calling C++
^^^
```{image} images/fortran_cpp.png
:height: 220
```
:::

:::{grid-item-card}
:link: cpp_fortran.md

Qt particle viewer
^^^
```{image} images/cpp_fortran.png
:height: 220
```
:::

:::{grid-item-card}
:link: simple_frame_2d.md

2D bar stiffness matrix
^^^
```{image} images/simple_frame_2d.png
:height: 220
```
:::

::::
