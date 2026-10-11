# Fortran - AMD 64-Bit Platform - Add Two Reals

Created with Grok Build

## Introduction

This page disassembles addition of `real` values on AMD64. The source is `add_reals.f08` from the [Disassembling-Binaries](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/AMD64/Real_Operations/Add_Reals) tree. A default `real` is four bytes, IEEE-754 single precision. The add uses an XMM register, not `eax`.

`main` is the same runtime prologue as on the [addition page](../ADD_INT/add_int.md).

## The program *add_reals.f08*

```{literalinclude} code/add_reals.f08
:language: fortran
```

`a` is 10.0, `b` is 2.0, and `c` is `b + a`. The sum is 12.0. The constants are not immediate operands. The compiler stores each one in `.rodata` and loads it with a rip-relative `movss`.

```bash
gfortran -ggdb3 add_reals.f08 -o add_reals_Fortran_AMD64_ggdb3
objdump -d -Mintel -S -w add_reals_Fortran_AMD64_ggdb3
```

`-S` interleaves the Fortran source. `-w` keeps each instruction on one line. Each instruction line is the address, the machine bytes, and the Intel disassembly. The notes after `//` were added to that objdump.

## The addition

```bash
0000000000001149 (MAIN__):
program add_reals
 1149: 55                   push rbp                                     // Save the caller's frame pointer.
 114a: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.

        implicit none

        real :: a, b, c

        a = 10.0
 114d: f30f1005d70e0000     movss xmm0, DWORD PTR [rip+0xed7]            // Load a from .rodata (202c <options.0.0+0x1c>).
 1155: f30f1145fc           movss DWORD PTR [rbp-0x4], xmm0              // Store a.

        b = 2.0
 115a: f30f1005ce0e0000     movss xmm0, DWORD PTR [rip+0xece]            // Load b from .rodata (2030 <options.0.0+0x20>).
 1162: f30f1145f8           movss DWORD PTR [rbp-0x8], xmm0              // Store b.

        c = b + a
 1167: f30f1045f8           movss xmm0, DWORD PTR [rbp-0x8]              // xmm0 = b.
 116c: f30f5845fc           addss xmm0, DWORD PTR [rbp-0x4]              // Scalar single add. xmm0 = b + a.
 1171: f30f1145f4           movss DWORD PTR [rbp-0xc], xmm0              // Store the result in c.

end program add_reals
 1176: 90                   nop                                          // Padding in front of the epilogue.
 1177: 5d                   pop rbp                                      // Restore the caller's frame pointer.
 1178: c3                   ret                                          // Pop the return address and return to the caller.
```

| Slot | Variable | Value |
| --- | --- | --- |
| `rbp-0x4` | `a` | 10.0 |
| `rbp-0x8` | `b` | 2.0 |
| `rbp-0xc` | `c` | 12.0 |

`movss` and `addss` move and add a scalar single. The `ss` suffix is the four-byte form. A double would be `movsd` and `addsd`. `xmm0` is the destination, and the second operand of `addss` may be memory, so `a` is added without a second XMM load.

The displacements belong to this build. They point just past the compiler's options block in `.rodata`. Another link will move them. The values at those addresses are the single-precision encodings of 10.0 and 2.0.

The body is a leaf, so the three singles sit in the red zone. `pop rbp` and `ret` return to `main`.
