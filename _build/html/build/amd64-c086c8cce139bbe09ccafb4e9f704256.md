# AMD64

Created with Grok Build

This section is Fortran compiled for AMD64, the 64-bit x86 platform. The programs are the ones in the [Disassembling-Binaries AMD64 tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/AMD64). The assembly is Intel syntax. Integer arithmetic stays in `eax`. Real arithmetic uses `xmm0`. A print, a read, and a function call leave the leaf-function shape and call the runtime or another procedure.

## Integer operations

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: ADD_INT/add_int

Add Two Integers
^^^
```{image} ../images/AMD64/running_add_int_Fortran_AMD64_in_GEF_showing_main.jpg
:height: 600
:width: 800
```
:::

:::{grid-item-card}
:link: MULT_INT/mult_int

Multiply Two Integers
^^^
```{image} ../images/AMD64/mult_Fortran_AMD64_splash.jpg
:height: 600
:width: 800
```
:::

:::{grid-item-card}
:link: DIV_INT/div_int

Divide Two Integers
^^^
```{image} ../images/AMD64/div_int_Fortran_AMD64.png
:height: 600
:width: 800
```
:::

::::

## Real operations

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: ADD_REALS/add_reals

Add Two Reals
^^^
```{image} ../images/AMD64/add_reals_Fortran_AMD64.png
:height: 600
:width: 800
```
:::

:::{grid-item-card}
:link: MULT_REALS/mult_reals

Multiply Two Reals
^^^
```{image} ../images/AMD64/mult_reals_Fortran_AMD64.png
:height: 600
:width: 800
```
:::

::::

## Control, a function, and output

::::{grid} 1 1 1 1

:::{grid-item-card}
:link: IF_THEN/if_then

An If-Then
^^^
```{image} ../images/AMD64/if_then_Fortran_AMD64.png
:height: 600
:width: 800
```
:::

:::{grid-item-card}
:link: ADD_FUNCTION/add_function

A Function Call
^^^
```{image} ../images/AMD64/add_function_Fortran_AMD64.png
:height: 600
:width: 800
```
:::

:::{grid-item-card}
:link: PRINT/print

A Print Statement
^^^
```{image} ../images/AMD64/print_Fortran_AMD64.png
:height: 600
:width: 800
```
:::

::::
