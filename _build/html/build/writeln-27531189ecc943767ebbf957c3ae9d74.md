# Pascal - AMD64 - Writeln

Created with Grok Build

## Introduction

This page disassembles `writeln_program` compiled for AMD64. The source is [InputOutput](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Pascal/Intel_Architecture/AMD64/InputOutput). The assembly is Intel syntax. The compiler is Free Pascal 3.0.4+dfsg-18ubuntu2, dated 2018/08/29, for x86_64. The banner is the `.fpc.n_version` section. `main` and `PASCALMAIN` are the same entry. On this build `INTEGER` is a 16-bit Smallint. The variables are BSS symbols. The code is in `.text.n_main`. The `.text` section is empty, so `objdump --section=.text` prints nothing useful. The notes after `//` were added to the listing. A `call` whose displacement is zero is an unapplied relocation, and objdump prints the next instruction as the target.

## The program *writeln.pp*

```{literalinclude} code/writeln.pp
:language: pascal
```

The program prints one line. The string in the object is the shortstring `Hello World!`.

## PASCALMAIN

The compile command was not recorded. This listing is:

```bash
objdump -d -Mintel -w -j .text.n_main writeln.o
```


```bash
0000000000000000 (main):
PROGRAM writeln_program;

BEGIN
    0: 55                   push rbp                                    // Save the caller's frame pointer.
    1: 4889e5               mov rbp, rsp                                // This frame starts at the current stack pointer.
    4: 488d6424f0           lea rsp, [rsp-0x10]                         // Open 16 bytes. rbx is saved in that slot.
    9: 48895df8             mov QWORD PTR [rbp-0x8], rbx                // Save rbx. The text-file pointer has to survive the later calls.
    d: e800000000           call 12 <main+0x12>                         // Call FPC_INITIALIZEUNITS. The displacement is unapplied.
	writeln('Hello World!');
   12: e800000000           call 17 <main+0x17>                         // Call fpc_get_output. The text file comes back in rax.
   17: 4889c3               mov rbx, rax                                // rbx = that text file.
   1a: 48ba0000000000000000 movabs rdx, 0x0                             // rdx = the shortstring _$WRITELN_PROGRAM$_Ld1. The immediate is the unapplied R_X86_64_64.
   24: 4889de               mov rsi, rbx                                // rsi = the text file, the second argument.
   27: bf00000000           mov edi, 0x0                                // edi = 0, the field width. Width 0 adds no blank padding.
   2c: e800000000           call 31 <main+0x31>                         // Call fpc_write_text_shortstr(width, text, shortstring). The displacement is unapplied.
   31: e800000000           call 36 <main+0x36>                         // Call FPC_IOCHECK. It checks the I/O result of the write.
   36: 4889df               mov rdi, rbx                                // rdi = the text file, the argument of fpc_writeln_end.
   39: e800000000           call 3e <main+0x3e>                         // Call fpc_writeln_end. It writes the line ending.
   3e: e800000000           call 43 <main+0x43>                         // Call FPC_IOCHECK again, for the line ending.
END.
   43: e800000000           call 48 <main+0x48>                         // Call FPC_DO_EXIT. The displacement is unapplied.
   48: 488b5df8             mov rbx, QWORD PTR [rbp-0x8]                // Restore rbx.
   4c: c9                   leave                                       // Release this frame.
   4d: c3                   ret                                         // Return.
```

The shortstring is 16 bytes. The first byte is the length. The AMD64 object holds `Hello World!`:

```text
0c 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 00 00 00
```

`fpc_write_text_shortstr` takes the field width, the text file, and the shortstring. The width in `edi` is 0. The helper writes the characters counted by the length byte, and it pads with blanks when the width is greater than that length. Width 0 adds no blanks. `FPC_IOCHECK` follows the write and the line ending.

`fpc_get_output` returns the output text file in `rax`, and the body keeps it in `rbx` across the calls. `fpc_writeln_end` writes the newline. `FPC_DO_EXIT` ends the program.

