---
title: Beej's Guide to C Programming
---

Executable walkthroughs of examples from **Beej's Guide to C Programming** by Brian “Beej Jorgensen” Hall.

- Guide: [https://beej.us/guide/bgc/](https://beej.us/guide/bgc/)
- Source: [https://github.com/beejjorgensen/bgc](https://github.com/beejjorgensen/bgc)

**License note:** Beej’s **C example code is public domain**. The guide prose is CC BY-NC-ND; these pages use the public-domain examples with **original** step-by-step explanations and deep links back to Beej’s sections.

Each notebook lists the program, explains it, then compiles and runs it with `gcc`.

## Chapter 5 — Pointers (Cower in Fear!)

::::{grid} 1 2 2 2

:::{grid-item-card}
:link: section_5_1_memory_and_variables.ipynb

5.1 Memory and Variables
^^^
```{image} images/card_beej_5_1.jpg
:height: 140
:align: center
```

Print a variable’s value and its address with `%p`.
:::

:::{grid-item-card}
:link: section_5_2_pointer_types.ipynb

5.2 Pointer Types
^^^
```{image} images/card_beej_5_2.jpg
:height: 140
:align: center
```

`int *` vs `double *` and sizes of pointers vs pointees.
:::

:::{grid-item-card}
:link: section_5_3_dereferencing.ipynb

5.3 Dereferencing
^^^
```{image} images/card_beej_5_3.jpg
:height: 140
:align: center
```

Use `*` to read/write the object a pointer refers to.
:::

:::{grid-item-card}
:link: section_5_4_passing_pointers_as_arguments.ipynb

5.4 Passing Pointers as Arguments
^^^
```{image} images/card_beej_5_4.jpg
:height: 140
:align: center
```

Let a function modify the caller’s variable via a pointer.
:::

:::{grid-item-card}
:link: section_5_5_null_pointer.ipynb

5.5 The NULL Pointer
^^^
```{image} images/card_beej_5_5.jpg
:height: 140
:align: center
```

Safe “points nowhere” value; check before dereference.
:::

:::{grid-item-card}
:link: section_5_6_declaring_pointers.ipynb

5.6 Declaring Pointers
^^^
```{image} images/card_beej_5_6.jpg
:height: 140
:align: center
```

How `*` binds in multi-declarator statements.
:::

:::{grid-item-card}
:link: section_5_7_sizeof_and_pointers.ipynb

5.7 `sizeof` and Pointers
^^^
```{image} images/card_beej_5_7.jpg
:height: 140
:align: center
```

Size of a pointer vs size of `*p`.
:::

::::

## Chapter 6 — Arrays

::::{grid} 1 2 2 2

:::{grid-item-card}
:link: section_6_1_arrays_an_easy_example.ipynb

6.1 Arrays — An Easy Example
^^^
```{image} images/card_beej_6_1.jpg
:height: 140
:align: center
```

Declare, fill, and print a simple array.
:::

:::{grid-item-card}
:link: section_6_2_getting_the_length_of_an_array.ipynb

6.2 Getting the Length of an Array
^^^
```{image} images/card_beej_6_2.jpg
:height: 140
:align: center
```

`sizeof` length trick—and why it fails in functions.
:::

:::{grid-item-card}
:link: section_6_3_arrays_array_initializers.ipynb

6.3 Array Initializers
^^^
```{image} images/card_beej_6_3.jpg
:height: 140
:align: center
```

Brace initializers for arrays.
:::

:::{grid-item-card}
:link: section_6_4_arrays_out_of_bounds.ipynb

6.4 Out of Bounds
^^^
```{image} images/card_beej_6_4.jpg
:height: 140
:align: center
```

What can go wrong when indexing past the end.
:::

:::{grid-item-card}
:link: section_6_5_arrays_multidimensional_arrays.ipynb

6.5 Multidimensional Arrays
^^^
```{image} images/card_beej_6_5.jpg
:height: 140
:align: center
```

2D arrays and nested loops.
:::

:::{grid-item-card}
:link: section_6_6_1_arrays_getting_a_pointer_to_an_array.ipynb

6.6.1 Getting a Pointer to an Array
^^^
```{image} images/card_beej_6_6_1.jpg
:height: 140
:align: center
```

`p = a` vs `&a[0]`.
:::

:::{grid-item-card}
:link: section_6_6_2_arrays_passing_single_dimensional_arrays_to_functions.ipynb

6.6.2 Passing 1D Arrays to Functions
^^^
```{image} images/card_beej_6_6_2.jpg
:height: 140
:align: center
```

Pointer / array parameter notations.
:::

:::{grid-item-card}
:link: section_6_6_3_arrays_changing_arrays_in_functions.ipynb

6.6.3 Changing Arrays in Functions
^^^
```{image} images/card_beej_6_6_3.jpg
:height: 140
:align: center
```

Callee mutations visible in the caller.
:::

:::{grid-item-card}
:link: section_6_6_4_arrays_passing_multidimensional_arrays_to_functions.ipynb

6.6.4 Passing Multidimensional Arrays
^^^
```{image} images/card_beej_6_6_4.jpg
:height: 140
:align: center
```

Pass a 2D array into a printing helper.
:::

::::

## Chapter 7 — Strings

::::{grid} 1 2 2 2

:::{grid-item-card}
:link: section_7_1_string_literals.ipynb

7.1 String Literals
^^^
```{image} images/card_beej_7_1.jpg
:height: 140
:align: center
```

Double-quoted string constants and escapes.
:::

:::{grid-item-card}
:link: section_7_2_string_variables.ipynb

7.2 String Variables
^^^
```{image} images/card_beej_7_2.jpg
:height: 140
:align: center
```

`char *` pointing at a literal.
:::

:::{grid-item-card}
:link: section_7_3_string_variables_as_arrays.ipynb

7.3 String Variables as Arrays
^^^
```{image} images/card_beej_7_3.jpg
:height: 140
:align: center
```

Index a `char *` string like an array.
:::

:::{grid-item-card}
:link: section_7_4_string_initializers.ipynb

7.4 String Initializers
^^^
```{image} images/card_beej_7_4.jpg
:height: 140
:align: center
```

Mutable `char s[] = "..."`.
:::

:::{grid-item-card}
:link: section_7_5_getting_string_length.ipynb

7.5 Getting String Length
^^^
```{image} images/card_beej_7_5.jpg
:height: 140
:align: center
```

`strlen` from `<string.h>`.
:::

:::{grid-item-card}
:link: section_7_6_string_termination.ipynb

7.6 String Termination
^^^
```{image} images/card_beej_7_6.jpg
:height: 140
:align: center
```

NUL terminators and a hand-rolled length walk.
:::

:::{grid-item-card}
:link: section_7_7_copying_a_string.ipynb

7.7 Copying a String
^^^
```{image} images/card_beej_7_7.jpg
:height: 140
:align: center
```

Pointer aliasing vs `strcpy`.
:::

::::

## Image credits

Technical stock photographs from [Unsplash](https://unsplash.com) under the [Unsplash License](https://unsplash.com/license) (circuits, code, servers, mathematics—no portraits).

| Card group | Theme |
|------------|--------|
| Ch. 5 cards | PCB / code / servers / digital matrix / analytics |
| Ch. 6 cards | Equations / code / algorithms / servers / calculator UI |
| Ch. 7 cards | Circuits / code / math / digital patterns |

## Resources

- [Beej's Guide to C Programming](https://beej.us/guide/bgc/)
- [GitHub: beejjorgensen/bgc](https://github.com/beejjorgensen/bgc)
