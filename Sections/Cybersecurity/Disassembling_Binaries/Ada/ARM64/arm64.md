# Ada Binaries: ARM64

Created with Grok Build

```{figure} ../../images/Ada/ARM64/add_Ada_ARM64_splash.jpg
:height: 600
:width: 800
:align: center
:class: clickable-figure

Radare2 session for Add_Int on ARM64
```

## Introduction

This section is Ada compiled for ARM64. The built program is `Add_Int` in the [Disassembling-Binaries ARM64 tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Ada/ARM_Architecture/ARM64). The listing is the object file, so its addresses start at 0. The compiler stored the sum 8.

`Add_Int_w_IO` is present as source and was not built for ARM64 in this tree. The same program, built for AMD64, is the page that shows the run-time `add`.

## Integer operations

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: ADD_INT/add_int

Add Two Integers
^^^
```{image} ../../images/Ada/ARM64/add_Ada_ARM64_splash.jpg
:height: 600
:width: 800
```
:::

::::
