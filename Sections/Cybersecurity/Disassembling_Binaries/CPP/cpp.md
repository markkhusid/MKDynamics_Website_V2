# C++

Created with Grok Build

```{figure} ../images/C++/c++_splash.jpg
:height: 500
:width: 800
:align: center
:class: clickable-figure

C++ splash.
```


## Introduction

The C++ tree is one program, `add.cpp`, built for AMD64, ARM64, ARM32, and i386. Each object stores 3 and 5 and adds them as 32-bit ints. The iostream header also leaves a static initializer in the object. That initializer constructs `std::__ioinit` and registers its destructor.

The notes on each listing were added to the objdump output. Addresses in the object files start at 0.

## Platforms

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: AMD64/amd64__HEAD__

C++ on AMD64
^^^
```{image} ../images/C++/c++_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: ARM64/arm64

C++ on ARM64
^^^
```{image} ../images/C++/c++_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: ARM32/arm32

C++ on ARM32
^^^
```{image} ../images/C++/c++_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: i386/i386__HEAD__

C++ on i386
^^^
```{image} ../images/C++/c++_splash.jpg
:height: 500
:width: 800
```
:::

::::


## Project Code on GitHub

[GitHub](https://github.com/markkhusid/Disassembling-Binaries/tree/master/C%2B%2B)
