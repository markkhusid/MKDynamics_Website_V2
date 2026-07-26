---
title: Types & Precision
---

Numeric kinds, overflow, conversions, and REAL32 vs REAL64 performance from the Fortran MOOC ([gjbex/Fortran-MOOC](https://github.com/gjbex/Fortran-MOOC)), built with **fpm**.

## Table of Contents

::::{grid} 1 2 2 2

:::{grid-item-card}
:link: Section_Type_Info.ipynb

Type Info — Limits
^^^
```{image} images/card_type_info.jpg
:height: 160
:align: center
```

Print huge/tiny/digits/range for integer and real kinds.
:::

:::{grid-item-card}
:link: Section_Type_Info_Overflow.ipynb

Integer Overflow
^^^
```{image} images/card_type_overflow.jpg
:height: 160
:align: center
```

Wrap-around behavior near huge(INT8).
:::

:::{grid-item-card}
:link: Section_Type_Info_Sqrt2.ipynb

sqrt(2) Identity
^^^
```{image} images/card_type_sqrt2.jpg
:height: 160
:align: center
```

Exact equality vs tolerance checks for floating-point identities.
:::

:::{grid-item-card}
:link: Section_Type_Info_Conversion.ipynb

Type Conversion
^^^
```{image} images/card_type_conv.jpg
:height: 160
:align: center
```

Precision loss when narrowing reals and integers.
:::

:::{grid-item-card}
:link: Section_Precision_Real32_vs_Real64.ipynb

REAL32 vs REAL64 Timing
^^^
```{image} images/card_type_precision.jpg
:height: 160
:align: center
```

Benchmark mixed- and double-precision axpy-style updates.
:::

::::

## Image credits

Card photographs are free stock images from [Unsplash](https://unsplash.com) (usable under the [Unsplash License](https://unsplash.com/license); attribution appreciated).

| Card | Source | License |
|------|--------|--------|
| Type Info — Limits | [Unsplash](https://unsplash.com/photos/aa79dcee981c) (`photo-1555949963-aa79dcee981c`) — coding theme | [Unsplash License](https://unsplash.com/license) |
| Integer Overflow | [Unsplash](https://unsplash.com/photos/d6fc5c10da5a) (`photo-1518432031352-d6fc5c10da5a`) — HPC theme | [Unsplash License](https://unsplash.com/license) |
| sqrt(2) Identity | [Unsplash](https://unsplash.com/photos/e363dbe005cb) (`photo-1635070041078-e363dbe005cb`) — math theme | [Unsplash License](https://unsplash.com/license) |
| Type Conversion | [Unsplash](https://unsplash.com/photos/72ae9ae6848d) (`photo-1509228627152-72ae9ae6848d`) — equations theme | [Unsplash License](https://unsplash.com/license) |
| REAL32 vs REAL64 Timing | [Unsplash](https://unsplash.com/photos/bebda4e38f71) (`photo-1551288049-bebda4e38f71`) — analytics theme | [Unsplash License](https://unsplash.com/license) |
