# Ada

Created with Grok Build

```{figure} images/ada_splash.jpg
:height: 500
:width: 800
:align: center
:class: clickable-figure

ada splash
```

## Introduction

Ada is a high-level programming language that was originally designed for the U.S. Department of Defense. It is known for its strong typing, modularity, and support for concurrent programming. Ada is often used in safety-critical systems, such as aerospace and defense applications, due to its reliability and maintainability.

The programs below are the ones built in the Disassembling-Binaries Ada tree. Each page is objdump of that build, with the address, the machine bytes, the instruction, and a comment, interleaved with the Ada source where the object has line numbers. `Add_Int` stores the constants 3 and 5 and the sum 8. `Add_Int_w_IO` reads the two integers, adds them, and checks the sum for overflow.

## Platforms

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: AMD64/amd64__HEAD__

Ada Binaries in AMD64
^^^
```{image} images/add_Ada_AMD64_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: ARM64/arm64

Ada Binaries in ARM64
^^^
```{image} ../images/Ada/ARM64/add_Ada_ARM64_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: ARM32/arm32

Ada Binaries in ARM32
^^^
```{image} ../images/Ada/ARM32/add_Ada_ARM32_splash.jpg
:height: 500
:width: 800
```
:::

:::{grid-item-card}
:link: i386/i386__HEAD__

Ada Binaries in i386
^^^
```{image} ../images/Ada/i386/add_Ada_i386_splash.jpg
:height: 500
:width: 800
```
:::

::::

## Project Code on GitHub

Project code and resources can be found on my GitHub repository: <br>
[GitHub](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Ada)
