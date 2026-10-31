# A 2D bar, as a Fortran object

Created with Grok Build

Source code by [Jonas Lindemann](https://github.com/jonaslindemann), from the [oop_fortran](https://github.com/jonaslindemann/oop_fortran) repository.

`simple_frame_2d` takes the same type-bound style as the [shape classes](general_oop.md) and uses it for one finite-element object. A bar has two end points, a Young's modulus, and an area. Its method `Ke` returns the 4 by 4 stiffness matrix in global coordinates. The program constructs one bar with the defaults, prints that matrix, and constructs a small model of nodes and elements. It does not solve a frame. The commented lines in `main` are the calls that would have printed the node and element tables.

Each section shows the declaration or the procedure, then what it does. The files are `code/simple_frame_2d/mf_datatypes.f90`, `mf_utils.f90`, `calfem.f90`, and `main.f90`.

```{figure} images/simple_frame_2d.png
:alt: One bar from (0, 0) to (1, 1)
:align: center
:class: clickable-figure

The default bar runs from (0, 0) to (1, 1). Every entry of Ke has the same magnitude.
```

## `mf_datatypes`

```{literalinclude} code/simple_frame_2d/mf_datatypes.f90
:language: fortran
```

`dp` is `real64`, a double, from `iso_fortran_env`. `sp` is `real32`. The bar code uses `real(dp)` for coordinates, $E$, $A$, and $K$. The particle module later in the Qt program is a different file: it also defines an integer kind `ik` and a double constant `pi`. The two files share a name and are separate modules, each compiled with its own program.

## `mf_utils`

The module keeps the print layout in four variables. Three of them are private.

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 5-24
```

The defaults are width 10, decimals 4, real edit descriptor `G`, and integer edit descriptor `I`. Generic interfaces are the overloading. `print_matrix` can be called with a double matrix, a single matrix, or an integer matrix. The compiler picks `print_matrix_d`, `print_matrix_s`, or `print_matrix_i` from the argument type. `print_vector`, `rand_mat`, and `rand_vec` are the same idea. The bar program only calls the double matrix printer.

### `set_print_format`

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 28-51
```

Each argument is optional. A present width replaces `field_width`. A present decimal count replaces `field_decimals`. A present one-character code replaces `field_code`.

The program calls `set_print_format(12)`, so the width becomes 12 and the other three stay at the defaults. The matrix in the output is four numbers per line in a `G12.4` field, which is why $7.424621\times 10^6$ appears as `0.7425E+07`.

The integer-code branch assigns `int_field_code = code`. `code` is the real edit descriptor, and `int_code` is the argument that was just tested. The demo never passes `int_code`, so the printed matrix uses the real descriptor `G`. A caller who passed an integer code would store `code` into `int_field_code`.

### `print_matrix_d`

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 53-110
```

This is the procedure behind the matrix you see. It reads the row and column counts with `size`. It builds a title format from the length of the name, and a data format with one `G` field per column.

For the bar, `cols` is 4 and `set_print_format(12)` has set `field_width` to 12, `field_decimals` to 4, and `field_code` to `G`. The branch taken is the one for fewer than 10 columns and a width of at least 10:

```fortran
write(fmt, '(A,I1,A,I2,A,I1,A)') '(', cols, field_code, field_width, '.', field_decimals, ')'
```

That writes the characters of the format `(4G12.4)`. `G12.4` asks for a field 12 characters wide with 4 significant digits. The title line is `Matrix Ke (  4 x   4) DP`. The rule of hyphens is `cols * field_width` characters wide. Each row is one `write` of that row of the matrix.

### `print_matrix_s`

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 112-169
```

Same layout as `print_matrix_d`, for `real(sp)`. The title ends in `SP`. `main` does not call it.

### `print_matrix_i`

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 171-228
```

Same layout for an integer matrix. The data format uses `int_field_code` and has no decimal point. With the defaults and four columns the format string is `(4I12)`. The title ends in `I`. `node_set_print` calls this one by name.

### `print_vector_d` and `print_vector_s`

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 231-284
```

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 286-339
```

These print one row of numbers, labeled `Vector`, for double and single precision. The implied-do `(a(i), i=1,cols)` is the whole vector in one `write`. `main` does not call either of them.

### The random helpers

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 341-352
```

`random_number` fills `A` with values $U$ in $[0, 1)$. The next line scales that into the requested range:

$$
A = a_{\min} + (a_{\max} - a_{\min})\, U
$$

`randMin + (randMax-randMin) * A` is that formula. The comment `min ---- max` is the same interval.

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 354-365
```

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 367-378
```

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 380-391
```

`rand_mat_s`, `rand_vec_d`, and `rand_vec_s` implement the same scaling for a single-precision matrix and for a double or single vector. The bar program does not call any of them.

```{literalinclude} code/simple_frame_2d/mf_utils.f90
:language: fortran
:lines: 393-402
```

`init_rand` calls `random_seed` with no argument on the size inquiry, then stores `values(8)` into every seed element. `values(8)` from `date_and_time` is the millisecond field. The local `r` is declared and never used. The bar program does not call `init_rand`.

## `NodeSet`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 14-26
```

A node set is the mesh's node table: `m_positions(n_nodes, 2)` and `m_dofs(n_nodes, n_dofs_per_node)`. Nothing is `private`. A caller can write the arrays directly. The bindings are `init`, `print`, `resize`, and a finalizer.

`interface NodeSet` makes `NodeSet(n_nodes, n_dofs_per_node)` call `node_set_constructor`.

### `node_set_init`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 98-110
```

Allocates the two arrays, sets every coordinate to 0, and sets every degree of freedom to $-1$. $-1$ means the degree of freedom has not been numbered yet. The constructor is the only caller in this program, with 4 nodes and 2 degrees of freedom per node.

### `node_set_print`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 112-119
```

Calls `print_matrix` on the coordinates and `print_matrix_i` on the degree-of-freedom table. `main` builds a node set and leaves the print commented out.

### `node_set_resize`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 121-152
```

Allocates copies of the old arrays, copies both, drops the old allocation, allocates the new shape, fills it with zeros and $-1$, and copies old coordinates back when the new row count is at least the old row count. The saved degree-of-freedom copy is never written back. `deallocate(positions, dofs)` drops it with the temporary coordinate copy. A resize would keep coordinates and reset every dof to $-1$. The program does not call `resize`.

### `node_set_destructor`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 155-163
```

Prints `node_set_destructor` and deallocates both arrays. The dummy is `type(NodeSet)`, the finalizer form. This is the finalizer the run does print. When it runs is under `BarModel` below.

### `node_set_constructor`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 165-175
```

Prints `node_set_constructor` and calls `node_set_init`. The result is a function temporary. The finalizer runs as soon as that temporary has been copied into the allocatable component that stores it. That is why the output prints the constructor and the destructor on consecutive lines, while the model still holds a live node set.

## `ElementSet`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 30-40
```

An element set stores topology in `m_topo(n_elements, n_dofs_per_element)`. The integers are element connectivity. The bindings are `init`, `print`, and `resize`. There is a subroutine `element_set_destructor`, and it is not registered with `final`, so the language does not call it. The run does not print `element_set_destructor`.

### `element_set_init`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 179-193
```

If the degree-of-freedom count is present, the topology has that many columns. If it is absent, the column count is 6. Every entry starts at $-1$.

### `element_set_print`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 195-201
```

Prints the topology through the generic `print_matrix`, which selects `print_matrix_i` because `m_topo` is integer. `main` does not call it.

### `element_set_resize`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 203-238
```

Saves the old topology, reallocates, fills with $-1$, and copies the overlapping corner back. This copy does get written back. The program does not call `resize`.

### `element_set_destructor`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 241-249
```

Would print `element_set_destructor` and deallocate `m_topo`. It is an ordinary subroutine with a `type(ElementSet)` dummy. No binding points at it.

### `element_set_constructor`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 251-261
```

Prints `node_set_constructor`. The string does not match the subroutine name. The body then calls `element_set_init`. `BarModel` does not call this constructor. It calls the bar-element constructor below, which has its own print. This string is absent from the output.

## `BarElementSet`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 44-53
```

`BarElementSet` extends `ElementSet` and overrides `init` and `resize`. A bar element in 2D has four degrees of freedom, two at each end, so both overrides ignore the passed column count and call the parent with 4.

### `bar_element_set_init` and `bar_element_set_resize`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 265-283
```

The parent is named by the parent type. `call this % elementset % init(n_topo, 4)` is the parent component. It is the same idea as `call shape_init(this)` in the shape example, written as a component call. `call this % init(...)` here would recurse into the override. `n_dofs_per_element` is accepted and then unused. The column count that is stored is the literal 4.

### `bar_element_set_constructor`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 285-294
```

Prints `bar_element_set_constructor` and calls `bar_element_set_init` with the element count and with 4 columns. `BarModel` calls this once, for 2 elements. The line appears twice in the output for a different reason, described with the program.

## `BarElement`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 57-73
```

This is the object the matrix comes from. It does not extend `ElementSet`. A single bar is a separate type from a set of elements. The components are `m_p0(2)`, `m_p1(2)`, `m_A`, and `m_E`, all visible. The bindings are `init`, `set_p0`, `set_p1`, `set_ep`, `Ke`, and `print`.

`interface BarElement` makes `BarElement()` and `BarElement(x0, y0, x1, y1, E, A)` call `bar_element_constructor`. Every argument of that function is optional, so both calls are legal.

### `bar_element_init`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 298-321
```

Sets a default bar, then applies whatever arguments the caller passed.

The defaults are $m_{p0} = 0$ and $m_{p1} = 1$, so the ends are $(0, 0)$ and $(1, 1)$. The modulus and area are

$$
E = 2.1\times 10^9, \qquad A = 0.1 \times 0.1 = 0.01
$$

`2.1e9_dp` and `0.1_dp*0.1_dp` are those two assignments. If the drawing is in metres, $E$ is in N/m² and $A$ is in m².

The six updates are each guarded by `present(x0)`. `y0`, `x1`, `y1`, `E`, and `A` are not the arguments tested. If the caller passes `x0`, all six are assigned. If the caller passes `E` and omits `x0`, the modulus stays at the default. The program calls `BarElement()` with no arguments, so only the defaults are used and this matrix comes from the defaults.

### `bar_element_set_p0`, `bar_element_set_p1`, `bar_element_set_ep`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 323-351
```

`set_p0` stores a new first end, `set_p1` stores a new second end, and `set_ep` stores a new modulus and area:

$$
m_{p0} = (x, y), \qquad m_{p1} = (x, y), \qquad m_E = E, \qquad m_A = A
$$

`main` does not call them. They are the way to move the default bar without going back through `init`.

### `bar_element_ke`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 353-382
```

Returns $K_e$, a 4 by 4 matrix. The four rows and columns are the global degrees of freedom of end 0 in $x$, end 0 in $y$, end 1 in $x$, and end 1 in $y$.

The end-to-end vector and its length are

$$
\mathbf{b} = \mathbf{p}_1 - \mathbf{p}_0, \qquad L = \sqrt{\mathbf{b}\cdot\mathbf{b}}
$$

`b(1)` and `b(2)` are the two components, and `L = sqrt(dot_product(b,b))` is the length. The axial stiffness is

$$
c = \frac{EA}{L}
$$

which is `c = this % m_E * this % m_A / L`. In local coordinates, along the bar, the 2 by 2 matrix is

$$
K_\mathrm{local} =
c \begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}
$$

`Kle(1,:) = (/ 1, -1 /) * c` and `Kle(2,:) = (/ -1, 1 /) * c` are those two rows. A positive displacement of end 0 pulls end 1 the other way, which is why the off-diagonals are negative.

`G` is 2 by 4. Its first row picks out the direction of the bar at end 0, and its second row picks out the same direction at end 1. For a unit vector $(n_x, n_y)$ along the bar,

$$
n_x = \frac{p_{1x}-p_{0x}}{L}, \qquad
n_y = \frac{p_{1y}-p_{0y}}{L}, \qquad
G = \begin{bmatrix} n_x & n_y & 0 & 0 \\ 0 & 0 & n_x & n_y \end{bmatrix}
$$

`nxx` and `nyx` are $n_x$ and $n_y$. The two assignments to `G` are the two rows.

The global matrix is

$$
K = G^{T} K_\mathrm{local} G
$$

`Ke = matmul(transpose(G), matmul(Kle, G))` is that product. `matmul(Kle, G)` is $K_\mathrm{local} G$, and `matmul(transpose(G), ...)` multiplies on the left by $G^T$.

For the default bar, $\mathbf{b} = (1, 1)$, so $L = \sqrt{2}$ and $(n_x, n_y) = (1/\sqrt{2},\, 1/\sqrt{2})$. Then

$$
c = \frac{2.1\times 10^9 \times 0.01}{\sqrt{2}} = 1.484924\times 10^7
$$

Every entry of $K$ has magnitude

$$
\frac{c}{2} = \frac{c}{(\sqrt{2})^2} = 7.424621\times 10^6
$$

because each product of direction cosines contributes a factor $1/\sqrt{2}\times 1/\sqrt{2} = 1/2$. The pattern is positive on the two ends' matching blocks and negative on the coupling blocks. `G12.4` prints the magnitude as `0.7425E+07`.

### `bar_element_print`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 384-390
```

Calls `print_matrix` on `this % Ke()`. The matrix is a function result. Printing the bar recomputes $K$.

### `bar_element_constructor`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 392-406
```

Prints `bar_element_set_constructor`. The string names the set constructor. The body then calls `bar_element_init` with the same optional arguments. `BarElement()` therefore prints `bar_element_set_constructor` once, before the matrix. That is the first line of the output, and it is this function. The set routine prints the same words later.

## `BarModel`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 77-88
```

A model owns one allocatable `NodeSet` and one allocatable `BarElementSet`. The bindings are `init`, `node_set`, and `element_set`.

### `bar_model_init`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 410-420
```

Assigns `m_node_set = NodeSet(n_nodes, 2)` and `m_element_set = BarElementSet(n_elements)`. The node constructor prints, the temporary is finalized, and the bar-element-set constructor prints. For `BarModel(4, 2)` that is three lines: `node_set_constructor`, `node_set_destructor`, `bar_element_set_constructor`.

### `bar_model_node_set` and `bar_model_element_set`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 422-438
```

Each function returns the component by value, a copy. `main` leaves both calls commented out. A copy of the node set would be another temporary, and its finalizer would print again.

### `bar_model_constructor`

```{literalinclude} code/simple_frame_2d/calfem.f90
:language: fortran
:lines: 440-448
```

Calls `bar_model_init` and does not print on its own. The lines you see come from the two objects it constructs.

## What `main` prints

```{literalinclude} code/simple_frame_2d/main.f90
:language: fortran
```

`set_print_format(12)` selects the `G12.4` layout. `bar = BarElement()` hits the single-bar constructor, whose print string is `bar_element_set_constructor`, and `bar % print()` writes $K$. `bar_model = BarModel(4, 2)` then builds the tables. `node_set` and `bar_element_set` are declared and never used. The commented assignments are what those variables were for.

```{literalinclude} code/simple_frame_2d/simple_frame_2d.out
:language: text
```

The second `bar_element_set_constructor` is the set constructor, from `BarElementSet(2)` inside the model. The first one is the single-bar constructor printing those same words.

## CMake

```{literalinclude} code/simple_frame_2d/CMakeLists.txt
:language: cmake
```

The list is the same shape as the shape program, with the project name `simple_frame_2d`. `cmake_minimum_required(VERSION 3.5)` is the version the list was written for. CMake 3.31 on this machine still configures it. `GLOB` collects four files: `mf_datatypes.f90`, `mf_utils.f90`, `calfem.f90`, and `main.f90`. CMake's Fortran dependency scanner compiles the modules before `main.f90`. The order in the log is datatypes, utils, `calfem`, then the program. `calfem` uses both modules, and `main` uses all three.

```{literalinclude} code/simple_frame_2d/cmake_configure.log
:language: text
```

The build directory is `/tmp/oop_learn/simple_frame_2d/build`. The transcript drops that prefix and the `-I` flags.

```{literalinclude} code/simple_frame_2d/cmake_build.log
:language: text
```

The link driver is `f95`. There is no C++ in this program, so the link line does not add `-lgfortran`. `f95` already knows the Fortran runtime. Running `./simple_frame_2d` produced the twelve lines above.
