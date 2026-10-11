# Ada Binaries: ARM32

Created with Grok Build

```{figure} ../../images/Ada/ARM32/add_Ada_ARM32_splash.jpg
:height: 600
:width: 800
:align: center
:class: clickable-figure

Radare2 session for Add_Int_w_IO on ARM32
```

## Introduction

This section is Ada compiled for ARM32. The built program is `Add_Int_w_IO` in the [Disassembling-Binaries ARM32 tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Ada/ARM_Architecture/ARM32). The listing is the object file. The two integers come from `Get`, so the sum is an `add` followed by Ada's overflow check.

`Add_Int` is present as source and was not built for ARM32 in this tree. The constant form of that program is the ARM64 page, where the compiler stored the sum 8.

## Integer operations

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: ADD_INT_W_IO/add_int_w_io

Add Two Integers with Input and Output
^^^
```{image} ../../images/Ada/ARM32/add_Ada_ARM32_splash.jpg
:height: 600
:width: 800
```
:::

::::
