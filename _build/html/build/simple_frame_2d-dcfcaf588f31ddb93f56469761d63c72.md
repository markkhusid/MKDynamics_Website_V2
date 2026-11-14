# 2D bar stiffness matrix

Created with Grok Build

`simple_frame_2d` builds one default bar and prints its 4×4 stiffness matrix, then constructs a `BarModel` with 4 nodes and 2 elements. The module is named `calfem`. This program is that module, the kind parameters, and the matrix printer. It is not the full CALFEM library.

```{figure} images/simple_frame_2d.png
:alt: Default bar from the origin to (1, 1) and its stiffness matrix
:align: center
:class: clickable-figure

The default bar runs from (0, 0) to (1, 1). The matrix is the gfortran 14.2.0 print, divided by 1e7 so the entries fit on the figure.
```

## Types

`NodeSet` stores positions and degrees of freedom. `NodeSet(n, n_dofs)` allocates both, sets positions to 0, and sets the degrees of freedom to −1. A final subroutine deallocates them and prints `node_set_destructor`.

`ElementSet` stores an integer topology. `BarElementSet` extends it and sizes each element for 4 degrees of freedom by calling the parent `init`.

`BarElement` stores the two end coordinates, Young's modulus `m_E`, and the area `m_A`. The constructor with no arguments leaves the defaults written in `bar_element_init`: `p0 = (0, 0)`, `p1 = (1, 1)`, $E = 2.1 \times 10^{9}$, and $A = 0.01$. The six assignments that would replace those defaults are each guarded by `present(x0)`. A call that passes arguments still tests only `x0`. `BarElement()` passes none, so the defaults stand.

`Ke` is the 4 by 4 stiffness for the two ends, each with `ux` and `uy`. The bar vector is `p1 - p0`, the length is $L$, and $c = EA/L$. The local axial matrix is $c$ on the diagonal and $-c$ off the diagonal. The direction cosines are $n_{xx} = (x_1 - x_0) / L$ and $n_{yx} = (y_1 - y_0) / L$, and $K_e = G^{T} K_{le} G$ rotates that axial matrix into global components.

For the default bar, $L = \sqrt{2}$ and $c = 2.1 \times 10^{7} / \sqrt{2}$. At 45 degrees the direction cosines are equal, so every entry has magnitude $c/2 = 7.424621 \times 10^{6}$, which the printer shows as `0.7425E+07`. The signs follow the usual bar pattern: positive on the blocks that tie an end to itself, negative on the blocks that tie one end to the other.

`BarModel(n_nodes, n_elements)` builds a `NodeSet` and a `BarElementSet`. The program constructs the model and does not print either set. The two commented lines in `main.f90` are the calls that would retrieve them.

## What the run printed

`set_print_format(12)` sets the printer width. The first `bar_element_set_constructor` line is the message in `bar_element_constructor`, the constructor of the single bar. The matrix follows. `node_set_constructor` and `node_set_destructor` are the temporary `NodeSet(4, 2)` created by the model and finalized after it is stored. The last `bar_element_set_constructor` line is the element-set constructor. Both constructors print that same string.

```{literalinclude} code/simple_frame_2d/simple_frame_2d.out
:language: text
```

## main.f90

```{literalinclude} code/simple_frame_2d/main.f90
:language: fortran
```

## calfem.f90

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
```

## mf_datatypes.f90

```{literalinclude} code/simple_frame_2d/mf_datatypes.f90
:language: fortran
```

## mf_utils.f90

`print_matrix` covers double, single, and integer arrays. `bar % print()` calls it with `Ke`.

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
```

## CMakeLists.txt

```{literalinclude} code/simple_frame_2d/CMakeLists.txt
:language: cmake
```
