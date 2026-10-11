# Ada - AMD 64-Bit Platform - Add Two Integers

Created with Grok Build

```{figure} ../images/add_Ada_AMD64_splash.jpg
:height: 600
:width: 800
:align: center
:class: clickable-figure

Radare2 session for Add_Int. The procedure stores 3, 5, and 8.
```

## Introduction

This page disassembles one Ada procedure compiled for AMD64, the 64-bit x86 platform. The program is `Add_Int` from the [Disassembling-Binaries Ada tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Ada/Intel_Architecture/AMD64/Integer_Operations/Add_Int/With_Debug_Info). The assembly is Intel syntax.

The screenshot is the Radare2 session. In that session the procedure begins near `0x137e`. The listing below is `objdump` of the debug executable from the same tree, where `_ada_add_int` begins at `0x262a`. A position-independent executable can be loaded at another address. The stores of 3, 5, and 8 are the same bytes in both views: `c745fc`, `c745f8`, and `c745f4`.

## The program *add_int.adb*

```{literalinclude} code/add_int.adb
:language: ada
```

`a` is 3, `b` is 5, and `c` is `a + b`. There is no input and no print. The context clause names `Gnat.Io`. This procedure never calls it, so the body has no call into the runtime.

On this GNAT build an `Integer` is four bytes. The processor is 64-bit, and the stores still write 32-bit memory operands.

The debug build recorded these commands:

```bash
gcc -c -S -ggdb3 add_int.adb
gnatmake -g add_int.adb
mv add_int add_int_Ada_AMD64_g
```

`gnatmake -g` compiles, binds, and links. The binder writes a C-style `main` that starts the Ada runtime and calls the procedure. GNAT names the procedure `_ada_add_int`. The compiler is GNU Ada 8.2.0, from GCC (Debian 8.2.0-14) 8.2.0. The executable's read-only data records `GNAT Version: 8.2.0`.

The saved objdump used `-x -D`, which also walks headers and debug sections. The listing on this page is `.text`:

```bash
objdump -d -Mintel -S -w add_int_Ada_AMD64_g
```

`-d` disassembles executable sections. `-S` interleaves the Ada source. `-w` keeps each instruction on one line. `-Mintel` selects Intel operand order, so the destination is the first operand. Each instruction line is the address, the machine bytes, and the Intel disassembly. The notes after `//` were added to that listing.

## The binder's *main*

`main` is not the Ada procedure. It spills `argc`, `argv`, and `envp`, publishes them for the runtime, and then calls initialization, elaboration, the procedure, and finalization.

```bash
0000000000002590 (main):
 2590: 55                   push rbp                                     // Save the caller's frame pointer.
 2591: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.
 2594: 4883ec30             sub rsp, 0x30                                // Room for argc, argv, envp, and the initialization argument.
 2598: 897dec               mov DWORD PTR [rbp-0x14], edi                // Spill argc.
 259b: 488975e0             mov QWORD PTR [rbp-0x20], rsi                // Spill argv.
 259f: 488955d8             mov QWORD PTR [rbp-0x28], rdx                // Spill envp.
 25a3: 488d058e0a0000       lea rax, [rip+0xa8e]                         // Address of __gnat_ada_main_program_name.
 25aa: 488945f0             mov QWORD PTR [rbp-0x10], rax                // Save that name.
 25ae: 8b45ec               mov eax, DWORD PTR [rbp-0x14]                // Reload argc.
 25b1: 8905892c0000         mov DWORD PTR [rip+0x2c89], eax              // Store it in gnat_argc.
 25b7: 488b45e0             mov rax, QWORD PTR [rbp-0x20]                // Reload argv.
 25bb: 488905062c0000       mov QWORD PTR [rip+0x2c06], rax              // Store it in gnat_argv.
 25c2: 488b45d8             mov rax, QWORD PTR [rbp-0x28]                // Reload envp.
 25c6: 488905832b0000       mov QWORD PTR [rip+0x2b83], rax              // Store it in gnat_envp.
 25cd: 488d45f8             lea rax, [rbp-0x8]                           // Argument block for __gnat_initialize.
 25d1: 4889c7               mov rdi, rax                                 // Pass that block in rdi.
 25d4: e8e7faffff           call 20c0 <__gnat_initialize@plt>            // Runtime startup.
 25d9: e890fdffff           call 236e <adainit>                          // Elaborate the Ada units named by this program.
 25de: e847000000           call 262a <_ada_add_int>                     // Call the program procedure.
 25e3: e85cfdffff           call 2344 <adafinal>                         // Run Ada finalization.
 25e8: e853faffff           call 2040 <__gnat_finalize@plt>              // Runtime shutdown.
 25ed: 8b05b52b0000         mov eax, DWORD PTR [rip+0x2bb5]              // Load gnat_exit_status. main returns that value.
 25f3: c9                   leave                                        // Release this frame.
 25f4: c3                   ret                                          // Return to the C startup.
```

`__gnat_ada_main_program_name` is the name the binder recorded, saved at `rbp-0x10`. `gnat_argc`, `gnat_argv`, and `gnat_envp` are the copies the runtime reads. The `lea` of `[rbp-0x8]` builds the argument block, and the next instruction passes that block to `__gnat_initialize` in `rdi`. `adainit` elaborates the units this program depends on. The call at `0x25de` enters `_ada_add_int`. `adafinal` and `__gnat_finalize` shut the runtime down. `main` returns `gnat_exit_status`.

`sub rsp, 0x30` opens the frame those spills live in. `leave` releases it. `ret` returns to the C startup that called `main`.

The program that reads two integers uses this same binder shape. That page shows the call into its own procedure and points back here for the surrounding instructions.

## The addition

```bash
000000000000262a (_ada_add_int):
--
-- Some numbers to come and go.
--
with Gnat.Io; use Gnat.Io;
procedure Add_Int is
 262a: 55                   push rbp                                     // Save the caller's frame pointer.
 262b: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.
   a, b, c: Integer;

begin

   a := 3;
 262e: c745fc03000000       mov DWORD PTR [rbp-0x4], 0x3                 // a = 3.
   b := 5;
 2635: c745f805000000       mov DWORD PTR [rbp-0x8], 0x5                 // b = 5.

   c := a + b;
 263c: c745f408000000       mov DWORD PTR [rbp-0xc], 0x8                 // c = 8. The compiler added the two constants while compiling.

end Add_Int;
 2643: 90                   nop                                          // Padding in front of the epilogue.
 2644: 5d                   pop rbp                                      // Restore the caller's frame pointer.
 2645: c3                   ret                                          // Return to the binder's main.
```

The frame grows downward. The three integers sit at negative offsets from `rbp`:

| Slot | Variable | Value |
| --- | --- | --- |
| `rbp-0x4` | `a` | 3 |
| `rbp-0x8` | `b` | 5 |
| `rbp-0xc` | `c` | 8 |

The assignment `c := a + b` is the store of 8. GNAT added the constants 3 and 5 while compiling, and the object code stores that sum.

This function never subtracts from `rsp`. The three stores land in the 128-byte red zone under `rsp`, which the System V AMD64 ABI leaves unused by signal handlers and by a caller. `pop rbp` restores the caller's frame pointer, and `ret` returns to the binder's `main`. The `nop` is padding in front of that epilogue.
