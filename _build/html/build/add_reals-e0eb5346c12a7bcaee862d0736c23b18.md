# Fortran - i386 - Add Two Reals

Created with Grok Build

## Introduction

This page disassembles a real addition compiled for i386. The source is `add_reals.f08` from the [Disassembling-Binaries i386 tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/i386/Real_Operations/Add_Reals). `main` is the same runtime prologue as on the [addition page](../ADD_INT/add_int.md). The arithmetic uses the x87 unit: `fld`, `fadd`, and `fstp`.

The debug object's `.comment` section names GCC (Ubuntu 7.3.0-27ubuntu1~18.04) 7.3.0. The saved commands dump the object and the executable:

```bash
objdump -x -D -S -s -g -t -Mintel add_reals.o > objdump_of_dot_o.txt
objdump -x -D -S -s -g -t -Mintel add_reals_Fortran_i386_ggdb3 > objdump_of_dot_exe.txt
```

The listing below is the code in the debug object:

```bash
objdump -d -Mintel -w --section=.text add_reals.o
```

Addresses in the object start at 0. The source lines are placed from the object's line-number table. The notes after `//` were added to the listing.

## The program *add_reals.f08*

```{literalinclude} code/add_reals.f08
:language: fortran
```

`a` is 10.0, `b` is 2.0, and `c` is `b + a`. A default Fortran `real` in this object is a 4-byte IEEE-754 float. The bytes of 10.0 are `00 00 20 41`. The bytes of 2.0 are `00 00 00 40`. Both sit in `.rodata`.

## The addition

The position-independent prologue leaves the GOT address in `eax`. Each `fld` uses that base. The displacement in the object is the `.rodata` offset of the constant, and the relocation is `R_386_GOTOFF`.

```bash
00000000 (MAIN__):
program add_reals
    0: 55                   push ebp                                     // Save the caller's frame pointer.
    1: 89e5                 mov ebp, esp                                 // This frame starts at the current stack pointer.
    3: 83ec10               sub esp, 0x10                                // Three reals need 12 bytes. The compiler opens a 16-byte frame.
    6: e8fcffffff           call 7 <MAIN__+0x7>                          // Unrelocated R_386_PC32 to __x86.get_pc_thunk.ax. The thunk loads its return address into eax.
    b: 0501000000           add eax, 0x1                                 // Unrelocated R_386_GOTPC. After linking, eax holds the GOT address. The loads below use it.
        
        implicit none

        real :: a, b, c

        a = 10.0
   10: d9801c000000         fld DWORD PTR [eax+0x1c]                     // Load 10.0. The displacement is the unapplied R_386_GOTOFF addend, and 0x1c is the .rodata offset of the bytes 00 00 20 41.
   16: d95dfc               fstp DWORD PTR [ebp-0x4]                     // Store a. A default real is a 4-byte float.

        b = 2.0
   19: d98020000000         fld DWORD PTR [eax+0x20]                     // Load 2.0. The addend 0x20 is the .rodata offset of the bytes 00 00 00 40.
   1f: d95df8               fstp DWORD PTR [ebp-0x8]                     // Store b.

        c = b + a
   22: d945f8               fld DWORD PTR [ebp-0x8]                      // Push b onto the x87 stack.
   25: d845fc               fadd DWORD PTR [ebp-0x4]                     // Add a. The source is c = b + a.
   28: d95df4               fstp DWORD PTR [ebp-0xc]                     // Store c. The sum of 2.0 and 10.0 is 12.0.

end program add_reals
   2b: 90                   nop                                          // Padding in front of the epilogue.
   2c: c9                   leave                                        // mov esp, ebp, then pop ebp.
   2d: c3                   ret                                          // Pop the return address and return to main.

```

| Slot | Variable | Value after the add |
| --- | --- | --- |
| `ebp-0x4` | `a` | 10.0 |
| `ebp-0x8` | `b` | 2.0 |
| `ebp-0xc` | `c` | 12.0 |

The source adds `b` to `a`, so the compiler pushes `b` and then adds `a`. `fstp` writes the sum and pops the x87 stack.
