# Ada - ARM 64-Bit Platform - Add Two Integers

Created with Grok Build

```{figure} ../../../images/Ada/ARM64/add_Ada_ARM64_splash.jpg
:height: 600
:width: 800
:align: center
:class: clickable-figure

Radare2 session for Add_Int on ARM64. The procedure stores 3, 5, and 8.
```

## Introduction

This page disassembles `Add_Int` compiled for ARM64, AArch64 in little-endian LP64. The program is the debug build in the [Disassembling-Binaries Ada tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Ada/ARM_Architecture/ARM64/Add_Int/With_Debug_info). The screenshot is the Radare2 session of the linked executable. The listing below is the `.text` of the object file from that same build. Object-file addresses start at 0. The linked session in the screenshot starts the procedure near `0x1450`.

The compiler is GNU Ada 7.3.0, `GCC (Ubuntu/Linaro 7.3.0-27ubuntu1~18.04) 7.3.0`, with `-ggdb3 -mlittle-endian -mabi=lp64`.

## The program *add_int.adb*

```{literalinclude} code/add_int.adb
:language: ada
```

`a` is 3, `b` is 5, and `c` is `a + b`. There is no input and no print. The context clause names `Gnat.Io`. This procedure never calls it. On this GNAT build an `Integer` is four bytes, so the stores use the 32-bit `w` registers.

The tree also contains `Add_Int_w_IO` as source. That program was not built for ARM64 in this tree, so it has no listing here. The AMD64 page of the same program shows the `add` and the overflow check: [Add Two Integers with Input and Output](../../AMD64/ADD_INT_W_IO/add_int_w_io.md).

The listing is the `.text` section of the objdump saved with the object. The notes after `//` were added to that listing. Radare2 prints `movz` for these small moves. objdump prints `mov`. The bytes are `52800060`, `528000a0`, and `52800100`.

## The binder's *main*

The screenshot's `main` calls `__gnat_initialize`, `adainit`, `_ada_add_int`, `adafinal`, and `__gnat_finalize`. That is the GNAT binder. The AMD64 page has that sequence as objdump, with the spills of `argc`, `argv`, and `envp`: [Add Two Integers](../../AMD64/ADD_INT/add_int.md).

## The addition

```bash
0000000000000000 (_ada_add_int):
--
-- Some numbers to come and go.
--
with Gnat.Io; use Gnat.Io;
procedure Add_Int is
    0: d10043ff sub sp, sp, #0x10                                // Open the frame for a, b, and c.
   a, b, c: Integer;

begin

   a := 3;
    4: 52800060 mov w0, #0x3                                     // a = 3.
    8: b9000fe0 str w0, [sp, #12]                                // Store a.
   b := 5;
    c: 528000a0 mov w0, #0x5                                     // b = 5.
   10: b9000be0 str w0, [sp, #8]                                 // Store b.

   c := a + b;
   14: 52800100 mov w0, #0x8                                     // c = 8. The compiler added the two constants while compiling.
   18: b90007e0 str w0, [sp, #4]                                 // Store c.

end Add_Int;
   1c: d503201f nop                                              // Padding in front of the epilogue.
   20: 910043ff add sp, sp, #0x10                                // Drop the 16-byte frame.
   24: d65f03c0 ret                                              // Return to the binder's main.
```

`sub sp, sp, #0x10` opens a 16-byte frame. The three integers live inside that frame:

| Slot | Variable | Value |
| --- | --- | --- |
| `sp+12` | `a` | 3 |
| `sp+8` | `b` | 5 |
| `sp+4` | `c` | 8 |

The assignment `c := a + b` is the store of 8. GNAT added the constants 3 and 5 while compiling, and the object code stores that sum. `add sp, sp, #0x10` drops the frame, and `ret` returns to the binder's `main`. The `nop` is padding in front of that epilogue.
