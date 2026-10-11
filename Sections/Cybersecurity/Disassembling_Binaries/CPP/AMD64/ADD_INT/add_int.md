# C++ - AMD64 - Add Two Integers

Created with Grok Build

## Introduction

This page disassembles `add.cpp` compiled for AMD64. The source is the program in the [Disassembling-Binaries C++ tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/C%2B%2B/Intel_Architecture/AMD64/Add_int). The assembly is Intel syntax.

`a` is 3, `b` is 5, and `c` is `a + b`. The sum stays in `c`. The source ends at the closing brace of `main`. GCC writes 0 into the return register before `ret`.

On this build an `int` is four bytes. The processor is 64-bit, and the stores still write 32-bit memory operands. The compiler is GCC (Ubuntu 5.4.0-6ubuntu1~16.04.11) 5.4.0 20160609, from the object's `.comment` section.

The tree saves the object and the compiler's assembly. The compile command itself was not recorded. The listing is objdump of that object. Addresses in the object start at 0. A linked executable can place the same instructions at another address.

```bash
objdump -d -Mintel -w --section=.text add.o
```

The iostream header defines a static `std::ios_base::Init` object, `__ioinit`. The demangled symbol is `std::__ioinit`. The body of `main` is the three assignments. The object file still contains `__static_initialization_and_destruction_0(int, int)` and `_GLOBAL__sub_I_main`, because that header defines `__ioinit`. The second calls the first with the arguments 1 and 0xffff. When both arguments match, the function constructs `__ioinit` and registers `std::ios_base::Init::~Init()` with `__cxa_atexit`.

## The program *add.cpp*

```{literalinclude} code/add.cpp
:language: cpp
```

## main

GCC opens the frame with `push rbp` and `mov rbp, rsp`. The three stores sit just below `rbp`, inside the 128-byte red zone. The epilogue is `pop rbp`.

```bash
0000000000000000 (main):
int main()
{
	int a, b, c;
    0: 55                   push rbp                                    // Save the caller's frame pointer.
    1: 4889e5               mov rbp, rsp                                // This frame starts at the current stack pointer.
	a = 3;
    4: c745f403000000       mov DWORD PTR [rbp-0xc], 0x3                // a = 3, at rbp-0xc.
	b = 5;
    b: c745f805000000       mov DWORD PTR [rbp-0x8], 0x5                // b = 5, at rbp-0x8.
	c = a+ b;
   12: 8b55f4               mov edx, DWORD PTR [rbp-0xc]                // edx = a.
   15: 8b45f8               mov eax, DWORD PTR [rbp-0x8]                // eax = b.
   18: 01d0                 add eax, edx                                // eax = b + a.
   1a: 8945fc               mov DWORD PTR [rbp-0x4], eax                // c = a + b, at rbp-0x4.
}
   1d: b800000000           mov eax, 0x0                                // eax = 0. main returns that value.
   22: 5d                   pop rbp                                     // Restore the caller's frame pointer.
   23: c3                   ret                                         // Return to the C startup.
```

The three ints sit at negative offsets from the frame pointer. `c` is the slot nearest the frame pointer.

| Slot | Variable | Value |
| --- | --- | --- |
| `rbp-0xc` | `a` | 3 |
| `rbp-0x8` | `b` | 5 |
| `rbp-0x4` | `c` | `a + b` |


## The iostream initializer

The initializer spills `edi` and `esi`, compares them with 1 and 0xffff, and on a match constructs `__ioinit`. `__cxa_atexit` takes the destructor in `edi`, the object in `esi`, and `__dso_handle` in `edx`. Each of those immediates is zero in the object. The relocation fills the address in when the object is linked. The `call` displacements are the same kind of placeholder, so objdump prints the next instruction as the target.

```bash
0000000000000024 (_Z41__static_initialization_and_destruction_0ii):
   24: 55                   push rbp                                    // Save the caller's frame pointer.
   25: 4889e5               mov rbp, rsp                                // This frame starts at the current stack pointer.
   28: 4883ec10             sub rsp, 0x10                               // Room for the two spilled arguments.
   2c: 897dfc               mov DWORD PTR [rbp-0x4], edi                // Spill the first argument. The guard compares it with 1.
   2f: 8975f8               mov DWORD PTR [rbp-0x8], esi                // Spill the second argument. The guard compares it with 0xffff.
   32: 837dfc01             cmp DWORD PTR [rbp-0x4], 0x1                // Compare the first argument with 1.
   36: 7527                 jne 5f <_Z41__static_initialization_and_destruction_0ii+0x3b>  // Skip the constructor when the first argument is any other value.
   38: 817df8ffff0000       cmp DWORD PTR [rbp-0x8], 0xffff             // Compare the second argument with 65535.
   3f: 751e                 jne 5f <_Z41__static_initialization_and_destruction_0ii+0x3b>  // Skip the constructor when the priority is any other value.
   41: bf00000000           mov edi, 0x0                                // edi = __ioinit. The immediate is the unapplied R_X86_64_32 to .bss.
   46: e800000000           call 4b <_Z41__static_initialization_and_destruction_0ii+0x27>  // Construct std::ios_base::Init. The displacement is the unapplied R_X86_64_PC32, so objdump prints the next instruction.
   4b: ba00000000           mov edx, 0x0                                // edx = __dso_handle. The immediate is the unapplied R_X86_64_32.
   50: be00000000           mov esi, 0x0                                // esi = __ioinit again, the object the destructor will receive.
   55: bf00000000           mov edi, 0x0                                // edi = std::ios_base::Init::~Init(). The immediate is the unapplied R_X86_64_32.
   5a: e800000000           call 5f <_Z41__static_initialization_and_destruction_0ii+0x3b>  // Register that destructor with __cxa_atexit. The displacement is unapplied.
   5f: 90                   nop                                         // Padding in front of the epilogue.
   60: c9                   leave                                       // Release this frame.
   61: c3                   ret                                         // Return to _GLOBAL__sub_I_main.
```

`_GLOBAL__sub_I_main` is what the `.init_array` slot calls before `main`. It passes the two guard values.

```bash
0000000000000062 (_GLOBAL__sub_I_main):
   62: 55                   push rbp                                    // Save the caller's frame pointer.
   63: 4889e5               mov rbp, rsp                                // This frame starts at the current stack pointer.
   66: beffff0000           mov esi, 0xffff                             // esi = 0xffff, the init priority.
   6b: bf01000000           mov edi, 0x1                                // edi = 1, the other half of the guard.
   70: e8afffffff           call 24 <_Z41__static_initialization_and_destruction_0ii>  // Call the initializer with those two arguments.
   75: 5d                   pop rbp                                     // Restore the caller's frame pointer.
   76: c3                   ret                                         // Return.
```


