# Pascal - ARM64 - Add Two Reals

Created with Grok Build

## Introduction

This page disassembles `add_floats` compiled for ARM64. The source is the debug build in [Real_Operations](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Pascal/ARM_Architecture/ARM64/Real_Operations/With_Debug_Info). The compiler is Free Pascal 3.0.4+dfsg-18ubuntu2, dated 2018/08/29, for aarch64. The banner is the `.fpc.n_version` section. `REAL` is an IEEE-754 double. The three variables are in one BSS block, eight bytes apart.

## The program *add_floats.pp*

```{literalinclude} code/add_floats.pp
:language: pascal
```

The debug build recorded these commands:

```bash
fpc -al -g add_floats.pp
mv add_floats add_floats_Pascal_ARM64_g
objdump -x -D -S -s -g -t add_floats.o > objdump_of_dot_o.txt
```

This page keeps `.text.n_main`. The notes after `//` were added.


## PASCALMAIN



```bash
0000000000000000 (main):
PROGRAM add_floats;

VAR
	a, b, c : REAL;

BEGIN
    0: a9bf7bfd stp x29, x30, [sp, #-16]!                       // Save the frame pointer and the return address.
    4: 910003fd mov x29, sp                                     // This frame starts at the current stack pointer.
    8: 94000000 bl 0 <FPC_INITIALIZEUNITS>                      // Call FPC_INITIALIZEUNITS.
	a := 3.3;
    c: 90000000 adrp x0, 0 <main>                               // Page of the GOT entry for _$ADD_FLOATS$_Ld1, the double 3.3. R_AARCH64_ADR_GOT_PAGE.
   10: f9400000 ldr x0, [x0]                                    // x0 = that GOT entry. R_AARCH64_LD64_GOT_LO12_NC.
   14: f8400001 ldur x1, [x0]                                   // x1 = the 8 bytes of 3.3.
   18: 90000000 adrp x0, 0 <main>                               // Page of a. The relocation is to .bss.
   1c: 91000000 add x0, x0, #0x0                                // Low 12 bits of a.
   20: f8000001 stur x1, [x0]                                   // Store the bits of 3.3 at a.
	b := 5.6;
   24: 90000000 adrp x0, 0 <main>                               // Page of the GOT entry for _$ADD_FLOATS$_Ld2, the double 5.6.
   28: f9400000 ldr x0, [x0]                                    // x0 = that GOT entry.
   2c: f8400001 ldur x1, [x0]                                   // x1 = the 8 bytes of 5.6.
   30: 90000000 adrp x0, 0 <main>                               // Page of b. The relocation is to .bss+8.
   34: 91000000 add x0, x0, #0x0                                // Low 12 bits of b.
   38: f8000001 stur x1, [x0]                                   // Store the bits of 5.6 at b.
	c := a + b;
   3c: 90000000 adrp x0, 0 <main>                               // Page of a, for the load.
   40: 91000000 add x0, x0, #0x0                                // Low 12 bits of a.
   44: fc400001 ldur d1, [x0]                                   // d1 = a.
   48: 90000000 adrp x0, 0 <main>                               // Page of b, for the load.
   4c: 91000000 add x0, x0, #0x0                                // Low 12 bits of b.
   50: fc400000 ldur d0, [x0]                                   // d0 = b.
   54: 1e602820 fadd d0, d1, d0                                 // d0 = a + b. fadd adds two doubles.
   58: 90000000 adrp x0, 0 <main>                               // Page of c. The relocation is to .bss+0x10.
   5c: 91000000 add x0, x0, #0x0                                // Low 12 bits of c.
   60: fc000000 stur d0, [x0]                                   // c = a + b.
END.
   64: 94000000 bl 0 <FPC_DO_EXIT>                              // Call FPC_DO_EXIT.
   68: a8c17bfd ldp x29, x30, [sp], #16                         // Restore the frame pointer and the return address.
   6c: d65f03c0 ret                                             // Return.
```

The two constants are IEEE-754 doubles. 3.3 and 5.6 are rounded to the values these bytes store, little-endian:

```text
_$ADD_FLOATS$_Ld1  66 66 66 66 66 66 0a 40    3.3
_$ADD_FLOATS$_Ld2  66 66 66 66 66 66 16 40    5.6
```

The assignment of each constant copies those 8 bytes into BSS. The sum is the floating-point add.

The constant is loaded through the GOT: `adrp` and `ldr` fetch the address, and `ldur` reads the eight bytes. Those bytes are stored to BSS with `stur`. The sum is `fadd d0, d1, d0`, with `d1` holding `a` and `d0` holding `b`.

| Offset | Variable |
| --- | --- |
| `.bss` | `a` |
| `.bss+8` | `b` |
| `.bss+0x10` | `c` |

