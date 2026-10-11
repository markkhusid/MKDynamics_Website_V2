# Ada - ARM 32-Bit Platform - Add Two Integers with Input and Output

Created with Grok Build

```{figure} ../../../images/Ada/ARM32/add_Ada_ARM32_splash.jpg
:height: 600
:width: 800
:align: center
:class: clickable-figure

Radare2 session for Add_Int_w_IO on ARM32. The sum is an add, followed by the overflow check.
```

## Introduction

This page disassembles `Add_Int_w_IO` compiled for ARM32, little-endian ARMv6 with the hard-float VFP ABI. The program reads two integers, adds them, and prints the sum. The source and the debug object are in the [Disassembling-Binaries Ada tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Ada/ARM_Architecture/ARM32/Add_Int_w_IO/With_Debug_Info).

The screenshot is the Radare2 session of the linked executable, so its addresses are the load addresses of that process. The listing below is the `.text` of the object file. Object-file addresses start at 0. The compiler is GNU Ada 6.3.0 20170516, with `-g -march=armv6 -mfloat-abi=hard -mfpu=vfp`.

The tree also contains `Add_Int` as source for ARM32. That program was not built in this tree, so it has no listing here. The constant form of the same assignment is on the ARM64 page, where the compiler stores 8: [Add Two Integers](../../ARM64/ADD_INT/add_int.md).

## The program *add_int_w_io.adb*

```{literalinclude} code/add_int_w_io.adb
:language: ada
```

`Get` reads `a` and `b`. `c` is their sum. The prompts keep the trailing space after `->`. On this GNAT build an `Integer` is four bytes. Because the two values are read at run time, the object code contains an `add` and Ada's overflow check.

The listing is the `.text` of the objdump saved with the object, through the `pop` that returns. The notes after `//` were added to that listing. A `bl` that objdump prints with target `0` is the unrelocated object. The relocation is `R_ARM_CALL` to the symbol named on that line. In the linked executable the branch lands on `Gnat.Io` or on the overflow check.

## The binder's *main*

The screenshot's `main` calls `__gnat_initialize`, `adainit`, `_ada_add_int_w_io`, `adafinal`, and `__gnat_finalize`. That is the GNAT binder. The AMD64 addition page has the same sequence as objdump: [Add Two Integers](../../AMD64/ADD_INT/add_int.md).

## The procedure

```bash
0000000000000000 (_ada_add_int_w_io):
--
-- Some numbers to come and go.  With IO.
--
with Gnat.Io; use Gnat.Io;
procedure Add_Int_w_IO is
    0: e92d48f0 push {r4, r5, r6, r7, fp, lr}                    // Save the registers this procedure uses, including the return address.
    4: e28db014 add fp, sp, #20                                  // fp is the frame pointer, 20 bytes above the saved area.
    8: e24dd010 sub sp, sp, #16                                  // Three integer slots.
   a, b, c: Integer;

begin

   Put ("Please enter first integer now followed by <CR> -> ");
    c: e59f20c4 ldr r2, [pc, #196] ; d8 <_ada_add_int_w_io+0xd8> // Address of the first prompt, loaded from the literal pool after the return.
   10: e59f30c4 ldr r3, [pc, #196] ; dc <_ada_add_int_w_io+0xdc> // Address of that string's bounds, from the same pool.
   14: e1a00002 mov r0, r2                                       // r0 = the characters.
   18: e1a01003 mov r1, r3                                       // r1 = the bounds.
   1c: ebfffffe bl 0 <gnat__io__put__6>                          // Print the string.
   Get (a);
   20: ebfffffe bl 0 <gnat__io__get>                             // Read an integer. The value comes back in r0.
   24: e1a03000 mov r3, r0                                       // r3 = the value just read.
   28: e50b3018 str r3, [fp, #-24] ; 0xffffffe8                  // a, at fp-24.

   Put ("Please enter second integer now followed by <CR> -> ");
   2c: e59f60ac ldr r6, [pc, #172] ; e0 <_ada_add_int_w_io+0xe0> // Address of the second prompt, loaded from the literal pool after the return.
   30: e59f70ac ldr r7, [pc, #172] ; e4 <_ada_add_int_w_io+0xe4> // Address of that string's bounds, from the same pool.
   34: e1a00006 mov r0, r6                                       // r0 = the characters.
   38: e1a01007 mov r1, r7                                       // r1 = the bounds.
   3c: ebfffffe bl 0 <gnat__io__put__6>                          // Print the string.
   Get (b);
   40: ebfffffe bl 0 <gnat__io__get>                             // Read the second integer into r0.
   44: e1a03000 mov r3, r0                                       // r3 = that value.
   48: e50b301c str r3, [fp, #-28] ; 0xffffffe4                  // b, at fp-28.

   c := a + b;
   4c: e51b301c ldr r3, [fp, #-28] ; 0xffffffe4                  // r3 = b.
   50: e1a03fa3 lsr r3, r3, #31                                  // Sign bit of b.
   54: e6ef2073 uxtb r2, r3                                      // Keep that sign bit in a byte.
   58: e51b1018 ldr r1, [fp, #-24] ; 0xffffffe8                  // r1 = a.
   5c: e51b301c ldr r3, [fp, #-28] ; 0xffffffe4                  // r3 = b.
   60: e0813003 add r3, r1, r3                                   // r3 = a + b.
   64: e1a01003 mov r1, r3                                       // Hold that sum.
   68: e51b3018 ldr r3, [fp, #-24] ; 0xffffffe8                  // r3 = a again, for the compare.
   6c: e1510003 cmp r1, r3                                       // Compare the sum with a.
   70: b3a03001 movlt r3, #1                                     // 1 when the sum is less than a.
   74: a3a03000 movge r3, #0                                     // 0 otherwise.
   78: e6ef3073 uxtb r3, r3                                      // Keep the compare result in a byte.
   7c: e0233002 eor r3, r3, r2                                   // Combine the compare with the sign bit of b.
   80: e6ef3073 uxtb r3, r3                                      // Keep the overflow flag in a byte.
   84: e3530000 cmp r3, #0                                       // Test the overflow flag.
   88: 0a000002 beq 98 <_ada_add_int_w_io+0x98>                  // Store c when the sum fits in an Integer.
   8c: e3a01010 mov r1, #16                                      // r1 = 16, the source line of c := a + b.
   90: e59f0050 ldr r0, [pc, #80] ; e8 <_ada_add_int_w_io+0xe8>  // r0 points at the file name add_int_w_io.adb.
   94: ebfffffe bl 0 <__gnat_rcheck_CE_Overflow_Check>           // Raise Constraint_Error for the overflow.
   98: e51b2018 ldr r2, [fp, #-24] ; 0xffffffe8                  // r2 = a, for the second add.
   9c: e51b301c ldr r3, [fp, #-28] ; 0xffffffe4                  // r3 = b.
   a0: e0823003 add r3, r2, r3                                   // r3 = a + b again, on the path that fits.
   a4: e50b3020 str r3, [fp, #-32] ; 0xffffffe0                  // c, at fp-32.

   Put ("The sum is : ");
   a8: e59f403c ldr r4, [pc, #60] ; ec <_ada_add_int_w_io+0xec>  // Address of "The sum is : ", loaded from the literal pool after the return.
   ac: e59f503c ldr r5, [pc, #60] ; f0 <_ada_add_int_w_io+0xf0>  // Address of that string's bounds, from the same pool.
   b0: e1a00004 mov r0, r4                                       // r0 = the characters.
   b4: e1a01005 mov r1, r5                                       // r1 = the bounds.
   b8: ebfffffe bl 0 <gnat__io__put__6>                          // Print the string.
   Put (c);
   bc: e51b0020 ldr r0, [fp, #-32] ; 0xffffffe0                  // r0 = c.
   c0: ebfffffe bl 0 <gnat__io__put__2>                          // Print the integer.
   New_Line;
   c4: e3a00001 mov r0, #1                                       // r0 = 1. A parameterless New_Line prints one line.
   c8: ebfffffe bl 0 <gnat__io__new_line__2>                     // Print the new line.

end Add_Int_w_IO;
   cc: e1a00000 nop ; (mov r0, r0)                               // Padding in front of the epilogue.
   d0: e24bd014 sub sp, fp, #20                                  // Restore sp from the frame pointer.
   d4: e8bd88f0 pop {r4, r5, r6, r7, fp, pc}                     // Restore the saved registers and return through pc.
```

### The frame

`push {r4, r5, r6, r7, fp, lr}` saves the registers this procedure uses, including the return address. `add fp, sp, #20` sets the frame pointer 20 bytes above that saved area. `sub sp, sp, #16` opens three integer slots, and one unused word, below `fp`:

| Slot | Variable | Value |
| --- | --- | --- |
| `fp-24` | `a` | the first `Get` |
| `fp-28` | `b` | the second `Get` |
| `fp-32` | `c` | the sum |

`sub sp, fp, #20` restores the stack pointer from the frame pointer. The final `pop` reloads the saved registers and returns by writing the saved link register into `pc`.

### The literal pool

Each `ldr rN, [pc, #imm]` loads an address from a word that sits after the return. Those words are a literal pool, not instructions. The pool holds the addresses of the two prompts, the text `The sum is : `, their bounds records, and the file name `add_int_w_io.adb`. objdump decodes the pool as `andeq` if the disassembly continues past the `pop`. This listing stops at the `pop`.

`Put` of a string is `gnat__io__put__6`. `r0` is the characters. `r1` is the bounds, `First` then `Last`. `First` is 1, and `Last` is 51, 52, and 13 for the three strings. `Get` returns the integer in `r0`. `Put` of an integer is `gnat__io__put__2`. `New_Line` with no arguments is `gnat__io__new_line__2` with `r0` equal to 1.

### The add and the overflow check

The check is the sequence from the load of `b` through the call of `__gnat_rcheck_CE_Overflow_Check`.

`lsr r3, r3, #31` keeps the sign bit of `b` in `r2`: 1 when `b` is negative, 0 otherwise. The first `add r3, r1, r3` computes `a + b` and holds it in `r1`. `cmp r1, r3` then compares that sum with `a`. `movlt` / `movge` write 1 when the sum is less than `a`, and 0 otherwise.

For a sum that fits, those two facts agree. When `b` is non-negative, `a + b` is greater than or equal to `a`. When `b` is negative, `a + b` is less than `a`. `eor r3, r3, r2` is 1 when the comparison and the sign bit disagree, which is the wrap. `cmp r3, #0` tests that flag. `beq` stores `c` when the flag is clear.

When the flag is set, `r1` is 16, the source line of `c := a + b`, and `r0` points at the file name. `__gnat_rcheck_CE_Overflow_Check` raises `Constraint_Error`. On the path that fits, a second `add` computes the sum again and stores it at `fp-32`.
