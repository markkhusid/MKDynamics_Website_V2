# Fortran - AMD 64-Bit Platform - An If-Then

Created with Grok Build

## Introduction

This page disassembles a conditional compiled for AMD64. The source is `if_then.f08` from the [Disassembling-Binaries](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/AMD64/Conditionals) tree. The program reads an integer and prints a line when that integer is greater than 5.

`main` is the same runtime prologue as on the [addition page](../ADD_INT/add_int.md). The program body is where the branch is.

## The program *if_then.f08*

```{literalinclude} code/if_then.f08
:language: fortran
```

`num2` is a `parameter`, so it is a compile-time constant. It never gets a stack slot. `num1` is a variable filled by `read`.

```bash
gfortran -ggdb3 if_then.f08 -o if_then_Fortran_AMD64_ggdb3
objdump -d -Mintel -S -w if_then_Fortran_AMD64_ggdb3
```

`-S` interleaves the Fortran source. `-w` keeps each instruction on one line. Each instruction line is the address, the machine bytes, and the Intel disassembly. The notes after `//` were added to that objdump.

## The test

`MAIN__` opens a 0x220-byte frame because each Fortran I/O statement builds a unit descriptor on the stack. The descriptor fields in the listing are internal to libgfortran. The calls around them are the part that matches the source.

The prompt is written in three calls. `_gfortran_st_write` opens the statement, `_gfortran_transfer_character_write` copies the characters, and `_gfortran_st_write_done` finishes it. The length in `edx` is `0x23`, which is 35, the length of `Enter a number between 1 and 10 -> `.

The read is the same shape with the read entry points. `_gfortran_transfer_integer` is told to move 4 bytes into `rbp-0x4`. That slot is `num1`.

```bash
00000000000011a9 (MAIN__):
program if_then
 11a9: 55                   push rbp                                     // Save the caller's frame pointer.
 11aa: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.
 11ad: 4881ec20020000       sub rsp, 0x220                               // Open the frame for num1 and the I/O descriptors.
      implicit none

      integer                   ::      num1
      integer, parameter        ::      num2 = 5

      print *, "Enter a number between 1 and 10 -> "
 11b4: 488d05550e0000       lea rax, [rip+0xe55]                         // Address of a runtime I/O constant (2010 <_IO_stdin_used+0x10>).
 11bb: 488985e8fdffff       mov QWORD PTR [rbp-0x218], rax               // Store that pointer in the descriptor.
 11c2: c785f0fdffff08000000 mov DWORD PTR [rbp-0x210], 0x8               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 11cc: c785e0fdffff80000000 mov DWORD PTR [rbp-0x220], 0x80              // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 11d6: c785e4fdffff06000000 mov DWORD PTR [rbp-0x21c], 0x6               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 11e0: 488d85e0fdffff       lea rax, [rbp-0x220]                         // Address of the unit descriptor.
 11e7: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 11ea: e8b1feffff           call 10a0 <_gfortran_st_write@plt>           // Begin a formatted write.
 11ef: 488d85e0fdffff       lea rax, [rbp-0x220]                         // Address of the unit descriptor.
 11f6: ba23000000           mov edx, 0x23                                // edx = 0x23, which is 35. The prompt is that many characters, including the trailing space.
 11fb: 488d0d9e0e0000       lea rcx, [rip+0xe9e]                         // Address of the character constant (20a0 <_IO_stdin_used+0xa0>).
 1202: 4889ce               mov rsi, rcx                                 // rsi receives the pointer just loaded.
 1205: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 1208: e843feffff           call 1050 <_gfortran_transfer_character_write@plt> // Transfer characters. rdi is the descriptor, rsi the string, edx the length.
 120d: 488d85e0fdffff       lea rax, [rbp-0x220]                         // Address of the unit descriptor.
 1214: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 1217: e854feffff           call 1070 <_gfortran_st_write_done@plt>      // Finish the write.
      read *, num1
 121c: 488d05ed0d0000       lea rax, [rip+0xded]                         // Address of a runtime I/O constant (2010 <_IO_stdin_used+0x10>).
 1223: 488985e8fdffff       mov QWORD PTR [rbp-0x218], rax               // Store that pointer in the descriptor.
 122a: c785f0fdffff09000000 mov DWORD PTR [rbp-0x210], 0x9               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 1234: c785e0fdffff80000000 mov DWORD PTR [rbp-0x220], 0x80              // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 123e: c785e4fdffff05000000 mov DWORD PTR [rbp-0x21c], 0x5               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 1248: 488d85e0fdffff       lea rax, [rbp-0x220]                         // Address of the unit descriptor.
 124f: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 1252: e809feffff           call 1060 <_gfortran_st_read@plt>            // Begin a formatted read.
 1257: 488d4dfc             lea rcx, [rbp-0x4]                           // Address of num1.
 125b: 488d85e0fdffff       lea rax, [rbp-0x220]                         // Address of the unit descriptor.
 1262: ba04000000           mov edx, 0x4                                 // edx = 4. One default integer is four bytes.
 1267: 4889ce               mov rsi, rcx                                 // rsi receives the pointer just loaded.
 126a: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 126d: e8cefdffff           call 1040 <_gfortran_transfer_integer@plt>   // Read one integer into the address in rsi.
 1272: 488d85e0fdffff       lea rax, [rbp-0x220]                         // Address of the unit descriptor.
 1279: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 127c: e8affdffff           call 1030 <_gfortran_st_read_done@plt>       // Finish the read.

      if (num1 > num2) then
 1281: 8b45fc               mov eax, DWORD PTR [rbp-0x4]                 // eax = num1. num2 is the constant 5 and has no slot.
 1284: 83f805               cmp eax, 0x5                                 // Compare num1 with 5. Flags record the result. The difference is not stored.
 1287: 7e68                 jle 12f1 <MAIN__+0x148>                      // Skip the then-body when num1 <= 5. The target is the nop before leave.
              print *, "Number entered greater than 5!"
 1289: 488d05800d0000       lea rax, [rip+0xd80]                         // Address of a runtime I/O constant (2010 <_IO_stdin_used+0x10>).
 1290: 488985e8fdffff       mov QWORD PTR [rbp-0x218], rax               // Store that pointer in the descriptor.
 1297: c785f0fdffff0c000000 mov DWORD PTR [rbp-0x210], 0xc               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 12a1: c785e0fdffff80000000 mov DWORD PTR [rbp-0x220], 0x80              // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 12ab: c785e4fdffff06000000 mov DWORD PTR [rbp-0x21c], 0x6               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 12b5: 488d85e0fdffff       lea rax, [rbp-0x220]                         // Address of the unit descriptor.
 12bc: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 12bf: e8dcfdffff           call 10a0 <_gfortran_st_write@plt>           // Begin a formatted write.
 12c4: 488d85e0fdffff       lea rax, [rbp-0x220]                         // Address of the unit descriptor.
 12cb: ba1e000000           mov edx, 0x1e                                // edx = 0x1e, which is 30, the length of "Number entered greater than 5!".
 12d0: 488d0dec0d0000       lea rcx, [rip+0xdec]                         // Address of the character constant (20c3 <_IO_stdin_used+0xc3>).
 12d7: 4889ce               mov rsi, rcx                                 // rsi receives the pointer just loaded.
 12da: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 12dd: e86efdffff           call 1050 <_gfortran_transfer_character_write@plt> // Transfer characters. rdi is the descriptor, rsi the string, edx the length.
 12e2: 488d85e0fdffff       lea rax, [rbp-0x220]                         // Address of the unit descriptor.
 12e9: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 12ec: e87ffdffff           call 1070 <_gfortran_st_write_done@plt>      // Finish the write.
      end if

end program if_then
 12f1: 90                   nop                                          // Padding in front of the epilogue.
 12f2: c9                   leave                                        // Release this frame and restore the caller's rbp.
 12f3: c3                   ret                                          // Pop the return address and return to the caller.
```

`cmp` subtracts 5 from `eax` for the flags and does not store the difference. The Fortran test is `num1 > num2`. The compiler emits the opposite branch: `jle` jumps over the second print when `num1` is less than or equal to 5. The target of that jump is the `nop` in front of `leave`. Falling through enters the then-body.

That body is another write. The length in `edx` is `0x1e`, which is 30, the length of `Number entered greater than 5!`. After it, execution joins the same `leave` and `ret` that the jump reached.

`leave` is required here. Unlike the leaf arithmetic programs, this frame subtracted from `rsp`, so the epilogue has to restore `rsp` before popping `rbp`.
