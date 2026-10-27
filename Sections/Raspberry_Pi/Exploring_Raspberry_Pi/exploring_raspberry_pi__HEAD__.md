# Exploring Raspberry Pi

```{figure} images/exploring_raspberry_pi.png
:height: 200
:align: center
:enumerated: false
:class: no-caption clickable-figure


```
## Introduction
In this section, I will share my projects and experiments with the Raspberry Pi. We will use the book "Exploring Raspberry Pi" by Derek Molloy as a guide.

The Raspberry Pi is a small, affordable computer that can be used for a wide range of applications, from learning programming to building complex projects.

The programs below are the sources in my [Raspberry-Pi](https://github.com/markkhusid/Raspberry-Pi) repository. The same source is stored under both `C_C++` and `Chapter 5`, and again next to the ARM and x86-64 build directories. Each program appears once here. The object files, binaries, preprocessor dumps, and objdump logs remain in that repository.

## Table of Contents

- [Hello World](#hello-world)
- [Short programs](#short-programs)
- [Variable sizes](#variable-sizes)
- [Strings in C](#strings-in-c)
- [The C++ string class](#the-cpp-string-class)
- [Boost.Python module](#boost-python-module)
- [GPIO LED in C](#gpio-led-in-c)
- [GPIO LEDs in C++](#gpio-leds-in-cpp)
- [Cython sine integral](#cython-sine-integral)
- [Function callbacks](#function-callbacks)
- [POSIX threads](#posix-threads)
- [GPIO notebook](#gpio-notebook)
- [Cyclictest log](#cyclictest-log)

## Resources and Textbooks Used

### "Exploring Raspberry Pi" by Derek Molloy
This book may be purchased here: <br>
[Amazon page to purchase "Exploring Raspberry Pi" by Derek Molloy (affiliate link)](https://amzn.to/44uOGnl)

(hello-world)=
## Hello World

`helloworld.c` prints one line and returns.

```{literalinclude} code/helloworld.c
:language: c
```

`helloworld.cpp` prints the same line with `std::cout`.

```{literalinclude} code/helloworld.cpp
:language: cpp
```

(short-programs)=
## Short programs

`short.c` and `short.cpp` are empty `main` functions. `short2.cpp` is the same program with a comment and a typed argument list. The repository keeps the built binaries beside them: `shortc`, `shortcpp`, `short_1`, `short_2`, and `short_static`.

```{literalinclude} code/short.c
:language: c
```

```{literalinclude} code/short.cpp
:language: cpp
```

```{literalinclude} code/short2.cpp
:language: cpp
```

(variable-sizes)=
## Variable sizes

`sizeofvariables.c` prints the value, size, and address of a double, a float, an int, a long, a char, and a bool.

```{literalinclude} code/sizeofvariables.c
:language: c
```

This is the output saved from the 32-bit ARM build:

```{literalinclude} code/sizeofvariables_arm_output.txt
:language: text
```

The float conversion in the source is `%4.2`, and the bool line has no comma between `sizeof(f)` and `&f`. The second and last lines of this saved run follow from that source. The other lines report 8 bytes for the double, 4 for the int, 4 for the long, and 1 for the char.

(strings-in-c)=
## Strings in C

`cstrings.c` builds "Hello World!", prints the length, replaces `w` with `W`, inserts " to the", and splits the result on spaces.

```{literalinclude} code/cstrings.c
:language: c
```

(the-cpp-string-class)=
## The C++ string class

`cppstrings.cpp` does the same work with `std::string` and a `stringstream`.

```{literalinclude} code/cppstrings.cpp
:language: cpp
```

(boost-python-module)=
## Boost.Python module

`erpi.cpp` exposes `hello` and `integrate_sin` as a Python module named `erpi`. `integrate_sin` sums `sin` from `a` to `b` in `n` steps.

```{literalinclude} code/erpi.cpp
:language: cpp
```

`test.py` calls both functions. It uses the Python 2 print statement and NumPy's `pi`.

```{literalinclude} code/erpi_test.py
:language: python
```

(gpio-led-in-c)=
## GPIO LED in C

`makeLED.c` takes one argument: `setup`, `on`, `off`, `status`, or `close`. It writes the sysfs files for GPIO 4.

```{literalinclude} code/makeLED.c
:language: c
```

(gpio-leds-in-cpp)=
## GPIO LEDs in C++

`makeLEDs.cpp` is an `LED` class. `main` creates objects for GPIO 4 and GPIO 17, flashes them in opposition for 50 steps of 50 ms, and prints each pin's value. The destructor unexports the pins.

```{literalinclude} code/makeLEDs.cpp
:language: cpp
```

(cython-sine-integral)=
## Cython sine integral

`test.pyx` is a Cython `integrate_sin`. When the extension is run as a program it integrates from 0 to 3.14159 with one million steps. `cython_test.py` is the same sum in Python. `setup.py` builds the `test` extension. The generated `test.c`, the annotation HTML, and `test.so` remain in the repository.

```{literalinclude} code/test.pyx
:language: python
```

```{literalinclude} code/cython_test.py
:language: python
```

```{literalinclude} code/setup.py
:language: python
```

(function-callbacks)=
## Function callbacks

`callback.cpp` passes `squareCallback` and `cubeCallback` into `doMath` and prints the square and the cube of 5.

```{literalinclude} code/callback.cpp
:language: cpp
```

(posix-threads)=
## POSIX threads

`pthreads.cpp` starts one thread that increments `x` until it reaches 5. `main` increments `y` at the same time, joins the thread, and prints `x`, `y`, and the returned `z`. The file under `pthreads_aarch32` is the same source as the file under `pthreads_elf64-x86-64`.

```{literalinclude} code/pthreads.cpp
:language: cpp
```

(gpio-notebook)=
## GPIO notebook

`Chapter 6/simple.ipynb` imports a module named `gpio` and `sleep`. The saved run printed `Start of the Python GPIO program`, then stopped with `AttributeError: module 'gpio' has no attribute 'GPIO'`. The later cells were not run. The notebook is stored with these pages as `code/simple.ipynb`.

```python
import gpio
from time import sleep

print ("Start of the Python GPIO program")

led = gpio.GPIO(17)
button = gpio.GPIO(27)

led.setDirection(1)
button.setDirection(0)

while button.getValue() == 0:
    led.setValue(1)
    sleep(0.1)
    led.setValue(0)
    sleep(0.1)

print ("End of the GPIO program")
```

(cyclictest-log)=
## Cyclictest log

The `rt-tests` entry in the repository is a Git submodule. It records upstream rt-tests commit `5f9f1e3fe327440a9d405f4af8feb16ff7a909eb` (Clark Williams, 9 June 2015, "makefile: fixed release target").

`histogram.dat` at the repository root is the cyclictest log from that work. The file is 3,780,980 bytes and 58,973 lines. The run sets `/dev/cpu_dma_latency` to 0 us and uses the fifo policy. The summary at the end of the file is:

```text
# Total: 000099980 000099995 000099986 000099992
# Min Latencies: 00005 00005 00004 00005
# Avg Latencies: 00011 00012 00011 00011
# Max Latencies: 00808 00439 00434 00277
# Histogram Overflows: 00020 00005 00014 00008
# Histogram Overflow at cycle number:
# Thread 0: 31803 47054 47480 49451 49453 71945 71947 71948 75087 75088 75114 77244 78186 78213 94108 94109 94110 94123 97321 97349
# Thread 1: 31884 49440 62482 65648 81359
# Thread 2: 49612 56202 59299 59300 59301 59319 62444 62468 65622 65623 65626 68766 68767 68770
# Thread 3: 38068 53023 56088 81336 84479 84504 87777 90981
```

The full log is [histogram.dat](https://github.com/markkhusid/Raspberry-Pi/blob/master/histogram.dat) in the repository.
