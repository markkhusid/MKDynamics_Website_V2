# Pascal - ARM32 - Add Two Integers

Created with Grok Build

## Introduction

This page disassembles the Free Pascal program `add` compiled for ARM32. The source is [ARM32](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Pascal/ARM_Architecture/ARM32). The compiler is Free Pascal 3.0.4+dfsg-11+rpi1+deb9u1, dated 2017/07/27, for arm. The banner is the `.fpc.n_version` section. `INTEGER` is a 16-bit Smallint. `a`, `b`, and `c` are the BSS symbols at offsets 0, 2, and 4.

## The program *add.pp*

```{literalinclude} code/add.pp
:language: pascal
```

The ARM32 directory also has a debug assembly file. The object dump saved beside `add.pp` is the one below. The compile command was not recorded in that directory. The notes after `//` were added. The listing stops at the return. The three words after it are the literal pool.


## PASCALMAIN

```bash
objdump -d add.o
```


```bash
0000000000000000 (main):
PROGRAM add;

VAR
	a, b, c : INTEGER;

BEGIN
    0: e1a0c00d mov ip, sp                                      // ip = the incoming stack pointer.
    4: e92dd800 push {fp, ip, lr, pc}                           // Save fp, ip, lr, and pc.
    8: e24cb004 sub fp, ip, #4                                  // fp = ip-4. The frame pointer addresses the saved registers.
    c: e24dd030 sub sp, sp, #48 ; 0x30                          // Open 48 bytes.
   10: fafffffe blx 0 <FPC_INITIALIZEUNITS>                     // Call FPC_INITIALIZEUNITS. objdump names the helper. The displacement is unapplied.
	a := 3;
   14: e3a00003 mov r0, #3                                      // r0 = 3.
   18: e59f1034 ldr r1, [pc, #52] ; 54 <main+0x54>              // r1 = the pool word at 0x54, the object-file address of a.
   1c: e1c100b0 strh r0, [r1]                                   // a = 3, a 16-bit store through r1.
	b := 5;
   20: e3a00005 mov r0, #5                                      // r0 = 5.
   24: e59f102c ldr r1, [pc, #44] ; 58 <main+0x58>              // r1 = the pool word at 0x58, the object-file address of b.
   28: e1c100b0 strh r0, [r1]                                   // b = 5.
	c := a + b;
   2c: e59f0020 ldr r0, [pc, #32] ; 54 <main+0x54>              // r0 = the address of a again.
   30: e1d010f0 ldrsh r1, [r0]                                  // r1 = a, sign-extended from 16 bits.
   34: e59f001c ldr r0, [pc, #28] ; 58 <main+0x58>              // r0 = the address of b.
   38: e1d000f0 ldrsh r0, [r0]                                  // r0 = b, sign-extended from 16 bits.
   3c: e0800001 add r0, r0, r1                                  // r0 = b + a.
   40: e6bf1070 sxth r1, r0                                     // r1 = the sum, narrowed back to 16 bits.
   44: e59f0010 ldr r0, [pc, #16] ; 5c <main+0x5c>              // r0 = the pool word at 0x5c, the object-file address of c.
   48: e1c010b0 strh r1, [r0]                                   // c = the sum.
END.
   4c: fafffffe blx 0 <FPC_DO_EXIT>                             // Call FPC_DO_EXIT. The displacement is unapplied.
   50: e91ba800 ldmdb fp, {fp, sp, pc}                          // Restore fp, the incoming stack pointer, and the return address.
```

The prologue captures the incoming stack pointer in `ip`, saves the frame registers, and opens 48 bytes. `a`, `b`, and `c` are addressed from the pool that follows the return.

| Pool address | Word in this object | Variable |
| --- | --- | --- |
| `0x54` | `0` | `a` |
| `0x58` | `2` | `b` |
| `0x5c` | `4` | `c` |

objdump decodes those words as `andeq`. They are data. The `ldr` instructions with a `pc` offset read them. The sum is `add r0, r0, r1`, and `sxth` narrows it to 16 bits before the store of `c`.

