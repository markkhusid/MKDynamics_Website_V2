# Shellcode Generation and Testing

*Built with Grok Build*

## Introduction

In this section we explore shellcode generation and testing on **x86**, **x86_64**, and **ARM** platforms. Shellcode is a small payload used when exploiting a software vulnerability. It is often designed to spawn a command shell (hence the name), though modern payloads may perform many other actions.

Typical development flow:

1. Write position-independent assembly that uses system calls (e.g. `setreuid` + `execve`)
2. Assemble and link with NASM / `ld`
3. Extract raw opcodes (`objcopy` / hex dump helpers)
4. Embed opcodes in a C test harness and run under GDB (PEDA / GEF)

```asm
section .text
    global _start

_start:
    ; Your assembly code here

    ; Exit the program
    mov eax, 1
    xor ebx, ebx
    int 0x80
```

## Platforms

::::{grid} 2 2 2 2

:::{grid-item-card}
:link: x86/shellcode_x86.md

x86 shellcode
^^^
```{image} images/gdb_peda_shellcode2.jpg
:height: 180
:align: center
```

Developing, extracting, and testing Linux x86 shellcode (`setreuid` + `execve` `/bin/sh`), based in part on *Gray Hat Hacking*.
:::

:::{grid-item-card}

ARM shellcode (assets)
^^^
```{image} images/ARM/ARM_shellcode_nulls_stripped.jpg
:height: 180
:align: center
```

Screenshots and walkthrough assets live under `images/ARM/`. A full MyST page can be added from the V1 ARM HTML when ready.
:::

::::
