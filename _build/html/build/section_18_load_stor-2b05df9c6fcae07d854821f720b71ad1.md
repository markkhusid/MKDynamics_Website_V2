---
title: Section 18 - Load, Store and Move Strings
---

*Built with Grok Build*

## Introduction

In this section we follow course material from the Pentester Academy
[SecurityTube Linux Assembly Language Expert 64-Bit (SLAE64)](https://www.pentesteracademy.com/course?id=7)
course. The topic is **string (and bulk memory) operations** in 64-bit Intel assembly on Linux:
loading, storing, and moving data with the `LODS*`, `STOS*`, and `MOVS*` families of instructions.

Project code is in my [GitHub repository](https://github.com/markkhusid/SLAE64).

```{figure} images/load_store_and_move_strings.png
:name: slae-s18-load-store-and-move-strings
:alt: Load, store, and move strings
:align: center

Load, store, and move strings in 64-bit assembly
```

## String instructions overview

These instructions operate with an implicit direction controlled by the **direction flag**
(cleared with `CLD` for forward, set with `STD` for backward). They use:

| Register | Role |
|----------|------|
| `RSI` | Source address (for loads / memory-to-memory moves) |
| `RDI` | Destination address (for stores / memory-to-memory moves) |
| `RCX` | Repeat count when used with `REP` / `REPE` / `REPNE` |
| `RAX` | Transfer register for `LODS*` / `STOS*` |

Width is selected by the suffix:

| Suffix | Size |
|--------|------|
| `B` | byte (8-bit) |
| `W` | word (16-bit) |
| `D` | doubleword (32-bit) |
| `Q` | quadword (64-bit) |

Common forms used in this lesson:

- **`MOVSB` / `MOVSW` / `MOVSD` / `MOVSQ`** — copy from `[RSI]` to `[RDI]`, then advance both pointers.
- **`STOSB` / … / `STOSQ`** — store `RAX` (or a portion of it) to `[RDI]`, then advance `RDI`.
- **`LODSB` / … / `LODSQ`** — load from `[RSI]` into `RAX` (or a portion), then advance `RSI`.
- **`REP`** — repeat the following string instruction `RCX` times (used here with `MOVSB`).

## The program `Strings-64.nasm`

The demonstration program exercises memory-to-memory moves (`MOVSQ`, `REP MOVSB`),
register-to-memory store (`STOSQ`), and memory-to-register load (`LODSQ`), then exits
via the Linux `exit` syscall (`rax = 0x3c`).

```{literalinclude} code/Strings-64.nasm
:language: nasm
```

### What the code does

1. **`MOVSQ` (memory → memory, one quadword)**  
   Clear the direction flag (`CLD`), point `RSI` at `HelloWorld` and `RDI` at `Copy`, then
   copy one 8-byte chunk with `MOVSQ`.

2. **`REP MOVSB` (memory → memory, byte-wise)**  
   Clear `Copy` by writing a zero quadword, then use `REP MOVSB` with `RCX = len` to copy
   the full `"Hello World"` string one byte at a time from `HelloWorld` into `Copy`.

3. **`STOSQ` (register → memory)**  
   Load a known immediate into `RAX`, point `RDI` at BSS buffer `var1`, and store that
   64-bit value with `STOSQ`.

4. **`LODSQ` (memory → register)**  
   Clear `RAX`, point `RSI` at `var1`, and load the stored value back with `LODSQ`.

5. **Exit**  
   `mov rax, 0x3c` / `mov rdi, 0` / `syscall` returns to the shell.

## Assembling, linking, and running

```bash
nasm -felf64 Strings-64.nasm -o Strings-64.o
ld Strings-64.o -o Strings-64
./Strings-64
```

The program performs the memory operations and exits with status 0. There is no console
output by design; the interesting behavior is in the registers and memory while single-stepping.

## Suggested GDB / GEF walkthrough

Load the binary under GDB with GEF (or PEDA) and single-step from `_start`:

```bash
gdb -q ./Strings-64
```

Useful checks at each stage:

- After the first `MOVSQ`: examine `Copy` (`x/s &Copy` or `x/8bx &Copy`) and note `RSI`/`RDI`.
- After `REP MOVSB`: confirm `Copy` holds `"Hello World"`.
- After `STOSQ`: `x/gx &var1` should show `0x0123456789abcdef`.
- After `LODSQ`: `RAX` should match that value.

Optionally open the same binary in **radare2** for a second view of the control flow and data
references.

## Summary

| Instruction | Direction | Effect in this demo |
|-------------|-----------|---------------------|
| `MOVSQ` | mem → mem | Copy first 8 bytes of `HelloWorld` into `Copy` |
| `REP MOVSB` | mem → mem | Copy full string into `Copy` byte by byte |
| `STOSQ` | reg → mem | Write pattern from `RAX` into `var1` |
| `LODSQ` | mem → reg | Read `var1` back into `RAX` |

These primitives are the same building blocks used later when building compact shellcode that
builds strings on the stack or in RW buffers without relying on high-level C string functions.

## Next steps

Continue with later SLAE64 modules on encoding, egg hunters, and polymorphic shellcode, or
revisit [Section 11 - Moving Data](../Section_11_Moving_Data/section_11_moving_data.md) for
general register/memory `mov` forms that complement these string ops.
