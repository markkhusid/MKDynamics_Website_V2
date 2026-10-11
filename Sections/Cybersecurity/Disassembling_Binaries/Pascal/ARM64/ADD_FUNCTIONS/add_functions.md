# Pascal - ARM64 - Add Two Integers in a Function

Created with Grok Build

## Introduction

This page disassembles `add_functions_program` compiled for ARM64. The source is the debug build in [Functions](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Pascal/ARM_Architecture/ARM64/Functions/With_Debug_Info). The compiler is Free Pascal 3.0.4+dfsg-18ubuntu2, dated 2018/08/29, for aarch64. The banner is the `.fpc.n_version` section. The function symbol spells the parameters `SMALLINT`. `INTEGER` is that 16-bit type.

## The program *add_functions.pp*

```{literalinclude} code/add_functions.pp
:language: pascal
```

The debug build recorded these commands:

```bash
fpc -al -g add_functions.pp
mv add_functions add_functions_Pascal_ARM64_g
objdump -x -D -S -s -g -t add_functions.o > objdump_of_dot_o.txt
```

The function and `PASCALMAIN` are separate sections, and each starts at address 0 in the object. The notes after `//` were added.


## add_function

`w0` is `f_a` and `w1` is `f_b`. The sum is `add`, then `sxth` narrows it, and `w0` carries it back.

```bash
0000000000000000 (P$ADD_FUNCTIONS_PROGRAM_$$_ADD_FUNCTION$SMALLINT$SMALLINT$$SMALLINT):
FUNCTION add_function(f_a : INTEGER; f_b : INTEGER) : INTEGER;

BEGIN
    0: a9bf7bfd stp x29, x30, [sp, #-16]!                       // Save the frame pointer and the return address.
    4: 910003fd mov x29, sp                                     // This frame starts at the current stack pointer.
    8: d10083ff sub sp, sp, #0x20                               // Open 32 bytes for the arguments and the result.
	add_function := f_a + f_b;
    c: 790003e0 strh w0, [sp]                                   // Spill f_a. The first Smallint arrives in w0.
   10: 790013e1 strh w1, [sp, #8]                               // Spill f_b. The second Smallint arrives in w1.
   14: 79c003e0 ldrsh w0, [sp]                                  // w0 = f_a, sign-extended.
   18: 79c013e1 ldrsh w1, [sp, #8]                              // w1 = f_b, sign-extended.
   1c: 0b000020 add w0, w1, w0                                  // w0 = f_b + f_a.
   20: 13003c00 sxth w0, w0                                     // Narrow the sum to 16 bits.
   24: 790023e0 strh w0, [sp, #16]                              // Store the 16-bit result at sp+16.
   28: 79c023e0 ldrsh w0, [sp, #16]                             // w0 = the result, the value the caller reads.
END;
   2c: 910003bf mov sp, x29                                     // Restore sp from the frame pointer.
   30: a8c17bfd ldp x29, x30, [sp], #16                         // Restore the frame pointer and the return address.
   34: d65f03c0 ret                                             // Return.
```

| Slot | Variable |
| --- | --- |
| `sp` | `f_a` |
| `sp+8` | `f_b` |
| `sp+16` | the 16-bit sum |

## PASCALMAIN

`a` is 2 and `b` is 3. The call passes `a` in `w0` and `b` in `w1`.

```bash
0000000000000000 (main):
BEGIN
    0: a9bf7bfd stp x29, x30, [sp, #-16]!                       // Save the frame pointer and the return address.
    4: 910003fd mov x29, sp                                     // This frame starts at the current stack pointer.
    8: 94000000 bl 0 <FPC_INITIALIZEUNITS>                      // Call FPC_INITIALIZEUNITS.
	a := 2;
    c: 52800041 mov w1, #0x2                                    // w1 = 2.
   10: 90000000 adrp x0, 0 <main>                               // Page of a. The relocation is to .bss.
   14: 91000000 add x0, x0, #0x0                                // Low 12 bits of a.
   18: 78000001 sturh w1, [x0]                                  // a = 2.
	b := 3;
   1c: 52800060 mov w0, #0x3                                    // w0 = 3.
   20: 90000001 adrp x1, 0 <main>                               // Page of b. The relocation is to .bss+2.
   24: 91000021 add x1, x1, #0x0                                // Low 12 bits of b.
   28: 78000020 sturh w0, [x1]                                  // b = 3.
	c := add_function(a, b);
   2c: 90000000 adrp x0, 0 <main>                               // Page of b, for the load.
   30: 91000000 add x0, x0, #0x0                                // Low 12 bits of b.
   34: 78c00001 ldursh w1, [x0]                                 // w1 = b. The second argument goes in w1.
   38: 90000000 adrp x0, 0 <main>                               // Page of a, for the load.
   3c: 91000000 add x0, x0, #0x0                                // Low 12 bits of a.
   40: 78c00000 ldursh w0, [x0]                                 // w0 = a. The first argument goes in w0.
   44: 94000000 bl 0 <main>                                     // Call add_function. The relocation names P$ADD_FUNCTIONS_PROGRAM_$$_ADD_FUNCTION$SMALLINT$SMALLINT$$SMALLINT.
   48: 90000001 adrp x1, 0 <main>                               // Page of c. The relocation is to .bss+4.
   4c: 91000021 add x1, x1, #0x0                                // Low 12 bits of c.
   50: 78000020 sturh w0, [x1]                                  // c = the 16-bit result in w0.
END.
   54: 94000000 bl 0 <FPC_DO_EXIT>                              // Call FPC_DO_EXIT.
   58: a8c17bfd ldp x29, x30, [sp], #16                         // Restore the frame pointer and the return address.
   5c: d65f03c0 ret                                             // Return.
```

| Offset | Variable | Value |
| --- | --- | --- |
| `.bss` | `a` | 2 |
| `.bss+2` | `b` | 3 |
| `.bss+4` | `c` | the 16-bit result |

