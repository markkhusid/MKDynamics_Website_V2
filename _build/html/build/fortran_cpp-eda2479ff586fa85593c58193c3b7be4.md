# Fortran calling C++

Created with Grok Build

Source code by [Jonas Lindemann](https://github.com/jonaslindemann), from the [oop_fortran](https://github.com/jonaslindemann/oop_fortran) repository.

This program is the language boundary without a window. A Fortran `program` calls six C++ functions. The object-oriented part is small on purpose. There is no derived type. The thing to learn is how an argument crosses `bind(C)`, because the [particle viewer](cpp_fortran.md) uses the same mechanism in the other direction.

Each section shows the Fortran interface and the C++ function, then what the call does. The complete files are `code/fortran_cpp/main.f90`, `code/fortran_cpp/mycpp.cpp`, and `code/fortran_cpp/mycpp.h`.

```{figure} images/fortran_cpp.png
:alt: Fortran main calling C++ functions
:align: center
:class: clickable-figure

The Fortran program calls the C++ functions. The arrays are 20 elements, and each sum is 85.
```

The header turns off C++ name mangling for the six functions.

```{literalinclude} code/fortran_cpp/mycpp.h
:language: cpp
:lines: 4-11
```

`extern "C"` makes the symbol `simple` rather than an encoded C++ name. The header and the Fortran interface have to describe the same arguments. The compiler does not check one against the other.

`iso_c_binding` gives Fortran names for C types: `c_int`, `c_float`, `c_double`. On this platform those are a 32-bit integer, a 32-bit real, and a 64-bit real. `bind(C, name="...")` sets the symbol the linker looks up.

## `simple`

```{literalinclude} code/fortran_cpp/main.f90
:language: fortran
:lines: 8-9
```

```{literalinclude} code/fortran_cpp/mycpp.cpp
:language: cpp
:lines: 6-9
```

The Fortran interface has no arguments. The C++ function prints `Hello form C++`. That spelling is the string in `mycpp.cpp`. The call is `call simple()`, and it is the first line of the output.

## `easy`

```{literalinclude} code/fortran_cpp/main.f90
:language: fortran
:lines: 11-16
```

```{literalinclude} code/fortran_cpp/mycpp.cpp
:language: cpp
:lines: 11-14
```

Fortran passes two `integer(c_int)` arguments with the `value` attribute. `value` means the C function receives the integer itself, which is what a C parameter `int a` expects. A dummy without `value` would be a pointer, and the C parameter would be `int*`.

`easy` prints `a = 2 b = 4`. The Fortran program does not print those integers again. The line in the output comes from `std::cout`.

## `no_problem`

```{literalinclude} code/fortran_cpp/main.f90
:language: fortran
:lines: 17-22
```

```{literalinclude} code/fortran_cpp/mycpp.cpp
:language: cpp
:lines: 16-21
```

Two inputs go across as `real(c_float), value`. The output is `real(c_float), intent(out)` with no `value`. On the C side that is `float* c`. Fortran's default for an argument is a pointer to the actual variable, and `intent(out)` documents that the subroutine writes it.

The body implements

$$
c = a + b
$$

with `*c = a + b`. The call uses `c1` and the values 2 and 4, so

$$
c_1 = 2 + 4 = 6
$$

C++ prints `a`, `b`, and `c = 6`. Fortran then prints `c1`, which is the same 6 in list-directed format, `6.00000000`.

## `no_problemas`

```{literalinclude} code/fortran_cpp/main.f90
:language: fortran
:lines: 24-29
```

```{literalinclude} code/fortran_cpp/mycpp.cpp
:language: cpp
:lines: 23-28
```

The Fortran interface is the same shape as `no_problem`. The C++ parameter is `float& c`, a reference. A C++ reference is an address at the ABI level, so it matches the Fortran argument that was passed as a pointer. The body assigns `c = a + b` and implements the same sum:

$$
c_2 = 2 + 4 = 6
$$

The output is a second copy of the same three lines, and Fortran prints `c2` as another `6.00000000`. Those two 6s are `c1` and `c2`. They come from these two calls, before the array loop.

## `many_numbers`

```{literalinclude} code/fortran_cpp/main.f90
:language: fortran
:lines: 31-37
```

```{literalinclude} code/fortran_cpp/mycpp.cpp
:language: cpp
:lines: 30-34
```

The Fortran interface describes three arrays and a length. The C++ function takes `float* a`, `float* b`, `float* c`, and `int n`. Fortran passes the address of the first element of a contiguous array, which is what those pointers expect. `n` has `value`, so it arrives as an `int`.

`n` appears in `a(n)` before the line that declares `integer(c_int), value :: n`. An interface body does not inherit `implicit none` from the host program, so the `n` in the array bound is an implicit integer as far as that specification is concerned. The explicit declaration is still the dummy that gets passed. Declaring `n` first, and putting `implicit none` inside the interface, matches the C `int` more tightly. The call with 20 elements still runs.

The program sets every `a(i)` to 42 and every `b(i)` to 43. The C++ loop writes

$$
c_i = a_i + b_i = 42 + 43 = 85
$$

with `c[i] = a[i] + b[i]`. Fortran's arrays are 1-based and C's index `i` runs from 0 through `n - 1`. Those are the same 20 elements in memory order. Fortran prints `c` from index 1 through 20. Every line is `85.0000000`. C++ does not print inside this function. All twenty lines are the Fortran loop.

## `myfunc`

```{literalinclude} code/fortran_cpp/main.f90
:language: fortran
:lines: 39-43
```

```{literalinclude} code/fortran_cpp/mycpp.cpp
:language: cpp
:lines: 36-39
```

This one is a function. Both sides return `double`. Fortran uses `real(c_double)` for the result and `value` for the input, matching `double myfunc(double x)`. The C++ body returns

$$
y = \sin x
$$

The program prints `myfunc(1.0_c_double)`. The suffix `c_double` makes the literal a double. The `value` dummy wants that double. The printed value is `0.84147098480789650`, which is $\sin 1$ for one radian.

## The program that calls them

```{literalinclude} code/fortran_cpp/main.f90
:language: fortran
:lines: 47-74
```

`allocate` makes three arrays of length 20. The assignments fill them before `many_numbers`. `x` and `y` are declared and the call passes a literal, so those two variables are never read. The empty `contains` section does not add an internal procedure.

## Output

```{literalinclude} code/fortran_cpp/fortran_cpp.out
:language: text
```

## CMake

```{literalinclude} code/fortran_cpp/CMakeLists.txt
:language: cmake
```

`cmake_minimum_required(VERSION 3.5)` is the version the list was written for. CMake 3.31 on this machine still configures it. `LANGUAGES CXX Fortran` turns on both compilers. `GLOB` collects `main.f90` and, separately, `mycpp.cpp` and `mycpp.h`. Headers in an executable target are not compiled on their own. CMake lists them so the generated Makefile rebuilds when the header changes.

Configure finds `c++` and `gfortran`.

```{literalinclude} code/fortran_cpp/cmake_configure.log
:language: text
```

The build directory in that log is `/tmp/oop_learn/fortran_cpp/build`. The transcript drops that prefix and the `-I` flags. The real compile lines included the source directory and the build directory.

```{literalinclude} code/fortran_cpp/cmake_build.log
:language: text
```

The link line is the part to read slowly. The driver is `/usr/bin/c++`, because the program contains C++. CMake adds `-lgfortran -lquadmath` so the Fortran runtime is still there for the Fortran `program` statement, the `print` statements, and the array assignments. A link driven by `gfortran` would have needed `-lstdc++` for the C++ standard library instead.

Running `./fortran_cpp` produced the output above.
