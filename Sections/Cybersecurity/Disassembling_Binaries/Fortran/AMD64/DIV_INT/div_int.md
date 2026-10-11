# Fortran - AMD 64-Bit Platform - Divide Two Integers

Created with Grok Build

## Introduction

This page disassembles integer division compiled for AMD64. The source is `div_int.f08` from the [Disassembling-Binaries](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/AMD64/Integer_Operations/Div_Int) tree. `main` is the same runtime prologue as on the [addition page](../ADD_INT/add_int.md). The new instructions are `cdq` and `idiv`.

## The program *div_int.f08*

```{literalinclude} code/div_int.f08
:language: fortran
```

`a` is 10, `b` is 5, and `c` is `a / b`. A default Fortran `integer` is four bytes, and integer division keeps the quotient. The remainder is not stored.

```bash
gfortran -ggdb3 div_int.f08 -o div_int_Fortran_AMD64_ggdb3
objdump -d -Mintel -S -w div_int_Fortran_AMD64_ggdb3
```

`-S` interleaves the Fortran source. `-w` keeps each instruction on one line. Each instruction line is the address, the machine bytes, and the Intel disassembly. The notes after `//` were added to that objdump.

## The division

`MAIN__` is a leaf. The three integers sit in the red zone under `rsp`.

```bash
0000000000001149 (MAIN__):
program div_int
 1149: 55                   push rbp                                     // Save the caller's frame pointer.
 114a: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.

        implicit none

        integer         :: a, b, c

        a = 10
 114d: c745fc0a000000       mov DWORD PTR [rbp-0x4], 0xa                 // a = 10.
        b = 5
 1154: c745f805000000       mov DWORD PTR [rbp-0x8], 0x5                 // b = 5.

        c = a / b
 115b: 8b45fc               mov eax, DWORD PTR [rbp-0x4]                 // eax = a.
 115e: 99                   cdq                                          // Sign-extend eax into edx. idiv divides the 64-bit pair edx:eax.
 115f: f77df8               idiv DWORD PTR [rbp-0x8]                     // Divide edx:eax by b. Quotient stays in eax. Remainder stays in edx.
 1162: 8945f4               mov DWORD PTR [rbp-0xc], eax                 // Store the result in c.

end program div_int
 1165: 90                   nop                                          // Padding in front of the epilogue.
 1166: 5d                   pop rbp                                      // Restore the caller's frame pointer.
 1167: c3                   ret                                          // Pop the return address and return to the caller.
```

| Slot | Variable | Value after the divide |
| --- | --- | --- |
| `rbp-0x4` | `a` | 10 |
| `rbp-0x8` | `b` | 5 |
| `rbp-0xc` | `c` | 2 |

`idiv r/m32` divides the 64-bit pair `edx:eax` by a 32-bit divisor. The quotient lands in `eax`. The remainder lands in `edx`. `cdq` fills `edx` with the sign bit of `eax`, so a positive 10 makes `edx` zero and a negative dividend stays a signed division. The compiler uses `idiv`, not the unsigned `div`, because a Fortran `integer` is signed.

Only `eax` is stored. Fortran's `/` on integers is the quotient, so the remainder in `edx` is dropped. Ten divided by five is the quotient 2 and the remainder 0.

`pop rbp` and `ret` leave the function the same way the addition body does.
