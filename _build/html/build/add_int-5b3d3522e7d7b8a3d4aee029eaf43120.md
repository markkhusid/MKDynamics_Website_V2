# Ada - i386 Platform - Add Two Integers

Created with Grok Build

```{figure} ../../../images/Ada/i386/add_Ada_i386_splash.jpg
:height: 600
:width: 800
:align: center
:class: clickable-figure

objdump of the i386 object. The three stores are 3, 5, and 8.
```

## Introduction

This page disassembles `Add_Int` compiled for i386, the 32-bit x86 platform. The source, the assembly, and the object are in the [Disassembling-Binaries Ada tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Ada/Intel_Architecture/i386). The assembly file records `GCC: (Ubuntu 7.3.0-27ubuntu1~18.04) 7.3.0`. The assembly is Intel syntax.

The listing is the object file saved in that tree. The screenshot is objdump of that object, so the addresses match the listing. The object has no line-number table, so objdump does not interleave the source. The three assignment lines in the listing were placed next to the stores by hand. They are the assignment lines of `add_int.adb`.

## The program *add_int.adb*

```{literalinclude} code/add_int.adb
:language: ada
```

`a` is 3, `b` is 5, and `c` is `a + b`. There is no input and no print. The context clause names `Gnat.Io`. This procedure never calls it. On this build an `Integer` is four bytes.

The listing command for the object is:

```bash
objdump -d -Mintel -w add_int.o
```

`-d` disassembles executable sections. `-Mintel` selects Intel operand order. The notes after `//` were added to that listing. The procedure listing stops at `ret`. The PIC helper that follows it in the object is a separate function, shown after the procedure.

## The binder's *main*

The object is the procedure. The binder's `main` is the same shape as the AMD64 listing: spill the arguments, call `__gnat_initialize` and `adainit`, call `_ada_add_int`, then call `adafinal` and `__gnat_finalize`. That objdump is on the AMD64 page: [Add Two Integers](../../AMD64/ADD_INT/add_int.md).

## The addition

```bash
0000000000000000 (_ada_add_int):
    0: 55                   push ebp                                     // Save the caller's frame pointer.
    1: 89e5                 mov ebp, esp                                 // This frame starts at the current stack pointer.
    3: 83ec18               sub esp, 0x18                                // Open the frame for a, b, and c.
    6: e8fcffffff           call 7 <_ada_add_int+0x7>                    // Relocation to __x86.get_pc_thunk.ax. That loads the return address into eax.
    b: 0501000000           add eax, 0x1                                 // Relocation that adds the GOT offset. The stores below do not use eax.
   a := 3;
   10: c745f403000000       mov DWORD PTR [ebp-0xc], 0x3                 // a = 3.
   b := 5;
   17: c745f005000000       mov DWORD PTR [ebp-0x10], 0x5                // b = 5.

   c := a + b;
   1e: c745ec08000000       mov DWORD PTR [ebp-0x14], 0x8                // c = 8. The compiler added the two constants while compiling.
   25: 90                   nop                                          // Padding in front of the epilogue.
   26: c9                   leave                                        // Release the frame and restore the caller's frame pointer.
   27: c3                   ret                                          // Return to the binder's main.
```

`sub esp, 0x18` opens a 24-byte frame. The three integers occupy three of its words:

| Slot | Variable | Value |
| --- | --- | --- |
| `ebp-0xc` | `a` | 3 |
| `ebp-0x10` | `b` | 5 |
| `ebp-0x14` | `c` | 8 |

The assignment `c := a + b` is the store of 8. GNAT added the constants 3 and 5 while compiling, and the object code stores that sum. `leave` releases the frame and restores the caller's frame pointer. `ret` returns to the binder's `main`. The `nop` is padding in front of that epilogue.

## The PIC sequence

The procedure calls `__x86.get_pc_thunk.ax` so that `eax` receives the address of the next instruction, and then adds the distance from there to the global offset table.

In the object those two sites are still relocations:

| Offset | Relocation | Symbol |
| --- | --- | --- |
| `0x7` | `R_386_PC32` | `__x86.get_pc_thunk.ax` |
| `0xc` | `R_386_GOTPC` | `_GLOBAL_OFFSET_TABLE_` |

objdump prints the unapplied bytes. The `call` displacement is the `R_386_PC32` placeholder, so the displayed target is address 7. `add eax, 0x1` is the `R_386_GOTPC` placeholder. After linking, that immediate is the distance from the next instruction to the global offset table. The three stores leave that value in `eax` unused. The helper itself is:

```bash
0000000000000000 (__x86.get_pc_thunk.ax):
    0: 8b0424               mov eax, DWORD PTR [esp]                     // eax = the return address, the instruction after the call.
    3: c3                   ret                                          // Return to that instruction.
```

`mov eax, DWORD PTR [esp]` reads the return address the `call` just pushed. That address is the program counter of the `add`. `ret` comes back to the `add`. The helper's `ret` is the return from the thunk to `_ada_add_int`, and the procedure's own `ret` is the one that returns to `main`.
