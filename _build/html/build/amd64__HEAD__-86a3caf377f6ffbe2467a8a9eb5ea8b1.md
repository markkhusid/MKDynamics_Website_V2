# Pascal Binaries: AMD64

Created with Grok Build

```{figure} ../../images/Pascal/pascal_splash.jpg
:height: 500
:width: 800
:align: center
:class: clickable-figure

The AMD64 add program in the editor.
```


## Introduction

This section is Free Pascal 3.0.4+dfsg-18ubuntu2 for x86_64, dated 2018/08/29. The assembly is Intel syntax. `INTEGER` is a 16-bit Smallint. The integer add encodes the sum as `lea` with scale 1. The real add is `addsd`. The function's symbol spells its parameters `SMALLINT`. `writeln` calls the text-file helpers.

## Programs

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: ADD_INT/add_int

Add Two Integers
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

:::{grid-item-card}
:link: WRITELN/writeln

Writeln
^^^
```{image} ../../images/Pascal/pascal_splash.jpg
:height: 500
:width: 800
```
:::

::::

