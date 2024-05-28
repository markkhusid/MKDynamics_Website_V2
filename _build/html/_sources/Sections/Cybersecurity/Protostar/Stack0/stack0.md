# Stack 0

## Introduction
Stack0 is the first challenge in the Protostar series of binary exploitation challenges. The challenge is designed to help you learn the basic techniques of binary exploitation by exploiting a simple stack buffer overflow vulnerability to modify a variable.

## Objective
The objective of the Stack0 challenge is to exploit a stack buffer overflow vulnerability to modify a variable in the program. The program reads a string from the user and copies it into a buffer on the stack. The buffer is not large enough to hold the string, so the program overflows the buffer and overwrites a variable on the stack.

## Architecture
The Stack0 challenge was solved and analyzed on the following architectures:

### x86
::::{grid} 1 1 1 1
:class-container: text-center
:gutter: 3

:::{grid-item-card}
:link: stack0_x86
:link-type: doc
:class-header: bg-dark

Stack0 - First Stack Buffer Overflow to Modify a Variable - x86 32 Bit Platform
^^^
```{image} images/r2_stack0_x86_splash.jpg
:height: 600
```
:::
::::


### ARM32
::::{grid} 1 1 1 1
:class-container: text-center
:gutter: 3

:::{grid-item-card}
:link: stack0_ARM32
:class-header: bg-dark

Stack0 - First Stack Buffer Overflow to Modify a Variable - ARM 32 Bit Platform
^^^
```{image} images/r2_stack0_ARM32_splash.jpg
:height: 600
```
:::
::::