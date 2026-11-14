# A 2D bar, as a Fortran object

Created with Grok Build

`simple_frame_2d` takes the same type-bound style as the [shape classes](general_oop.md) and uses it for one finite-element object. A bar has two end points, a Young's modulus, and an area. Its method `Ke` returns the 4 by 4 stiffness matrix in global coordinates. The program constructs one bar with the defaults, prints that matrix, and constructs a small model of nodes and elements. It does not solve a frame. The commented lines in `main` are the calls that would have printed the node and element tables.

```{figure} images/simple_frame_2d.png
:alt: One bar from (0, 0) to (1, 1)
:align: center
:class: clickable-figure

The default bar runs from (0, 0) to (1, 1). Every entry of Ke has the same magnitude.
```

## `mf_datatypes`

This copy of the module defines two kinds and nothing else.

`dp` is `real64`, a double, from `iso_fortran_env`. `sp` is `real32`. The bar code uses `real(dp)` for coordinates, `E`, `A`, and `Ke`. The particle module later in the Qt program is a different file: it also defines an integer kind `ik` and a double constant `pi`. The two files share a name and are not the same module.

## `mf_utils`

The module keeps the print layout in four private variables: width 10, decimals 4, real edit descriptor `G`, integer edit descriptor `I`. The program calls `set_print_format(12)`, so the width becomes 12 and the other three stay at the defaults. The matrix in the output is four numbers per line in a `G12.4` field, which is why `7424621` appears as `0.7425E+07`.

Generic interfaces are the overloading. `print_matrix` can be called with a double matrix, a single matrix, or an integer matrix. The compiler picks `print_matrix_d`, `print_matrix_s`, or `print_matrix_i` from the argument type. `print_vector`, `rand_mat`, and `rand_vec` are the same idea. The bar program only calls the double matrix printer.

### `set_print_format`

Each argument is optional. A present width replaces `field_width`. A present decimal count replaces `field_decimals`. A present one-character code replaces `field_code`.

The integer-code branch does not use its own argument. When `int_code` is present, the assignment is `int_field_code = code`. `code` is the real edit descriptor. The demo never passes `int_code`, so the bug is not in the printed matrix. A caller who passed only an integer code would change `int_field_code` to an undefined `code`, or to the real code if that argument was also present.

### `print_matrix_d`

This is the procedure behind the matrix you see. It reads the row and column counts with `size`. It builds a title format that prints the name, the row count, and the column count, and a data format with one `G` field per column. The title line is `Matrix Ke (  4 x   4) DP`. The rule of hyphens is as wide as the fields. Each row is one `write` of that row of the matrix. `print_matrix_s` and `print_matrix_i` follow the same pattern for the other types. `print_vector_d` and `print_vector_s` print a column instead of a matrix. None of those four are called by `main`.

### The random helpers

`rand_mat_d`, `rand_mat_s`, `rand_vec_d`, and `rand_vec_s` fill an array with `random_number` scaled into a range. `init_rand` calls `random_seed` with no argument, which resets the generator to the implementation default. `init_rand` also declares a `real(real64) :: r` that it does not use. `-Wall` reports it. The bar program does not call any of these.

## `NodeSet`

A node set is the mesh's node table: `m_positions(n_nodes, 2)` and `m_dofs(n_nodes, n_dofs_per_node)`. Nothing is `private`. A caller can write the arrays directly. The bindings are `init`, `print`, `resize`, and a finalizer.

`interface NodeSet` makes `NodeSet(n_nodes, n_dofs_per_node)` call `node_set_constructor`.

### `node_set_init`

Allocates the two arrays, sets every coordinate to 0, and sets every degree of freedom to `-1`. `-1` means "not numbered yet." The constructor is the only caller in this program, with 4 nodes and 2 degrees of freedom per node.

### `node_set_print`

Calls `print_matrix` on the coordinates and `print_matrix_i` on the degree-of-freedom table. `main` computes a node set and does not print it. The call is one of the commented lines.

### `node_set_resize`

Allocates copies of the old arrays, drops the old allocation, allocates the new shape, fills it with the empty-table values, and copies old coordinates back when the new row count is at least the old row count. The saved degree-of-freedom copy is never written back. It is deallocated with the temporary coordinate copy. A resize would keep coordinates and reset every dof to `-1`. The program does not call `resize`.

### `node_set_destructor`

Prints `node_set_destructor` and deallocates both arrays. The dummy is `type(NodeSet)`, the finalizer form. This is the one finalizer the run does print, apart from the story of when it runs, which is under `BarModel` below.

### `node_set_constructor`

Prints `node_set_constructor` and calls `node_set_init`. The result is a function temporary. The finalizer runs as soon as that temporary has been copied into the allocatable component that stores it. That is why the output prints the constructor and the destructor on consecutive lines, while the model still holds a live node set.

## `ElementSet`

An element set stores topology in `m_topo(n_elements, n_dofs_per_element)`. The integers are element connectivity, not coordinates. The bindings are `init`, `print`, and `resize`. There is a subroutine `element_set_destructor`, and it is not registered with `final`, so nothing in the language calls it. The run does not print `element_set_destructor`.

### `element_set_init`

If the degree-of-freedom count is present, the topology has that many columns. If it is absent, the column count is 6. Every entry starts at `-1`.

### `element_set_print`

Prints the topology through `print_matrix`. Not called by `main`.

### `element_set_resize`

Same shape as the node resize: save, reallocate, fill with `-1`, copy the overlapping corner, drop the temporary. This copy does get written back. Not called by `main`.

### `element_set_destructor`

Would print `element_set_destructor` and deallocate `m_topo`. It is an ordinary subroutine with a `type(ElementSet)` dummy. No binding points at it.

### `element_set_constructor`

Prints `node_set_constructor`. The string does not match the subroutine. The body then calls `element_set_init`. `BarModel` does not call this constructor. It calls the bar-element constructor below, which has its own print. So this wrong string is not in the output.

## `BarElementSet`

`BarElementSet` extends `ElementSet` and overrides `init` and `resize`. A bar element in 2D has four degrees of freedom, two at each end, so both overrides ignore the passed column count and call the parent with 4.

The parent is named by the parent type. `call this % elementset % init(...)` is the parent component. It is the same idea as `call shape_init(this)` in the shape example, written as a component call instead of a procedure call. Using `call this % init(...)` here would recurse into the override.

### `bar_element_set_constructor`

Prints `bar_element_set_constructor` and calls `bar_element_set_init` with the element count and with 4 columns. `BarModel` calls this once, for 2 elements. The line appears twice in the output for a different reason, described with the program.

## `BarElement`

This is the object the matrix comes from. It does not extend `ElementSet`. A single bar is not a set of elements. The components are `m_p0(2)`, `m_p1(2)`, `m_A`, and `m_E`, all visible. The bindings are `init`, `set_p0`, `set_p1`, `set_ep`, `Ke`, and `print`.

`interface BarElement` makes `BarElement()` and `BarElement(x0, y0, x1, y1, E, A)` call `bar_element_constructor`. Every argument of that function is optional, so both calls are legal.

### `bar_element_init`

Sets a default bar, then applies whatever arguments the caller passed.

The defaults are `m_p0 = 0`, `m_p1 = 1`, so the ends are `(0, 0)` and `(1, 1)`. `m_E = 2.1e9`, steel-range modulus in N/m² if the drawing is in metres. `m_A = 0.1 * 0.1`, which is `0.01` m².

The six updates are each guarded by `present(x0)`. `y0`, `x1`, `y1`, `E`, and `A` are not tested. If the caller passes `x0`, all six are assigned, and a missing later argument would be undefined. If the caller passes `E` and not `x0`, the modulus stays at the default. The program calls `BarElement()` with no arguments, so only the defaults are used and the bug does not change this matrix.

### `bar_element_set_p0`, `bar_element_set_p1`, `bar_element_set_ep`

Store a new end, or a new modulus and area. `main` does not call them. They are the way to move the default bar without going back through `init`.

### `bar_element_ke`

Returns `Ke(4, 4)`. The four rows and columns are the global degrees of freedom of end 0 in $x$, end 0 in $y$, end 1 in $x$, and end 1 in $y$.

The end-to-end vector is `b = p1 - p0`. The length is $L = \sqrt{b \cdot b}$. The axial stiffness is $c = EA / L$. In local coordinates, along the bar, the 2 by 2 matrix is

$$
K_\mathrm{local} = c \begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}
$$

A positive displacement of end 0 pulls end 1 the other way, which is why the off-diagonals are negative.

`G` is 2 by 4. Its first row picks out the direction of the bar at end 0, and its second row picks out the same direction at end 1. For a unit vector $(n_x, n_y)$ along the bar,

$$
G = \begin{bmatrix} n_x & n_y & 0 & 0 \\ 0 & 0 & n_x & n_y \end{bmatrix}
$$

The global matrix is $K = G^T K_\mathrm{local} G$. `matmul` and `transpose` are the Fortran for that product.

For the default bar, $b = (1, 1)$, so $L = \sqrt{2}$ and $(n_x, n_y) = (1/\sqrt{2}, 1/\sqrt{2})$. Then

$$
c = \frac{2.1\times 10^9 \times 0.01}{\sqrt{2}} = 1.484924\times 10^7
$$

and every entry of $K$ has magnitude $c/2 = 7.424621\times 10^6$. The pattern is positive on the two ends' matching blocks and negative on the coupling blocks. `G12.4` prints the magnitude as `0.7425E+07`.

### `bar_element_print`

Calls `print_matrix` on `this % Ke()`. The matrix is a function result, not a stored component. Printing the bar recomputes `Ke`.

### `bar_element_constructor`

Prints `bar_element_set_constructor`. The string names the set constructor, not this function. It then calls `bar_element_init` with the same optional arguments. `BarElement()` therefore prints `bar_element_set_constructor` once, before the matrix. That is the first line of the output, and it is this function, not `bar_element_set_constructor` the set routine. The set routine prints the same words later.

## `BarModel`

A model owns one allocatable `NodeSet` and one allocatable `BarElementSet`. The bindings are `init`, `node_set`, and `element_set`.

### `bar_model_init`

Assigns `m_node_set = NodeSet(n_nodes, 2)` and `m_element_set = BarElementSet(n_elements)`. The node constructor prints, the temporary is finalized, and the bar-element-set constructor prints. For `BarModel(4, 2)` that is three lines: `node_set_constructor`, `node_set_destructor`, `bar_element_set_constructor`.

### `bar_model_node_set` and `bar_model_element_set`

Return the components by value, a copy. `main` leaves both calls commented out. A copy of the node set would be another temporary, and its finalizer would print again.

### `bar_model_constructor`

Calls `bar_model_init` and does not print on its own. The lines you see come from the two objects it constructs.

## What `main` prints

`set_print_format(12)` selects the `G12.4` layout. `bar = BarElement()` hits the single-bar constructor, whose print string is `bar_element_set_constructor`, and `bar % print()` writes `Ke`. `bar_model = BarModel(4, 2)` then builds the tables. `node_set` and `bar_element_set` are declared and never used. `-Wall` reports both. The commented assignments are what those variables were for.

```{literalinclude} code/simple_frame_2d/simple_frame_2d.out
:language: text
```

The second `bar_element_set_constructor` really is the set constructor, from `BarElementSet(2)` inside the model. The first one is the single-bar constructor printing the wrong words.

## Warnings

```{literalinclude} code/simple_frame_2d/gfortran_wall.log
:language: text
```

The unused dummy `n_dofs_per_element` is the argument `BarElementSet` accepts and then ignores when it forces 4 columns. The unused `r` is the one in `init_rand`.

## CMake

```{literalinclude} code/simple_frame_2d/CMakeLists.txt
:language: cmake
```

The list is the same shape as the shape program, with a different project name. `GLOB` collects four files: `mf_datatypes.f90`, `mf_utils.f90`, `calfem.f90`, and `main.f90`. CMake's Fortran dependency scanner compiles the modules before `main.f90`. The order in the log is datatypes, utils, `calfem`, then the program. `calfem` uses both modules, and `main` uses all three.

```{literalinclude} code/simple_frame_2d/cmake_configure.log
:language: text
```

The build directory is `/tmp/oop_learn/simple_frame_2d/build`. The transcript drops that prefix and the `-I` flags.

```{literalinclude} code/simple_frame_2d/cmake_build.log
:language: text
```

The link driver is `f95`. There is no C++ in this program, so `-lgfortran` does not appear. `f95` already knows the Fortran runtime. Running `./simple_frame_2d` produced the twelve lines above.

## Source

```{literalinclude} code/simple_frame_2d/mf_datatypes.f90
:language: fortran
```

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
```

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
```

```{literalinclude} code/simple_frame_2d/main.f90
:language: fortran
```
