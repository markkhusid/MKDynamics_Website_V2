# Fortran objects behind a Qt window

Created with Grok Build

The particle program is the same Fortran style as the [shape classes](general_oop.md), with the call direction reversed from the [Fortran-calls-C++ example](fortran_cpp.md). `ParticleSystem` and `ParticleSimulation` are derived types with private data and type-bound procedures. A Fortran module holds one of each and publishes `bind(C)` procedures. The C++ window never sees a particle array. It calls those procedures, and `paintEvent` draws whatever they return.

Qt Widgets 6.8.2 supplied the window. The clip below is that window, recorded on this machine while the pointer used Pause, the scaling slider, and Update.

:::{figure} oop_fortran_particles.mp4
:align: center

The particle window. The pointer pauses the motion, drags the scaling slider to the right, sets 80 particles with radii 0.012 and 0.040, and clicks Update. The recording is 16.8 seconds at 894 by 710.
:::

```{figure} images/cpp_fortran_window.png
:alt: The Qt window with 500 particles
:align: center
:class: clickable-figure

The window as it opens. Five hundred particles, minimum radius 0.005, maximum radius 0.015, scaling 600.
```

```{figure} images/cpp_fortran_updated.png
:alt: The same window after Update, with 80 particles
:align: center
:class: clickable-figure

Later in the recording, the fields read 80, 0.012, and 0.040, and the pointer is on Update.
```

```{figure} images/cpp_fortran.png
:alt: Yellow for a small radius, white for a large radius
:align: center
:class: clickable-figure

The color rule in paintEvent. A small radius is yellow. A large radius is white.
```

## `mf_datatypes` and `mf_utils`

`dp` is `real64`, `sp` is `real32`, and `ik` is `int32`. `pi` is a double constant used when a random direction is turned into a velocity vector. This is not the [bar program's](simple_frame_2d.md) `mf_datatypes`. The names match. The contents do not. Each program compiles the copy that sits in its own directory.

`mf_utils` here is a smaller printer than the bar program's copy. `set_print_format` takes width, decimals, and a real edit code. It has no integer-code argument, so it does not have that assignment bug. The particle window never calls the printers. The console driver does not call them either. They are linked because `particle_interface` uses the module.

## `init_random_seed`

`particle_utils` has one subroutine. It reads `date_and_time` into an eight-element integer array, asks `random_seed` how long the seed is, and fills every seed element with `values(8)`, which is the millisecond field. The generator is then seeded from that array. Two starts in the same millisecond get the same sequence. A local `r` is declared and unused. `-Wall` reports it.

`particle_system_init` calls this once, before it draws positions and radii.

## `ParticleSystem`

The type is the box of particles. Everything is `private`: the count, the speed `m_v0`, the radius limits, a time step `m_dt` that nothing ever sets, and three pointers. `m_pos` is `(n, 2)`, `m_vel` is `(n, 2)`, and `m_r` is `(n)`. They are pointers rather than allocatables so the accessors can hand the caller a pointer to the same memory.

The bindings are the methods. `init`, `destroy`, `print`, `write_sizes`, and `write_positions` change or report the whole set. `count`, `v0`, `rmin`, `rmax`, `dt`, `positions`, `velocities`, and `radius` are the readers. `set_v0`, `set_rmin`, and `set_rmax` are the writers. `particle` and `particle_count` are the two the C++ window uses on every frame.

### `particle_system_init`

The count is required. The radius limits and the speed are optional. Missing values become `v0 = 0.001`, `rmin = 0.005`, and `rmax = 0.015`, which are also the numbers in the window's text fields.

The subroutine allocates the three arrays, seeds the generator, fills `m_pos` and `m_r` with `random_number`, and gives every particle a speed of `v0` in a random direction. The angle is `alfa = 2 π u` for a uniform `u`, and the components are `v0 cos alfa` and `v0 sin alfa`. The radius is then scaled from the unit interval into `[rmin, rmax]`.

Positions land in the unit square because `random_number` returns values in `[0, 1)`. The window draws that square. A particle is not kept inside the square by this subroutine. The simulation does that later, and only by flipping a velocity.

### `particle_system_destroy`

Deallocates the three arrays and sets the count to `-1`. The window calls the C wrapper of this from the `MainWindow` destructor, and again when Update builds a new system.

### `particle_system_print`

Prints the maximum and minimum of each coordinate. Neither driver calls it. The integer `i` is unused, and `-Wall` says so.

### `particle_system_write_sizes` and `particle_system_write_positions`

Both open `particle.state` with `ACCESS='APPEND'`, write the count as an integer of width 10, write one record per particle, and close the file. `write_sizes` writes `m_r(i)` with format `(2F12.5)`. The format asks for two reals and the output list has one, so each radius is a single `F12.5` number. `write_positions` writes `m_pos(i, :)`, which really is two reals, so each position line has `x` and `y`.

The console driver is what calls these. The window calls `run_iteration`, which does not write the file.

### The readers and writers

`v0`, `rmin`, `rmax`, and `dt` return the matching component. `dt` returns `m_dt`, and `init` never assigns `m_dt`, so a caller of `dt()` would print an undefined value. The stepper does not call `dt()`. It computes a step from `rmin` and `v0` when the caller does not pass one.

`set_rmin`, `set_rmax`, and `set_v0` store one number. They do not rebuild the arrays. The window does not call them. Update destroys the system and initializes a new one, which is a different path.

`positions`, `velocities`, and `radius` return pointers associated with the private arrays. The simulation writes through those pointers. That is why the private attribute does not stop the stepper from moving particles: the stepper is in the same module.

### `particle_system_particle` and `particle_system_particle_count`

`particle` copies `x`, `y`, and `r` for a 1-based index out through `intent(out)` arguments. This is the procedure the paint loop calls. `particle_count` returns `size(m_pos, 1)`, the allocated row count, rather than `m_n_particles`. After a normal `init` those two numbers match. After `destroy`, the arrays are gone and `particle_count` must not be called.

## `ParticleSimulation`

The simulator holds one `class(ParticleSystem)` pointer. It does not own the particles. `init` saves the pointer the caller already allocated. The bindings are `update`, `check_boundaries`, `check_collisions`, `run`, and `run_iteration`.

### `particle_simulator_update`

Reads positions, velocities, and radii through the accessors. The radius pointer is unused. The index `i` is unused. `-Wall` reports `i`.

If the caller passes `dtin`, that is the step. If not, the step is `rmin / (10 v0)`. With the defaults that is `0.005 / 0.01 = 0.5`. A particle at speed `0.001` moves `0.0005` per step, in a square of side 1. The window never passes a step, so every frame uses that formula, including after you change the radii and click Update.

The update itself is one array assignment: `pos = pos + vel * dt`.

### `particle_simulator_check_boundaries`

For each particle, if the center has gone past a wall by less than a radius, the matching velocity component is negated. The four tests are `x < r`, `x > 1 - r`, `y < r`, and `y > 1 - r`. The position is not moved back inside. A center that stays past the wall will have its velocity flipped on the next step as well, so a particle that has penetrated a wall can jitter instead of settling on the boundary.

### `particle_simulator_check_collisions`

The nested loop compares each pair once, `j` from `i + 1` to the count. `n` is the vector from `i` to `j`. `d` is its length. `vdiff` is `vel(j) - vel(i)`.

A pair collides when the circles overlap, `d < r(i) + r(j)`, and the particles are approaching, `n · vdiff < 0`. The response assumes equal mass and exchanges the component of velocity along `n`:

$$
q = \frac{v_\mathrm{diff} \cdot n}{n \cdot n}, \qquad
v_i \leftarrow v_i + q\, n, \qquad
v_j \leftarrow v_j - q\, n
$$

`r1`, `r2`, `vi`, `vj`, `si`, and `sj` are declared and unused. The radii actually used are `r(i)` and `r(j)`. `-Wall` reports the unused locals. The cost is the double loop. Five hundred particles are about `500 × 499 / 2` pairs on every frame, which is why the window's timer makes the process busy.

### `particle_simulator_run` and `particle_simulator_run_iteration`

`run` writes the radius block once, then for each requested iteration checks collisions, checks walls, steps, and appends the positions. The console program calls `run(1000)`.

`run_iteration` is one pass of the same three calls and does not touch `particle.state`. The timer calls this.

## `particle_interface`

The module is the C API. Two module variables, `p_particle_system` and `p_particle_simulation`, are `private` polymorphic pointers. Every `bind(C)` procedure uses those two objects. There is one system in the process, not one per window.

### `particle_system_init`

The C name is `particle_system_init`. The Fortran name is `particle_intf_system_init`. `n`, `min_radius`, `max_radius`, and `v0` all have `value`, so they match `int` and `double` parameters passed by value. The body prints `Allocating particle system...`, allocates both objects, and calls the type-bound `init` on each. When standard output is a terminal, that line shows up. When this page's GUI run redirected standard output to a file, the Fortran buffer was still holding it at exit, so the GUI log did not contain the line. The console driver does not go through this interface.

### `particle_system_params`

Copies `rmin`, `rmax`, and `v0` out through `intent(out)` doubles. Those are pointers on the C side. `paintEvent` uses the two radii to scale the color. `v0` is retrieved and not used by the painter.

### `particle_system_particle`

The Fortran arguments are `idx`, `x`, `y`, and `r`, with `idx` passed by value. The C header names the last pointer `z`.

```c
void particle_system_particle(int idx, double* x, double* y, double* z);
```

The value written through that pointer is the radius, not a third coordinate. The painter stores it in `r` and draws a circle. The comment in the header that says `z` is the wrong name for a correct address.

### `particle_system_particle_count`

Returns `integer(c_int)`. The C header returns `int`. The body calls the type-bound `particle_count`.

### `particle_system_run_iteration` and `particle_system_destroy`

One calls `run_iteration`. The other prints `Deallocating particle system ...` and deallocates both pointers. The same buffering note applies to that print.

The header also contains a block of Fortran, commented out with `/* */`. It is an older sketch of the interface, with different names and a fixed count of 1000. It is not compiled.

## The C++ window

### `main`

`main` constructs a `QApplication`, a `MainWindow`, shows it, and enters the event loop. There is no particle code here. Building the window runs `MainWindow`'s constructor, and that constructor creates the Fortran system.

### `MainWindow`

The members are the particle count, the two radii, `m_v0`, a `m_firstTime` flag, and `m_maxSize`. The defaults written in the initializer list are 500, 0.005, 0.015, 0.001, `true`, and 600. There is no widget for `m_v0`. Update cannot change the speed. It stays 0.001 unless something else assigns the member, and nothing does.

The constructor calls `setupUi`, which is generated from `mainwindow.ui`, then `updateControls`, then `createParticleSystem`. The destructor calls `particle_system_destroy` and deletes the generated UI object.

`updateParams` reads the spin box into `m_nParticles`. It parses the two radius fields with `toDouble`. A field that does not parse is left unchanged, because `ok` is tested before the assignment. It does not read a speed. It finishes by writing the members back into the widgets, so a rejected parse snaps the text back to the old value.

`updateControls` is that write-back: the spin box, both radius fields, and the slider. The slider value is `int(m_maxSize)`.

`createParticleSystem` stops the timer, destroys the Fortran system unless this is the first call, calls `particle_system_init` with the four members, clears `m_firstTime`, and starts the timer.

`on_actionRun_triggered` starts the timer. `on_actionStop_triggered` stops it. The toolbar text for that action is Pause, not Stop. The name `actionStop` is the object name in the `.ui` file. Qt connects the action to the slot by that name because the slot follows the pattern `on_<object>_<signal>`.

`on_maxSizeSlider_valueChanged` passes the integer to `ParticleCanvas::setMaxSize`. Dragging the slider rescales the drawing on the next paint. It does not rebuild the particles and it does not change a Fortran value.

`on_actionUpdate_triggered` runs `updateParams` and `createParticleSystem`. That is the button in the recording. The fields were set to 80, 0.012, and 0.040, and Update constructed a new system with those numbers.

File → New and File → Open are actions in the menu. No slot is connected to them. Choosing them does nothing.

The `.ui` file puts Run, Pause, and Update on the toolbar. The spin box runs from the default up to 10000, with a step of 100. The slider runs from 100 to 2000 and starts at 600. The window's designed size is 894 by 709. That is the size in the recording, plus one row so the H.264 frame height is even.

### `ParticleCanvas`

The canvas is a `QWidget` promoted in the `.ui` file. Qt Creator writes that as a custom widget whose header is `particle_canvas.h`. `uic` turns the promotion into a member `ui->drawingArea`.

The constructor creates a `QTimer` owned by the widget and connects `timeout()` to `on_timer_update()`. The connection uses the `SIGNAL` / `SLOT` macros. `m_maxSize` starts at 600, the same default as the window.

`runSimulation` calls `m_timer->start()` with no interval. A `QTimer` interval of 0 fires whenever the event loop is idle. The window therefore steps the particles as fast as the collision loop and the paint allow. `stopSimulation` stops the timer. Pause in the recording is that call. The frames sit still while the timer is stopped, which is why the pointer can edit the fields without the collision loop eating the clicks.

`setMaxSize` stores the slider value. The next `paintEvent` uses it.

`on_timer_update` calls `particle_system_run_iteration` and then `repaint()`.

`paintEvent` fills the widget with a black rectangle and a blue pen, asks Fortran for the count and the radius limits, and draws each particle from index 1 through `count`. The color is

$$
c = 255 \frac{r - r_\min}{r_\max - r_\min}
$$

with red and green fixed at 255. A radius equal to `rmin` is yellow, `QColor(255, 255, 0)`. A radius equal to `rmax` is white, `QColor(255, 255, 255)`. The circle is centered at

$$
\left(\frac{w}{2} - \frac{s}{2} + x s,\; \frac{h}{2} - \frac{s}{2} + y s\right)
$$

with radius `r * s`, where `s` is `m_maxSize` and `(x, y)` is the Fortran position in the unit square. Dragging the slider to the right increases `s`, so the same unit square is drawn across more pixels and the disks grow. That is the slider motion in the clip.

## The console driver

`main.f90` is a second program in the same directory. It is not in the CMake target. `PROJECT_SOURCES` lists the Fortran modules and the C++ window, and it does not list `main.f90`. Building the window does not build this driver.

It allocates a system and a simulation on polymorphic pointers, initializes 1000 particles with the default radii and speed, and calls `run(1000)`. There is no `print`. Standard output is empty. The result is the file `particle.state` in the working directory.

Compiled and run on this machine:

```text
$ gfortran -O2 -c mf_datatypes.f90 mf_utils.f90 particle_utils.f90 particle_classes.f90 main.f90
$ gfortran -O2 -o particle_console mf_datatypes.o mf_utils.o particle_utils.o particle_classes.o main.o
```

The run took 2 seconds. `particle.state` is 24 MB and 1,002,001 lines. The first line of the radius block is the count 1000, then one radius per line. Each of the 1000 iterations appends the count and 1000 position lines. `1001 + 1000 × 1001 = 1002001`. The coordinates are one draw of the random generator. A second run will not match them.

The excerpt is the start of the radius block, the start of the first position block, and the last three lines of the file.

```{literalinclude} code/cpp_fortran/logs/console_particle_state.txt
:language: text
```

## Warnings

`-Wall` on the Fortran files, separate from the CMake build:

```{literalinclude} code/cpp_fortran/logs/gfortran_wall.log
:language: text
```

## CMake

```{literalinclude} code/cpp_fortran/CMakeLists.txt
:language: cmake
```

`project` enables C, C++, and Fortran. The C compiler is detected because Qt's own checks use it. None of this project's sources are C.

`CMAKE_AUTOUIC`, `CMAKE_AUTOMOC`, and `CMAKE_AUTORCC` are the three generators. `CMAKE_CXX_STANDARD 17` matches the language Qt 6 headers use. `find_package(QT NAMES Qt6 Qt5 ...)` and the following `find_package(Qt${QT_VERSION_MAJOR} ...)` are the usual Qt 5-or-6 form. On this machine that resolved to Qt 6.8.2 Widgets.

`qt_add_executable` is the Qt 6 way to build the program. The `else` branch is the Qt 5 form, and it was not taken. `target_link_libraries` attaches `Qt6::Widgets`, which brings `Qt6::Gui`, `Qt6::Core`, and the OpenGL libraries those targets need. The bundle and install lines are for macOS and for `cmake --install`. The recording did not install anything. It ran the binary from the build directory.

`main.f90` is absent from `PROJECT_SOURCES`, as noted above. `particle_interface.h` is listed so the build rebuilds when the C prototypes change.

Configure on this machine. CMake warns that the `VERSION 3.5` requirement is old. It also reports that the XKB development files were not found. The runtime library `libxkbcommon` is on the machine, the link succeeded, and the window ran. The XKB line is that development-package check, and it did not stop the build.

```{literalinclude} code/cpp_fortran/logs/cmake_configure.log
:language: text
```

The build directory is `/tmp/oop_learn/cpp_fortran/build`. The transcript drops that prefix, the long `-I` and `-D` lists, and Make's directory chatter. What remains is the real order: `moc` on the two headers that contain `Q_OBJECT`, `uic` on `mainwindow.ui`, five Fortran compiles, four C++ compiles including the generated `mocs_compilation.cpp`, and the link.

```{literalinclude} code/cpp_fortran/logs/cmake_build.log
:language: text
```

The link line is `/usr/bin/c++` plus the Qt libraries, `-lgfortran`, and `-lquadmath`. That is the same reason as in the small Fortran-calls-C++ program: the driver has to be the C++ compiler, and the Fortran runtime is an extra library. The `rpath` points at the Qt 6 library directory so the dynamic loader finds `libQt6Widgets.so.6` when the binary starts.

## Source

```{literalinclude} code/cpp_fortran/mf_datatypes.f90
:language: fortran
```

```{literalinclude} code/cpp_fortran/mf_utils.f90
:language: fortran
```

```{literalinclude} code/cpp_fortran/particle_utils.f90
:language: fortran
```

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
```

```{literalinclude} code/cpp_fortran/particle_interface.f90
:language: fortran
```

```{literalinclude} code/cpp_fortran/particle_interface.h
:language: cpp
```

```{literalinclude} code/cpp_fortran/main.cpp
:language: cpp
```

```{literalinclude} code/cpp_fortran/mainwindow.h
:language: cpp
```

```{literalinclude} code/cpp_fortran/mainwindow.cpp
:language: cpp
```

```{literalinclude} code/cpp_fortran/particle_canvas.h
:language: cpp
```

```{literalinclude} code/cpp_fortran/particle_canvas.cpp
:language: cpp
```

```{literalinclude} code/cpp_fortran/mainwindow.ui
:language: xml
```

```{literalinclude} code/cpp_fortran/main.f90
:language: fortran
```
