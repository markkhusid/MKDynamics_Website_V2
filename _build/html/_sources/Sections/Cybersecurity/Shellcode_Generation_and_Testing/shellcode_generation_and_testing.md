# Shellcode Generation and Testing

## Introduction

### What is Shellcode?

Shellcode is a small piece of code that is used as the payload in the exploitation of a software vulnerability. It is called shellcode because it typically starts a command shell from which the attacker can control the compromised machine, but any piece of code that performs a similar task can be called shellcode. Because the function of a payload is not limited to merely spawning a shell, some have suggested that the name shellcode is insufficient. However, attempts at replacing the term have not gained wide acceptance.

section .text
    global _start

_start:
    ; Your assembly code here

    ; Exit the program
    mov eax, 1
    xor ebx, ebx
    int 0x80
