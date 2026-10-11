# Fortran - AMD 64-Bit Platform - A Print Statement

Created with Grok Build

## Introduction

This page disassembles one `print` compiled for AMD64. The source is `print.f08` from the [Disassembling-Binaries](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/AMD64/InputOutput) tree. The statement becomes three calls into libgfortran. There is no write system call in the program body. The runtime does that later.

`main` is the same runtime prologue as on the [addition page](../ADD_INT/add_int.md).

## The program *print.f08*

```{literalinclude} code/print.f08
:language: fortran
```

The string is `Hello World!`, twelve characters.

```bash
gfortran -ggdb3 print.f08 -o print_Fortran_AMD64_ggdb3
objdump -d -Mintel -S -w print_Fortran_AMD64_ggdb3
```

`-S` interleaves the Fortran source. `-w` keeps each instruction on one line. Each instruction line is the address, the machine bytes, and the Intel disassembly. The notes after `//` were added to that objdump.

## The three calls

`MAIN__` subtracts `0x210` from `rsp`. That space is the unit descriptor the I/O runtime expects, plus room for the saved registers around the calls. The descriptor fields are internal. The three calls are the statement.

```bash
0000000000001179 (MAIN__):
program print_program
 1179: 55                   push rbp                                     // Save the caller's frame pointer.
 117a: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.
 117d: 4881ec10020000       sub rsp, 0x210                               // Open the frame for the I/O descriptor.

      print *, "Hello World!"
 1184: 488d05850e0000       lea rax, [rip+0xe85]                         // Address of a runtime I/O constant (2010 <_IO_stdin_used+0x10>).
 118b: 488985f8fdffff       mov QWORD PTR [rbp-0x208], rax               // Store that pointer in the descriptor.
 1192: c78500feffff03000000 mov DWORD PTR [rbp-0x200], 0x3               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 119c: c785f0fdffff80000000 mov DWORD PTR [rbp-0x210], 0x80              // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 11a6: c785f4fdffff06000000 mov DWORD PTR [rbp-0x20c], 0x6               // A descriptor field. libgfortran reads it. It is not a Fortran variable.
 11b0: 488d85f0fdffff       lea rax, [rbp-0x210]                         // Address of the unit descriptor.
 11b7: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 11ba: e8b1feffff           call 1070 <_gfortran_st_write@plt>           // Begin a formatted write.
 11bf: 488d85f0fdffff       lea rax, [rbp-0x210]                         // Address of the unit descriptor.
 11c6: ba0c000000           mov edx, 0xc                                 // edx = 0xc, which is 12, the length of "Hello World!".
 11cb: 488d0dc70e0000       lea rcx, [rip+0xec7]                         // Address of the character constant (2099 <_IO_stdin_used+0x99>).
 11d2: 4889ce               mov rsi, rcx                                 // rsi receives the pointer just loaded.
 11d5: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 11d8: e853feffff           call 1030 <_gfortran_transfer_character_write@plt> // Transfer characters. rdi is the descriptor, rsi the string, edx the length.
 11dd: 488d85f0fdffff       lea rax, [rbp-0x210]                         // Address of the unit descriptor.
 11e4: 4889c7               mov rdi, rax                                 // rdi receives the descriptor pointer.
 11e7: e854feffff           call 1040 <_gfortran_st_write_done@plt>      // Finish the write.

end program print_program
 11ec: 90                   nop                                          // Padding in front of the epilogue.
 11ed: c9                   leave                                        // Release this frame and restore the caller's rbp.
 11ee: c3                   ret                                          // Pop the return address and return to the caller.
```

`_gfortran_st_write` begins a formatted write. The descriptor pointer is the only argument, in `rdi`. `_gfortran_transfer_character_write` then receives that same descriptor in `rdi`, the string address in `rsi`, and the length in `edx`. `0xc` is 12, the length of `Hello World!`. The characters themselves live in `.rodata`, reached by a rip-relative `lea`. `_gfortran_st_write_done` ends the statement.

`leave` restores the large frame. A leaf arithmetic body can get away with `pop rbp`. This one cannot, because it subtracted from `rsp` and it called other functions.
