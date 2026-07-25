---
title: Fortran MOOC
---

In this section we follow examples from **Fortran for scientific programming**, a MOOC hosted by FutureLearn. Course material is on GitHub:

[https://github.com/gjbex/Fortran-MOOC](https://github.com/gjbex/Fortran-MOOC)

Each example is packaged with the **Fortran Package Manager (fpm)** and presented as an executable Jupyter notebook: source listing, step-by-step explanation, build, and run outputs.

Original course sources live under `Fortran_Code/OG_Source_Code/`. Working fpm projects are under `Fortran_Code/Section_*`.

## Table of Contents

::::{grid} 1 2 2 2

:::{grid-item-card}
:link: Section_Arrays__HEAD__.md

Arrays
^^^
```{image} images/card_arrays.jpg
:height: 160
:align: center
```

Dynamic arrays, reshape, normalize, identity matrices, timing, and related demos.
:::

:::{grid-item-card}
:link: Section_Ball_Throw__Head__.ipynb

Ball Throw
^^^
```{image} images/card_ball_throw.jpg
:height: 160
:align: center
```

Projectile motion with a Runge–Kutta ODE integrator.
:::

:::{grid-item-card}
:link: Section_Bit_Manipulations__Head__.ipynb

Bit Manipulations
^^^
```{image} images/card_bit_manipulations.jpg
:height: 160
:align: center
```

Bit counting, lookup tables, and low-level bit operations.
:::

:::{grid-item-card}
:link: Section_Floating_Point.ipynb

Floating Point / IEEE
^^^
```{image} images/card_floating_point.jpg
:height: 160
:align: center
```

IEEE-style floating-point behavior, including zero vs non-zero demos.
:::

:::{grid-item-card}
:link: Section_Call_By_Semantics.ipynb

Call-by Semantics
^^^
```{image} images/card_call_by.jpg
:height: 160
:align: center
```

Call by value, reference, and intent-based argument association.
:::

:::{grid-item-card}
:link: Section_Cellular_Automata__Head__.ipynb

Cellular Automata
^^^
```{image} images/card_cellular.jpg
:height: 160
:align: center
```

Grid-based cellular automata examples in Fortran.
:::

:::{grid-item-card}
:link: Section_Computing_Pi.ipynb

Computing π
^^^
```{image} images/card_computing_pi.jpg
:height: 160
:align: center
```

Numerical integration for π, including an OpenMP variant.
:::

:::{grid-item-card}
:link: Section_Implicit_vs_Explicit_Loops__Head__.ipynb

Implicit vs Explicit Loops
^^^
```{image} images/card_loops.jpg
:height: 160
:align: center
```

Array syntax versus explicit `do` loops and performance style.
:::

:::{grid-item-card}
:link: Section_Block_Matrices__Head__.ipynb

Block Matrices
^^^
```{image} images/card_block_matrices.jpg
:height: 160
:align: center
```

Working with block-structured matrix data.
:::

:::{grid-item-card}
:link: Section_BLAS_LAPACK__Head__.ipynb

BLAS / LAPACK
^^^
```{image} images/card_blas.jpg
:height: 160
:align: center
```

Dense linear algebra kernels: DOT, GEMV, SV, timings, and BLAS95 style.
:::

:::{grid-item-card}
:link: Section_Hello_Basics__Head__.md

Hello & Basics
^^^
```{image} images/card_hello_basics.jpg
:height: 160
:align: center
```

Hello Fortran, GCD, leap year, calculator, recursion, enumerators, optional arguments.
:::

:::{grid-item-card}
:link: Section_Types_Precision__Head__.md

Types & Precision
^^^
```{image} images/card_types_precision.jpg
:height: 160
:align: center
```

Numeric kinds, overflow, conversions, and REAL32 vs REAL64 timing.
:::

:::{grid-item-card}
:link: Section_Strings_I_O__Head__.md

Strings & I/O
^^^
```{image} images/card_strings_io.jpg
:height: 160
:align: center
```

ASCII codes, string assignment, palindromes, summing stdin, and distances.
:::

:::{grid-item-card}
:link: Section_Random_Numbers_Sampling__Head__.md

Random Numbers & Sampling
^^^
```{image} images/card_random.jpg
:height: 160
:align: center
```

RNG seeding, random integers, Buffon’s needle, Sierpinski chaos game, and sampling demos.
:::

:::{grid-item-card}
:link: Section_Algorithms__Head__.md

Algorithms
^^^
```{image} images/card_algorithms.jpg
:height: 160
:align: center
```

Primes, Fibonacci verification, Kaprekar’s routine, coin change, and Towers of Hanoi.
:::

::::

For the complete notebook tree, use the left sidebar under **Fortran MOOC**.

## Image credits

Card photographs are free stock images from [Unsplash](https://unsplash.com) (usable under the [Unsplash License](https://unsplash.com/license); attribution appreciated).

| Card | Source | License |
|------|--------|---------|
| Arrays | [Unsplash](https://unsplash.com/photos/aa79dcee981c) (`photo-1555949963-aa79dcee981c`) — coding / software theme | [Unsplash License](https://unsplash.com/license) |
| Ball Throw | [Unsplash](https://unsplash.com/photos/aadea25e6e68) (`photo-1575361204480-aadea25e6e68`) — ball / sports motion theme | [Unsplash License](https://unsplash.com/license) |
| Bit Manipulations | [Unsplash](https://unsplash.com/photos/4636190af475) (`photo-1518770660439-4636190af475`) — electronics / circuit board theme | [Unsplash License](https://unsplash.com/license) |
| Floating Point / IEEE | [Unsplash](https://unsplash.com/photos/a5951ee6f620) (`photo-1587145820266-a5951ee6f620`) — calculator / numeric precision theme | [Unsplash License](https://unsplash.com/license) |
| Call-by Semantics | [Unsplash](https://unsplash.com/photos/f06f85e504b3) (`photo-1516321318423-f06f85e504b3`) — programming instruction theme | [Unsplash License](https://unsplash.com/license) |
| Cellular Automata | [Unsplash](https://unsplash.com/photos/43490279c0fa) (`photo-1451187580459-43490279c0fa`) — grid / Earth-from-space theme | [Unsplash License](https://unsplash.com/license) |
| Computing π | [Unsplash](https://unsplash.com/photos/e363dbe005cb) (`photo-1635070041078-e363dbe005cb`) — chalkboard mathematics theme | [Unsplash License](https://unsplash.com/license) |
| Implicit vs Explicit Loops | [Unsplash](https://unsplash.com/photos/8466d910aaa4) (`photo-1515879218367-8466d910aaa4`) — source code on screen | [Unsplash License](https://unsplash.com/license) |
| Block Matrices | [Unsplash](https://unsplash.com/photos/72ae9ae6848d) (`photo-1509228627152-72ae9ae6848d`) — equations / linear algebra theme | [Unsplash License](https://unsplash.com/license) |
| BLAS / LAPACK | [Unsplash](https://unsplash.com/photos/d6fc5c10da5a) (`photo-1518432031352-d6fc5c10da5a`) — high-performance computing / servers | [Unsplash License](https://unsplash.com/license) |
| Hello & Basics | [Unsplash](https://unsplash.com/photos/dccba630e2f6) (`photo-1461749280684-dccba630e2f6`) — code editor / first programs theme | [Unsplash License](https://unsplash.com/license) |
| Types & Precision | [Unsplash](https://unsplash.com/photos/bebda4e38f71) (`photo-1551288049-bebda4e38f71`) — data / analytics dashboard theme | [Unsplash License](https://unsplash.com/license) |
| Strings & I/O | [Unsplash](https://unsplash.com/photos/044cdead277a) (`photo-1455390582262-044cdead277a`) — writing / text theme | [Unsplash License](https://unsplash.com/license) |
| Random Numbers & Sampling | [Unsplash](https://unsplash.com/photos/7f61d4dc18c5) (`photo-1526374965328-7f61d4dc18c5`) — digital “matrix” / randomness theme | [Unsplash License](https://unsplash.com/license) |
| Algorithms | [Unsplash](https://unsplash.com/photos/53e697fedbea) (`photo-1516116216624-53e697fedbea`) — coding / algorithms theme | [Unsplash License](https://unsplash.com/license) |
