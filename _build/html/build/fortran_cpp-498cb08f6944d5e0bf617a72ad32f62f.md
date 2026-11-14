# Fortran calling C++

Created with Grok Build

`fortran_cpp` is a Fortran program that calls six C++ functions. Each C++ function is inside `extern "C"`, and each Fortran interface uses `bind(C, name="...")` with the same name. The arguments use kinds from `iso_c_binding`.

```{figure} images/fortran_cpp.png
:alt: Fortran bind(C) calls and the values they return
:align: center
:class: clickable-figure

The five calls in main.f90 and the values from the gfortran 14.2.0 run.
```

## The six calls

`simple` takes no arguments and prints `Hello form C++`. That spelling is the string in `mycpp.cpp`.

`easy` takes two `integer(c_int)` arguments with `value`, so Fortran passes them by value. The call is `easy(2, 4)`.

`no_problem` takes two `real(c_float)` arguments by value and one `intent(out)` float. On the C++ side the third argument is `float*`. The call `no_problem(2.0, 4.0, c1)` stores 6 in `c1`.

`no_problemas` has the same Fortran interface. On the C++ side the third argument is `float&`, which is still a pointer at the call boundary. The call stores 6 in `c2`.

`many_numbers` takes three explicit-shape `real(c_float)` arrays and an `integer(c_int)` length passed by value. The C++ loop writes `c[i] = a[i] + b[i]`. The program fills `a` with 42, `b` with 43, and `c` with 0, then asks for 20 elements. Every printed sum is 85.

`myfunc` is a `real(c_double)` function. The C++ body returns `sin(x)`. `myfunc(1.0_c_double)` prints `sin(1)`.

The executable linked here is `g++ -c mycpp.cpp`, `gfortran -c main.f90`, and `gfortran -o fortran_cpp main.o mycpp.o -lstdc++`.

## Output

```{literalinclude} code/fortran_cpp/fortran_cpp.out
:language: text
```

The two `6.00000000` lines are Fortran printing `c1` and `c2`. The twenty `85.0000000` lines are the array `c`. The last line is `sin(1)`.

## main.f90

```{literalinclude} code/fortran_cpp/main.f90
:language: fortran
```

## mycpp.cpp

```{literalinclude} code/fortran_cpp/mycpp.cpp
:language: cpp
```

## mycpp.h

```{literalinclude} code/fortran_cpp/mycpp.h
:language: cpp
```

## CMakeLists.txt

```{literalinclude} code/fortran_cpp/CMakeLists.txt
:language: cmake
```
