# Pascal Binaries: ARM64

Created with Grok Build

```{figure} ../../images/Pascal/ARM64/add_Pascal_ARM64_splash.jpg
:height: 500
:width: 800
:align: center
:class: clickable-figure

Radare2 session for the ARM64 add program. PASCALMAIN is at 0x4001c0.
```


## Introduction

This section is Free Pascal 3.0.4+dfsg-18ubuntu2 for aarch64, dated 2018/08/29. The integer add in this tree is `c := a + 5`, and the multiply is `c := a * 5`. The real add is `fadd` of two doubles. The function add is `add` of two Smallints.

## Programs

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: ADD_INT/add_int

Add an Integer and a Constant
^^^
```{image} ../../images/Pascal/ARM64/add_Pascal_ARM64_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: MULT_INT/mult_int

Multiply an Integer by a Constant
^^^
```{image} ../../images/Pascal/pascal_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: ADD_FLOATS/add_floats

Add Two Reals
^^^
```{image} ../../images/Pascal/pascal_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: ADD_FUNCTIONS/add_functions

Add Two Integers in a Function
^^^
```{image} ../../images/Pascal/pascal_splash.jpg
:height: 500
:width: 800
```
:::

::::

