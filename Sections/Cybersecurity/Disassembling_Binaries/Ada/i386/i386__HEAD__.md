# Ada Binaries: i386

Created with Grok Build

```{figure} ../../images/Ada/i386/add_Ada_i386_splash.jpg
:height: 600
:width: 800
:align: center
:class: clickable-figure

objdump of the i386 Add_Int object
```

## Introduction

This section is Ada compiled for i386, the 32-bit x86 platform. The program is `Add_Int` in the [Disassembling-Binaries i386 tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Ada/Intel_Architecture/i386). The listing is the object file. The compiler stored the sum 8. The object also contains the i386 position-independent call that loads the program counter. That call is a relocation, and the three stores do not use its result.

## Integer operations

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: ADD_INT/add_int

Add Two Integers
^^^
```{image} ../../images/Ada/i386/add_Ada_i386_splash.jpg
:height: 600
:width: 800
```
:::

::::
