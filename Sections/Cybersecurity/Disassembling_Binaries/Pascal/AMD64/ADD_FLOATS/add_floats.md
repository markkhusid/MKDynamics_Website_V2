# Pascal - AMD64 - Add Two Reals

Created with Grok Build

## Introduction

This page disassembles the Free Pascal program `add_floats` compiled for AMD64. The source is the debug build in [Add_Floats](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Pascal/Intel_Architecture/AMD64/Floats/Add_Floats/With_Debug_Info). The assembly is Intel syntax. The compiler is Free Pascal 3.0.4+dfsg-18ubuntu2, dated 2018/08/29, for x86_64. The banner is the `.fpc.n_version` section. The object carries debug info. The compile command itself was not recorded beside this object. `main` and `PASCALMAIN` are the same entry. On this build `INTEGER` is a 16-bit Smallint. The variables are BSS symbols. The code is in `.text.n_main`. The `.text` section is empty, so `objdump --section=.text` prints nothing useful. The notes after `//` were added to the listing. A `call` whose displacement is zero is an unapplied relocation, and objdump prints the next instruction as the target. `REAL` is an IEEE-754 double, eight bytes.

## The program *add_floats.pp*

```{literalinclude} code/add_floats.pp
:language: pascal
```

`a` is 3.3, `b` is 5.6, and `c` is `a + b`. Each variable is its own BSS section.

## PASCALMAIN

```bash
objdump -d -Mintel -w -j .text.n_main add_floats.o
```


```bash
0000000000000000 (main):
PROGRAM add_floats;

VAR
	a, b, c : REAL;

BEGIN
    0: 55                   push rbp                                    // Save the caller's frame pointer.
    1: 4889e5               mov rbp, rsp                                // This frame starts at the current stack pointer.
    4: 488d6424f0           lea rsp, [rsp-0x10]                         // Open 16 bytes. The three REAL variables live in BSS, and this slot keeps the calls aligned.
    9: e800000000           call e <main+0xe>                           // Call FPC_INITIALIZEUNITS. The displacement is unapplied.
	a := 3.3;
    e: 48a10000000000000000 movabs rax, ds:0x0                          // rax = the 8 bytes of 3.3. The relocation is R_X86_64_64 to _$ADD_FLOATS$_Ld1.
   18: 48a30000000000000000 movabs ds:0x0, rax                          // Store those bits at a. The relocation names U_$P$ADD_FLOATS_$$_A.
	b := 5.6;
   22: 48a10000000000000000 movabs rax, ds:0x0                          // rax = the 8 bytes of 5.6, from _$ADD_FLOATS$_Ld2.
   2c: 48a30000000000000000 movabs ds:0x0, rax                          // Store those bits at b.
	c := a + b;
   36: f20f10042500000000   movsd xmm0, QWORD PTR ds:0x0                // xmm0 = a, as a double.
   3f: f20f58042500000000   addsd xmm0, QWORD PTR ds:0x0                // xmm0 = a + b. addsd is a scalar double add.
   48: f20f11042500000000   movsd QWORD PTR ds:0x0, xmm0                // c = a + b. The relocation names U_$P$ADD_FLOATS_$$_C.
END.
   51: e800000000           call 56 <main+0x56>                         // Call FPC_DO_EXIT. The displacement is unapplied.
   56: c9                   leave                                       // Release this frame.
   57: c3                   ret                                         // Return.
```

The two constants are IEEE-754 doubles. 3.3 and 5.6 are rounded to the values these bytes store, little-endian:

```text
_$ADD_FLOATS$_Ld1  66 66 66 66 66 66 0a 40    3.3
_$ADD_FLOATS$_Ld2  66 66 66 66 66 66 16 40    5.6
```

The assignment of each constant copies those 8 bytes into BSS. The sum is the floating-point add.

| Symbol | Variable | Bytes |
| --- | --- | --- |
| `U_$P$ADD_FLOATS_$$_A` | `a` | the double 3.3 |
| `U_$P$ADD_FLOATS_$$_B` | `b` | the double 5.6 |
| `U_$P$ADD_FLOATS_$$_C` | `c` | `a + b` |

