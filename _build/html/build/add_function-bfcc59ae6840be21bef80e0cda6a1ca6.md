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
objdump -d -Mintel add_function_Fortran_AMD64_ggdb3
```

## The call

`MAIN__` has to call out, so it subtracts `0x10` from `rsp` instead of using only the red zone.

```asm
mov    DWORD PTR [rbp-0x8], 0x2     ; a = 2
mov    DWORD PTR [rbp-0xc], 0x3     ; b = 3
lea    rdx, [rbp-0xc]               ; pointer to b
lea    rax, [rbp-0x8]               ; pointer to a
mov    rsi, rdx
mov    rdi, rax
call   __function_module_MOD_add_function
mov    DWORD PTR [rbp-0x4], eax     ; c = returned sum
```

| Slot | Variable |
| --- | --- |
| `rbp-0x8` | `a` |
| `rbp-0xc` | `b` |
| `rbp-0x4` | `c` |

Fortran's default argument passing for these integers is by reference. `rdi` and `rsi` hold addresses, not the numbers 2 and 3. The System V register order still applies: the first argument is `rdi`, the second is `rsi`.

## The function

```asm
push   rbp
mov    rbp, rsp
mov    QWORD PTR [rbp-0x18], rdi    ; save pointer to f_a
mov    QWORD PTR [rbp-0x20], rsi    ; save pointer to f_b
mov    rax, QWORD PTR [rbp-0x18]
mov    edx, DWORD PTR [rax]         ; edx = *f_a
mov    rax, QWORD PTR [rbp-0x20]
mov    eax, DWORD PTR [rax]         ; eax = *f_b
add    eax, edx                     ; eax = f_b + f_a
mov    DWORD PTR [rbp-0x4], eax     ; f_c
mov    eax, DWORD PTR [rbp-0x4]     ; return f_c in eax
pop    rbp
ret
```

The loads through `rax` are the dereferences. `add eax, edx` is the same integer add as a program that adds in place. A function result of type `integer` is returned in `eax`, the ordinary 32-bit return register. The caller then writes that register to `c`.

`MAIN__` ends with `leave` and `ret` because it allocated a frame. The function itself only pushed `rbp`, so `pop rbp` is enough.
