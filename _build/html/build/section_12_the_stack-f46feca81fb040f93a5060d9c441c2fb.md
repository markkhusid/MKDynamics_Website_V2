---
title: Section 12 - The Stack
---

*Built with Grok Build*

## Introduction

In this section we will be following along with and completing course material from the Pentester Academy's SecurityTube Linux Assembly language Expert 64 Bit course. As the title suggests, this assignment deals with the stack. The stack is a Last In First Out (LIFO) data structure. It is used extensively in high level programming languages, such as C.

The stack is manipulated with the Push and Pop operations. The pointer to the top of the stack in 64 bit Intel based machines is called RSP. The stack grows from high memory to low memory.

We will write an assembly program that manipulates the stack in 64 bit Intel assembly instructions. This program will be coded, assembled, linked and run. Execution is then to be monitored via GDB. We will use the GEF add-on for GDB to enhance the visual presentation from GDB. We will also use Radare2 to run through the program execution to gain another perspective.

Project code is contained in my [GitHub repository](https://github.com/markkhusid/SLAE64).

## The program stack.nasm

The screenshot below displays the contents of the program stack.nasm.

```{figure} images/stack_nasm.jpg
:name: slae-s12-stack-nasm-1
:alt: stack nasm
:align: center

stack nasm
```

The program stack.nasm

 The program pushes an immediate onto the stack. The immediate is: 0x1122334455667788. It does this by first moving the immediate into RAX and then pushing RAX.

Next it pushes data labled by sample. As shown in the program, this data is:

 sample:	db 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x11, 0x22

First sample is pushed. What this does it push the memory address of sample onto the stack. Then the contents of the memory address labled as sample is pushed onto the stack, as denoted by the brackets (i.e. []) around the label.

Then the contents of the stack is popped off into R15, R14 and RBX. The first item pushed onto the stack is the last item to come out. Therefore, RBX will contain the contents of RAX.

Finally, the familiar exit syscall is executed to gracefully exit back to the shell.

The program is assembled with:

```bash
$ nasm -felf64 stack.nasm -o stack.o
```

 And linked with:

```bash
$ ld stack.o -o stack
```

We then run the executable and look at it's objdump. The results of these operations is shown below:

```{figure} images/assembling_linking_and_objdump_of_stack_c.jpg
:name: slae-s12-assembling-linking-and-objdump-of-stack-c-2
:alt: assembling linking and objdump of stack c
:align: center

assembling linking and objdump of stack c
```

Assembling, Linking and Executing the Program stack.nasm

 Running stack in GDB + GEF

 Setup and before run

```{figure} images/setup_GDB.jpg
:name: slae-s12-setup-gdb-3
:alt: setup GDB
:align: center

setup GDB
```

helloworld in GDB before run

 Running helloworld in GDB + GEF

 Running step 1

```{figure} images/step_1.jpg
:name: slae-s12-step-1-4
:alt: step 1
:align: center

step 1
```

Running step 1

 Running helloworld in GDB + GEF

 Running step 2

```{figure} images/step_2.jpg
:name: slae-s12-step-2-5
:alt: step 2
:align: center

step 2
```

Running step 2

 Running helloworld in GDB + GEF

 Running step 3

```{figure} images/step_3.jpg
:name: slae-s12-step-3-6
:alt: step 3
:align: center

step 3
```

Running step 3

 Running helloworld in GDB + GEF

 Running step 4

```{figure} images/step_4.jpg
:name: slae-s12-step-4-7
:alt: step 4
:align: center

step 4
```

Running step 4

 Running helloworld in GDB + GEF

 Running step 5

```{figure} images/step_5.jpg
:name: slae-s12-step-5-8
:alt: step 5
:align: center

step 5
```

Running step 5

 Running helloworld in GDB + GEF

 Running step 6

```{figure} images/step_6.jpg
:name: slae-s12-step-6-9
:alt: step 6
:align: center

step 6
```

Running step 6

 Running helloworld in GDB + GEF

 Running step 7

```{figure} images/step_7.jpg
:name: slae-s12-step-7-10
:alt: step 7
:align: center

step 7
```

Running step 7

 Running helloworld in GDB + GEF

 Running step 8

```{figure} images/step_8.jpg
:name: slae-s12-step-8-11
:alt: step 8
:align: center

step 8
```

Running step 8

 Running helloworld in GDB + GEF

 Examining Memory

```{figure} images/step_9.jpg
:name: slae-s12-step-9-12
:alt: step 9
:align: center

step 9
```

Examining Memory

 Running helloworld in GDB + GEF

 Examining Memory

```{figure} images/step_10.jpg
:name: slae-s12-step-10-13
:alt: step 10
:align: center

step 10
```

Examining Memory

 Running helloworld in GDB + GEF

 Examining Memory

```{figure} images/step_11.jpg
:name: slae-s12-step-11-14
:alt: step 11
:align: center

step 11
```
