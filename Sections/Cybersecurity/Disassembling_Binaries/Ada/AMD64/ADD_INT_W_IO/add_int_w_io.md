# Ada - AMD 64-Bit Platform - Add Two Integers with Input and Output

Created with Grok Build

```{figure} ../../../images/Ada/AMD64/add_IO_Ada_AMD64_splash.jpg
:height: 600
:width: 800
:align: center
:class: clickable-figure

Radare2 session for Add_Int_w_IO. The sum is an add, followed by the overflow check.
```

## Introduction

This page disassembles `Add_Int_w_IO` for AMD64. The program reads two integers, adds them, and prints the sum. The source and the debug executable are in the [Disassembling-Binaries Ada tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Ada/Intel_Architecture/AMD64/Integer_Operations/Add_Int_w_IO/With_Debug_Info). The assembly is Intel syntax.

The screenshot is the Radare2 session of `add_int_w_io_Ada_AMD64_ggdb3`. The listing below is `objdump` of that executable. `_ada_add_int_w_io` is at `0x152e` in both.

## The program *add_int_w_io.adb*

```{literalinclude} code/add_int_w_io.adb
:language: ada
```

`Get` reads `a` and `b`. `c` is their sum. The prompts are the strings in the source, including the trailing space after `->`. `The sum is : ` has a space on each side of the colon.

On this GNAT build an `Integer` is four bytes. Because `a` and `b` are values read at run time, the compiler emits an `add`, and it emits Ada's check for `Constraint_Error` on overflow.

The debug build recorded these commands:

```bash
gcc -c -S -ggdb3 add_int_w_io.adb
gnatmake -g add_int_w_io.adb
mv add_int_w_io add_int_w_io_Ada_AMD64_ggdb3
```

The compiler is GNU Ada 7.3.0. The executable's read-only data records `GNAT Version: 7.3.0`. GNAT names the procedure `_ada_add_int_w_io`.

The saved objdump used `-x -D`, which also walks headers and debug sections. The listing on this page is `.text`:

```bash
objdump -d -Mintel -S -w add_int_w_io_Ada_AMD64_ggdb3
```

`-d` disassembles executable sections. `-S` interleaves the Ada source. `-w` keeps each instruction on one line. `-Mintel` selects Intel operand order. The notes after `//` were added to that listing.

## The binder's *main*

`main` is the same binder shape as [Add Two Integers](../ADD_INT/add_int.md). On this executable it starts at `0x14c8`. The calls are:

```bash
 150c: e8cffcffff           call 11e0 <__gnat_initialize@plt>            // Runtime startup.
 1511: e88efeffff           call 13a4 <adainit>                          // Elaborate the Ada units named by this program.
 1516: e813000000           call 152e <_ada_add_int_w_io>                // Call the program procedure.
 151b: e85afeffff           call 137a <adafinal>                         // Run Ada finalization.
 1520: e84bfcffff           call 1170 <__gnat_finalize@plt>              // Runtime shutdown.
```

`__gnat_initialize`, `adainit`, the procedure, `adafinal`, and `__gnat_finalize` run in that order. The full spill of `argc`, `argv`, and `envp` is on the addition page. Here `main` enters the procedure at `0x152e`.

## The procedure

```bash
000000000000152e (_ada_add_int_w_io):
--
-- Some numbers to come and go.  With IO.
--
with Gnat.Io; use Gnat.Io;
procedure Add_Int_w_IO is
 152e: 55                   push rbp                                     // Save the caller's frame pointer.
 152f: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.
 1532: 4157                 push r15                                     // Save a register the string calls will use.
 1534: 4156                 push r14                                     // Save a register the string calls will use.
 1536: 4155                 push r13                                     // Save a register the string calls will use.
 1538: 4154                 push r12                                     // Save a register the string calls will use.
 153a: 53                   push rbx                                     // Save a register the string calls will use.
 153b: 4883ec18             sub rsp, 0x18                                // Open slots for a, b, and c.
   a, b, c: Integer;

begin

   Put ("Please enter first integer now followed by <CR> -> ");
 153f: 488d057a020000       lea rax, [rip+0x27a]                         // Address of the first prompt, at 17c0.
 1546: 488d1503030000       lea rdx, [rip+0x303]                         // Bounds of that string, at 1850.
 154d: 4889c1               mov rcx, rax                                 // Copy a pointer toward the argument registers.
 1550: 4889d3               mov rbx, rdx                                 // Copy a pointer toward the argument registers.
 1553: 4889d0               mov rax, rdx                                 // Copy a pointer toward the argument registers.
 1556: 4889cf               mov rdi, rcx                                 // rdi = the characters.
 1559: 4889c6               mov rsi, rax                                 // rsi = the bounds.
 155c: e8cffcffff           call 1230 <gnat__io__put__6@plt>             // Print the string. put__6 is Gnat.Io's string Put.
   Get (a);
 1561: e85afcffff           call 11c0 <gnat__io__get@plt>                // Read an integer. The value comes back in eax.
 1566: 8945cc               mov DWORD PTR [rbp-0x34], eax                // a = eax.

   Put ("Please enter second integer now followed by <CR> -> ");
 1569: 4c8d3588020000       lea r14, [rip+0x288]                         // Address of the second prompt, at 17f8.
 1570: 4c8d3de1020000       lea r15, [rip+0x2e1]                         // Bounds of that string, at 1858.
 1577: 4c89f1               mov rcx, r14                                 // Copy a pointer toward the argument registers.
 157a: 4c89fb               mov rbx, r15                                 // Copy a pointer toward the argument registers.
 157d: 4c89f0               mov rax, r14                                 // Copy a pointer toward the argument registers.
 1580: 4c89fa               mov rdx, r15                                 // Copy a pointer toward the argument registers.
 1583: 4889d0               mov rax, rdx                                 // Copy a pointer toward the argument registers.
 1586: 4889cf               mov rdi, rcx                                 // rdi = the characters.
 1589: 4889c6               mov rsi, rax                                 // rsi = the bounds.
 158c: e89ffcffff           call 1230 <gnat__io__put__6@plt>             // Print the string. put__6 is Gnat.Io's string Put.
   Get (b);
 1591: e82afcffff           call 11c0 <gnat__io__get@plt>                // Read the second integer into eax.
 1596: 8945c8               mov DWORD PTR [rbp-0x38], eax                // b = eax.

   c := a + b;
 1599: b900000000           mov ecx, 0x0                                 // Overflow flag starts clear.
 159e: 8b55cc               mov edx, DWORD PTR [rbp-0x34]                // edx = a.
 15a1: 8b45c8               mov eax, DWORD PTR [rbp-0x38]                // eax = b.
 15a4: 01d0                 add eax, edx                                 // eax = a + b. The flags record signed overflow.
 15a6: 7105                 jno 15ad <_ada_add_int_w_io+0x7f>            // Skip the flag store when the add did not overflow.
 15a8: b901000000           mov ecx, 0x1                                 // Remember that the add overflowed.
 15ad: 89c2                 mov edx, eax                                 // Hold the sum in edx.
 15af: 89c8                 mov eax, ecx                                 // eax = the overflow flag.
 15b1: 85c0                 test eax, eax                                // Test the overflow flag.
 15b3: 7411                 je 15c6 <_ada_add_int_w_io+0x98>             // Store c when the sum fits in an Integer.
 15b5: be10000000           mov esi, 0x10                                // esi = 16, the source line of c := a + b.
 15ba: 488d3d6b020000       lea rdi, [rip+0x26b]                         // rdi points at the file name add_int_w_io.adb.
 15c1: e87afcffff           call 1240 <__gnat_rcheck_CE_Overflow_Check@plt> // Raise Constraint_Error for the overflow.
 15c6: 89d0                 mov eax, edx                                 // eax = the sum.
 15c8: 8945c4               mov DWORD PTR [rbp-0x3c], eax                // c = the sum.

   Put ("The sum is : ");
 15cb: 4c8d256b020000       lea r12, [rip+0x26b]                         // Address of "The sum is : ", at 183d.
 15d2: 4c8d2d87020000       lea r13, [rip+0x287]                         // Bounds of that string, at 1860.
 15d9: 4c89e1               mov rcx, r12                                 // Copy a pointer toward the argument registers.
 15dc: 4c89eb               mov rbx, r13                                 // Copy a pointer toward the argument registers.
 15df: 4c89e0               mov rax, r12                                 // Copy a pointer toward the argument registers.
 15e2: 4c89ea               mov rdx, r13                                 // Copy a pointer toward the argument registers.
 15e5: 4889d0               mov rax, rdx                                 // Copy a pointer toward the argument registers.
 15e8: 4889cf               mov rdi, rcx                                 // rdi = the characters.
 15eb: 4889c6               mov rsi, rax                                 // rsi = the bounds.
 15ee: e83dfcffff           call 1230 <gnat__io__put__6@plt>             // Print the string. put__6 is Gnat.Io's string Put.
   Put (c);
 15f3: 8b45c4               mov eax, DWORD PTR [rbp-0x3c]                // eax = c.
 15f6: 89c7                 mov edi, eax                                 // The integer to print goes in edi.
 15f8: e813fcffff           call 1210 <gnat__io__put__2@plt>             // Print the integer. put__2 is Gnat.Io's integer Put.
   New_Line;
 15fd: bf01000000           mov edi, 0x1                                 // edi = 1. A parameterless New_Line prints one line.
 1602: e819fcffff           call 1220 <gnat__io__new_line__2@plt>        // Print the new line.

end Add_Int_w_IO;
 1607: 90                   nop                                          // Padding in front of the epilogue.
 1608: 4883c418             add rsp, 0x18                                // Drop the local slots.
 160c: 5b                   pop rbx                                      // Restore a saved register.
 160d: 415c                 pop r12                                      // Restore a saved register.
 160f: 415d                 pop r13                                      // Restore a saved register.
 1611: 415e                 pop r14                                      // Restore a saved register.
 1613: 415f                 pop r15                                      // Restore a saved register.
 1615: 5d                   pop rbp                                      // Restore the caller's frame pointer.
 1616: c3                   ret                                          // Return to the binder's main.
```

### The frame

The prologue saves `rbp`, then `r15`, `r14`, `r13`, `r12`, and `rbx`. The string calls use those callee-saved registers as temporary copies of the two pointers. `sub rsp, 0x18` opens the slots for the three integers:

| Slot | Variable | Value |
| --- | --- | --- |
| `rbp-0x34` | `a` | the first `Get` |
| `rbp-0x38` | `b` | the second `Get` |
| `rbp-0x3c` | `c` | the sum |

The epilogue drops those 24 bytes, restores the five saved registers, restores the caller's frame pointer, and returns to `main`.

### Printing a string

`Gnat.Io.Put` of a string is `gnat__io__put__6`. Ada passes a string as two pointers. `rdi` is the characters. `rsi` is the bounds record, two 32-bit integers, `First` and `Last`. `First` is 1. `Last` is the length of these strings, because each one starts at 1.

The `mov` instructions between the `lea` and the `call` copy those two pointers toward `rdi` and `rsi`. The bytes of the strings live in `.rodata`:

| Text | Characters | Bounds | Last |
| --- | --- | --- | --- |
| first prompt | `0x17c0` | `0x1850` | 51 (`0x33`) |
| second prompt | `0x17f8` | `0x1858` | 52 (`0x34`) |
| `The sum is : ` | `0x183d` | `0x1860` | 13 (`0x0d`) |

The second prompt is 52 characters and ends where the file name `add_int_w_io.adb` begins, at `0x182c`. The bounds record tells `Put` how many characters to write, so the prompt is not terminated by a null byte.

`Get` is `gnat__io__get`. The integer comes back in `eax`, and the next instruction stores it.

### The add and the overflow check

```bash
 1599: b900000000           mov ecx, 0x0                                 // Overflow flag starts clear.
 159e: 8b55cc               mov edx, DWORD PTR [rbp-0x34]                // edx = a.
 15a1: 8b45c8               mov eax, DWORD PTR [rbp-0x38]                // eax = b.
 15a4: 01d0                 add eax, edx                                 // eax = a + b. The flags record signed overflow.
 15a6: 7105                 jno 15ad <_ada_add_int_w_io+0x7f>            // Skip the flag store when the add did not overflow.
 15a8: b901000000           mov ecx, 0x1                                 // Remember that the add overflowed.
```

`ecx` starts clear. `add eax, edx` adds `a` into the register that holds `b` and sets the signed-overflow flag. `jno` skips the store of 1 when that flag is clear. The sum is then held in `edx` while `eax` is reloaded with the flag. `test eax, eax` and `je` reach the store of `c` when the sum fits in an `Integer`.

When the flag is set, `esi` is 16, the source line of `c := a + b`, and `rdi` points at `add_int_w_io.adb` at `0x182c`. `__gnat_rcheck_CE_Overflow_Check` raises `Constraint_Error`. On the path that fits, `c` is stored at `rbp-0x3c`.

### Printing the sum

`Put` of an integer is `gnat__io__put__2`. The value goes in `edi`. `New_Line` with no arguments is `gnat__io__new_line__2` with `edi` equal to 1, which prints one line.
