# Fortran - AMD 64-Bit Platform - Multiply Two Reals

Created with Grok Build

## Introduction

This page disassembles multiplication of `real` values on AMD64. The source is `mult_reals.f08` from the [Disassembling-Binaries](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/AMD64/Real_Operations/Mult_Reals) tree. The integer multiply on the [integer page](../MULT_INT/mult_int.md) is `imul` of two dwords. This one is `mulss` of two singles in `xmm0`.

`main` is the same runtime prologue as on the [addition page](../ADD_INT/add_int.md).

## The program *mult_reals.f08*

```{literalinclude} code/mult_reals.f08
:language: fortran
```

`a` is 2.2, `b` is 3.3, and `c` is `b * a`. Neither literal is exact in binary. The stored product is the IEEE-754 single-precision product, not a decimal the programmer wrote down.

```bash
gfortran -ggdb3 mult_reals.f08 -o mult_reals_Fortran_AMD64_ggdb3
objdump -d -Mintel -S -w mult_reals_Fortran_AMD64_ggdb3
```

`-S` interleaves the Fortran source. `-w` keeps each instruction on one line. Each instruction line is the address, the machine bytes, and the Intel disassembly. The notes after `//` were added to that objdump.

## The multiplication

```bash
0000000000001149 (MAIN__):
program mult_reals
 1149: 55                   push rbp                                     // Save the caller's frame pointer.
 114a: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.

        implicit none

        real :: a, b, c

        a = 2.2
 114d: f30f1005d70e0000     movss xmm0, DWORD PTR [rip+0xed7]            // Load a from .rodata (202c <options.0.0+0x1c>).
 1155: f30f1145fc           movss DWORD PTR [rbp-0x4], xmm0              // Store a.

        b = 3.3
 115a: f30f1005ce0e0000     movss xmm0, DWORD PTR [rip+0xece]            // Load b from .rodata (2030 <options.0.0+0x20>).
 1162: f30f1145f8           movss DWORD PTR [rbp-0x8], xmm0              // Store b.

        c = b * a
 1167: f30f1045f8           movss xmm0, DWORD PTR [rbp-0x8]              // xmm0 = b.
 116c: f30f5945fc           mulss xmm0, DWORD PTR [rbp-0x4]              // Scalar single multiply. xmm0 = b * a.
 1171: f30f1145f4           movss DWORD PTR [rbp-0xc], xmm0              // Store the result in c.

end program mult_reals
 1176: 90                   nop                                          // Padding in front of the epilogue.
 1177: 5d                   pop rbp                                      // Restore the caller's frame pointer.
 1178: c3                   ret                                          // Pop the return address and return to the caller.
```

| Slot | Variable | Role |
| --- | --- | --- |
| `rbp-0x4` | `a` | 2.2 as a single |
| `rbp-0x8` | `b` | 3.3 as a single |
| `rbp-0xc` | `c` | the `mulss` product |

The shape matches [adding two reals](../ADD_REALS/add_reals.md). Constants are loaded from `.rodata`, kept in the red zone, and combined in `xmm0`. `mulss` replaces `addss`. The `ss` suffix means scalar single precision. The displacements belong to this build.

`pop rbp` and `ret` return to `main`.
