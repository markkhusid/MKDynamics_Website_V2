# Fortran - AMD 64-Bit Platform - Multiply Two Integers

Created with Grok Build

```{figure} ../../images/AMD64/mult_Fortran_AMD64_splash.jpg
:height: 600
:width: 800
:class: clickable-figure

Radare2 session for mult.f08, with the program body and main
```

## Introduction

This page disassembles the Fortran multiplication program compiled for AMD64. The captured session is Radare2, in Intel syntax, on the same kind of machine as the [addition page](../ADD_INT/add_int.md). The source is the multiplication example from the ARM64 section. The new instruction is `imul`.

Project code for the whole comparison lives in [Disassembling-Binaries](https://github.com/markkhusid/Disassembling-Binaries).

## The program *mult.f08*

```{literalinclude} code/mult.f08
:language: fortran
```

`a` is 2, `b` is 3, and `c` is `a * b`. There is no input and no print. A default Fortran `integer` is four bytes here, so the product is a 32-bit multiply even though the processor is 64-bit.

The compile line matches the addition example:

```bash
gfortran -ggdb3 mult.f08 -o mult_Fortran_AMD64_ggdb3
```

`-ggdb3` is what lets Radare2 print `a = 2` beside the store. The Intel listing is:

```bash
objdump -d -Mintel -S -w mult_Fortran_AMD64_ggdb3
```

`-S` interleaves the Fortran source. `-w` keeps each instruction on one line. The listing below is that objdump of `MAIN__`. Each instruction line is the address, the machine bytes, and the Intel disassembly. The notes after `//` were added to the listing.

## What the screenshot is showing

The left pane is `mult.f08`. The right pane is the disassembly. Radare2 names stack slots from the frame pointer: `local_4h` is `rbp-0x4`, `local_8h` is `rbp-0x8`, and `local_ch` is `rbp-0xc`. The program body in that session is `sym.MAIN`. A current gfortran emits the same body as `MAIN__`.

`main` is the same entry as on the addition page. It spills `argc` and `argv`, calls `_gfortran_set_args`, points a register at the seven option words, calls `_gfortran_set_options`, calls the program body, and returns 0 with `leave` and `ret`.

## The multiplication

The body is a leaf function. It sets up a frame and never calls anything, so the three integers sit in the red zone under `rsp`.

```bash
0000000000001149 (MAIN__):
program mult
 1149: 55                   push rbp                                     // Save the caller's frame pointer.
 114a: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.

    implicit none

    integer :: a, b, c

    a = 2
 114d: c745fc02000000       mov DWORD PTR [rbp-0x4], 0x2                 // a = 2.
    b = 3
 1154: c745f803000000       mov DWORD PTR [rbp-0x8], 0x3                 // b = 3.

    c = a * b
 115b: 8b45fc               mov eax, DWORD PTR [rbp-0x4]                 // eax = a.
 115e: 0faf45f8             imul eax, DWORD PTR [rbp-0x8]                // Two-operand imul. eax becomes the low 32 bits of eax times b.
 1162: 8945f4               mov DWORD PTR [rbp-0xc], eax                 // Store the result in c.

end program mult
 1165: 90                   nop                                          // Padding in front of the epilogue.
 1166: 5d                   pop rbp                                      // Restore the caller's frame pointer.
 1167: c3                   ret                                          // Pop the return address and return to the caller.
```

| Slot | Variable | Value after the multiply |
| --- | --- | --- |
| `rbp-0x4` | `a` | 2 |
| `rbp-0x8` | `b` | 3 |
| `rbp-0xc` | `c` | 6 |

`imul eax, DWORD PTR [rbp-0x8]` is the two-operand form. It multiplies `eax` by the dword in memory and writes the low 32 bits of the product back to `eax`. The compiler did not load `b` into a second register first. The addition on the other page did: it loaded both values and then used `add eax, edx`.

This is also not the one-operand form, `imul r/m32`. That form multiplies by `eax` and writes the full 64-bit product across `edx:eax`. A Fortran `integer` product is one 32-bit value, and 2 times 3 fits in those 32 bits, so the compiler keeps the low half and discards the high half by never asking for it.

`pop rbp` restores the caller's frame pointer. `ret` returns to `main`. The `nop` is padding in front of that pair.

## A current gfortran build

The listing above is that rebuild. The body is named `MAIN__`. Radare2 called the same body `sym.MAIN`. `main` is the entry on the [addition page](../ADD_INT/add_int.md): it stages the options address through `rax` on the way into `rsi`. Addresses are for a position-independent executable, so they will not match the screenshot.

The product is still formed by one `imul` of `eax` by the dword at `rbp-0x8`, then stored at `rbp-0xc`.
