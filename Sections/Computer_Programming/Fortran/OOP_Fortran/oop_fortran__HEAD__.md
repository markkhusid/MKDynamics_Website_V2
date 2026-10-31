# Object-oriented Fortran

Created with Grok Build

Source code by [Jonas Lindemann](https://github.com/jonaslindemann), from the [oop_fortran](https://github.com/jonaslindemann/oop_fortran) repository.

The source is copied here once, under `code/`, and the pages below walk through every procedure. Each section shows the procedure, then what that procedure does. Where a procedure calculates a number, the formula is written next to the lines that implement it. The lecture PDF stays in that repository.

The theme is one idea used four ways. A Fortran derived type is the object. A type-bound procedure is the method. `class(...)` is what makes the method follow the dynamic type. `private` hides the data. `extends` is inheritance. The later examples use that same shape for a bar element and for a box of particles, and `bind(C)` is how the Fortran objects are called from C++.

The four programs were configured and built on this machine with CMake 3.31, gfortran 14.2.0, and g++ 14.2.0. The Qt particle window was built against Qt 6.8.2 and recorded while the controls were used. Each page has the configure log, the compiler commands, and the output of the run.

## What the Fortran is teaching

A derived type collects data the way a C struct does. This is a derived type with no methods. The program in `general_oop` declares one and never uses the variable.

```fortran
type Particle
    real :: pos(3)
    real :: vel(3)
    real :: mass
end type
```

`pos(3)` is a three-component position, `vel(3)` is a velocity, and `mass` is a scalar. There is no `contains` section, so the type has no procedures and no finalizer.

A type becomes an object when procedures are bound to it. The binding names the method the caller writes. The procedure after `=>` is the subroutine that actually runs.

```fortran
type Shape
    private
    real :: pos(2)
contains
    procedure :: init => shape_init
    procedure :: print => shape_print
    final :: shape_destructor
end type
```

`private` on the type means only the module that defines the type can touch `pos`. Callers go through the procedures. That is the encapsulation. `private` on one component, rather than on the whole type, hides that component and leaves the others visible.

`call s % print()` is the call. Fortran passes `s` as the first argument, the passed-object dummy. Inside the module that dummy is written `class(Shape) :: this`, so the same subroutine can run for a `Shape` and for any type that extends `Shape`. The attribute that says the object is passed is the default. The source does not write `PASS`.

```fortran
subroutine shape_init(this)

    class(Shape) :: this

    print*, 'shape_init()'
    this % pos = (/ 0.0, 0.0 /)

end subroutine
```

The body prints `shape_init()` and stores the origin in the private array. The array constructor `(/ 0.0, 0.0 /)` is the two components of `pos`.

`class` and `type` are different declarations.

- `type(Shape)` holds a `Shape`. An assignment from a `Square` keeps the `Shape` part. The extra `side` component is sliced away.
- `class(Shape)` is polymorphic. A `class(Shape)` pointer can point at a `Shape`, a `Square`, or a `Circle`. The call `call p % print()` uses the binding of the object that was allocated.

`extends(Shape)` makes `Square` contain a `Shape` plus its own components. A binding written again on `Square` overrides the parent's binding. `square_init` still calls `shape_init` by name, which is how the child reuses the parent through the procedure name rather than the overridden binding.

A generic interface with the same name as the type replaces the automatic structure constructor.

```fortran
interface Shape
    module procedure shape_constructor
end interface
```

After that, `Shape()` calls `shape_constructor`.

```fortran
function shape_constructor() result(shape_inst)

    type(Shape) :: shape_inst

    print*, 'shape_constructor()'
    call shape_init(shape_inst)

end function
```

The result is `type(Shape)`, a real `Shape`. The function result is a temporary. The `final` subroutine runs when that temporary is destroyed, which is why the first lines of the shape program are the constructor and then the destructor, before the object you stored has been printed.

`final` is a subroutine the language calls when an object of that type goes away. The dummy of a final subroutine is `type(Shape)`. On the gfortran 14.2.0 run recorded here, the finalizer prints for the constructor temporaries, for one local, for one allocatable, and for an allocatable array that is deallocated. The pages say which of those lines are in the output.

These examples do not use `abstract` types or `deferred` bindings. Every binding names a real procedure. A later program can add an abstract shape that only the extensions are allowed to construct. That is the step these examples leave open.

## What CMake does

CMake is the build description. It does not compile anything by itself. `cmake -S <source> -B <build>` reads `CMakeLists.txt`, finds the compilers, and writes a Makefile into a separate build directory. `cmake --build <build>` runs that Makefile. Keeping the build directory outside the source directory means the `.o` files and the `.mod` files never sit next to the Fortran.

The three Fortran programs share this list. The project name is the only line that changes.

```cmake
cmake_minimum_required(VERSION 3.5)

if (APPLE)
        set(CMAKE_Fortran_COMPILER "/usr/local/bin/gfortran")
endif()

project(oop1 LANGUAGES Fortran)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

file(GLOB fortran_files *.f90)

add_executable(oop1 ${fortran_files})
```

The same five ideas show up in each list.

- `cmake_minimum_required` says which CMake language the file was written for. These files say 3.5. CMake 3.31 on this machine still reads that and configures the projects. The sources were left as they are.
- `project(... LANGUAGES ...)` names the target and turns on compilers. A Fortran-only project finds `f95` or `gfortran`. A project that lists `CXX` before `Fortran` links the executable with `c++` and adds `-lgfortran`, because the C++ runtime is the main link and the Fortran runtime is a library.
- `file(GLOB *.f90)` collects every Fortran file in the directory at configure time. Adding a file later does not update the build until CMake is run again. That is the usual tradeoff of `GLOB`.
- `add_executable` turns that list into a program. The name of the program is the first argument, which can differ from the name of the `program` statement in the Fortran.
- `target_link_libraries` adds libraries. Only the Qt program needs it. The Fortran programs have their runtime attached by the Fortran link line.

The Apple test sets a Homebrew path for `gfortran` and does nothing on this Linux machine. `CMAKE_INCLUDE_CURRENT_DIR ON` puts the source directory and the build directory on the compiler's include path, which is where a `.mod` file has to be found when a later file uses the module.

The Qt list adds three switches that are the whole reason that build looks different.

```cmake
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)
```

`CMAKE_AUTOMOC` runs `moc` on headers that contain `Q_OBJECT`. `CMAKE_AUTOUIC` runs `uic` on `mainwindow.ui` and generates `ui_mainwindow.h`. `CMAKE_AUTORCC` would compile a resource file. This project has no `.qrc`, so that switch has nothing to compile. `find_package` locates Qt 6, then Qt 5 if Qt 6 is absent, and imports the `Widgets` target that carries the include paths and the libraries.

Each program page shows that project's `CMakeLists.txt`, then the configure log from this machine, then the compiler and link lines. The verbose Make output also contains directory bookkeeping. The build transcripts keep the compiler, the source file, and the link line. Include flags such as `-I` of the build directory are omitted in that transcript. They were present on the real command because `CMAKE_INCLUDE_CURRENT_DIR` is `ON`.

`fpm` on this machine is a small gfortran wrapper that reports version 0.0.1. It is the local wrapper, and it is separate from the Fortran Package Manager. These examples ship CMake lists, and the CMake output is part of what the pages are here to show, so the builds below are CMake builds.

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
