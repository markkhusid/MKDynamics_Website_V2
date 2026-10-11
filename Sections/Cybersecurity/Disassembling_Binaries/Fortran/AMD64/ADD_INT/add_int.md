# Fortran - AMD 64-Bit Platform - Add Two Integers

Created with Grok Build

```{figure} ../../images/AMD64/add_int_f08.jpg
:height: 600
:width: 800
:class: clickable-figure

The three assignments, captured while the program was still named add
```

## Introduction

This page disassembles one Fortran program compiled for AMD64, the 64-bit x86 platform. The debugger session was captured in GDB with GEF, and the assembly is shown in Intel syntax. The same source is the addition example from the ARM64 section. What changes is the machine code around it.

Project code for the whole comparison lives in [Disassembling-Binaries](https://github.com/markkhusid/Disassembling-Binaries).

## The program *add_int.f08*

```{literalinclude} code/add_int.f08
:language: fortran
```

`a` is 1, `b` is 9, and `c` is `a + b`. There is no input and no print. The program exists so the compiler has to store two integers and add them.

On this platform a default Fortran `integer` is four bytes. The processor is 64-bit, and the add still uses the 32-bit registers `eax` and `edx`. The editor screenshot above is an earlier save of the same three lines, under the name `program add`. The binary in the debugger was built from `program add_int`, which is the symbol GEF prints.

The session ran on a small AMD64 instance. The compile line was:

```bash
gfortran -ggdb3 add_int.f08 -o add_int_Fortran_AMD64_ggdb3
```

`-ggdb3` keeps the source lines next to the instructions. Two more products are worth keeping beside the executable:

```bash
gfortran -S -ggdb3 add_int.f08 -o add_int.s
gfortran -c -ggdb3 add_int.s -o add_int.o
```

`-S` writes the compiler's own assembly. `-c` stops after the object file. The listing used with the screenshots was Intel syntax:

```bash
objdump -d -Mintel -S -w add_int_Fortran_AMD64_ggdb3
```

`-d` disassembles executable sections. `-S` interleaves the Fortran source. `-w` keeps each instruction on one line. `-Mintel` selects Intel operand order, so `mov eax, edx` reads as "eax becomes edx." Without `-Mintel`, objdump prints AT&T syntax and the operand order is reversed. The listings below are that objdump of a current build. Each instruction line is the address, the machine bytes, and the Intel disassembly. The notes after `//` were added to the listing. Addresses belong to a position-independent executable, so they will not match the screenshots. A current gfortran also names the program body `MAIN__`. The captured session named it `add_int`.

## Two procedures

gfortran does not put the Fortran program in `main`. `main` is a small C-style entry point. It saves the incoming arguments, calls the gfortran runtime, and then calls the program body.

In the captured binary that body is the symbol `add_int`, taken from the program name. A current gfortran emits the same body under the symbol `MAIN__`. The instructions are the ones below either way. Set the breakpoint on the symbol the binary actually has:

```bash
break *add_int
```

or, on a current gfortran:

```bash
break *MAIN__
```

The `*` stops at the first instruction of the symbol.

## *main* in the captured session

```{figure} ../../images/AMD64/running_add_int_Fortran_AMD64_in_GEF_showing_main.jpg
:alt: Disassembly of main
:align: center
:class: clickable-figure

Disassembly of main
```

`main` is the System V AMD64 prologue, then two runtime calls, then the program.

```bash
0000000000001169 (main):
 1169: 55                   push rbp                                     // Save the caller's frame pointer.
 116a: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.
 116d: 4883ec10             sub rsp, 0x10                                // Open 16 bytes for the spilled argc and argv.
 1171: 897dfc               mov DWORD PTR [rbp-0x4], edi                 // Spill argc.
 1174: 488975f0             mov QWORD PTR [rbp-0x10], rsi                // Spill argv.
 1178: 488b55f0             mov rdx, QWORD PTR [rbp-0x10]                // Reload argv.
 117c: 8b45fc               mov eax, DWORD PTR [rbp-0x4]                 // Reload argc.
 117f: 4889d6               mov rsi, rdx                                 // argv goes to the runtime in rsi.
 1182: 89c7                 mov edi, eax                                 // argc goes to the runtime in edi.
 1184: e8b7feffff           call 1040 <_gfortran_set_args@plt>           // Give the runtime the incoming argc and argv.
 1189: 488d05800e0000       lea rax, [rip+0xe80]                         // Address of the compiler's options block (2010 <options.0.0>).
 1190: 4889c6               mov rsi, rax                                 // The options address is the second argument.
 1193: bf07000000           mov edi, 0x7                                 // edi = 7, the number of 32-bit option words.
 1198: e893feffff           call 1030 <_gfortran_set_options@plt>        // Hand the runtime its seven option words.
 119d: e8a7ffffff           call 1149 <MAIN__>                           // Enter the Fortran program.
 11a2: b800000000           mov eax, 0x0                                 // main returns 0.
 11a7: c9                   leave                                        // Release this frame and restore the caller's rbp.
 11a8: c3                   ret                                          // Pop the return address and return to the caller.
```

`push rbp` saves the caller's frame pointer. `mov rbp, rsp` makes the current stack pointer the frame for this function. `sub rsp, 0x10` opens 16 bytes of local storage. The incoming `argc` arrived in `edi` and `argv` arrived in `rsi`. At `-O0` the compiler spills both to the frame and then copies them back into `edi` and `rsi`, which are the argument registers for the next call. `_gfortran_set_args` receives that pair.

The options block is a rip-relative address. `lea rax, [rip+0xe80]` puts that address in `rax` without reading memory, and the next instruction copies it to `rsi`. In the captured session the options address was formed directly with `lea rsi, [rip+0xaf]`. `edi` is 7, the number of 32-bit option words. `_gfortran_set_options` consumes that pair. Only then does `call 1149 <MAIN__>` enter the Fortran program. The captured session called `add_int`, which is the name that binary gave the program body.

`mov eax, 0` is the return value of `main`. `leave` is `mov rsp, rbp` followed by `pop rbp`, which drops the 16-byte frame and restores the caller. `ret` pops the return address.

## The addition

```{figure} ../../images/AMD64/running_add_Fortran_aarch64_in_GEF_showing_add_int.jpg
:alt: Disassembly of add_int
:align: center
:class: clickable-figure

Disassembly of add_int
```

The filename on that screenshot still says aarch64. The instructions in it are AMD64. This is the body from the current objdump:

```bash
0000000000001149 (MAIN__):
program add_int
 1149: 55                   push rbp                                     // Save the caller's frame pointer.
 114a: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.

    implicit none

    integer :: a, b, c

    a = 1
 114d: c745fc01000000       mov DWORD PTR [rbp-0x4], 0x1                 // a = 1.
    b = 9
 1154: c745f809000000       mov DWORD PTR [rbp-0x8], 0x9                 // b = 9.

    c = a + b
 115b: 8b55fc               mov edx, DWORD PTR [rbp-0x4]                 // edx = a.
 115e: 8b45f8               mov eax, DWORD PTR [rbp-0x8]                 // eax = b.
 1161: 01d0                 add eax, edx                                 // eax = eax + edx.
 1163: 8945f4               mov DWORD PTR [rbp-0xc], eax                 // Store the result in c.

end program add_int
 1166: 90                   nop                                          // Padding in front of the epilogue.
 1167: 5d                   pop rbp                                      // Restore the caller's frame pointer.
 1168: c3                   ret                                          // Pop the return address and return to the caller.
```

The frame grows downward, so the three integers sit at negative offsets from `rbp`:

| Slot | Variable | Value after the add |
| --- | --- | --- |
| `rbp-0x4` | `a` | 1 |
| `rbp-0x8` | `b` | 9 |
| `rbp-0xc` | `c` | 10 (`0xa`) |

`add eax, edx` adds `edx` into `eax` and leaves the sum in `eax`. Intel syntax names the destination first. The store writes that sum to `c`.

This function never subtracts from `rsp`. The three stores land in the 128-byte red zone under `rsp`, which the System V AMD64 ABI leaves unused by signal handlers and by a caller. `pop rbp` restores the caller's frame pointer, and `ret` returns to `main`. The `nop` is padding in front of that epilogue, the same role the ARM builds give a `nop` before the return.

## A current gfortran build

The two listings above are that rebuild. The program body is `MAIN__` instead of the captured session's `add_int`, and the options address is staged through `rax` before it is placed in `rsi`. The arithmetic is unchanged: load 1, load 9, add the 32-bit registers, store the sum at `rbp-0xc`.
