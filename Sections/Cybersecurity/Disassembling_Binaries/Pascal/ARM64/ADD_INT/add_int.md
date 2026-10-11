# Pascal - ARM64 - Add an Integer and a Constant

Created with Grok Build

```{figure} ../../../images/Pascal/ARM64/add_Pascal_ARM64_splash.jpg
:height: 600
:width: 800
:align: center
:class: clickable-figure

Radare2 session for the ARM64 add program. PASCALMAIN is at 0x4001c0.
```

## Introduction

This page disassembles the Free Pascal program `add` compiled for ARM64. The source is the debug build in [Add_Ints](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Pascal/ARM_Architecture/ARM64/Integer_Operations/Add_Ints/With_Debug_Info). The compiler is Free Pascal 3.0.4+dfsg-18ubuntu2, dated 2018/08/29, for aarch64. The banner is the `.fpc.n_version` section. `main` and `PASCALMAIN` are the same entry. `INTEGER` is a 16-bit Smallint. `a`, `b`, and `c` are halfwords in one BSS block, at offsets 0, 2, and 4.

## The program *add.pp*

```{literalinclude} code/add.pp
:language: pascal
```

The source line is `c := a + 5`. `b` is still assigned 5. The add reads `a` and the constant 5.

In the Radare2 session the procedure begins at `0x4001c0`. The listing below is the object file, so its addresses start at 0. The `adrp`, `add`, and `bl` immediates in the object are the unrelocated form. The session is the linked image, where those relocations have been applied. The add of the constant is `add w0, w0, #5`, instruction word `11001400`.

The debug build recorded these commands:

```bash
fpc -al -g add.pp
objdump -x -D -S -s -g -t add.o > objdump_of_dot_o.txt
```

The saved objdump also walks debug sections. This page keeps `.text.n_main`. The notes after `//` were added.


## PASCALMAIN



```bash
0000000000000000 (main):
PROGRAM add;

VAR
	a, b, c : INTEGER;

BEGIN
    0: a9bf7bfd stp x29, x30, [sp, #-16]!                       // Save the frame pointer and the return address.
    4: 910003fd mov x29, sp                                     // This frame starts at the current stack pointer.
    8: 94000000 bl 0 <FPC_INITIALIZEUNITS>                      // Call FPC_INITIALIZEUNITS. The relocation is R_AARCH64_CALL26, and the immediate in the object is 0.
	a := 3;
    c: 52800060 mov w0, #0x3                                    // w0 = 3.
   10: 90000001 adrp x1, 0 <main>                               // Page of a. R_AARCH64_ADR_PREL_PG_HI21 to .bss. The immediate in the object is 0.
   14: 91000021 add x1, x1, #0x0                                // Low 12 bits of a. R_AARCH64_ADD_ABS_LO12_NC to .bss. The immediate in the object is 0.
   18: 78000020 sturh w0, [x1]                                  // a = 3, a 16-bit store.
	b := 5;
   1c: 528000a1 mov w1, #0x5                                    // w1 = 5.
   20: 90000000 adrp x0, 0 <main>                               // Page of b. The relocation is to .bss+2.
   24: 91000000 add x0, x0, #0x0                                // Low 12 bits of b.
   28: 78000001 sturh w1, [x0]                                  // b = 5.
	c := a + 5;
   2c: 90000000 adrp x0, 0 <main>                               // Page of a, for the load.
   30: 91000000 add x0, x0, #0x0                                // Low 12 bits of a.
   34: 78c00000 ldursh w0, [x0]                                 // w0 = a, sign-extended from 16 bits.
   38: 11001400 add w0, w0, #0x5                                // w0 = a + 5. The source adds the constant 5.
   3c: 13003c00 sxth w0, w0                                     // Narrow the sum to 16 bits.
   40: 90000001 adrp x1, 0 <main>                               // Page of c. The relocation is to .bss+4.
   44: 91000021 add x1, x1, #0x0                                // Low 12 bits of c.
   48: 78000020 sturh w0, [x1]                                  // c = a + 5.
END.
   4c: 94000000 bl 0 <FPC_DO_EXIT>                              // Call FPC_DO_EXIT. R_AARCH64_CALL26, immediate 0.
   50: a8c17bfd ldp x29, x30, [sp], #16                         // Restore the frame pointer and the return address.
   54: d65f03c0 ret                                             // Return.
```

| Offset | Variable | Role |
| --- | --- | --- |
| `.bss` | `a` | 3, then the value that is added to 5 |
| `.bss+2` | `b` | 5 |
| `.bss+4` | `c` | `a + 5` |

`sxth` narrows the sum to 16 bits before the store of `c`.

