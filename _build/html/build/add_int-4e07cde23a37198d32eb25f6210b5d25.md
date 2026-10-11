# C++ - ARM32 - Add Two Integers

Created with Grok Build

## Introduction

This page disassembles `add.cpp` compiled for ARM32. The source is the program in the [Disassembling-Binaries C++ tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/C%2B%2B/ARM_Architecture/ARM32). The assembly is ARM syntax.

`a` is 3, `b` is 5, and `c` is `a + b`. The sum stays in `c`. The source ends at the closing brace of `main`. GCC writes 0 into the return register before `ret`.

On this build an `int` is four bytes. The stores write 32-bit registers. The compiler is GCC (Raspbian 6.3.0-18+rpi1+deb9u1) 6.3.0 20170516, from the object's `.comment` section.

The tree saves the object and the compiler's assembly. The compile command itself was not recorded. The listing is objdump of that object. Addresses in the object start at 0. A linked executable can place the same instructions at another address.

```bash
objdump -d add.o
```

The iostream header defines a static `std::ios_base::Init` object, `__ioinit`. The demangled symbol is `std::__ioinit`. The body of `main` is the three assignments. The object file still contains `__static_initialization_and_destruction_0(int, int)` and `_GLOBAL__sub_I_main`, because that header defines `__ioinit`. The second calls the first with the arguments 1 and 0xffff. When both arguments match, the function constructs `__ioinit` and registers `std::ios_base::Init::~Init()` with `__aeabi_atexit`.

## The program *add.cpp*

```{literalinclude} code/add.cpp
:language: cpp
```

## main

`push {fp}` saves the frame pointer, and `add fp, sp, #0` copies `sp` into `fp`. `sub sp, sp, #20` opens the frame. `add sp, fp, #0` restores `sp`, `pop {fp}` reloads the frame pointer, and `bx lr` returns.

```bash
0000000000000000 (main):
int main()
{
	int a, b, c;
    0: e52db004 push {fp} ; (str fp, [sp, #-4]!)                // Save the frame pointer.
    4: e28db000 add fp, sp, #0                                  // fp = sp. The frame pointer is the stack pointer on entry to the body.
    8: e24dd014 sub sp, sp, #20                                 // Open 20 bytes.
	a = 3;
    c: e3a03003 mov r3, #3                                      // r3 = 3.
   10: e50b3008 str r3, [fp, #-8]                               // a = 3, at fp-8.
	b = 5;
   14: e3a03005 mov r3, #5                                      // r3 = 5.
   18: e50b300c str r3, [fp, #-12]                              // b = 5, at fp-12.
	c = a+ b;
   1c: e51b2008 ldr r2, [fp, #-8]                               // r2 = a.
   20: e51b300c ldr r3, [fp, #-12]                              // r3 = b.
   24: e0823003 add r3, r2, r3                                  // r3 = a + b.
   28: e50b3010 str r3, [fp, #-16]                              // c = a + b, at fp-16.
}
   2c: e3a03000 mov r3, #0                                      // r3 = 0.
   30: e1a00003 mov r0, r3                                      // r0 = 0. main returns 0.
   34: e28bd000 add sp, fp, #0                                  // Restore sp from fp.
   38: e49db004 pop {fp} ; (ldr fp, [sp], #4)                   // Restore the caller's frame pointer.
   3c: e12fff1e bx lr                                           // Return through lr.
```

| Slot | Variable | Value |
| --- | --- | --- |
| `fp-8` | `a` | 3 |
| `fp-12` | `b` | 5 |
| `fp-16` | `c` | `a + b` |


## The iostream initializer

The ARM32 initializer uses `__aeabi_atexit` to register the destructor. The guard compares the spilled arguments with 1 and with the literal 0xffff. The `bl` displacements are unapplied. objdump names `std::ios_base::Init::Init()` and `__aeabi_atexit`.

```bash
0000000000000040 (_Z41__static_initialization_and_destruction_0ii):
   40: e92d4800 push {fp, lr}                                   // Save the frame pointer and the return address.
   44: e28db004 add fp, sp, #4                                  // fp = sp+4, just above the saved frame pointer.
   48: e24dd008 sub sp, sp, #8                                  // Open 8 bytes for the spilled arguments.
   4c: e50b0008 str r0, [fp, #-8]                               // Spill the first argument, r0.
   50: e50b100c str r1, [fp, #-12]                              // Spill the second argument, r1.
   54: e51b3008 ldr r3, [fp, #-8]                               // Reload the first argument.
   58: e3530001 cmp r3, #1                                      // Compare it with 1.
   5c: 1a000009 bne 88 <_Z41__static_initialization_and_destruction_0ii+0x48>  // Skip the constructor when it is any other value.
   60: e51b300c ldr r3, [fp, #-12]                              // Reload the second argument.
   64: e59f2028 ldr r2, [pc, #40] ; 94 <_Z41__static_initialization_and_destruction_0ii+0x54>  // r2 = the pool word at 0x94, which is 0xffff.
   68: e1530002 cmp r3, r2                                      // Compare the priority with 65535.
   6c: 1a000005 bne 88 <_Z41__static_initialization_and_destruction_0ii+0x48>  // Skip the constructor when the priority is any other value.
   70: e59f0020 ldr r0, [pc, #32] ; 98 <_Z41__static_initialization_and_destruction_0ii+0x58>  // r0 = the pool word at 0x98. In this object that word is 0. It is the __ioinit address.
   74: ebfffffe bl 0 <_ZNSt8ios_base4InitC1Ev>                  // Construct std::ios_base::Init. The displacement is unapplied, and objdump names the constructor.
   78: e59f201c ldr r2, [pc, #28] ; 9c <_Z41__static_initialization_and_destruction_0ii+0x5c>  // r2 = the pool word at 0x9c, an argument of __aeabi_atexit. The word is 0 in this object.
   7c: e59f101c ldr r1, [pc, #28] ; a0 <_Z41__static_initialization_and_destruction_0ii+0x60>  // r1 = the pool word at 0xa0, an argument of __aeabi_atexit. The word is 0 in this object.
   80: e59f0010 ldr r0, [pc, #16] ; 98 <_Z41__static_initialization_and_destruction_0ii+0x58>  // r0 is loaded again from the same pool word as the constructor's object argument.
   84: ebfffffe bl 0 <__aeabi_atexit>                           // Register the destructor with __aeabi_atexit. The displacement is unapplied.
   88: e1a00000 nop ; (mov r0, r0)                              // Padding in front of the epilogue. objdump prints it as mov r0, r0.
   8c: e24bd004 sub sp, fp, #4                                  // Restore sp from the frame pointer.
   90: e8bd8800 pop {fp, pc}                                    // Restore the saved registers and return through pc.
```

`_GLOBAL__sub_I_main` is what the `.init_array` slot calls before `main`. It passes the two guard values.

```bash
00000000000000a4 (_GLOBAL__sub_I_main):
   a4: e92d4800 push {fp, lr}                                   // Save the frame pointer and the return address.
   a8: e28db004 add fp, sp, #4                                  // fp = sp+4.
   ac: e59f1008 ldr r1, [pc, #8] ; bc <_GLOBAL__sub_I_main+0x18>  // r1 = the pool word at 0xbc, which is 0xffff.
   b0: e3a00001 mov r0, #1                                      // r0 = 1.
   b4: ebffffe1 bl 40 <_Z41__static_initialization_and_destruction_0ii>  // Call the initializer with r0 = 1 and r1 = 0xffff.
   b8: e8bd8800 pop {fp, pc}                                    // Restore the saved registers and return through pc.
```

The word at 0x94 is `0x0000ffff`. The `ldr` at 0x64 uses it as the priority. The words at 0x98, 0x9c, and 0xa0 are zero in this object. They are the addresses the constructor and `__aeabi_atexit` load. objdump decodes the word at 0x94 as `strdeq`. It is the literal pool, so it stays outside the listing above. `_GLOBAL__sub_I_main` has its own pool word at 0xbc, also `0x0000ffff`, which is the priority in `r1`.

