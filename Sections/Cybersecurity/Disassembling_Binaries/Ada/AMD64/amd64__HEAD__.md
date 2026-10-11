# Ada Binaries: AMD64

Created with Grok Build

```{figure} images/add_Ada_AMD64_splash.jpg
:height: 600
:width: 800
:align: center
:class: clickable-figure

Radare2 session for Add_Int on AMD64
```

## Introduction

This section is Ada compiled for AMD64, the 64-bit x86 platform. The programs are the debug builds in the [Disassembling-Binaries AMD64 tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Ada/Intel_Architecture/AMD64/Integer_Operations). The assembly is Intel syntax.

`Add_Int` stores the constants 3 and 5 and the sum 8. `Add_Int_w_IO` reads two integers, so the sum is an `add` followed by Ada's overflow check. GNAT names the procedures `_ada_add_int` and `_ada_add_int_w_io`. A binder-generated `main` calls the runtime, then the procedure.

## Integer operations

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: ADD_INT/add_int

Add Two Integers
^^^
```{image} images/add_Ada_AMD64_splash.jpg
:height: 600
:width: 800
```
:::

:::{grid-item-card}
:link: ADD_INT_W_IO/add_int_w_io

Add Two Integers with Input and Output
^^^
```{image} ../../images/Ada/AMD64/add_IO_Ada_AMD64_splash.jpg
:height: 600
:width: 800
```
:::

::::
