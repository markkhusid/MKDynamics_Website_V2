# Fortran - i386 - Divide Two Integers

Created with Grok Build

## Introduction

This page disassembles integer division compiled for i386. The source is `div_int.f08` from the [Disassembling-Binaries i386 tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/i386/Integer_Operations/Div_Int). `main` is the same runtime prologue as on the [addition page](../ADD_INT/add_int.md). The new instructions are `cdq` and `idiv`.

The debug object's `.comment` section names GCC (Ubuntu 7.3.0-27ubuntu1~18.04) 7.3.0. The compile command was not recorded. The listing is:

```bash
objdump -d -Mintel -w --section=.text div_int.o
```

Addresses in the object start at 0. The source lines are placed from the object's line-number table. The notes after `//` were added to the listing.

## The program *div_int.f08*

```{literalinclude} code/div_int.f08
:language: fortran
```

`a` is 10, `b` is 5, and `c` is `a / b`. A default Fortran `integer` is four bytes, and integer division keeps the quotient.

## The division

`MAIN__` opens a 16-byte frame. The position-independent prologue loads the GOT address into `eax`, and the division does not read it.

```bash
00000000 (MAIN__):
program div_int
    0: 55                   push ebp                                     // Save the caller's frame pointer.
    1: 89e5                 mov ebp, esp                                 // This frame starts at the current stack pointer.
    3: 83ec10               sub esp, 0x10                                // Three integers need 12 bytes. The compiler opens a 16-byte frame.
    6: e8fcffffff           call 7 <MAIN__+0x7>                          // Unrelocated R_386_PC32 to __x86.get_pc_thunk.ax. The thunk loads its return address into eax.
    b: 0501000000           add eax, 0x1                                 // Unrelocated R_386_GOTPC. The immediate is a placeholder. The division below does not read eax.

        implicit none

        integer         :: a, b, c

        a = 10
   10: c745fc0a000000       mov DWORD PTR [ebp-0x4], 0xa                 // a = 10.
        b = 5
   17: c745f805000000       mov DWORD PTR [ebp-0x8], 0x5                 // b = 5.

        c = a / b
   1e: 8b45fc               mov eax, DWORD PTR [ebp-0x4]                 // eax = a.
   21: 99                   cdq                                          // Sign-extend eax into edx. idiv divides the 64-bit pair edx:eax.
   22: f77df8               idiv DWORD PTR [ebp-0x8]                     // Divide edx:eax by b. The quotient stays in eax. The remainder stays in edx.
   25: 8945f4               mov DWORD PTR [ebp-0xc], eax                 // Store the quotient in c.

end program div_int
   28: 90                   nop                                          // Padding in front of the epilogue.
   29: c9                   leave                                        // mov esp, ebp, then pop ebp.
   2a: c3                   ret                                          // Pop the return address and return to main.

```

| Slot | Variable | Value after the divide |
| --- | --- | --- |
| `ebp-0x4` | `a` | 10 |
| `ebp-0x8` | `b` | 5 |
| `ebp-0xc` | `c` | 2 |

`idiv` divides the 64-bit pair `edx:eax` by a 32-bit divisor. `cdq` fills `edx` with the sign of `eax`, so a positive 10 makes `edx` zero. The quotient lands in `eax` and the remainder lands in `edx`. Only `eax` is stored. Ten divided by five is the quotient 2 and the remainder 0.
