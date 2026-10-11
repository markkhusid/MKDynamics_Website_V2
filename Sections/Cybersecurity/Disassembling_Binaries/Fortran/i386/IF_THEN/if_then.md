# Fortran - i386 - An If-Then

Created with Grok Build

## Introduction

This page disassembles a conditional compiled for i386. The source is `if_then.f08` from the [Disassembling-Binaries i386 tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/i386/Conditionals). The program reads an integer and prints a line when that integer is greater than 5.

`main` is the same runtime prologue as on the [addition page](../ADD_INT/add_int.md). The branch is in `MAIN__`.

The debug object's `.comment` section names GCC (Ubuntu 7.3.0-27ubuntu1~18.04) 7.3.0. The recorded commands are:

```bash
gfortran -m32 -ggdb3 -S if_then.f08
gfortran -m32 -ggdb3 -c if_then.s
gfortran -m32 -ggdb3 if_then.o -o if_then_Fortran_i386_ggdb3
objdump -x -D -S -s -g -t -Mintel if_then.o > objdump_of_dot_o.txt
```

The listing below is the code in that object:

```bash
objdump -d -Mintel -w --section=.text if_then.o
```

Addresses in the object start at 0. The source lines are placed from the object's line-number table. The notes after `//` were added to the listing.

## The program *if_then.f08*

```{literalinclude} code/if_then.f08
:language: fortran
```

`num2` is a parameter, so it is the immediate 5 and it has no stack slot. `num1` is filled by `read`.

## The test

`MAIN__` saves `ebx` and subtracts `0x164` from `esp`. `ebx` holds the GOT address, and the I/O descriptors occupy the rest of the frame. `num1` is the 4-byte slot at `ebp-0xc`.

Each Fortran I/O statement builds a descriptor and calls the runtime. `_gfortran_st_write` opens a print, `_gfortran_transfer_character_write` copies the characters, and `_gfortran_st_write_done` finishes it. The read uses `_gfortran_st_read`, `_gfortran_transfer_integer`, and `_gfortran_st_read_done`. On i386 the arguments are pushed, last argument first.

The prompt is 35 characters and starts at `.rodata` offset `0xc`. The second message is 30 characters and starts at offset `0x2f`. Those lengths are the immediates `0x23` and `0x1e`.

```bash
00000000 (MAIN__):
program if_then
    0: 55                   push ebp                                     // Save the caller's frame pointer.
    1: 89e5                 mov ebp, esp                                 // This frame starts at the current stack pointer.
    3: 53                   push ebx                                     // Save ebx. The PIC base stays in ebx, so num1 is not stored at ebp-0x4.
    4: 81ec64010000         sub esp, 0x164                               // Open the frame for num1 and the I/O descriptors.
    a: e8fcffffff           call b <MAIN__+0xb>                          // Unrelocated R_386_PC32 to __x86.get_pc_thunk.bx.
    f: 81c302000000         add ebx, 0x2                                 // Unrelocated R_386_GOTPC. After linking, ebx holds the GOT address.

      implicit none

      integer                   ::      num1
      integer, parameter        ::      num2 = 5

      print *, "Enter a number between 1 and 10 -> "
   15: 8d8300000000         lea eax, [ebx+0x0]                           // Pointer to the start of .rodata. Those bytes are the filename if_then.f08. The relocation is R_386_GOTOFF.
   1b: 8985a8feffff         mov DWORD PTR [ebp-0x158], eax               // Store that pointer in the descriptor.
   21: c785acfeffff08000000 mov DWORD PTR [ebp-0x154], 0x8               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
   2b: c785a0feffff80000000 mov DWORD PTR [ebp-0x160], 0x80              // A descriptor field. libgfortran reads it. It is not a Fortran variable.
   35: c785a4feffff06000000 mov DWORD PTR [ebp-0x15c], 0x6               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
   3f: 83ec0c               sub esp, 0xc                                 // One argument is 4 bytes. The pad keeps the call 16-byte aligned.
   42: 8d85a0feffff         lea eax, [ebp-0x160]                         // Address of the descriptor.
   48: 50                   push eax                                     // Push the descriptor. It is the argument of _gfortran_st_write.
   49: e8fcffffff           call 4a <MAIN__+0x4a>                        // Unrelocated R_386_PLT32 to _gfortran_st_write. This opens the prompt.
   4e: 83c410               add esp, 0x10                                // Drop the argument and the alignment pad.
   51: 83ec04               sub esp, 0x4                                 // Three arguments are 12 bytes. The extra 4 bytes keep the call aligned.
   54: 6a23                 push 0x23                                    // The prompt is 35 characters.
   56: 8d830c000000         lea eax, [ebx+0xc]                           // The prompt starts at .rodata offset 0xc. The relocation is R_386_GOTOFF.
   5c: 50                   push eax                                     // Push the address of the prompt.
   5d: 8d85a0feffff         lea eax, [ebp-0x160]                         // Address of the descriptor.
   63: 50                   push eax                                     // Push the descriptor. It is the first argument.
   64: e8fcffffff           call 65 <MAIN__+0x65>                        // Unrelocated R_386_PLT32 to _gfortran_transfer_character_write.
   69: 83c410               add esp, 0x10                                // Drop the arguments and the alignment pad.
   6c: 83ec0c               sub esp, 0xc                                 // One argument is 4 bytes. The pad keeps the call 16-byte aligned.
   6f: 8d85a0feffff         lea eax, [ebp-0x160]                         // Address of the descriptor.
   75: 50                   push eax                                     // Push the descriptor.
   76: e8fcffffff           call 77 <MAIN__+0x77>                        // Unrelocated R_386_PLT32 to _gfortran_st_write_done. This finishes the prompt.
   7b: 83c410               add esp, 0x10                                // Drop the argument and the alignment pad.
      read *, num1
   7e: 8d8300000000         lea eax, [ebx+0x0]                           // Same .rodata pointer, the filename, for the read. The relocation is R_386_GOTOFF.
   84: 8985a8feffff         mov DWORD PTR [ebp-0x158], eax               // Store that pointer in the descriptor.
   8a: c785acfeffff09000000 mov DWORD PTR [ebp-0x154], 0x9               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
   94: c785a0feffff80000000 mov DWORD PTR [ebp-0x160], 0x80              // A descriptor field. libgfortran reads it. It is not a Fortran variable.
   9e: c785a4feffff05000000 mov DWORD PTR [ebp-0x15c], 0x5               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
   a8: 83ec0c               sub esp, 0xc                                 // One argument is 4 bytes. The pad keeps the call 16-byte aligned.
   ab: 8d85a0feffff         lea eax, [ebp-0x160]                         // Address of the descriptor.
   b1: 50                   push eax                                     // Push the descriptor.
   b2: e8fcffffff           call b3 <MAIN__+0xb3>                        // Unrelocated R_386_PLT32 to _gfortran_st_read. This opens the read.
   b7: 83c410               add esp, 0x10                                // Drop the argument and the alignment pad.
   ba: 83ec04               sub esp, 0x4                                 // Three arguments are 12 bytes. The extra 4 bytes keep the call aligned.
   bd: 6a04                 push 0x4                                     // num1 is a 4-byte integer.
   bf: 8d45f4               lea eax, [ebp-0xc]                           // Address of num1, at ebp-0xc.
   c2: 50                   push eax                                     // Push the address of num1.
   c3: 8d85a0feffff         lea eax, [ebp-0x160]                         // Address of the descriptor.
   c9: 50                   push eax                                     // Push the descriptor. It is the first argument.
   ca: e8fcffffff           call cb <MAIN__+0xcb>                        // Unrelocated R_386_PLT32 to _gfortran_transfer_integer.
   cf: 83c410               add esp, 0x10                                // Drop the arguments and the alignment pad.
   d2: 83ec0c               sub esp, 0xc                                 // One argument is 4 bytes. The pad keeps the call 16-byte aligned.
   d5: 8d85a0feffff         lea eax, [ebp-0x160]                         // Address of the descriptor.
   db: 50                   push eax                                     // Push the descriptor.
   dc: e8fcffffff           call dd <MAIN__+0xdd>                        // Unrelocated R_386_PLT32 to _gfortran_st_read_done. This finishes the read.
   e1: 83c410               add esp, 0x10                                // Drop the argument and the alignment pad.

      if (num1 > num2) then
   e4: 8b45f4               mov eax, DWORD PTR [ebp-0xc]                 // eax = num1.
   e7: 83f805               cmp eax, 0x5                                 // Compare num1 with 5. num2 is a parameter, so it is the immediate.
   ea: 7e69                 jle 155 <MAIN__+0x155>                       // Skip the second print when num1 is less than or equal to 5.
              print *, "Number entered greater than 5!"
   ec: 8d8300000000         lea eax, [ebx+0x0]                           // Same .rodata pointer, the filename, for the second print. The relocation is R_386_GOTOFF.
   f2: 8985a8feffff         mov DWORD PTR [ebp-0x158], eax               // Store that pointer in the descriptor.
   f8: c785acfeffff0c000000 mov DWORD PTR [ebp-0x154], 0xc               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
  102: c785a0feffff80000000 mov DWORD PTR [ebp-0x160], 0x80              // A descriptor field. libgfortran reads it. It is not a Fortran variable.
  10c: c785a4feffff06000000 mov DWORD PTR [ebp-0x15c], 0x6               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
  116: 83ec0c               sub esp, 0xc                                 // One argument is 4 bytes. The pad keeps the call 16-byte aligned.
  119: 8d85a0feffff         lea eax, [ebp-0x160]                         // Address of the descriptor.
  11f: 50                   push eax                                     // Push the descriptor.
  120: e8fcffffff           call 121 <MAIN__+0x121>                      // Unrelocated R_386_PLT32 to _gfortran_st_write. This opens the second print.
  125: 83c410               add esp, 0x10                                // Drop the argument and the alignment pad.
  128: 83ec04               sub esp, 0x4                                 // Three arguments are 12 bytes. The extra 4 bytes keep the call aligned.
  12b: 6a1e                 push 0x1e                                    // The message is 30 characters.
  12d: 8d832f000000         lea eax, [ebx+0x2f]                          // The message starts at .rodata offset 0x2f. The relocation is R_386_GOTOFF.
  133: 50                   push eax                                     // Push the address of the message.
  134: 8d85a0feffff         lea eax, [ebp-0x160]                         // Address of the descriptor.
  13a: 50                   push eax                                     // Push the descriptor. It is the first argument.
  13b: e8fcffffff           call 13c <MAIN__+0x13c>                      // Unrelocated R_386_PLT32 to _gfortran_transfer_character_write.
  140: 83c410               add esp, 0x10                                // Drop the arguments and the alignment pad.
  143: 83ec0c               sub esp, 0xc                                 // One argument is 4 bytes. The pad keeps the call 16-byte aligned.
  146: 8d85a0feffff         lea eax, [ebp-0x160]                         // Address of the descriptor.
  14c: 50                   push eax                                     // Push the descriptor.
  14d: e8fcffffff           call 14e <MAIN__+0x14e>                      // Unrelocated R_386_PLT32 to _gfortran_st_write_done. This finishes the second print.
  152: 83c410               add esp, 0x10                                // Drop the argument and the alignment pad.
      end if

end program if_then
  155: 90                   nop                                          // Padding in front of the epilogue. The jle lands here.
  156: 8b5dfc               mov ebx, DWORD PTR [ebp-0x4]                 // Restore ebx from the slot under the frame pointer.
  159: c9                   leave                                        // mov esp, ebp, then pop ebp.
  15a: c3                   ret                                          // Pop the return address and return to main.
```

`cmp eax, 0x5` and `jle` turn `num1 > num2` into a skip. When `num1` is greater than 5, execution falls into the second print. When it is 5 or less, the branch lands on the `nop` in front of the epilogue.

The epilogue reloads `ebx` from `ebp-0x4` before `leave` and `ret`.
