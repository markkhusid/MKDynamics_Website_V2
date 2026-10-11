# Fortran - i386 - Multiply Two Integers

Created with Grok Build

```{figure} ../../images/i386/mult_Fortran_i386_splash.jpg
:height: 600
:width: 800
:class: clickable-figure

Radare2 session for the i386 multiply program
```

## Introduction

This page disassembles integer multiplication compiled for i386. The source is `mult.f08` from the [Disassembling-Binaries i386 tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/i386/Integer_Operations/Mult_Int). The tree saves the executable and its objdump. It does not save a separate object file, so the listing below is `MAIN__` from `mult_Fortran_i386`.

The executable's `.comment` section names GCC (Ubuntu 8.2.0-1ubuntu2~18.04) 8.2.0. The compile command was not recorded. The figure is a Radare2 session of this program. The listing is objdump of the saved executable, in Intel syntax:

```bash
objdump -d -Mintel -w mult_Fortran_i386
```

The source lines are placed from the executable's line-number table. The notes after `//` were added to the listing. `main` does the same runtime setup described on the [addition page](../ADD_INT/add_int.md).

## The program *mult.f08*

```{literalinclude} code/mult.f08
:language: fortran
```

`a` is 2, `b` is 3, and `c` is `a * b`. A default Fortran `integer` is four bytes.

## The multiplication

`MAIN__` is at `0x5a9` in this executable. The thunk call and the GOT add already have their displacements filled in. The stores of `a` and `b` are immediates, and the multiply overwrites `eax`, so the product does not read the GOT address.

```bash
000005a9 (MAIN__):
program mult
  5a9: 55                   push ebp                                     // Save the caller's frame pointer.
  5aa: 89e5                 mov ebp, esp                                 // This frame starts at the current stack pointer.
  5ac: 83ec10               sub esp, 0x10                                // Three integers need 12 bytes. The compiler opens a 16-byte frame.
  5af: e874000000           call 628 <__x86.get_pc_thunk.ax>             // Call __x86.get_pc_thunk.ax. The thunk is mov eax, DWORD PTR [esp], then ret.
  5b4: 05201a0000           add eax, 0x1a20                              // eax becomes the GOT base. This displacement is already filled in. The multiply below does not read eax.

	implicit none

	integer		:: a, b, c

	a = 2
  5b9: c745fc02000000       mov DWORD PTR [ebp-0x4], 0x2                 // a = 2.
	b = 3
  5c0: c745f803000000       mov DWORD PTR [ebp-0x8], 0x3                 // b = 3.

	c = a * b
  5c7: 8b45fc               mov eax, DWORD PTR [ebp-0x4]                 // eax = a.
  5ca: 0faf45f8             imul eax, DWORD PTR [ebp-0x8]                // eax = a * b.
  5ce: 8945f4               mov DWORD PTR [ebp-0xc], eax                 // Store the product in c.

end program mult
  5d1: 90                   nop                                          // Padding in front of the epilogue.
  5d2: c9                   leave                                        // mov esp, ebp, then pop ebp.
  5d3: c3                   ret                                          // Pop the return address and return to main.
```

| Slot | Variable | Value after the multiply |
| --- | --- | --- |
| `ebp-0x4` | `a` | 2 |
| `ebp-0x8` | `b` | 3 |
| `ebp-0xc` | `c` | 6 |

`imul eax, DWORD PTR [ebp-0x8]` multiplies `eax` by `b` and leaves the product in `eax`. Two times three is 6.
