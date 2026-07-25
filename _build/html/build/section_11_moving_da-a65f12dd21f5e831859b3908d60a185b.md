---
title: Section 11 - Moving Data
---

*Built with Grok Build*

## Introduction

In this section we will be continuing our progress on completing course material from the Pentester Academy's SecurityTube Linux Assembly language Expert 64 Bit course. The current topic is the movement of data in a 64 Bit environment. A segment of assembly code is used to demonstrate the various methods and ways that data can be moved from memory to registers, registers to memory, registers to registers and memory to memory.

The demonstration program is assembled, linked and run. Execution is then to be monitored via GDB. We will use the GEF add-on for GDB to enhance the visual presentation from GDB.

Project code is contained in my [GitHub repository](https://github.com/markkhusid/SLAE64).

## The program MovingData-64.nasm

The screenshot below displays the contents of the program MovingData-64.nasm. The program contains a series of various types of data movements. We will assemble, link, run and instruction step this program in GDB+GEF. At each step, we will provide a brief description.

```{figure} images/MovingData-64_nasm.jpg
:name: slae-s11-movingdata-64-nasm-1
:alt: MovingData-64 nasm
:align: center

MovingData-64 nasm
```

The program helloworld.asm

 The program is assembled with:

```bash
$ nasm -felf64 MovingData-64.nasm -o MovingData-64.o
```

 And linked with:

```bash
$ ld MovingData-64.o -o MovingData-64.o
```

We then use radare2 to look at the executable's objdump:

```{figure} images/radare_view_and_assembly_code2.jpg
:name: slae-s11-radare-view-and-assembly-code2-2
:alt: radare view and assembly code2
:align: center

radare view and assembly code2
```

Viewing the opcodes and disassebly of MovingData-64.nasm in radare2

 Running MovingData-64 in GDB + GEF

 Setup and before run

```{figure} images/setup_in_gdb.jpg
:name: slae-s11-setup-in-gdb-3
:alt: setup in gdb
:align: center

setup in gdb
```

MovingData-64 in GDB before run

 Casual observation of the contents of the program MovingData-64.nasm versus its disassebly in GDB+GEF shows a few minor differences. For example, mov opcodes in the assembly code are changed to movabs in the disassembly. Obviously, variable names are replaced with their appropriate memory addresses in the data segment.

## Running MovingData-64 in GDB + GEF

Running step 1

We begin by running the first instruction movabs rax, 0xaaaaaaaabbbbbbbb.

This instruction moves 0xaaaaaaaabbbbbbbb into RAX.

 Running step 1

 This instruction moves 0xaaaaaaaabbbbbbbb into RAX. We see the effects of this instruction in the next step.

### Running MovingData-64 in GDB + GEF

Running step 2

The effect of executing movabs rax, 0xaaaaaaaabbbbbbbb.

```{figure} images/gdb_step_2.jpg
:name: slae-s11-gdb-step-2-4
:alt: gdb step 2
:align: center

gdb step 2
```

Running step 2

We can see that after executing the instruction movabs rax, 0xaaaaaaaabbbbbbbb, we have the following effect on RAX:

`$rax : 0xaaaaaaaabbbbbbbb`

The next instruction to be executed is: mov eax, 0xaaaaaaaa.

This instruction moves the word 0xaaaaaaaa in EAX. EAX is the 32 bit portion of the 64 bit RAX; therefore, all of RAX will be wiped out and replaced with the 32 bit word 0xaaaaaaaa.

### Running MovingData-64 in GDB + GEF

Running step 3

Effect of executing mov eax, 0xaaaaaaaa

```{figure} images/gdb_step_3.jpg
:name: slae-s11-gdb-step-3-5
:alt: gdb step 3
:align: center

gdb step 3
```

Running step 3

We can see that after executing the instruction: mov eax, 0xaaaaaaaa, RAX was affected as shown below:

`$rax : 0xaaaaaaaa`

The next instruction to be executed is: movabs rax, 0xaaaaaaaabbbbbbbb

This instruction will have the same effect on RAX as described previously.

### Running MovingData-64 in GDB + GEF

Running step 4

Effect of executing movabs rax, 0xaaaaaaaabbbbbbbb

```{figure} images/gdb_step_4.jpg
:name: slae-s11-gdb-step-4-6
:alt: gdb step 4
:align: center

gdb step 4
```

Running step 4

After executing movabs rax, 0xaaaaaaaabbbbbbbb, RAX will be affected as follows:

`$rax : 0xaaaaaaaabbbbbbbb`

The next instruction to be executed is: mov al, 0x11. This instruction loads 0x11 into the lowest byte of RAX, known as AL. After this instruction executes, we can expect RAX to contain:

`$rax : 0xaaaaaaaabbbbbb11`

Notice that unlike when moving an immediate in to EAX, which wiped out the entire RAX with the immediate, moving into AL affects only the lowest byte of RAX.

### Running MovingData-64 in GDB + GEF

Running step 5

Effect of executing 0x401019 mov al, 0x11

```{figure} images/gdb_step_5.jpg
:name: slae-s11-gdb-step-5-7
:alt: gdb step 5
:align: center

gdb step 5
```

Running step 5

After executing 0x401019 mov al, 0x11, RAX will be affected as follows:

`$rax : 0xaaaaaaaabbbbbb11`

Notice that unlike when moving an immediate in to EAX, which wiped out the entire RAX with the immediate, moving into AL affects only the lowest byte of RAX.

The next instruction to be executed is: 0x40101b movabs rax, 0xaaaaaaaabbbbbbbb. This instruction loads 0xaaaaaaaabbbbbbbb into RAX. After this instruction executes, we can expect RAX to contain:

`$rax : 0xaaaaaaaabbbbbbbb`

### Running MovingData-64 in GDB + GEF

Running step 6

Effect of executing 0x40101b movabs rax, 0xaaaaaaaabbbbbbbb

```{figure} images/gdb_step_6.jpg
:name: slae-s11-gdb-step-6-8
:alt: gdb step 6
:align: center

gdb step 6
```

Running step 6

After executing 0x40101b movabs rax, 0xaaaaaaaabbbbbbbb, RAX will be affected as follows:

`$rax : 0xaaaaaaaabbbbbbbb`

As stated before, this instruction simply moves the immediate 0xaaaaaaaabbbbbbbb into RAX.

The next instruction to be executed is: 0x401025 mov ah, 0xcc. This instruction loads 0xcc into bits 8-15 of RAX. After this instruction executes, we can expect RAX to contain:

`$rax : 0xaaaaaaaabbbbccbb`

### Running MovingData-64 in GDB + GEF

Running step 7

Effect of executing 0x401025 mov ah, 0xcc

```{figure} images/gdb_step_7.jpg
:name: slae-s11-gdb-step-7-9
:alt: gdb step 7
:align: center

gdb step 7
```

Running step 7

After executing 0x401025 mov ah, 0xcc, RAX will be affected as follows:

`$rax : 0xaaaaaaaabbbbccbb`

This instruction loads 0xcc into bits 8 through 15 of AX. Notice that unlike moving into EAX, the rest of RAX was not modified.

The next instruction to be executed is: 0x401027 movabs rax, 0xaaaaaaaabbbbbbbb. This instruction loads 0xaaaaaaaabbbbbbbb into RAX. After this instruction executes, we can expect RAX to contain:

`$rax : 0xaaaaaaaabbbbbbbb`

### Running MovingData-64 in GDB + GEF

Running step 8

Effect of executing 0x401027 movabs rax, 0xaaaaaaaabbbbbbbb

```{figure} images/gdb_step_8.jpg
:name: slae-s11-gdb-step-8-10
:alt: gdb step 8
:align: center

gdb step 8
```

Running step 8

After executing 0x401027 movabs rax, 0xaaaaaaaabbbbbbbb, RAX will be affected as follows:

`$rax : 0xaaaaaaaabbbbbbbb`

This instruction loads 0xaaaaaaaabbbbbbbb into RAX.

The next instruction to be executed is: 0x401031 mov ax, 0xdddd. This instruction loads 0xdddd into bit 0 through 15 of RAX. After this instruction executes, we can expect RAX to contain:

`$rax : 0xaaaaaaaabbbbdddd`

### Running MovingData-64 in GDB + GEF

Running step 9

Effect of executing the instruction 0x401031 mov ax, 0xdddd

```{figure} images/gdb_step_9.jpg
:name: slae-s11-gdb-step-9-11
:alt: gdb step 9
:align: center

gdb step 9
```

Running step 9

After executing 0x401031 mov ax, 0xdddd, RAX will be affected as follows:

`$rax : 0xaaaaaaaabbbbdddd`

This instruction loads 0xdddd into AX. Notice that unlike loading EAX, the rest of RAX remains unmodified.

The next instruction to be executed is: 0x401035 mov rbp, rax. This instruction loads the contents of RAX into RBP. After this instruction executes, we can expect RBP to contain:

`$rbp : 0xaaaaaaaabbbbdddd`

### Running MovingData-64 in GDB + GEF

Running step 10

Effect of executing the instruction 0x401035 mov rbp, rax.

```{figure} images/gdb_step_10.jpg
:name: slae-s11-gdb-step-10-12
:alt: gdb step 10
:align: center

gdb step 10
```

Running step 10

After executing 0x401035 mov rbp, rax, RBP was affected as follows:

`$rbp : 0xaaaaaaaabbbbdddd`

This instruction loads the contents of RAX into RBP.

The next instruction to be executed is: 0x401038 mov r10, rbp. This instruction loads the contents of RBP into R10. After this instruction executes, we can expect R10 to contain:

 `$r10` : 0xaaaaaaaabbbbdddd

### Running MovingData-64 in GDB + GEF

Running step 11

Effect of executing 0x401038 mov r10, rbp

```{figure} images/gdb_step_11.jpg
:name: slae-s11-gdb-step-11-13
:alt: gdb step 11
:align: center

gdb step 11
```

Running step 11

 After executing 0x401038 mov r10, rbp, R10 was affected as follows:

 `$r10` : 0xaaaaaaaabbbbdddd

This instruction loads the contents of RBP into R10.

The next instruction to be executed is: 0x40103b mov r11d, r10d. This instruction loads bits 0 to 31 of R10 into bits 0 to 31 of R11. This is so because of the "d" suffixes after the register names. After this instruction executes, we can expect R11 to contain:

 `$r11` : 0xbbbbdddd

### Running MovingData-64 in GDB + GEF

Running step 12

Effect of executing 0x40103b mov r11d, r10d

```{figure} images/gdb_step_12.jpg
:name: slae-s11-gdb-step-12-14
:alt: gdb step 12
:align: center

gdb step 12
```

Running step 12

 After executing 0x40103b mov r11d, r10d, R11 was affected as follows:

 `$r11` : 0xbbbbdddd

This instruction loads bits 0 to 31 of R10 into bits 0 to 31 of R11.

The next instruction to be executed is: 0x40103e mov r12w, r11w. This instruction loads bits 0 to 15 of R11 into bits 0 to 15 of R12. This is so because of the "w" suffixes after the register names. After this instruction executes, we can expect R12 to contain:

 `$r12` : 0xdddd

### Running MovingData-64 in GDB + GEF

Running step 13

Effect of executing 0x40103e mov r12w, r11w

```{figure} images/gdb_step_13.jpg
:name: slae-s11-gdb-step-13-15
:alt: gdb step 13
:align: center

gdb step 13
```

Running step 13

 After executing 0x40103e mov r12w, r11w, R12 was affected as follows:

 `$r12` : 0xdddd

This instruction loads bits 0 to 15 of R11 into bits 0 to 15 of R12.

The next instruction to be executed is: 0x401042 mov r13b, r12b. This instruction loads bits 0 to 7 of R12 into bits 0 to 7 of R13. This is so because of the "b" suffixes after the register names. After this instruction executes, we can expect R13 to contain:

 `$r13` : 0xdd

### Running MovingData-64 in GDB + GEF

Running step 14

Effect of executing 0x401042 mov r13b, r12b

```{figure} images/gdb_step_14.jpg
:name: slae-s11-gdb-step-14-16
:alt: gdb step 14
:align: center

gdb step 14
```

Running step 14

 After executing 0x401042 mov r13b, r12b, R13 was affected as follows:

 `$r13` : 0xdd

This instruction loads bits 0 to 7 of R12 into bits 0 to 7 of R13.

The next instruction to be executed is: 0x401045 mov rsi, QWORD PTR ds:0x402008. This instruction loads the contents of memory at QWORD PTR ds:0x402008 into RSI. We examing the contents of memory at this location to obtain:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample2

 0x402008:	0x1122334455667788

 gef➤

```text
After executing this instruction, we expect RSI to contain:

`$rsi : 0x1122334455667788`
```

### Running MovingData-64 in GDB + GEF

Running step 15

Effect of executing 0x401045 mov rsi, QWORD PTR ds:0x402008

```{figure} images/gdb_step_15.jpg
:name: slae-s11-gdb-step-15-17
:alt: gdb step 15
:align: center

gdb step 15
```

Running step 15

After executing 0x401045 mov rsi, QWORD PTR ds:0x402008, RSI was affected as follows:

`$rsi : 0x1122334455667788`

This instruction loads the contents of memory at QWORD PTR ds:0x402008 into RSI.

The next instruction to be executed is: 0x40104d mov r14d, DWORD PTR ds:0x402000. This instruction loads bits 0 to 31 of the contents of memory at QWORD PTR ds:0x402000 into R14. We examing the contents of memory at this location to obtain:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbbaa

 gef➤

Recall that in the code, the variables were defined as follows:

 section .data

 sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22

 sample2: dq 0x1122334455667788

 sample3: times 8 db 0x00

samples was defined as 0xaabbccddeeff1122 in the code, but was stored as 0x2211ffeeddccbbaa because of little-endianess.

After executing this instruction, we expect R14 to contain:

 `$r14` : 0xddccbbaa

### Running MovingData-64 in GDB + GEF

Running step 16

Effect of executing 0x40104d mov r14d, DWORD PTR ds:0x402000

```{figure} images/gdb_step_16.jpg
:name: slae-s11-gdb-step-16-18
:alt: gdb step 16
:align: center

gdb step 16
```

Running step 16

 After executing 0x40104d mov r14d, DWORD PTR ds:0x402000, R14 was affected as follows:

 `$r14` : 0xddccbbaa

This instruction loads a double word (32 bits) of memory at DWORD PTR ds:0x402000 into R14. We saw in the previous section that the contents of memory location DWORD PTR ds:0x402000 contains:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbbaa

 gef➤

Therefore, loading the first 32 bits at that location would result in R14 containing:

 `$r14` : 0xddccbbaa

The next instruction to be executed is: 0x401055 mov r15w, WORD PTR ds:0x402000. This instruction loads bits 0 to 16 of the contents of memory at WORD PTR ds:0x402000 into R15. We examing the contents of memory at this location to obtain:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbbaa

 gef➤

Recall that in the code, the variables were defined as follows:

 section .data

 sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22

 sample2: dq 0x1122334455667788

 sample3: times 8 db 0x00

samples was defined as 0xaabbccddeeff1122 in the code, but was stored as 0x2211ffeeddccbbaa because of little-endianess.

After executing this instruction, we expect R15 to contain:

 `$r15` : 0xbbaa

 because only the first 16 bits were loaded from memory at location WORD PTR ds:0x402000 into R15.

### Running MovingData-64 in GDB + GEF

Running step 17

Effect of executing 0x401055 mov r15w, WORD PTR ds:0x402000

```{figure} images/gdb_step_17.jpg
:name: slae-s11-gdb-step-17-19
:alt: gdb step 17
:align: center

gdb step 17
```

Running step 17

 After executing x401055 mov r15w, WORD PTR ds:0x402000, R15 was affected as follows:

 `$r15` : 0xbbaa

This instruction loads a word (16 bits) of memory at WORD PTR ds:0x402000 into R15. We saw in the previous section that the contents of memory location WORD PTR ds:0x402000 contains:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbbaa

 gef➤

Therefore, loading the first 16 bits at that location would result in R15 containing:

 `$r15` : 0xbbaa

The next instruction to be executed is: 0x40105e mov dil, BYTE PTR ds:0x402000. This instruction loads bits 0 to 8 of the contents of memory at WORD PTR ds:0x402000 into bits 0 to 7 of RDI. We examing the contents of memory at this location to obtain:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbbaa

 gef➤

Recall that in the code, the variables were defined as follows:

 section .data

 sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22

 sample2: dq 0x1122334455667788

 sample3: times 8 db 0x00

samples was defined as 0xaabbccddeeff1122 in the code, but was stored as 0x2211ffeeddccbbaa because of little-endianess.

After executing this instruction, we expect RDI to contain:

`$rdi : 0xaa`

because only the first 8 bits were loaded from memory at location WORD PTR ds:0x402000 into RDI.

### Running MovingData-64 in GDB + GEF

Running step 18

Effect of executing 0x40105e mov dil, BYTE PTR ds:0x402000

```{figure} images/gdb_step_18.jpg
:name: slae-s11-gdb-step-18-20
:alt: gdb step 18
:align: center

gdb step 18
```

Running step 18

After executing 0x40105e mov dil, BYTE PTR ds:0x402000, RDI was affected as follows:

`$rdi : 0xaa`

This instruction loads a byte (8 bits) of memory at WORD PTR ds:0x402000 into RDI. We saw in the previous section that the contents of memory location WORD PTR ds:0x402000 contains:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbbaa

 gef➤

```text
Therefore, loading the first 16 bits at that location would result in R15 containing:

`$rdi : 0xaa`
```

The next instruction to be executed is: 0x401066 mov rax, QWORD PTR ds:0x402008. This instruction loads bits 0 to 63 of the contents of memory at QWORD PTR ds:0x402008 into bits 0 to 63 of RAX. We examing the contents of memory at this location to obtain:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample2

 0x402008:	0x1122334455667788

 gef➤

Recall that in the code, the variables were defined as follows:

 section .data

 sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22

 sample2: dq 0x1122334455667788

 sample3: times 8 db 0x00

sample2 was defined as sample2: dq 0x1122334455667788 in the code, and that is the way it was stored in memory. Therefore, when defining a quad word immediate, the way it was defined is the way it is stored in memory in terms of endianess.

After executing this instruction, we expect RAX to contain:

`$rax : 0x1122334455667788`

because bits 0 to 63 were loaded from memory at location QWORD PTR ds:0x402008 into RAX.

### Running MovingData-64 in GDB + GEF

Running step 19

Effect of executing 0x401066 mov rax, QWORD PTR ds:0x402008

```{figure} images/gdb_step_19.jpg
:name: slae-s11-gdb-step-19-21
:alt: gdb step 19
:align: center

gdb step 19
```

Running step 19

After executing 0x401066 mov rax, QWORD PTR ds:0x402008, RAX was affected as follows:

`$rax : 0x1122334455667788`

This instruction loads a quad word (64 bits) of memory at QWORD PTR ds:0x402008 into RAX. We saw in the previous section that the contents of memory location WORD PTR ds:0x402008 contains:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample2

 0x402008:	0x1122334455667788

 gef➤

```text
Therefore, loading 64 bits at that location would result in RAX containing:

`$rax : 0x1122334455667788`
```

The next instruction to be executed is: 0x40106e mov BYTE PTR ds:0x402000, al. This instruction loads bits 0 to 7 of the contents of RAX into memory at BYTE PTR ds:0x402000. We examing the contents of memory at this location to obtain:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbbaa

 gef➤

Recall that in the code, the variables were defined as follows:

 section .data

 sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22

 sample2: dq 0x1122334455667788

 sample3: times 8 db 0x00

sample was defined as sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22 in the code, but it is stored in memory as: 0x2211ffeeddccbbaa due to little-endianess.

```text
Recall that RAX contains:

`$rax : 0x1122334455667788`
```

Before executing this instruction, memory at BYTE PTR ds:0x402000 contains:

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbbaa

 gef➤

After executing this instruction, we expect memory at BYTE PTR ds:0x402000 to contain:

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbb88

 gef➤

### Running MovingData-64 in GDB + GEF

Running step 20

Effect of executing 0x40106e mov BYTE PTR ds:0x402000, al

```{figure} images/gdb_step_20.jpg
:name: slae-s11-gdb-step-20-22
:alt: gdb step 20
:align: center

gdb step 20
```

Running step 20

 After executing:

 0x40106e mov BYTE PTR ds:0x402000, al

 the memory at BYTE PTR ds:0x402000 was affected as follows:

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbb88

 gef➤

This instruction loads the lower byte (8 bits) of RAX into the location memory at BYTE PTR ds:0x402000. We saw in the previous section that the contents of memory location WORD PTR ds:0x402000 contains:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbbaa

 gef➤

Therefore, loading the lower 8 bits of RAX into that location would result in the location containing:

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbb88

 gef➤

The next instruction to be executed is: 0x401075 mov WORD PTR ds:0x402000, ax. This instruction loads bits 0 to 15 of the contents of RAX into memory at WORD PTR ds:0x402000. We examing the contents of memory at this location to obtain:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbb88

 gef➤

Recall that in the code, the variables were defined as follows:

 section .data

 sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22

 sample2: dq 0x1122334455667788

 sample3: times 8 db 0x00

sample was defined as sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22 in the code, but it is stored in memory as: 0x2211ffeeddccbbaa due to little-endianess.

```text
Recall that RAX contains:

`$rax : 0x1122334455667788`
```

Before executing this instruction, memory at WORD PTR ds:0x402000 contains:

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbb88

 gef➤

After executing this instruction, we expect memory at WORD PTR ds:0x402000 to contain:

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddcc7788

 gef➤

### Running MovingData-64 in GDB + GEF

Running step 21

Effect of executing 0x401075 mov WORD PTR ds:0x402000, ax

```{figure} images/gdb_step_21.jpg
:name: slae-s11-gdb-step-21-23
:alt: gdb step 21
:align: center

gdb step 21
```

Running step 21

 After executing:

 0x401075 mov WORD PTR ds:0x402000, ax

 the memory at WORD PTR ds:0x402000 was affected as follows:

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddcc7788

 gef➤

This instruction loads the lower word (16 bits) of RAX into the location memory at WORD PTR ds:0x402000. We saw in the previous section that the contents of memory location WORD PTR ds:0x402000 contains:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddccbb88

 gef➤

Therefore, loading the lower 16 bits of RAX into that location would result in the location containing:

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddcc7788

 gef➤

The next instruction to be executed is: 0x40107d mov DWORD PTR ds:0x402000, eax. This instruction loads bits 0 to 31 of the contents of RAX into memory at DWORD PTR ds:0x402000. We examing the contents of memory at this location to obtain:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddcc7788

 gef➤

Recall that in the code, the variables were defined as follows:

 section .data

 sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22

 sample2: dq 0x1122334455667788

 sample3: times 8 db 0x00

sample was defined as sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22 in the code, but it is stored in memory as: 0x2211ffeeddccbbaa due to little-endianess.

```text
Recall that RAX contains:

`$rax : 0x1122334455667788`
```

Before executing this instruction, memory at WORD PTR ds:0x402000 contains:

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddcc7788

 gef➤

After executing this instruction, we expect memory at WORD PTR ds:0x402000 to contain:

 gef➤ x/xg &sample

 0x402000:	0x2211ffee55667788

 gef➤

### Running MovingData-64 in GDB + GEF

Running step 22

Effect of executing 0x40107d mov DWORD PTR ds:0x402000, eax

```{figure} images/gdb_step_22.jpg
:name: slae-s11-gdb-step-22-24
:alt: gdb step 22
:align: center

gdb step 22
```

Running step 22

 After executing:

 0x40107d mov DWORD PTR ds:0x402000, eax

 the memory at DWORD PTR ds:0x402000 was affected as follows:

 gef➤ x/xg &sample

 0x402000:	0x2211ffee55667788

 gef➤

This instruction loads the lower double-word (32 bits) of RAX into the location memory at DWORD PTR ds:0x402000. We saw in the previous section that the contents of memory location DWORD PTR ds:0x402000 contains:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffeeddcc7788

 gef➤

Therefore, loading the lower 32 bits of RAX into that location would result in the location containing:

 gef➤ x/xg &sample

 0x402000:	0x2211ffee55667788

 gef➤

The next instruction to be executed is: 0x401084 mov QWORD PTR ds:0x402000, rax. This instruction loads bits 0 to 63 of the contents of RAX into memory at QWORD PTR ds:0x402000. We examing the contents of memory at this location to obtain:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffee55667788

 gef➤

Recall that in the code, the variables were defined as follows:

 section .data

 sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22

 sample2: dq 0x1122334455667788

 sample3: times 8 db 0x00

sample was defined as sample: db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22 in the code, but it is stored in memory as: 0x2211ffeeddccbbaa due to little-endianess.

```text
Recall that RAX contains:

`$rax : 0x1122334455667788`
```

Before executing this instruction, memory at WORD PTR ds:0x402000 contains:

 gef➤ x/xg &sample

 0x402000:	0x2211ffee55667788

 gef➤

After executing this instruction, we expect memory at WORD PTR ds:0x402000 to contain:

 gef➤ x/xg &sample

 0x402000:	0x1122334455667788

 gef➤

### Running MovingData-64 in GDB + GEF

Running step 23

Effect of executing 0x401084 mov QWORD PTR ds:0x402000, rax

```{figure} images/gdb_step_23.jpg
:name: slae-s11-gdb-step-23-25
:alt: gdb step 23
:align: center

gdb step 23
```

Running step 23

 After executing:

 0x401084 mov QWORD PTR ds:0x402000, rax

 the memory at QWORD PTR ds:0x402000 was affected as follows:

 gef➤ x/xg &sample

 0x402000:	0x1122334455667788

 gef➤

This instruction loads the full quad-word (64 bits) of RAX into the location memory at QWORD PTR ds:0x402000. We saw in the previous section that the contents of memory location QWORD PTR ds:0x402000 contains:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x2211ffee55667788

 gef➤

Therefore, loading the contents of RAX into that location would result in the location containing:

 gef➤ x/xg &sample

 0x402000:	0x1122334455667788

 gef➤

The next instruction to be executed is: 0x40108c lea rax, ds:0x402000. This instruction loads the effective address of the memory location ds:0x402000 into RAX. We examing the contents of memory at this location to obtain:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

 gef➤ x/xg &sample

 0x402000:	0x1122334455667788

 gef➤

Therefore, the address of ds:0x402000 is 0x0000000000402000, and this is what will be loaded into RAX

```text
Before executing this instruction, RAX contains:

`$rax : 0x1122334455667788`
```

```text
After executing this instruction, we expect RAX to contain:

`$rax : 0x0000000000402000`
```

### Running MovingData-64 in GDB + GEF

Running step 24

Effect of executing 0x40108c lea rax, ds:0x402000

```{figure} images/gdb_step_24.jpg
:name: slae-s11-gdb-step-24-26
:alt: gdb step 24
:align: center

gdb step 24
```

Running step 24

 After executing:

 0x40108c lea rax, ds:0x402000

 RAX is loaded with the memory address ds:0x402000.

We saw in the previous section that the defined variables were:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

```text
Therefore, loading the memory address of ds:0x402000 into RAX would result in RAX containing:

`$rax : 0x0000000000402000`
```

The next instruction to be executed is: 0x401094 lea rbx, [rax]. This instruction loads the effective address of what RAX points to, as indicated by the square brackets, into RBX. We examing the contents of RAX to obtain:

 `gef➤ x/xg $rax`

 0x402000:	0x1122334455667788

 and we examine the contents of RBX to obtain:

 gef➤ print `$rbx`

 \$1 = 0x0

Therefore RAX contains 0x402000, and when treated as a memory location, the contents of RAX points memory at 0x402000 which contains the value 0x1122334455667788. The address 0x402000 will be loaded into RBX.

```text
Before executing this instruction, RBX contains:

`$rbx : 0x0`
```

```text
After executing this instruction, we expect RBX to contain:

`$rbx : 0x0000000000402000`
```

### Running MovingData-64 in GDB + GEF

Running step 25

Effect of executing 0x401094 lea rbx, [rax]

```{figure} images/gdb_step_25.jpg
:name: slae-s11-gdb-step-25-27
:alt: gdb step 25
:align: center

gdb step 25
```

Running step 25

 After executing:

 0x401094 lea rbx, [rax]

 RBX is loaded with the memory address ds:0x402000.

We saw in the previous section that the defined variables were:

 gef➤ info variables

 All defined variables:

 Non-debugging symbols:

 0x0000000000402000 sample

 0x0000000000402008 sample2

 0x0000000000402010 sample3Mbr>
 0x0000000000402018 __bss_start

 0x0000000000402018 _edata

 0x0000000000402018 _end

```text
Therefore, loading the effective address of what RAX points to would result in RBX containing:

`$rbx : 0x0000000000402000`
```

The next instruction to be executed is: 0x401097 movabs rax, 0x1234567890abcdef. This instruction simply loads the immediate 0x1234567890abcdef into RAX.

We examine the contents of RAX to obtain:

`$rax : 0x0000000000402000`

```text
After executing this instruction, we expect RAX to contain:

`$rax : 0x1234567890abcdef`
```

### Running MovingData-64 in GDB + GEF

Running step 26

Effect of executing 0x401097 movabs rax, 0x1234567890abcdef

```{figure} images/gdb_step_26.jpg
:name: slae-s11-gdb-step-26-28
:alt: gdb step 26
:align: center

gdb step 26
```

Running step 26

 After executing:

 0x401097 movabs rax, 0x1234567890abcdef

 RAX is loaded with the immediate 0x1234567890abcdef.

The next instruction to be executed is: 0x4010a1 movabs rbx, 0x9999999999999999. This instruction simply loads the immediate 0x9999999999999999 into RBX.

We examing the contents of RBX to obtain:

`$rbx : 0x0000000000402000`

```text
After executing this instruction, we expect RBX to contain:

`$rbx : 0x9999999999999999`
```

### Running MovingData-64 in GDB + GEF

Running step 27

Effect of executing 0x4010a1 movabs rbx, 0x9999999999999999

```{figure} images/gdb_step_27.jpg
:name: slae-s11-gdb-step-27-29
:alt: gdb step 27
:align: center

gdb step 27
```

Running step 27

 After executing:

 0x4010a1 movabs rbx, 0x9999999999999999

 RBX is loaded with the immediate 0x9999999999999999.

The next instruction to be executed is: 0x4010ab xchg rbx, rax. This instruction exchanges the contents of RAX with the contents of RBX. It is an interesting question of whether the CPU has an intermediate location to store the contents of the registers as it exchanges them.

 We examine the contents of RAX to obtain:

 `$rax` : 0x1234567890abcdef

 and we examine the contents of RBX to obtain:

 `$rbx` : 0x9999999999999999

```text
After executing this instruction, we expect RAX to contain:

`$rax : 0x9999999999999999`
```

```text
And RBX to contain:

`$rbx : 0x1234567890abcdef`
```

### Running MovingData-64 in GDB + GEF

Running step 28

Effect of executing 0x4010ab xchg rbx, rax

```{figure} images/gdb_step_28.jpg
:name: slae-s11-gdb-step-28-30
:alt: gdb step 28
:align: center

gdb step 28
```

Running step 28

 After executing:

 0x4010ab xchg rbx, rax

 The contents of RAX is exchanged with the contents of RBX.

The next instruction to be executed is: 0x4010ad mov eax, 0x3c. This instruction simply loads the immediate 0x3c into EAX. This in preparation to exit gracefully back to the shell. 0x3c is the number of the system call to execute an exit.

We examine the contents of RAX to obtain:

`$rax : 0x9999999999999999`

```text
After executing this instruction, we expect RAX to contain:

`$rax : 0x3c`
```

### Running MovingData-64 in GDB + GEF

Running step 29

Effect of executing 0x4010ad mov eax, 0x3c

```{figure} images/gdb_step_29.jpg
:name: slae-s11-gdb-step-29-31
:alt: gdb step 29
:align: center

gdb step 29
```

Running step 29

 After executing:

 0x4010ad mov eax, 0x3c

 The contents of RAX is loaded with the immediate 0x3c.

The next instruction to be executed is: 4010b2 mov edi, 0x0. This instruction simply loads the immediate 0x0c into RDI. This in preparation to exit gracefully back to the shell. The 0x0 represents the exit status of the program.

We examine the contents of RDI to obtain:

`$rdi : 0xaa`

```text
After executing this instruction, we expect RDI to contain:

`$rdi : 0x0`
```

### Running MovingData-64 in GDB + GEF

Running step 30

Effect of executing 4010b2 mov edi, 0x0

```{figure} images/gdb_step_30.jpg
:name: slae-s11-gdb-step-30-32
:alt: gdb step 30
:align: center

gdb step 30
```

Running step 30

 After executing:

 4010b2 mov edi, 0x0

 The contents of EDI is loaded with the immediate 0x0.

The next instruction to be executed is: 0x4010b7 syscall. This instruction calls the system to execute a system call with number in RAX and parameters in RDI.

We examine the contents of RAX to obtain:

`$rax : 0x3c`

```text
We examine the contents of RDI to obtain:

`$rdi : 0x0`
```

After executing this instruction, we expect the program to exit with status 0.

### Running MovingData-64 in GDB + GEF

Running step 31

Effect of executing 0x4010b7 syscall.

```{figure} images/gdb_step_31.jpg
:name: slae-s11-gdb-step-31-33
:alt: gdb step 31
:align: center

gdb step 31
```

Running step 31

 After executing:

 0x4010b7 syscall

 The program exits gracefully with exit status 0.
