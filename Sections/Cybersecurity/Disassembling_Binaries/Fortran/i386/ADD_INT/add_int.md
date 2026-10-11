# Fortran - i386 - Add Two Integers

Created with Grok Build

## Introduction

This page disassembles integer addition compiled for i386, the 32-bit x86 platform. The source is `add_int.f08` from the [Disassembling-Binaries i386 tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/i386/Integer_Operations/Add_Int). The program name in the source is `add`. gfortran names the body `MAIN__`.

The debug object's `.comment` section names GCC (Debian 8.2.0-14) 8.2.0. The compile command was not recorded. The saved objdump command is:

```bash
objdump -x -D -S -s -g -t -Mintel add_int.o > objdump_of_dot_o.txt
```

The listing below is the code in that object:

```bash
objdump -d -Mintel -w --section=.text add_int.o
```

Addresses in the object start at 0. A call whose displacement is still the relocation placeholder is printed as a call to the next instruction. The source lines are placed from the object's line-number table. The notes after `//` were added to the listing.

A default Fortran `integer` is four bytes.

## The program *add_int.f08*

```{literalinclude} code/add_int.f08
:language: fortran
```

`a` is 1, `b` is 9, and `c` is `a + b`. There is no input and no print.

## The addition

The prologue subtracts `0x10` from `esp`. `a` is at `ebp-0x4`, `b` is at `ebp-0x8`, and `c` is at `ebp-0xc`.

The first call and the following add are the i386 position-independent prologue. `__x86.get_pc_thunk.ax` returns the address of the next instruction in `eax`, and the add turns that into the GOT address. The stores of `a` and `b` use immediates. The add then overwrites `eax` with `b`, so the arithmetic does not read the GOT address.

```bash
00000000 (MAIN__):
program add
    0: 55                   push ebp                                     // Save the caller's frame pointer.
    1: 89e5                 mov ebp, esp                                 // This frame starts at the current stack pointer.
    3: 83ec10               sub esp, 0x10                                // Three integers need 12 bytes. The compiler opens a 16-byte frame.
    6: e8fcffffff           call 7 <MAIN__+0x7>                          // Unrelocated R_386_PC32 to __x86.get_pc_thunk.ax. The thunk loads its return address into eax.
    b: 0501000000           add eax, 0x1                                 // Unrelocated R_386_GOTPC. The immediate is a placeholder. After linking, eax holds the GOT address. The stores below do not read eax.

	implicit none

	integer		:: a, b, c

	a = 1
   10: c745fc01000000       mov DWORD PTR [ebp-0x4], 0x1                 // a = 1.
	b = 9
   17: c745f809000000       mov DWORD PTR [ebp-0x8], 0x9                 // b = 9.

	c = a + b
   1e: 8b55fc               mov edx, DWORD PTR [ebp-0x4]                 // edx = a.
   21: 8b45f8               mov eax, DWORD PTR [ebp-0x8]                 // eax = b.
   24: 01d0                 add eax, edx                                 // eax = a + b.
   26: 8945f4               mov DWORD PTR [ebp-0xc], eax                 // Store the sum in c.

end program add
   29: 90                   nop                                          // Padding in front of the epilogue.
   2a: c9                   leave                                        // mov esp, ebp, then pop ebp.
   2b: c3                   ret                                          // Pop the return address and return to main.
```

| Slot | Variable | Value after the add |
| --- | --- | --- |
| `ebp-0x4` | `a` | 1 |
| `ebp-0x8` | `b` | 9 |
| `ebp-0xc` | `c` | 10 |

`add eax, edx` is the sum. `leave` restores `esp` and `ebp`. `ret` returns to `main`.

## *main*

`main` is in the same object. It aligns `esp` to 16 bytes, passes `argc` and `argv` to `_gfortran_set_args`, passes seven option words to `_gfortran_set_options`, calls `MAIN__`, and returns 0. The division and real-add objects contain this same `main`. The if-then object's `main` follows the same steps. Its option words sit at `.rodata` offset `0x50`, after the filename and the two messages, so that `lea` uses addend `0x50`.

```bash
0000002c (main):
   2c: 8d4c2404             lea ecx, [esp+0x4]                           // ecx points at argc. argv begins four bytes later.
   30: 83e4f0               and esp, 0xfffffff0                          // Align esp to 16 bytes.
   33: ff71fc               push DWORD PTR [ecx-0x4]                     // Keep the return address on the aligned stack.
   36: 55                   push ebp                                     // Save the caller's frame pointer.
   37: 89e5                 mov ebp, esp                                 // This frame starts at the current stack pointer.
   39: 53                   push ebx                                     // Save ebx. The PIC base will live there.
   3a: 51                   push ecx                                     // Save the pointer to argc.
   3b: e8fcffffff           call 3c <main+0x10>                          // Unrelocated R_386_PC32 to __x86.get_pc_thunk.bx.
   40: 81c302000000         add ebx, 0x2                                 // Unrelocated R_386_GOTPC. After linking, ebx holds the GOT address.
   46: 89c8                 mov eax, ecx                                 // eax = the saved pointer to argc.
   48: 83ec08               sub esp, 0x8                                 // Open the argument area.
   4b: ff7004               push DWORD PTR [eax+0x4]                     // Push argv.
   4e: ff30                 push DWORD PTR [eax]                         // Push argc. It is the first argument of _gfortran_set_args.
   50: e8fcffffff           call 51 <main+0x25>                          // Unrelocated R_386_PLT32 to _gfortran_set_args.
   55: 83c410               add esp, 0x10                                // Drop the arguments and the alignment pad.
   58: 83ec08               sub esp, 0x8                                 // Open the argument area for the next call.
   5b: 8d8300000000         lea eax, [ebx+0x0]                           // Unrelocated R_386_GOTOFF to .rodata. eax will point at the seven option words.
   61: 50                   push eax                                     // Push the address of the options.
   62: 6a07                 push 0x7                                     // Push 7, the number of option words. It is the first argument of _gfortran_set_options.
   64: e8fcffffff           call 65 <main+0x39>                          // Unrelocated R_386_PLT32 to _gfortran_set_options.
   69: 83c410               add esp, 0x10                                // Drop the arguments and the alignment pad.
   6c: e88fffffff           call 0 <MAIN__>                              // Call the program body. This displacement points at MAIN__ in the same object.
   71: b800000000           mov eax, 0x0                                 // main returns 0.
   76: 8d65f8               lea esp, [ebp-0x8]                           // Point esp at the saved ecx.
   79: 59                   pop ecx                                      // Restore the pointer to argc.
   7a: 5b                   pop ebx                                      // Restore ebx.
   7b: 5d                   pop ebp                                      // Restore the caller's frame pointer.
   7c: 8d61fc               lea esp, [ecx-0x4]                           // Restore the incoming esp.
   7f: c3                   ret                                          // Return to the caller of main.
```

The seven option words sit in `.rodata`. libgfortran reads them. They are not Fortran variables.
