# Shapes, inheritance, and polymorphism

Created with Grok Build

`general_oop` is the small version of the idea on the [section page](oop_fortran__HEAD__.md). One module defines the types. One program constructs them, stores some of them in arrays, and calls `print` through a polymorphic pointer. CMake names the executable `oop1`. The Fortran `program` line is `myfortran`.

```{figure} images/general_oop.png
:alt: Square, circle, and triangle
:align: center
:class: clickable-figure

Square and Circle extend Shape. Triangle holds three Point objects.
```

## `Particle`

`Particle` is only data: `pos(3)`, `vel(3)`, and `mass`. There is no `contains` section, so it has no methods and no `final` subroutine. The program declares `type(Particle) :: p` and never mentions `p` again. `gfortran -Wall` reports that unused variable. The type is here so a plain derived type can be compared with the types that follow.

## `Shape`

`Shape` is the parent. `pos(2)` is `private`, so a caller outside the module cannot write `s % pos`. The bindings are `init`, `set_pos`, and `print`. `final :: shape_destructor` registers the finalizer.

`interface Shape` maps the type name onto `shape_constructor`. `s = Shape()` calls that function instead of zeroing the components with the intrinsic structure constructor.

### `shape_init`

The dummy is `class(Shape) :: this`. `class` matters: `square_init` calls `shape_init` and passes a `Square`. A `type(Shape)` dummy would not accept that actual argument. The body prints `shape_init()` and sets both components of `pos` to 0.

### `shape_constructor`

The result is `type(Shape)`, a real `Shape`, not a polymorphic object. It prints `shape_constructor()` and calls `shape_init`. The function result is a temporary. On this gfortran, assigning that temporary prints `shape_destructor()` twice before the stored object is printed. Those two lines are the temporaries of `s = Shape()`, not a finalizer call on `s` itself.

### `shape_destructor`

The dummy is `type(Shape) :: this`, which is the form a final subroutine uses. The body ignores `this` and prints `shape_destructor()`. `-Wall` reports the unused dummy. A final subroutine still has to declare the object, because that is how the language knows which type is being finalized.

On the run below the line appears 24 times: the two constructor temporaries, the local inside `make_objects`, the allocatable `s2` when it is deallocated, and the 20 elements of `dyn_shapes` when that array is deallocated. The static array, the scalar locals, and the `deallocate` of the `type(Shape)` pointers do not add more lines. The subroutine is part of the type either way. This output is what gfortran 14.2.0 did with it.

### `shape_set_pos`

`class(Shape) :: this` plus two `real` arguments with `intent(in)`. It stores `x` in `pos(1)` and `y` in `pos(2)`. There is no print. The program uses it twice: once to move `s` to `(2, 2)`, and once inside `make_objects` to move a local shape to `(5, 6)`.

### `shape_print`

Prints `shape_print()`, then `x` and `y` from the private components. `Square` and `Circle` override `print`, and each of those overrides calls `shape_print` at the end so the coordinates still appear.

## `Square`

`Square` extends `Shape`, so a square has `pos` and a new private `side`. The bindings `init` and `print` are written again, which overrides the parent for a dynamic type of `Square`. `set_pos` is not overridden, so a square moves with `shape_set_pos`.

### `square_init`

Prints `square_init()`, calls `shape_init(this)` to zero `pos`, then sets `side = 1`. The parent call is by the procedure name, not by the binding. If it had been `call this % init()`, the call would have gone back into `square_init`.

### `square_print`

Prints `square_print()` and `side`, then calls `shape_print(this)` for the coordinates. A square that was never initialized prints `side = 0` on this compiler and then prints whatever bits were in `pos`. That second case is the polymorphic loop further down.

## `Circle`

`Circle` extends `Shape` with a private `radius` and three bindings: `init`, `print`, and `set_radius`.

### `circle_init`

Prints `circle_init()`, calls `shape_init`, and sets `radius = 1`.

### `circle_set_radius`

The dummy is `class(Circle), intent(out)`. `intent(out)` means the object becomes undefined on entry, and then the subroutine defines `radius`. The position inherited from `Shape` would not survive a call. The program never calls this procedure, so the circles that get printed still have the radius and the origin from `circle_init`.

### `circle_print`

Prints `cirlce_print()`. That spelling is the string in the source. It then prints `radius` and calls `shape_print`.

## `Point`

`Point` does not extend `Shape`. It is a separate type with private `m_x` and `m_y`. Nothing in the program prints a finalizer for it, because it has no `final` binding.

### `point_init`

Stores the two arguments. They are not `intent(in)`. The language still treats them as inputs because the body only reads them. `triangle_init` calls this with `(0, 0)`.

### `point_set_pos`

Same assignment as `point_init`. The triangle demo uses this one, not `init`, to move a vertex after construction.

### `point_print`

Prints the word `Point` and then both coordinates on one line. The format is the default list-directed format, so the numbers do not line up with the `shape_print` numbers.

## `PointElement` and `Triangle`

`PointElement` is a one-component type whose only field is `class(Point), pointer :: p_element`. `Triangle` is `private` and holds `m_points(3)` of that element type. A triangle does not contain three `Point` values. It contains three pointers to points allocated somewhere else. That is composition: the triangle is built out of another type, and it does not inherit from that type.

### `triangle_init`

Allocates a `class(Point)` pointer three times, initializes each point to `(0, 0)`, and stores the pointer. The local `p_point` is reused. Each `allocate` creates a new target, and the pointer assignment `=>` saves that target in the element. `-Wall` does not warn about `p_point` here. The unused `p_point` is the one in `triangle_print`.

### `triangle_get_point`

Returns `class(Point), pointer`. The result is associated with `m_points(idx) % p_element`. It does not allocate and it does not copy. Two calls with the same index return two names for one point.

### `triangle_print`

Prints `Triangle`, then calls `print` on each stored point. The local `p_point` is declared and never used. `-Wall` points at that declaration. The loop uses `this % m_points(i) % p_element % print()` directly.

## What `main` does, in order

The program's own types, `SimpleArrayElement` and `ShapeArrayElement`, are not in the module. The first holds a `type(Shape)` pointer. The second holds a `class(Shape)` pointer. Only the second can point at a `Square`.

`s = Shape()` runs the constructor. The stored shape prints as `(0, 0)`, then `set_pos(2, 2)` makes the second print `(2, 2)`.

`make_objects` is an internal subroutine, so it is inside the program rather than a module procedure. Its local `s4` is initialized, moved to `(5, 6)`, printed, and finalized when the subroutine returns. That is the single `shape_destructor()` just before the next `shape_init()`.

`allocate(s2)` creates an allocatable `Shape` without calling the constructor. `init` and `print` show the origin. `deallocate(s2)` is the next destructor line.

`sq % init()` and `c % init()` are the first extended objects. The square print shows side 1 and the origin. The circle print shows the misspelled label, radius 1, and the origin.

Three loops of 20 then build arrays of plain shapes.

- `static_shapes` is a fixed `type(Shape)` array. Each element is initialized and prints the origin. A `type(Shape)` array cannot hold squares. The element itself is a `Shape`.
- `dyn_shapes` is an allocatable array of `Shape`, same prints, and `deallocate` runs the finalizer twenty times. That block of `shape_destructor()` lines is this deallocate.
- `simple_shapes` stores `type(Shape)` pointers. The program allocates each target, initializes it, prints through the pointer, and deallocates the pointer. Those prints are the same origin lines. They are not a new result, and this run does not add a destructor line for those pointer deallocations.

The polymorphic section is the part that uses `class`.

`allocate(p_square)` and `allocate(p_circle)` create a square and a circle on the heap. `init` on each one runs `square_init` and `circle_init`, because the dynamic type supplies the binding. A `class(Shape)` pointer is then aimed at the square and `print` is called. The output is `square_print`, not `shape_print` alone. The same pointer is aimed at the circle and the next print is `cirlce_print`. The declared type of the pointer never changes. The dynamic type does.

The following loop allocates twenty squares, stores the pointers in `class(Shape)` elements, and prints them without `init`. `side` stays 0 on this compiler. `pos` was never written, so the coordinates are whatever was in that memory. Two runs back to back do not print the same numbers. The first uninitialized square of each run is below. The rest of that loop is the same kind of line and is not part of the lesson.

`deallocate(shapes)` frees the array of pointer holders. It does not deallocate the twenty squares those pointers aimed at, and it does not print `shape_destructor` for them.

The triangle is the composition example, and it is also a pointer bug.

```fortran
p_p0 => p_triangle % get_point(1)
p_p1 => p_triangle % get_point(1)
p_p2 => p_triangle % get_point(1)
```

All three calls pass index 1. `p_p0`, `p_p1`, and `p_p2` are three names for vertex 1. The later `set_pos` calls overwrite that one vertex, and the last call wins, so vertex 1 is `(1, 1)`. Vertices 2 and 3 stay at the origin from `triangle_init`. A call with indices 1, 2, and 3 would have placed the three corners the comments suggest. `deallocate(p_triangle)` frees the triangle object. The three `Point` targets are a separate allocation and this program does not free them.

## Output of one run

The full printout is 417 lines. The first 34 lines are the constructor, `make_objects`, the allocatable shape, and the first square and circle. The static and allocatable arrays repeat `shape_init` / `shape_print` / origin. Those repeats are the loops of 20 described above.

```{literalinclude} code/general_oop/opening.txt
:language: text
```

The two initialized polymorphic objects print real values. The `-----` lines are the prints in `main` around that demonstration.

The first uninitialized square from two consecutive runs:

```{literalinclude} code/general_oop/uninitialized_a.txt
:language: text
```

```{literalinclude} code/general_oop/uninitialized_b.txt
:language: text
```

Thirty-seven lines differ between those two runs, and they are all in this uninitialized block. `side` is 0 both times. The coordinates are not a result of the program.

The triangle is the same on both runs, because nothing in that path reads uninitialized memory.

```{literalinclude} code/general_oop/triangle.txt
:language: text
```

## What `-Wall` adds

The CMake build does not pass `-Wall`, so the configure-and-build transcript is clean. Compiling the same two files with warnings names three things the lesson already used: the unused `Particle`, the unused finalizer dummy, and the unused pointer in `triangle_print`.

```{literalinclude} code/general_oop/gfortran_wall.log
:language: text
```

## CMake

```{literalinclude} code/general_oop/CMakeLists.txt
:language: cmake
```

`cmake_minimum_required(VERSION 3.5)` is the line CMake 3.31 warns about. The Apple test sets a Homebrew path for `gfortran` and does nothing on this Linux machine. `project(oop1 LANGUAGES Fortran)` is why the executable is `oop1` and why only the Fortran compiler is detected. `CMAKE_INCLUDE_CURRENT_DIR ON` puts the source directory and the build directory on the compiler's include path, which is where `shape_classes.mod` has to be found when `main.f90` is compiled. `file(GLOB)` picks up `shape_classes.f90` and `main.f90`. A third `.f90` dropped into the directory would be ignored until CMake is run again.

Configure, from this machine. The Fortran compiler it found is `/usr/bin/f95`, which is gfortran 14.2.0.

```{literalinclude} code/general_oop/cmake_configure.log
:language: text
```

The build directory in that log is `/tmp/oop_learn/general_oop/build`. The transcript below drops that prefix. Each real compile line also carried `-I` of the build directory and `-I` of the source directory.

```{literalinclude} code/general_oop/cmake_build.log
:language: text
```

CMake compiles `shape_classes.f90` first because `main.f90` uses the module. It copies `shape_classes.mod` into the target directory, compiles `main.f90`, and links both objects with `f95`. The link line has no extra libraries. The Fortran runtime is pulled in by the `f95` driver.

Running `./oop1` produced the 417 lines this page quotes.

## Source

```{literalinclude} code/general_oop/shape_classes.f90
:language: fortran
```

```{literalinclude} code/general_oop/main.f90
:language: fortran
```
