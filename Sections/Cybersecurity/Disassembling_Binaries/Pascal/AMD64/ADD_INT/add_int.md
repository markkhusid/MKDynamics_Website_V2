# Pascal - AMD64 - Add Two Integers

Created with Grok Build

## Introduction

This page disassembles the Free Pascal program `add` compiled for AMD64. The source is [Add_Int](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Pascal/Intel_Architecture/AMD64/Add_Int). The assembly is Intel syntax. The compiler is Free Pascal 3.0.4+dfsg-18ubuntu2, dated 2018/08/29, for x86_64. The banner is the `.fpc.n_version` section. `main` and `PASCALMAIN` are the same entry. On this build `INTEGER` is a 16-bit Smallint. The variables are BSS symbols. The code is in `.text.n_main`. The `.text` section is empty, so `objdump --section=.text` prints nothing useful. The notes after `//` were added to the listing. A `call` whose displacement is zero is an unapplied relocation, and objdump prints the next instruction as the target.

## The program *add.pp*

```{literalinclude} code/add.pp
:language: pascal
```

`a` is 3, `b` is 5, and `c` is `a + b`. Each variable is its own BSS section: `U_$P$ADD_$$_A`, `U_$P$ADD_$$_B`, and `U_$P$ADD_$$_C`.

## PASCALMAIN

The saved tree has the object and the assembly. The compile command itself was not recorded. This listing is:

```bash
objdump -d -Mintel -w -j .text.n_main add.o
```


```bash
0000000000000000 (main):
PROGRAM add;

VAR
	a, b, c : INTEGER;

BEGIN
    0: 55                   push rbp                                    // Save the caller's frame pointer.
    1: 4889e5               mov rbp, rsp                                // This frame starts at the current stack pointer.
    4: e800000000           call 9 <main+0x9>                           // Call FPC_INITIALIZEUNITS. The displacement is the unapplied R_X86_64_PC32, so objdump prints the next instruction.
	a := 3;
    9: 66c70425000000000300 mov WORD PTR ds:0x0, 0x3                    // a = 3. The address is the unapplied R_X86_64_32S to .bss.n_u_$p$add_$$_a, the symbol U_$P$ADD_$$_A.
	b := 5;
   13: 66c70425000000000500 mov WORD PTR ds:0x0, 0x5                    // b = 5. The relocation names U_$P$ADD_$$_B.
	c := a + b;
   1d: 0fbf142500000000     movsx edx, WORD PTR ds:0x0                  // edx = a, sign-extended from 16 bits to 32.
   25: 0fbf042500000000     movsx eax, WORD PTR ds:0x0                  // eax = b, sign-extended from 16 bits to 32.
   2d: 678d0402             lea eax, [edx+eax*1]                        // eax = a + b. The 0x67 prefix selects the 32-bit address form. Scale 1 makes this lea an add.
   31: 66a30000000000000000 movabs ds:0x0, ax                           // Store the low 16 bits at c. The relocation is R_X86_64_64 to U_$P$ADD_$$_C.
END.
   3b: e800000000           call 40 <main+0x40>                         // Call FPC_DO_EXIT. The displacement is unapplied.
   40: c9                   leave                                       // Release this frame.
   41: c3                   ret                                         // Return.
```

`lea eax, [edx+eax*1]` is the sum. Free Pascal encodes `a + b` as a load-effective-address with scale 1, and the `0x67` prefix keeps that address calculation 32 bits wide. The following `movabs` stores the low 16 bits, which is the Smallint result.

| Symbol | Variable | Value |
| --- | --- | --- |
| `U_$P$ADD_$$_A` | `a` | 3 |
| `U_$P$ADD_$$_B` | `b` | 5 |
| `U_$P$ADD_$$_C` | `c` | the low 16 bits of `a + b` |

`FPC_INITIALIZEUNITS` starts the runtime. `FPC_DO_EXIT` ends the program. `leave` and `ret` follow that call.

