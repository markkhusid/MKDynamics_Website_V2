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
objdump -d -Mintel add_reals_Fortran_AMD64_ggdb3
```

## The addition

```asm
push   rbp
mov    rbp, rsp
movss  xmm0, DWORD PTR [rip+0xed7]  ; a = 10.0 from .rodata
movss  DWORD PTR [rbp-0x4], xmm0
movss  xmm0, DWORD PTR [rip+0xece]  ; b = 2.0 from .rodata
movss  DWORD PTR [rbp-0x8], xmm0
movss  xmm0, DWORD PTR [rbp-0x8]    ; xmm0 = b
addss  xmm0, DWORD PTR [rbp-0x4]    ; xmm0 = b + a
movss  DWORD PTR [rbp-0xc], xmm0    ; c
nop
pop    rbp
ret
```

| Slot | Variable | Value |
| --- | --- | --- |
| `rbp-0x4` | `a` | 10.0 |
| `rbp-0x8` | `b` | 2.0 |
| `rbp-0xc` | `c` | 12.0 |

`movss` and `addss` move and add a scalar single. The `ss` suffix is the four-byte form. A double would be `movsd` and `addsd`. `xmm0` is the destination, and the second operand of `addss` may be memory, so `a` is added without a second XMM load.

The displacements belong to this build. They point just past the compiler's options block in `.rodata`. Another link will move them. The values at those addresses are the single-precision encodings of 10.0 and 2.0.

The body is a leaf, so the three singles sit in the red zone. `pop rbp` and `ret` return to `main`.
