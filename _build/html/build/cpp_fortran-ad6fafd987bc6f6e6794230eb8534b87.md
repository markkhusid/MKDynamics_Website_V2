# Fortran objects behind a Qt window

Created with Grok Build

Source code by [Jonas Lindemann](https://github.com/jonaslindemann), from the [oop_fortran](https://github.com/jonaslindemann/oop_fortran) repository.

The particle program is the same Fortran style as the [shape classes](general_oop.md), with the call direction reversed from the [Fortran-calls-C++ example](fortran_cpp.md). `ParticleSystem` and `ParticleSimulation` are derived types with private data and type-bound procedures. A Fortran module holds one of each and publishes `bind(C)` procedures. The C++ window never sees a particle array. It calls those procedures, and `paintEvent` draws whatever they return.

Each section shows the procedure, then what it does. A procedure that computes a position, a radius, a time step, a collision, or a color has the formula next to the lines that implement it.

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

## `mf_datatypes`

```{literalinclude} code/cpp_fortran/mf_datatypes.f90
:language: fortran
```

`dp` is `real64`, `sp` is `real32`, and `ik` is `int32`. `pi` is the double constant used when a random direction becomes a velocity. This is separate from the [bar program's](simple_frame_2d.md) `mf_datatypes`. The names match. The contents differ. Each program compiles the copy that sits in its own directory.

$$
\pi = 3.141592653589793238462643383279502884197
$$

That literal is the value of `pi`. The velocity loop multiplies by it.

## `mf_utils`

This copy is a smaller printer than the bar program's copy. It has no integer matrix printer and no integer edit code.

```{literalinclude} code/cpp_fortran/mf_utils.f90
:language: fortran
:lines: 5-23
```

The defaults are width 10, decimals 4, and real edit descriptor `G`.

### `set_print_format`

```{literalinclude} code/cpp_fortran/mf_utils.f90
:language: fortran
:lines: 27-45
```

A present width, decimal count, or one-character code replaces the matching variable. There is no integer-code argument. The particle window never calls this subroutine. The console driver does not call it either. `particle_interface` uses the module, which is why the file is on the link line.

### `print_matrix_d` and `print_matrix_s`

```{literalinclude} code/cpp_fortran/mf_utils.f90
:language: fortran
:lines: 47-104
```

```{literalinclude} code/cpp_fortran/mf_utils.f90
:language: fortran
:lines: 106-163
```

These build a `G` format the same way the [bar printer](simple_frame_2d.md) does. The title ends in `DP` or `SP`. With the defaults and four columns the data format is `(4G10.4)`. Nothing in the particle program calls them.

### `print_vector_d` and `print_vector_s`

```{literalinclude} code/cpp_fortran/mf_utils.f90
:language: fortran
:lines: 165-218
```

```{literalinclude} code/cpp_fortran/mf_utils.f90
:language: fortran
:lines: 220-273
```

One `write` prints the whole vector. The titles say `DP` and `SP`. Nothing in the particle program calls them.

### The random helpers and `init_rand`

```{literalinclude} code/cpp_fortran/mf_utils.f90
:language: fortran
:lines: 275-286
```

`random_number` fills the array with $U \in [0, 1)$, and the next statement scales it:

$$
A = a_{\min} + (a_{\max} - a_{\min})\, U
$$

`A = randMin + (randMax-randMin) * A` is that formula. The particle system does not call `rand_mat_d`. It calls `random_number` itself and scales the radii with the same expression, written out in `particle_system_init`.

```{literalinclude} code/cpp_fortran/mf_utils.f90
:language: fortran
:lines: 288-325
```

`rand_mat_s`, `rand_vec_d`, and `rand_vec_s` are the same scaling for the other ranks and kinds.

```{literalinclude} code/cpp_fortran/mf_utils.f90
:language: fortran
:lines: 327-336
```

`init_rand` seeds the generator from the millisecond field `values(8)`. The local `r` is declared and never used. The particle system calls `init_random_seed` in `particle_utils` instead of this subroutine.

## `init_random_seed`

```{literalinclude} code/cpp_fortran/particle_utils.f90
:language: fortran
```

`particle_utils` has this one subroutine. It reads `date_and_time` into an eight-element integer array, asks `random_seed` how long the seed is, and fills every seed element with `values(8)`, the millisecond field. The generator is then seeded from that array. Two starts in the same millisecond get the same sequence. The local `r` is declared and never used.

`particle_system_init` calls this once, before it draws positions and radii.

## `ParticleSystem`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 8-41
```

The type is the box of particles. Everything is `private`: the count, the speed `m_v0`, the radius limits, a time step `m_dt` that `init` never sets, and three pointers. `m_pos` is $(n, 2)$, `m_vel` is $(n, 2)$, and `m_r` is $(n)$. They are pointers so the accessors can hand the caller a pointer to the same memory.

The bindings are the methods. `init`, `destroy`, `print`, `write_sizes`, and `write_positions` change or report the whole set. `count`, `v0`, `rmin`, `rmax`, `dt`, `positions`, `velocities`, and `radius` are the readers. `set_v0`, `set_rmin`, and `set_rmax` are the writers. `particle` and `particle_count` are the two the C++ window uses on every frame.

### `particle_system_init`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 57-105
```

The count is required. The radius limits and the speed are optional. Missing values become

$$
v_0 = 0.001, \qquad r_\min = 0.005, \qquad r_\max = 0.015
$$

which are the numbers in the window's text fields and in the three `else` branches.

The subroutine allocates the three arrays, seeds the generator, and fills `m_pos` and `m_r` with `random_number`. Positions land in the unit square because `random_number` returns values in $[0, 1)$. The window draws that square.

Each particle then gets a speed of $v_0$ in a random direction. `random_number(alfa)` draws $u \in [0, 1)$, and the next three lines are

$$
\alpha = 2\pi u, \qquad
v_x = v_0 \cos\alpha, \qquad
v_y = v_0 \sin\alpha
$$

`alfa = 2.0_dp*pi*alfa` overwrites the uniform draw with the angle. `m_vel(i,1)` and `m_vel(i,2)` are $v_x$ and $v_y$. The speed of every particle is $v_0$, because $\cos^2\alpha + \sin^2\alpha = 1$.

The radius line scales the unit draw already stored in `m_r`:

$$
r = r_\min + u\,(r_\max - r_\min)
$$

`this % m_r = this % m_rmin + this % m_r * (this % m_rmax - this % m_rmin)` is that formula, applied to the whole array at once. A particle is not kept inside the square by this subroutine. The simulation does that later, and only by flipping a velocity.

### `particle_system_destroy`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 107-114
```

Deallocates the three arrays and sets the count to $-1$. The window calls the C wrapper of this from the `MainWindow` destructor, and again when Update builds a new system.

### `particle_system_print`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 116-126
```

Prints the maximum and minimum of each coordinate, `maxval` and `minval` of the two columns of `m_pos`. Neither driver calls it. The integer `i` is declared and never used.

### `particle_system_write_sizes` and `particle_system_write_positions`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 128-154
```

Both open `particle.state` with `ACCESS='APPEND'`, write the count as an integer of width 10, write one record per particle, and close the file.

`write_sizes` writes `m_r(i)` with format `(2F12.5)`. The output list has one real, so each radius record is one `F12.5` number. `write_positions` writes `m_pos(i, :)`, which is two reals, so each position line has $x$ and $y$ in two `F12.5` fields.

The console driver is what calls these. The window calls `run_iteration`, which does not write the file.

### Readers and writers

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 156-249
```

`v0`, `rmin`, `rmax`, and `dt` return the matching component. `dt` returns `m_dt`, and `init` never assigns `m_dt`, so a caller of `dt()` reads a component that this program never sets. The stepper does not call `dt()`. It computes a step from $r_\min$ and $v_0$ when the caller does not pass one.

`set_rmin`, `set_rmax`, and `set_v0` store one number. They do not rebuild the arrays. The window does not call them. Update destroys the system and initializes a new one.

`positions`, `velocities`, and `radius` return pointers associated with the private arrays. The simulation writes through those pointers. The stepper is in the same module, so the private attribute still allows that write.

`count` returns `m_n_particles`.

### `particle_system_particle` and `particle_system_particle_count`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 251-270
```

`particle` copies $x$, $y$, and $r$ for a 1-based index out through `intent(out)` arguments:

$$
x = p_{i,1}, \qquad y = p_{i,2}, \qquad r = r_i
$$

This is the procedure the paint loop calls. `particle_count` returns `size(m_pos, 1)`, the allocated row count, rather than `m_n_particles`. After a normal `init` those two numbers match. After `destroy`, the arrays are gone and `particle_count` must not be called.

## `ParticleSimulation`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 43-53
```

The simulator holds one `class(ParticleSystem)` pointer. It does not own the particles. `init` saves the pointer the caller already allocated. The bindings are `update`, `check_boundaries`, `check_collisions`, `run`, and `run_iteration`.

### `particle_simulator_init`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 274-281
```

`this % m_psys => psys` stores the caller's pointer. The simulator and the caller then name the same particle system.

### `particle_simulator_update`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 283-306
```

Reads positions, velocities, and radii through the accessors. The radius pointer `r` is fetched and never used. The index `i` is declared and never used.

If the caller passes `dtin`, that is the step. If not, the step is

$$
\Delta t = \frac{r_\min}{10\, v_0}
$$

`dt = this % m_psys % rmin()/(10.0_dp*this % m_psys % v0())` is that quotient. With the defaults,

$$
\Delta t = \frac{0.005}{10 \times 0.001} = 0.5
$$

The update itself is one array assignment, `pos = pos + vel * dt`, which is

$$
\mathbf{p} \leftarrow \mathbf{p} + \mathbf{v}\,\Delta t
$$

A particle at speed $0.001$ therefore moves

$$
v_0\,\Delta t = 0.001 \times 0.5 = 5\times 10^{-4}
$$

per step, in a square of side 1. The window never passes a step, so every frame uses this formula, including after you change the radii and click Update. Changing the radii changes $r_\min$ in a new system, and the next default step changes with it. The speed stays $0.001$, because the window has no control for $v_0$.

### `particle_simulator_check_boundaries`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 308-331
```

For each particle, if the center has crossed a wall by less than a radius, the matching velocity component is negated. The four tests are

$$
\begin{aligned}
x < r &\Rightarrow v_x \leftarrow -v_x \\
x > 1 - r &\Rightarrow v_x \leftarrow -v_x \\
y < r &\Rightarrow v_y \leftarrow -v_y \\
y > 1 - r &\Rightarrow v_y \leftarrow -v_y
\end{aligned}
$$

`pos(i,1) < r(i)` and the three lines after it are those four tests. The position is not assigned. A center that stays past the wall has its velocity flipped again on the next step, so a particle that has penetrated a wall can jitter. The test does not look at the sign of the velocity. The `associate` block is commented out. The live code uses the pointers from the three accessor calls.

### `particle_simulator_check_collisions`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 333-374
```

The nested loop compares each pair once, $j$ from $i+1$ to the count. The comment sketches two circles of radii $r_1$ and $r_2$ whose centers are a distance $d$ apart. The locals `r1`, `r2`, `vi`, `vj`, `si`, and `sj` are declared and never used. The radii actually used are `r(i)` and `r(j)`.

For each pair the code builds

$$
\mathbf{n} = \mathbf{p}_j - \mathbf{p}_i, \qquad
d = \sqrt{(x_j-x_i)^2 + (y_j-y_i)^2}, \qquad
\mathbf{v}_{\mathrm{diff}} = \mathbf{v}_j - \mathbf{v}_i
$$

`n = pos(j,:) - pos(i,:)` is $\mathbf{n}$. The `sqrt` of the two squared differences is $d$, which is $|\mathbf{n}|$. `vdiff = vel(j,:) - vel(i,:)` is the relative velocity of particle $j$ as seen from particle $i$.

A pair collides when the circles overlap and the particles are approaching:

$$
d < r_i + r_j \qquad\text{and}\qquad \mathbf{n}\cdot\mathbf{v}_{\mathrm{diff}} < 0
$$

`d<(r(i)+r(j))` and `dot_product(n,vdiff)<0.0_dp` are those two tests. The response assumes equal mass and exchanges the component of velocity along $\mathbf{n}$:

$$
q = \frac{\mathbf{v}_{\mathrm{diff}}\cdot\mathbf{n}}{\mathbf{n}\cdot\mathbf{n}}, \qquad
\mathbf{v}_i \leftarrow \mathbf{v}_i + q\,\mathbf{n}, \qquad
\mathbf{v}_j \leftarrow \mathbf{v}_j - q\,\mathbf{n}
$$

`q = dot_product(vdiff,n)/dot_product(n,n)` is the scalar. Adding `n * q` to `vel(i,:)` and subtracting it from `vel(j,:)` is the exchange. For equal mass, that swap is what an elastic collision does to the relative velocity along the line of centers: the normal component of $\mathbf{v}_{\mathrm{diff}}$ changes sign, and the tangential component is left alone.

The cost is the double loop. Five hundred particles are $500 \times 499 / 2$ pairs on every frame, which is why the window's timer makes the process busy.

### `particle_simulator_run` and `particle_simulator_run_iteration`

```{literalinclude} code/cpp_fortran/particle_classes.f90
:language: fortran
:lines: 376-401
```

`run` writes the radius block once, then for each requested iteration checks collisions, checks walls, steps, and appends the positions. The console program calls `run(1000)`.

`run_iteration` is one pass of the same three calls and does not touch `particle.state`. The timer calls this.

## `particle_interface`

```{literalinclude} code/cpp_fortran/particle_interface.f90
:language: fortran
:lines: 1-16
```

The module is the C API. Two module variables, `p_particle_system` and `p_particle_simulation`, are `private` polymorphic pointers. Every `bind(C)` procedure uses those two objects. There is one system in the process.

### `particle_intf_system_init`

```{literalinclude} code/cpp_fortran/particle_interface.f90
:language: fortran
:lines: 22-37
```

The C name is `particle_system_init`. The Fortran name is `particle_intf_system_init`. `n`, `min_radius`, `max_radius`, and `v0` all have `value`, so they match `int` and `double` parameters passed by value. The body prints `Allocating particle system...`, allocates both objects, and calls the type-bound `init` on each. When standard output is a terminal, that line shows up. When the GUI run that produced the recording redirected standard output to a file, the Fortran buffer was still holding the line at exit, so the saved GUI log did not contain it. The console driver does not go through this interface.

### `particle_intf_system_particle_params`

```{literalinclude} code/cpp_fortran/particle_interface.f90
:language: fortran
:lines: 41-51
```

Copies $r_\min$, $r_\max$, and $v_0$ out through `intent(out)` doubles. Those are pointers on the C side. `paintEvent` uses the two radii to scale the color. `v0` is retrieved and the painter does not use it.

### `particle_intf_system_particle`

```{literalinclude} code/cpp_fortran/particle_interface.f90
:language: fortran
:lines: 55-62
```

The Fortran arguments are `idx`, `x`, `y`, and `r`, with `idx` passed by value. The C header names the last pointer `z`.

```{literalinclude} code/cpp_fortran/particle_interface.h
:language: cpp
:lines: 4-12
```

The value written through that pointer is the radius. The painter stores it in a variable named `r` and draws a circle. The header's name `z` is the name of that radius pointer.

### `particle_intf_system_particle_count`

```{literalinclude} code/cpp_fortran/particle_interface.f90
:language: fortran
:lines: 66-72
```

Returns `integer(c_int)`. The C header returns `int`. The body calls the type-bound `particle_count`.

### `particle_intf_system_run_iteration` and `particle_intf_system_destroy`

```{literalinclude} code/cpp_fortran/particle_interface.f90
:language: fortran
:lines: 76-89
```

One calls `run_iteration`. The other prints `Deallocating particle system ...` and deallocates both pointers. The same buffering note applies to that print.

```{literalinclude} code/cpp_fortran/particle_interface.h
:language: cpp
:lines: 15-42
```

The header also contains a block of Fortran, commented out with `/* */`. It is an older sketch of the interface, with different names and a fixed count of 1000. It is not compiled.

## The C++ window

### `main`

```{literalinclude} code/cpp_fortran/main.cpp
:language: cpp
```

`main` constructs a `QApplication`, a `MainWindow`, shows it, and enters the event loop. There is no particle code here. Building the window runs `MainWindow`'s constructor, and that constructor creates the Fortran system.

### `MainWindow`

```{literalinclude} code/cpp_fortran/mainwindow.h
:language: cpp
```

The members are the particle count, the two radii, `m_v0`, a `m_firstTime` flag, and `m_maxSize`. The slots follow the names of the actions and the slider, which is how Qt connects them.

```{literalinclude} code/cpp_fortran/mainwindow.cpp
:language: cpp
:lines: 9-41
```

The constructor's initializer list sets 500, 0.005, 0.015, 0.001, `true`, and 600. There is no widget for `m_v0`. Update cannot change the speed. It stays 0.001. The constructor calls `setupUi`, which is generated from `mainwindow.ui`, then `updateControls`, then `createParticleSystem`. The destructor calls `particle_system_destroy` and deletes the generated UI object.

```{literalinclude} code/cpp_fortran/mainwindow.cpp
:language: cpp
:lines: 43-69
```

`updateParams` reads the spin box into `m_nParticles`. It parses the two radius fields with `toDouble`. A field that does not parse is left unchanged, because `ok` is tested before the assignment. It does not read a speed. It finishes by writing the members back into the widgets, so a rejected parse snaps the text back to the old value.

`updateControls` is that write-back: the spin box, both radius fields, and the slider. The slider value is `int(m_maxSize)`.

```{literalinclude} code/cpp_fortran/mainwindow.cpp
:language: cpp
:lines: 71-116
```

`createParticleSystem` stops the timer, destroys the Fortran system unless this is the first call, calls `particle_system_init` with the four members, clears `m_firstTime`, and starts the timer.

`on_actionRun_triggered` starts the timer. `on_actionStop_triggered` stops it. The toolbar text for that action is Pause. The name `actionStop` is the object name in the `.ui` file. Qt connects the action to the slot by that name because the slot follows the pattern `on_<object>_<signal>`.

`on_maxSizeSlider_valueChanged` passes the integer to `ParticleCanvas::setMaxSize`. Dragging the slider rescales the drawing on the next paint. It does not rebuild the particles and it does not change a Fortran value.

`on_actionUpdate_triggered` runs `updateParams` and `createParticleSystem`. That is the button in the recording. The fields were set to 80, 0.012, and 0.040, and Update constructed a new system with those numbers.

The window description puts the controls in a row and the canvas under them.

```{literalinclude} code/cpp_fortran/mainwindow.ui
:language: xml
:lines: 4-16
```

The designed size is 894 by 709. That is the size in the recording, plus one row so the H.264 frame height is even.

```{literalinclude} code/cpp_fortran/mainwindow.ui
:language: xml
:lines: 46-139
```

The spin box runs from the default up to 10000, with a step of 100, and starts at 500. The slider runs from 100 to 2000 and starts at 600. The two radius fields are `minRadiusText` and `maxRadiusText`.

```{literalinclude} code/cpp_fortran/mainwindow.ui
:language: xml
:lines: 157-161
```

```{literalinclude} code/cpp_fortran/mainwindow.ui
:language: xml
:lines: 174-239
```

File → New and File → Open are actions in the menu. No slot is connected to them. Choosing them does nothing. Run, Pause, and Update are on the toolbar. The canvas is a promoted widget: `uic` turns `ParticleCanvas` and the header `particle_canvas.h` into the member `ui->drawingArea`.

### `ParticleCanvas`

```{literalinclude} code/cpp_fortran/particle_canvas.h
:language: cpp
```

The canvas is a `QWidget`. `Q_OBJECT` is what `moc` looks for. `m_maxSize` is the slider's scale, in pixels, of the unit square.

```{literalinclude} code/cpp_fortran/particle_canvas.cpp
:language: cpp
:lines: 8-19
```

The constructor creates a `QTimer` owned by the widget and connects `timeout()` to `on_timer_update()`. The connection uses the `SIGNAL` / `SLOT` macros. `m_maxSize` starts at 600, the same default as the window.

```{literalinclude} code/cpp_fortran/particle_canvas.cpp
:language: cpp
:lines: 21-62
```

`paintEvent` fills the widget with a black rectangle and a blue pen, asks Fortran for the count and the radius limits, and draws each particle from index 1 through `count`. Fortran arrays are 1-based, so the loop starts at 1.

The color channel is

$$
c = 255\,\frac{r - r_\min}{r_\max - r_\min}
$$

`c = 255.0 * (r - rmin) / (rmax - rmin)` is that quotient. Red and green stay at 255, and `int(c)` is the blue channel. A radius equal to $r_\min$ gives $c = 0$, so the color is `QColor(255, 255, 0)`, yellow. A radius equal to $r_\max$ gives $c = 255$, so the color is `QColor(255, 255, 255)`, white.

The circle is centered at

$$
\left(\frac{w}{2} - \frac{s}{2} + x s,\; \frac{h}{2} - \frac{s}{2} + y s\right)
$$

with radius $r s$, where $s$ is `m_maxSize` and $(x, y)$ is the Fortran position in the unit square. The `drawEllipse` call is those two expressions: `width()/2.0 - m_maxSize/2.0 + x*m_maxSize` and the same form for `height()` and `y`, and both radii are `r*m_maxSize`. Dragging the slider to the right increases $s$, so the same unit square is drawn across more pixels and the disks grow. That is the slider motion in the clip.

```{literalinclude} code/cpp_fortran/particle_canvas.cpp
:language: cpp
:lines: 64-87
```

`setMaxSize` stores the slider value. The next `paintEvent` uses it.

`runSimulation` calls `m_timer->start()` with no interval. A `QTimer` started that way uses an interval of 0 and fires whenever the event loop is idle. The window therefore steps the particles as fast as the collision loop and the paint allow. `stopSimulation` stops the timer. Pause in the recording is that call. The frames sit still while the timer is stopped, which is why the pointer can edit the fields without the collision loop eating the clicks.

`on_timer_update` calls `particle_system_run_iteration` and then `repaint()`.

## The console driver

`main.f90` is a second program in the same directory. It is not in the CMake target. `PROJECT_SOURCES` lists the Fortran modules and the C++ window, and it does not list `main.f90`. Building the window does not build this driver.

```{literalinclude} code/cpp_fortran/main.f90
:language: fortran
```

It allocates a system and a simulation on polymorphic pointers, initializes 1000 particles with the default radii and speed, and calls `run(1000)`. There is no `print`. Standard output is empty. The result is the file `particle.state` in the working directory.

Compiled and run on this machine:

```text
$ gfortran -O2 -c mf_datatypes.f90 mf_utils.f90 particle_utils.f90 particle_classes.f90 main.f90
$ gfortran -O2 -o particle_console mf_datatypes.o mf_utils.o particle_utils.o particle_classes.o main.o
```

The run took 2 seconds. `particle.state` is 24 MB and 1,002,001 lines. The first line of the radius block is the count 1000, then one radius per line. Each of the 1000 iterations appends the count and 1000 position lines. The line count is

$$
1001 + 1000 \times 1001 = 1002001
$$

The coordinates are one draw of the random generator. A second run will not match them.

The excerpt is the start of the radius block, the start of the first position block, and the last three lines of the file.

```{literalinclude} code/cpp_fortran/logs/console_particle_state.txt
:language: text
```

## CMake

```{literalinclude} code/cpp_fortran/CMakeLists.txt
:language: cmake
```

`cmake_minimum_required(VERSION 3.5)` is the version the list was written for. CMake 3.31 on this machine still configures it. `project` enables C, C++, and Fortran. The C compiler is detected because Qt's own checks use it. None of this project's sources are C.

`CMAKE_AUTOUIC`, `CMAKE_AUTOMOC`, and `CMAKE_AUTORCC` are the three generators. `CMAKE_CXX_STANDARD 17` matches the language Qt 6 headers use. `find_package(QT NAMES Qt6 Qt5 ...)` and the following `find_package(Qt${QT_VERSION_MAJOR} ...)` are the usual Qt 5-or-6 form. On this machine that resolved to Qt 6.8.2 Widgets.

`qt_add_executable` is the Qt 6 way to build the program. The `else` branch is the Qt 5 form, and it was not taken. `target_link_libraries` attaches `Qt6::Widgets`, which brings `Qt6::Gui`, `Qt6::Core`, and the OpenGL libraries those targets need. The bundle and install lines are for macOS and for `cmake --install`. The recording did not install anything. It ran the binary from the build directory.

`main.f90` is absent from `PROJECT_SOURCES`. `particle_interface.h` is listed so the build rebuilds when the C prototypes change.

Configure on this machine:

```{literalinclude} code/cpp_fortran/logs/cmake_configure.log
:language: text
```

The build directory is `/tmp/oop_learn/cpp_fortran/build`. The transcript drops that prefix, the long `-I` and `-D` lists, and Make's directory chatter. What remains is the real order: `moc` on the two headers that contain `Q_OBJECT`, `uic` on `mainwindow.ui`, five Fortran compiles, four C++ compiles including the generated `mocs_compilation.cpp`, and the link.

```{literalinclude} code/cpp_fortran/logs/cmake_build.log
:language: text
```

The link line is `/usr/bin/c++` plus the Qt libraries, `-lgfortran`, and `-lquadmath`. That is the same reason as in the small Fortran-calls-C++ program: the driver is the C++ compiler, and the Fortran runtime is an extra library. The `rpath` points at the Qt 6 library directory so the dynamic loader finds `libQt6Widgets.so.6` when the binary starts.
