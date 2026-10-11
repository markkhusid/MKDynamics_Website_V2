# Pascal - ARM64 - Multiply an Integer by a Constant

Created with Grok Build

## Introduction

This page disassembles the Free Pascal program `mult` compiled for ARM64. The source is the debug build in [Mult_Ints](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Pascal/ARM_Architecture/ARM64/Integer_Operations/Mult_Ints/With_Debug_Info). The compiler is Free Pascal 3.0.4+dfsg-18ubuntu2, dated 2018/08/29, for aarch64. The banner is the `.fpc.n_version` section. `INTEGER` is a 16-bit Smallint. The variables are halfwords in one BSS block.

## The program *mult_int.pp*

```{literalinclude} code/mult_int.pp
:language: pascal
```

The source line is `c := a * 5`. The product is `mul` of `a` and the constant 5.

The debug build recorded these commands:

```bash
fpc -al -g mult_int.pp
objdump -x -D -S -s -g -t mult_int.o > objdump_of_dot_o.txt
```

This page keeps `.text.n_main` from that object dump. The notes after `//` were added. Addresses in the object start at 0.


## PASCALMAIN



```bash
0000000000000000 (main):
PROGRAM mult;

VAR
	a, b, c : INTEGER;

BEGIN
    0: a9bf7bfd stp x29, x30, [sp, #-16]!                       // Save the frame pointer and the return address.
    4: 910003fd mov x29, sp                                     // This frame starts at the current stack pointer.
    8: 94000000 bl 0 <FPC_INITIALIZEUNITS>                      // Call FPC_INITIALIZEUNITS. R_AARCH64_CALL26, immediate 0.
	a := 3;
    c: 52800060 mov w0, #0x3                                    // w0 = 3.
   10: 90000001 adrp x1, 0 <main>                               // Page of a. The relocation is to .bss.
   14: 91000021 add x1, x1, #0x0                                // Low 12 bits of a.
   18: 78000020 sturh w0, [x1]                                  // a = 3.
	b := 5;
   1c: 528000a1 mov w1, #0x5                                    // w1 = 5.
   20: 90000000 adrp x0, 0 <main>                               // Page of b. The relocation is to .bss+2.
   24: 91000000 add x0, x0, #0x0                                // Low 12 bits of b.
   28: 78000001 sturh w1, [x0]                                  // b = 5.
	c := a * 5;
   2c: 90000000 adrp x0, 0 <main>                               // Page of a, for the load.
   30: 91000000 add x0, x0, #0x0                                // Low 12 bits of a.
   34: 78c00000 ldursh w0, [x0]                                 // w0 = a, sign-extended.
   38: 528000a1 mov w1, #0x5                                    // w1 = 5, the constant in c := a * 5.
   3c: 1b017c00 mul w0, w0, w1                                  // w0 = a * 5.
   40: 13003c00 sxth w0, w0                                     // Narrow the product to 16 bits.
   44: 90000001 adrp x1, 0 <main>                               // Page of c. The relocation is to .bss+4.
   48: 91000021 add x1, x1, #0x0                                // Low 12 bits of c.
   4c: 78000020 sturh w0, [x1]                                  // c = a * 5.
END.
   50: 94000000 bl 0 <FPC_DO_EXIT>                              // Call FPC_DO_EXIT.
   54: a8c17bfd ldp x29, x30, [sp], #16                         // Restore the frame pointer and the return address.
   58: d65f03c0 ret                                             // Return.
```

| Offset | Variable | Role |
| --- | --- | --- |
| `.bss` | `a` | 3, the value that is multiplied |
| `.bss+2` | `b` | 5 |
| `.bss+4` | `c` | `a * 5` |

