# C++ - i386 - Add Two Integers

Created with Grok Build

## Introduction

This page disassembles `add.cpp` compiled for i386. The source is the program in the [Disassembling-Binaries C++ tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/C%2B%2B/Intel_Architecture/i386/Add_Int). The assembly is Intel syntax.

`a` is 3, `b` is 5, and `c` is `a + b`. The sum stays in `c`. The source ends at the closing brace of `main`. GCC writes 0 into the return register before `ret`.

On this build an `int` is four bytes. The stores write 32-bit memory operands. The compiler is GCC (Ubuntu 5.4.0-6ubuntu1~16.04.11) 5.4.0 20160609, from the object's `.comment` section. The object is ELF 32-bit.

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

`sub esp, 0x10` opens the frame. `leave` releases it. The calling convention for the initializer, further down, passes arguments on the stack.

```bash
0000000000000000 (main):
int main()
{
	int a, b, c;
    0: 55                   push ebp                                    // Save the caller's frame pointer.
    1: 89e5                 mov ebp, esp                                // This frame starts at the current stack pointer.
    3: 83ec10               sub esp, 0x10                               // Open 16 bytes for the three ints.
	a = 3;
    6: c745f403000000       mov DWORD PTR [ebp-0xc], 0x3                // a = 3, at ebp-0xc.
	b = 5;
    d: c745f805000000       mov DWORD PTR [ebp-0x8], 0x5                // b = 5, at ebp-0x8.
	c = a+ b;
   14: 8b55f4               mov edx, DWORD PTR [ebp-0xc]                // edx = a.
   17: 8b45f8               mov eax, DWORD PTR [ebp-0x8]                // eax = b.
   1a: 01d0                 add eax, edx                                // eax = b + a.
   1c: 8945fc               mov DWORD PTR [ebp-0x4], eax                // c = a + b, at ebp-0x4.
}
   1f: b800000000           mov eax, 0x0                                // main returns 0.
   24: c9                   leave                                       // Release this frame.
   25: c3                   ret                                         // Return to the C startup.
```

The three ints sit at negative offsets from the frame pointer. `c` is the slot nearest the frame pointer.

| Slot | Variable | Value |
| --- | --- | --- |
| `ebp-0xc` | `a` | 3 |
| `ebp-0x8` | `b` | 5 |
| `ebp-0x4` | `c` | `a + b` |


## The iostream initializer

On i386 the guard reads its arguments from `ebp+8` and `ebp+0xc`. The constructor call pushes `__ioinit` and calls `std::ios_base::Init::Init()`. The registration then pushes `__dso_handle`, `__ioinit`, and the destructor, which is the cdecl order for `__cxa_atexit(destructor, object, dso)`. The `push 0` immediates and the `call` displacements are unapplied relocations. `e8 fc ff ff ff` is a displacement of -4, so objdump prints the next instruction as the target. The call inside `_GLOBAL__sub_I_main` is different: its displacement is applied, and the target is the initializer at 0x26.

```bash
0000000000000026 (_Z41__static_initialization_and_destruction_0ii):
   26: 55                   push ebp                                    // Save the caller's frame pointer.
   27: 89e5                 mov ebp, esp                                // This frame starts at the current stack pointer.
   29: 83ec08               sub esp, 0x8                                // Open 8 bytes under the spills.
   2c: 837d0801             cmp DWORD PTR [ebp+0x8], 0x1                // Compare the first stack argument with 1.
   30: 7533                 jne 65 <_Z41__static_initialization_and_destruction_0ii+0x3f>  // Skip the constructor when that argument is any other value.
   32: 817d0cffff0000       cmp DWORD PTR [ebp+0xc], 0xffff             // Compare the second stack argument with 65535.
   39: 752a                 jne 65 <_Z41__static_initialization_and_destruction_0ii+0x3f>  // Skip the constructor when the priority is any other value.
   3b: 83ec0c               sub esp, 0xc                                // Alignment before the argument push.
   3e: 6800000000           push 0x0                                    // Push __ioinit. The immediate is the unapplied R_386_32 to .bss.
   43: e8fcffffff           call 44 <_Z41__static_initialization_and_destruction_0ii+0x1e>  // Construct std::ios_base::Init. The displacement is the unapplied R_386_PC32.
   48: 83c410               add esp, 0x10                               // Drop the argument and the alignment slot.
   4b: 83ec04               sub esp, 0x4                                // Alignment before the three argument pushes.
   4e: 6800000000           push 0x0                                    // Push __dso_handle, the third argument of __cxa_atexit.
   53: 6800000000           push 0x0                                    // Push __ioinit, the object the destructor receives.
   58: 6800000000           push 0x0                                    // Push std::ios_base::Init::~Init(), the first argument.
   5d: e8fcffffff           call 5e <_Z41__static_initialization_and_destruction_0ii+0x38>  // Register the destructor. The displacement is the unapplied R_386_PC32 to __cxa_atexit.
   62: 83c410               add esp, 0x10                               // Drop the three arguments and the alignment slot.
   65: 90                   nop                                         // Padding in front of the epilogue.
   66: c9                   leave                                       // Release this frame.
   67: c3                   ret                                         // Return to _GLOBAL__sub_I_main.
```

`_GLOBAL__sub_I_main` is what the `.init_array` slot calls before `main`. It passes the two guard values.

```bash
0000000000000068 (_GLOBAL__sub_I_main):
   68: 55                   push ebp                                    // Save the caller's frame pointer.
   69: 89e5                 mov ebp, esp                                // This frame starts at the current stack pointer.
   6b: 83ec08               sub esp, 0x8                                // Open 8 bytes.
   6e: 83ec08               sub esp, 0x8                                // Open 8 more bytes so the upcoming call stays aligned.
   71: 68ffff0000           push 0xffff                                 // Push 0xffff, the init priority.
   76: 6a01                 push 0x1                                    // Push 1, the other half of the guard.
   78: e8a9ffffff           call 26 <_Z41__static_initialization_and_destruction_0ii>  // Call the initializer. This displacement is applied. The target is 0x26.
   7d: 83c410               add esp, 0x10                               // Drop the two arguments and the 8-byte slot opened for them.
   80: c9                   leave                                       // Restore esp from ebp and pop the saved frame pointer.
   81: c3                   ret                                         // Return.
```


