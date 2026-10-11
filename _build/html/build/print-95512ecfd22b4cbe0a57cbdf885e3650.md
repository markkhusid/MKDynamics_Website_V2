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
objdump -d -Mintel print_Fortran_AMD64_ggdb3
```

## The three calls

`MAIN__` subtracts `0x210` from `rsp`. That space is the unit descriptor the I/O runtime expects, plus room for the saved registers around the calls. The descriptor fields are internal. The three calls are the statement.

```asm
lea    rax, [rbp-0x210]
mov    rdi, rax
call   _gfortran_st_write

lea    rax, [rbp-0x210]
mov    edx, 0xc                         ; 12 characters
lea    rcx, [rip+...]                   ; "Hello World!"
mov    rsi, rcx
mov    rdi, rax
call   _gfortran_transfer_character_write

lea    rax, [rbp-0x210]
mov    rdi, rax
call   _gfortran_st_write_done
nop
leave
ret
```

`_gfortran_st_write` begins a formatted write. The descriptor pointer is the only argument, in `rdi`. `_gfortran_transfer_character_write` then receives that same descriptor in `rdi`, the string address in `rsi`, and the length in `edx`. `0xc` is 12, the length of `Hello World!`. The characters themselves live in `.rodata`, reached by a rip-relative `lea`. `_gfortran_st_write_done` ends the statement.

`leave` restores the large frame. A leaf arithmetic body can get away with `pop rbp`. This one cannot, because it subtracted from `rsp` and it called other functions.
