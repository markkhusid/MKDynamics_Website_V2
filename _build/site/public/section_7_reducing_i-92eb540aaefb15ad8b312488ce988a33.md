---
title: Section 7 - Reducing Instruction Sizes and Removing Nulls
---

*Built with Grok Build*

## Introduction

In this section we will be following along with and completing course material from the Pentester Academy's SecurityTube Linux Assembly language Expert 64 Bit course. The third assignment is attempting to reduce the instruction size and remove nulls from the Hello World program written in the previous section. We will show some techniques that can be used to accomplish making the code more compact and to remove nulls within the opcodes.

Compact code without nulls is desireable for shellcode, since often the memory buffers that are available within vulnerabilities are limited. In this section, we will code, assemble, link and run the enhanced version of helloworld.nasm, while making references to the original version. We will run the enhanced version of the shellcode to verify that it still works as before. Execution is to be monitored via GDB. We will use the GEF or PEDA add-ons for GDB to enhance the visual presentation from GDB.

Project code is contained in my [GitHub repository](https://github.com/markkhusid/SLAE64).

## The program helloworld-small1_mod.nasm versus the program helloword.nasm

The screenshot below displays the contents of the program helloworld-small1_mod.nasm as well as helloworld.nasm side by side.

Note that in the course material, the instructor only modifies the first instruction to make it more compact and to remove nulls. That version of helloworld.nasm is in the file name helloworld-small1.nasm. What we did is to go ahead to apply changes to the rest of helloworld-small1.nasm so the generated opcodes are more comapct and nulls are removed to the extent possible.

```{figure} images/helloworld_and_helloword_small_side_by_side.jpg
:name: slae-s7-helloworld-and-helloword-small-side-by-side-1
:alt: helloworld and helloword small side by side
:align: center
:class: clickable-figure

helloworld and helloword small side by side
```

The program helloworld-small1.nasm and helloworld.nasm

 In the above screenshot, helloworld.nasm is shown for comparison to helloworld-small1_mod.nasm. What we have done to helloworld.nasm to make it helloworld-small1_mod.nasm is to modify the instructions so that helloworld-small1_mod.nasm has a reduced size and removed nulls from an opcodes perspective. The screenshot below displays the objdump output of both assembled programs to elucidate this further.

```{figure} images/helloworld_and_helloword_small_side_by_side_with_objdump.jpg
:name: slae-s7-helloworld-and-helloword-small-side-by-side-with-o-2
:alt: helloworld and helloword small side by side with objdump
:align: center
:class: clickable-figure

helloworld and helloword small side by side with objdump
```

The program helloworld.asm and helloworld-small1_mod.nasm with their opcodes.

 In the screenshot above, we show both programs as well as their generated opcodes. We can see from the opcodes of helloworld-small1_mod.nasm, that the first few opcodes are:

```text
0:	b0 01 mov $0x1,%al
```

 rather than the much longer and null ridden:

```text
0:	48 b8 01 00 00 00 00 movabs $0x1,%rax
7:	00 00 00
```

In both cases, the same action effectively occurs, the immediate 1 is moved into the register RAX; however, in the helloworld-small1_mod.nasm version, what was done is to move the 8 bit version of the immediate 1 into the 8 bit portion of RAX. Therefore, both the opcode and the immediate are more compact. Actually, the compact version uses only 2 bytes, while the non-compact version uses 10 bytes, for a savings of 8 bytes.

In the next line, we have implemented the instruction:

 mov rdi, 1

 as:

 mov di, ax

What this instruction has done is to copy the contents of the 16-bit register ax into the 16-bit register di. Since ax already contains the immediate value 1, this instruction effectively moves the immediate value 1 into the 16-bit register di as well.

Looking at the opcodes from both files, the opcodes generated from helloworld.nasm for this instruction were:

```text
a:	48 bf 01 00 00 00 00 movabs $0x1,%rdi
11:	00 00 00
```

 while the opcodes generated from helloworld-small1_mods.nasm were:

```text
2:	66 89 c7 mov %ax,%di
```

 for a savings of 7 bytes.

Such copying and reusing immediates from one register to another, or from the stack as we will see later, is a frequent "trick" used by shellcode composers to remove nulls and compactify code.

Note that we could have moved the immediate 1 into the 8-bit register DIL directly. In this case, the instruction would be:

 mov dil, 1

 and the generated opcodes would be:

```text
2: 40 b7 01 mov $0x1,%dil
```

 for a savings of 7 bytes again. Or we could have moved the contents of the 8-bit register AL into the the 8-bit register DIL. In this case the instruction would be:

 mov dil, al

 and the generated opcodes would be:

```text
2:	40 88 c7 mov %al,%dil
```

 for a savings of 7 bytes in both cases.

This brings up an obvious point. There are many ways to accomplish the same thing. The idea is to compactify the generated opcodes as much as possible and remove all of the nulls.

The astute observer will notice something else. We have not been able to remove the nulls when it comes to operations that involve memory addresses. Namely, the operation:

 mov rsi, hello_world

 produces the opcodes:

```text
5:	48 be 00 00 00 00 00 movabs $0x0,%rsi
c:	00 00 00
```

for an operation that takes up 10 bytes. Also notice that at this point in the compilation process, the assembler moved the immediate 0 into the register RSI, rather than the memory address of the string hello_world. This is because the assembler left a placeholder for the linker to fill in the actual address when the executable is produced. So if we look at the objdump of the executable, we get the following:

```bash
$ objdump -d helloworld
```

helloworld: file format elf64-x86-64

Disassembly of section .text:

0000000000401000 :
```text
401000:	48 b8 01 00 00 00 00 movabs $0x1,%rax
401007:	00 00 00
40100a:	48 bf 01 00 00 00 00 movabs $0x1,%rdi
401011:	00 00 00
401014:	48 be 00 20 40 00 00 movabs $0x402000,%rsi
40101b:	00 00 00
40101e:	48 ba 22 00 00 00 00 movabs $0x22,%rdx
401025:	00 00 00
401028:	0f 05 syscall
40102a:	48 b8 3c 00 00 00 00 movabs $0x3c,%rax
401031:	00 00 00
401034:	48 bf 0b 00 00 00 00 movabs $0xb,%rdi
40103b:	00 00 00
40103e:	0f 05 syscall
```

We can see from the above objdump that the linker has filled in the proper address for the string hello_world. Notice also that the memory address of the string hello_world contains nulls, making these opcodes not shellcode friendly.

There are techniques for removing nulls in memory address calls. One such technique is the JMP-CALL-POP technique, which we will see in later sections.
