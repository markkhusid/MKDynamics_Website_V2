# C++ - ARM64 - Add Two Integers

Created with Grok Build

## Introduction

This page disassembles `add.cpp` compiled for ARM64. The source is the program in the [Disassembling-Binaries C++ tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/C%2B%2B/ARM_Architecture/ARM64). The assembly is ARM syntax, as objdump prints it for AArch64.

`a` is 3, `b` is 5, and `c` is `a + b`. The sum stays in `c`. The source ends at the closing brace of `main`. GCC writes 0 into the return register before `ret`.

On this build an `int` is four bytes. The stores write 32-bit `w` registers. The compiler is GCC (Debian 8.2.0-13). The `.comment` section begins `GCC: (Debian 8.2.0-13) 8.2.`

The tree saves the object and the compiler's assembly. The compile command itself was not recorded. The listing is objdump of that object. Addresses in the object start at 0. A linked executable can place the same instructions at another address.

```bash
objdump -d add.o
```

The iostream header defines a static `std::ios_base::Init` object, `__ioinit`. The demangled symbol is `std::__ioinit`. The body of `main` is the three assignments. The object file still contains `__static_initialization_and_destruction_0(int, int)` and `_GLOBAL__sub_I_main`, because that header defines `__ioinit`. The second calls the first with the arguments 1 and 0xffff. When both arguments match, the function constructs `__ioinit` and registers `std::ios_base::Init::~Init()` with `__cxa_atexit`.

## The program *add.cpp*

```{literalinclude} code/add.cpp
:language: cpp
```

## main

`sub sp, sp, #0x10` opens four words. One word, at `sp`, stays unused. `add sp, sp, #0x10` drops the frame.

```bash
0000000000000000 (main):
int main()
{
	int a, b, c;
    0: d10043ff sub sp, sp, #0x10                               // Open four words.
	a = 3;
    4: 52800060 mov w0, #0x3                                    // w0 = 3.
    8: b9000fe0 str w0, [sp, #12]                               // a = 3, at sp+12.
	b = 5;
    c: 528000a0 mov w0, #0x5                                    // w0 = 5.
   10: b9000be0 str w0, [sp, #8]                                // b = 5, at sp+8.
	c = a+ b;
   14: b9400fe1 ldr w1, [sp, #12]                               // w1 = a.
   18: b9400be0 ldr w0, [sp, #8]                                // w0 = b.
   1c: 0b000020 add w0, w1, w0                                  // w0 = a + b.
   20: b90007e0 str w0, [sp, #4]                                // c = a + b, at sp+4.
}
   24: 52800000 mov w0, #0x0                                    // main returns 0.
   28: 910043ff add sp, sp, #0x10                               // Drop the frame.
   2c: d65f03c0 ret                                             // Return to the C startup.
```

| Slot | Variable | Value |
| --- | --- | --- |
| `sp+12` | `a` | 3 |
| `sp+8` | `b` | 5 |
| `sp+4` | `c` | `a + b` |


## The iostream initializer

The AArch64 initializer keeps the arguments in `w0` and `w1`, spills them, and compares them with 1 and 0xffff. On a match it builds the three arguments of `__cxa_atexit`: the destructor in `x0`, `__ioinit` in `x1`, and `__dso_handle` in `x2`. The `adrp` and `add` immediates are 0 in this object, and the `bl` displacement is 0. objdump still names the constructor, the destructor, `__dso_handle`, and `__cxa_atexit` from the relocations.

```bash
0000000000000030 (_Z41__static_initialization_and_destruction_0ii):
   30: a9be7bfd stp x29, x30, [sp, #-32]!                       // Save the frame pointer and the return address, and open 32 bytes.
   34: 910003fd mov x29, sp                                     // This frame starts at the current stack pointer.
   38: b9001fe0 str w0, [sp, #28]                               // Spill the first argument.
   3c: b9001be1 str w1, [sp, #24]                               // Spill the second argument.
   40: b9401fe0 ldr w0, [sp, #28]                               // Reload the first argument.
   44: 7100041f cmp w0, #0x1                                    // Compare it with 1.
   48: 540001e1 b.ne 84 <_Z41__static_initialization_and_destruction_0ii+0x54>  // Skip the constructor when it is any other value.
   4c: b9401be1 ldr w1, [sp, #24]                               // Reload the second argument.
   50: 529fffe0 mov w0, #0xffff                                 // w0 = 65535.
   54: 6b00003f cmp w1, w0                                      // Compare the priority with 65535.
   58: 54000161 b.ne 84 <_Z41__static_initialization_and_destruction_0ii+0x54>  // Skip the constructor when the priority is any other value.
   5c: 90000000 adrp x0, 0 <main>                               // Page immediate is 0 in this object. x0 will be the __ioinit address passed to the constructor.
   60: 91000000 add x0, x0, #0x0                                // Page offset is 0 in this object.
   64: 94000000 bl 0 <_ZNSt8ios_base4InitC1Ev>                  // Construct std::ios_base::Init. The displacement is 0 in this object, and objdump names the constructor.
   68: 90000000 adrp x0, 0 <__dso_handle>                       // Page immediate is 0. objdump names __dso_handle.
   6c: 91000002 add x2, x0, #0x0                                // x2 = __dso_handle, the third argument of __cxa_atexit.
   70: 90000000 adrp x0, 0 <main>                               // Page immediate is 0. This address is __ioinit.
   74: 91000001 add x1, x0, #0x0                                // x1 = __ioinit, the object the destructor receives.
   78: 90000000 adrp x0, 0 <_ZNSt8ios_base4InitD1Ev>            // Page immediate is 0. objdump names std::ios_base::Init::~Init().
   7c: f9400000 ldr x0, [x0]                                    // x0 = that destructor, the first argument of __cxa_atexit.
   80: 94000000 bl 0 <__cxa_atexit>                             // Register the destructor. The displacement is 0 in this object.
   84: d503201f nop                                             // Padding in front of the epilogue.
   88: a8c27bfd ldp x29, x30, [sp], #32                         // Restore the frame pointer and the return address.
   8c: d65f03c0 ret                                             // Return to _GLOBAL__sub_I_main.
```

`_GLOBAL__sub_I_main` is what the `.init_array` slot calls before `main`. It passes the two guard values.

```bash
0000000000000090 (_GLOBAL__sub_I_main):
   90: a9bf7bfd stp x29, x30, [sp, #-16]!                       // Save the frame pointer and the return address.
   94: 910003fd mov x29, sp                                     // This frame starts at the current stack pointer.
   98: 529fffe1 mov w1, #0xffff                                 // w1 = 65535, the init priority.
   9c: 52800020 mov w0, #0x1                                    // w0 = 1, the other half of the guard.
   a0: 97ffffe4 bl 30 <_Z41__static_initialization_and_destruction_0ii>  // Call the initializer with those two arguments.
   a4: a8c17bfd ldp x29, x30, [sp], #16                         // Restore the frame pointer and the return address.
   a8: d65f03c0 ret                                             // Return.
```


