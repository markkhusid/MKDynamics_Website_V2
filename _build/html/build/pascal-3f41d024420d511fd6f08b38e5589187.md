# Pascal

Created with Grok Build

```{figure} ../images/Pascal/pascal_splash.jpg
:height: 500
:width: 800
:align: center
:class: clickable-figure

The AMD64 add program in the editor.
```


## Introduction

These pages are the Free Pascal programs in the Disassembling-Binaries tree that were built and saved with an object or an objdump. On these Free Pascal 3.0.4 builds, `INTEGER` is a 16-bit Smallint and `REAL` is an IEEE-754 double. `main` and `PASCALMAIN` are the same entry. The code lives in `.text.n_main`, and a function lives in its own `.text` section.

The AMD64 pages are integer add, real add, a function call, and `writeln`. The ARM64 pages are an integer added to the constant 5, an integer multiplied by the constant 5, real add, and a function call. The ARM32 page is the integer add. The i386 directory saves sources. The writeln object in that directory is a 64-bit ELF, and its code matches the AMD64 writeln page.

## Platforms

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: AMD64/amd64__HEAD__

Pascal on AMD64
^^^
```{image} ../images/Pascal/pascal_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: ARM64/arm64

Pascal on ARM64
^^^
```{image} ../images/Pascal/ARM64/add_Pascal_ARM64_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: ARM32/arm32

Pascal on ARM32
^^^
```{image} ../images/Pascal/pascal_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: i386/i386__HEAD__

Pascal on i386
^^^
```{image} ../images/Pascal/pascal_splash.jpg
:height: 500
:width: 800
```
:::

::::


## Project Code on GitHub

[GitHub](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Pascal)
