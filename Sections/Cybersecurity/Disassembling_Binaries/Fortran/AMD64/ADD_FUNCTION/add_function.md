# Fortran - AMD 64-Bit Platform - A Function Call

Created with Grok Build

## Introduction

This page disassembles a Fortran function compiled for AMD64. The source is `add_function.f08` from the [Disassembling-Binaries](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Fortran/Intel_architecture/AMD64/Functions/Add_Functions_Int) tree. The arithmetic is the same add as the [addition page](../ADD_INT/add_int.md). What is new is the call: the arguments are pointers, and the sum comes back in `eax`.

`main` is the same runtime prologue as that addition page. It calls `MAIN__`, and `MAIN__` calls the function.

## The program *add_function.f08*

```{literalinclude} code/add_function.f08
:language: fortran
```

The function lives in `function_module`. gfortran mangles that into `__function_module_MOD_add_function`. The program sets `a` to 2 and `b` to 3, then stores the returned sum in `c`.

```bash
gfortran -ggdb3 add_function.f08 -o add_function_Fortran_AMD64_ggdb3
objdump -d -Mintel -S -w add_function_Fortran_AMD64_ggdb3
```

`-S` interleaves the Fortran source. `-w` keeps each instruction on one line. Each instruction line is the address, the machine bytes, and the Intel disassembly. The notes after `//` were added to that objdump.

## The call

`MAIN__` has to call out, so it subtracts `0x10` from `rsp` instead of using only the red zone.

```bash
000000000000116b (MAIN__):

end module function_module

program use_functions
 116b: 55                   push rbp                                     // Save the caller's frame pointer.
 116c: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.
 116f: 4883ec10             sub rsp, 0x10                                // Open a frame. This procedure calls out, so it cannot use only the red zone.
      use function_module
      implicit none

      integer           :: a, b, c

      a = 2
 1173: c745f802000000       mov DWORD PTR [rbp-0x8], 0x2                 // a = 2.

      b = 3
 117a: c745f403000000       mov DWORD PTR [rbp-0xc], 0x3                 // b = 3.

      c = add_function(a, b)
 1181: 488d55f4             lea rdx, [rbp-0xc]                           // Pointer to b.
 1185: 488d45f8             lea rax, [rbp-0x8]                           // Pointer to a.
 1189: 4889d6               mov rsi, rdx                                 // Second argument, the pointer to b.
 118c: 4889c7               mov rdi, rax                                 // First argument, the pointer to a.
 118f: e8b5ffffff           call 1149 <__function_module_MOD_add_function> // Call the module function. The arguments are pointers.
 1194: 8945fc               mov DWORD PTR [rbp-0x4], eax                 // c = the integer returned in eax.

end program use_functions
 1197: 90                   nop                                          // Padding in front of the epilogue.
 1198: c9                   leave                                        // Release this frame and restore the caller's rbp.
 1199: c3                   ret                                          // Pop the return address and return to the caller.
```

| Slot | Variable |
| --- | --- |
| `rbp-0x8` | `a` |
| `rbp-0xc` | `b` |
| `rbp-0x4` | `c` |

Fortran's default argument passing for these integers is by reference. `rdi` and `rsi` hold addresses, not the numbers 2 and 3. The System V register order still applies: the first argument is `rdi`, the second is `rsi`.

## The function

```bash
0000000000001149 (__function_module_MOD_add_function):

      implicit none

contains

      function add_function(f_a, f_b) result (f_c)
 1149: 55                   push rbp                                     // Save the caller's frame pointer.
 114a: 4889e5               mov rbp, rsp                                 // This frame starts at the current stack pointer.
 114d: 48897de8             mov QWORD PTR [rbp-0x18], rdi                // Save the incoming pointer to f_a. Arguments arrive by reference.
 1151: 488975e0             mov QWORD PTR [rbp-0x20], rsi                // Save the incoming pointer to f_b.
              integer   :: f_a, f_b, f_c

              f_c = f_a + f_b
 1155: 488b45e8             mov rax, QWORD PTR [rbp-0x18]                // Reload the pointer to f_a.
 1159: 8b10                 mov edx, DWORD PTR [rax]                     // edx = the integer f_a points at.
 115b: 488b45e0             mov rax, QWORD PTR [rbp-0x20]                // Reload the pointer to f_b.
 115f: 8b00                 mov eax, DWORD PTR [rax]                     // eax = the integer f_b points at.
 1161: 01d0                 add eax, edx                                 // eax = eax + edx.
 1163: 8945fc               mov DWORD PTR [rbp-0x4], eax                 // f_c, a local in this frame.

      end function add_function
 1166: 8b45fc               mov eax, DWORD PTR [rbp-0x4]                 // A Fortran integer result is returned in eax.
 1169: 5d                   pop rbp                                      // Restore the caller's frame pointer.
 116a: c3                   ret                                          // Pop the return address and return to the caller.
```

The loads through `rax` are the dereferences. `add eax, edx` is the same integer add as a program that adds in place. A function result of type `integer` is returned in `eax`, the ordinary 32-bit return register. The caller then writes that register to `c`.

`MAIN__` ends with `leave` and `ret` because it allocated a frame. The function itself only pushed `rbp`, so `pop rbp` is enough.
