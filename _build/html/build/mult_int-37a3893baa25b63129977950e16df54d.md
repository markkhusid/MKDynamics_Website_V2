# Multiplying Integers: i386

```{image} images/mult_int_C_i386_splash.png
:height: 500
:width: 800
```

## Introduction
In this section we will examine the disassembly of a simple C program that multiplies two integers. The program is compiled for the i386 architecture, which is a 32-bit architecture commonly used in older computers and embedded systems. The disassembly will help us understand how the C code translates into assembly instructions, and how these instructions are executed by the CPU.

## The C Program
```{literalinclude} code/mult_int.c
```

## Compilation of the C Program to Produce Assembly Code and Object Code
The C program is compiled using the GCC compiler with the `-m32` flag to specify the i386 architecture. The `-masm=intel` flag creates assembly code in the Intel format. The `-S` flag generates assembly code, the `-fverbose-asm` flag includes C source code in the assembly code, and the `-c` flag compiles the assembly code into an object file.

```bash
gcc --sysroot=/ -m32 -masm=intel -S -fverbose-asm mult_int.c -o mult_int.s
gcc --sysroot=/ -m32 -c mult_int.s -o mult_int.o
```

## Viewing the Assembly Code
The assembly code is in Intel syntax, which is commonly used for x86 assembly language.

```{literalinclude} code/mult_int.s
```

## Explanation of the Assembly Code
The attached code is an assembly file (`mult_int.s`) generated from a simple C program (`mult_int.c`) that performs integer multiplication. It is written in Intel syntax and compiled for a 32-bit architecture (`-m32`) using GCC 14.2.0. Below is a detailed explanation of the code:

---

### **Header Information**
```asm
.file	"mult_int.c"
	.intel_syntax noprefix
```
- `.file "mult_int.c"`: Indicates that this assembly code was generated from the C source file `mult_int.c`.
- `.intel_syntax noprefix`: Specifies that the assembly code uses Intel syntax (as opposed to AT&T syntax).

---

### **Global and Function Declarations**
```asm
	.text
	.globl	main
	.type	main, @function
```
- `.text`: Marks the beginning of the code (text) section where executable instructions are stored.
- `.globl main`: Declares the `main` function as global, making it accessible to the linker.
- `.type main, @function`: Specifies that `main` is a function.

---

### **Main Function**
```asm
main:
.LFB0:
	.cfi_startproc
```
- `main:`: The label for the `main` function.
- `.LFB0:`: A local label used internally by the assembler for debugging purposes.
- `.cfi_startproc`: Marks the start of the Call Frame Information (CFI) for the function, used for stack unwinding during debugging.

---

#### **Prologue**
```asm
	push	ebp	#
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	mov	ebp, esp	#,
	.cfi_def_cfa_register 5
	sub	esp, 16	#,
```
- `push ebp`: Saves the base pointer (`ebp`) of the previous stack frame onto the stack.
- `mov ebp, esp`: Sets the current base pointer (`ebp`) to the value of the stack pointer (`esp`), establishing a new stack frame.
- `sub esp, 16`: Allocates 16 bytes of space on the stack for local variables.

---

#### **Global Offset Table Setup**
```asm
	call	__x86.get_pc_thunk.ax	#
	add	eax, OFFSET FLAT:_GLOBAL_OFFSET_TABLE_	# tmp98,
```
- `call __x86.get_pc_thunk.ax`: Calls a helper function to get the program counter (PC) value.
- `add eax, OFFSET FLAT:_GLOBAL_OFFSET_TABLE_`: Adjusts the PC value to point to the Global Offset Table (GOT), which is used for position-independent code.

---

#### **Variable Initialization**
```asm
# mult_int.c:7: 	a = 2;
	mov	DWORD PTR -4[ebp], 2	# a,
# mult_int.c:8: 	b = 3;
	mov	DWORD PTR -8[ebp], 3	# b,
```
- `mov DWORD PTR -4[ebp], 2`: Stores the value `2` in the memory location `-4[ebp]`, which corresponds to the variable `a`.
- `mov DWORD PTR -8[ebp], 3`: Stores the value `3` in the memory location `-8[ebp]`, which corresponds to the variable `b`.

---

#### **Multiplication**
```asm
# mult_int.c:10: 	c = a * b;
	mov	eax, DWORD PTR -4[ebp]	# tmp102, a
	imul	eax, DWORD PTR -8[ebp]	# c_3, b
	mov	DWORD PTR -12[ebp], eax	# c, c_3
```
- `mov eax, DWORD PTR -4[ebp]`: Loads the value of `a` into the `eax` register.
- `imul eax, DWORD PTR -8[ebp]`: Multiplies the value in `eax` (i.e., `a`) by the value of `b` (stored at `-8[ebp]`), storing the result in `eax`.
- `mov DWORD PTR -12[ebp], eax`: Stores the result of the multiplication (`c`) in the memory location `-12[ebp]`.

---

#### **Return Value**
```asm
	mov	eax, 0	# _4,
```
- `mov eax, 0`: Sets the return value of the `main` function to `0` (standard convention for successful execution).

---

#### **Epilogue**
```asm
	leave	
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret	
	.cfi_endproc
```
- `leave`: Restores the previous stack frame by setting `esp` to `ebp` and popping the old `ebp` value from the stack.
- `ret`: Returns control to the caller.

---

### **Helper Function: `__x86.get_pc_thunk.ax`**
```asm
	.section	.text.__x86.get_pc_thunk.ax,"axG",@progbits,__x86.get_pc_thunk.ax,comdat
	.globl	__x86.get_pc_thunk.ax
	.hidden	__x86.get_pc_thunk.ax
	.type	__x86.get_pc_thunk.ax, @function
__x86.get_pc_thunk.ax:
.LFB1:
	.cfi_startproc
	mov	eax, DWORD PTR [esp]	#,
	ret
	.cfi_endproc
```
- This function retrieves the program counter (PC) value and stores it in the `eax` register. It is used for position-independent code to calculate addresses relative to the GOT.

---

### **Footer**
```asm
	.ident	"GCC: (conda-forge gcc 14.2.0-2) 14.2.0"
	.section	.note.GNU-stack,"",@progbits
```
- `.ident`: Contains metadata about the compiler version used.
- `.section .note.GNU-stack`: Marks the stack as non-executable for security purposes.

---

### **Summary**
This assembly code implements a simple C program that multiplies two integers (`a = 2` and `b = 3`) and stores the result in a variable (`c`). The `main` function sets up the stack frame, performs the multiplication using the `imul` instruction, and returns `0` as the exit status. The helper function `__x86.get_pc_thunk.ax` is used for position-independent code.

## Compilation to Produce Executable Code
The object file is linked to create an executable file using the `-o` flag.

```bash
/usr/bin/gcc -m32 mult_int.o -o mult_int_C_i386
```

## Disassembly of the Executable Code
The executable file is disassembled using the `objdump` command with the `-d` flag to display the disassembly.

```bash
objdump -x -D -s -t -Mintel mult_int.o > objdump_of_dot_o.txt
objdump -x -D -s -t -Mintel mult_int_C_i386 > objdump_of_dot_exe.txt
```

### Explanation of the Switches used in the `objdump` command:
- `-x`: Displays all headers.
- `-D`: Disassembles all sections.
- `-s`: Displays the full contents of all sections.
- `-t`: Displays the symbol table.
- `-Mintel`: Specifies Intel syntax for disassembly.

## Viewing the Object File Disassembly
```{literalinclude} code/objdump_of_dot_o.txt
```

## Explanation the Object File Disassembly
The attached file is the output of the `objdump` command applied to an object file (`mult_int.o`). It provides a detailed view of the binary structure, including sections, symbols, and disassembled machine code. Below is a detailed explanation of the key parts of the file:

---

### **File Metadata**
```objdump
mult_int.o:     file format elf32-i386
architecture: i386, flags 0x00000011:
HAS_RELOC, HAS_SYMS
start address 0x00000000
```
- **File format**: The object file is in the ELF (Executable and Linkable Format) for a 32-bit Intel architecture (`elf32-i386`).
- **Architecture**: The code is compiled for the i386 architecture (32-bit x86).
- **Flags**:
  - `HAS_RELOC`: The file contains relocation entries, which are used to adjust addresses during linking.
  - `HAS_SYMS`: The file contains a symbol table.
- **Start address**: The entry point of the object file is at address `0x00000000`.

---

### **Sections**
The object file is divided into sections, each serving a specific purpose. Below are the key sections:

#### **1. `.group`**
```objdump
Idx Name          Size      VMA       LMA       File off  Algn
  0 .group        00000008  00000000  00000000  00000034  2**2
                  CONTENTS, READONLY, GROUP, LINK_ONCE_DISCARD
```
- **Purpose**: Groups related sections for optimization and linking.
- **Attributes**:
  - `CONTENTS`: Contains data.
  - `READONLY`: Read-only section.
  - `GROUP`: Groups related sections.
  - `LINK_ONCE_DISCARD`: Ensures only one copy of the section is kept during linking.

#### **2. `.text`**
```objdump
  1 .text         0000002f  00000000  00000000  0000003c  2**0
                  CONTENTS, ALLOC, LOAD, RELOC, READONLY, CODE
```
- **Purpose**: Contains the executable code for the program.
- **Attributes**:
  - `CODE`: Contains machine instructions.
  - `READONLY`: Read-only section.
  - `RELOC`: Contains relocation entries for linking.

#### **3. `.data`**
```objdump
  2 .data         00000000  00000000  00000000  0000006b  2**0
                  CONTENTS, ALLOC, LOAD, DATA
```
- **Purpose**: Contains initialized global and static variables.
- **Attributes**:
  - `DATA`: Contains data.
  - `ALLOC`: Allocated in memory during execution.

#### **4. `.bss`**
```objdump
  3 .bss          00000000  00000000  00000000  0000006b  2**0
                  ALLOC
```
- **Purpose**: Contains uninitialized global and static variables.
- **Attributes**:
  - `ALLOC`: Allocated in memory during execution but not stored in the object file.

#### **5. `.text.__x86.get_pc_thunk.ax`**
```objdump
  4 .text.__x86.get_pc_thunk.ax 00000004  00000000  00000000  0000006b  2**0
                  CONTENTS, ALLOC, LOAD, READONLY, CODE
```
- **Purpose**: Contains the helper function `__x86.get_pc_thunk.ax`, used for position-independent code.
- **Attributes**:
  - `CODE`: Contains machine instructions.
  - `READONLY`: Read-only section.

#### **6. `.comment`**
```objdump
  5 .comment      00000028  00000000  00000000  0000006f  2**0
                  CONTENTS, READONLY
```
- **Purpose**: Contains metadata about the compiler and build environment.
- **Attributes**:
  - `READONLY`: Read-only section.

#### **7. `.note.gnu.property`**
```objdump
  7 .note.gnu.property 00000028  00000000  00000000  00000098  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
```
- **Purpose**: Contains properties for GNU tools, such as security features.
- **Attributes**:
  - `DATA`: Contains data.
  - `READONLY`: Read-only section.

#### **8. `.eh_frame`**
```objdump
  8 .eh_frame     0000004c  00000000  00000000  000000c0  2**2
                  CONTENTS, ALLOC, LOAD, RELOC, READONLY, DATA
```
- **Purpose**: Contains exception handling information for stack unwinding.
- **Attributes**:
  - `DATA`: Contains data.
  - `RELOC`: Contains relocation entries for linking.

---

### **Symbol Table**
```objdump
SYMBOL TABLE:
00000000 l    df *ABS*	00000000 mult_int.c
00000000 l    d  .text	00000000 .text
00000000 l    d  .text.__x86.get_pc_thunk.ax	00000000 .text.__x86.get_pc_thunk.ax
00000000 g     F .text	0000002f main
00000000 g     F .text.__x86.get_pc_thunk.ax	00000000 .hidden __x86.get_pc_thunk.ax
00000000         *UND*	00000000 _GLOBAL_OFFSET_TABLE_
```
- **Symbols**:
  - `main`: The main function, located in the `.text` section.
  - `__x86.get_pc_thunk.ax`: A helper function for position-independent code.
  - `_GLOBAL_OFFSET_TABLE_`: An undefined symbol used for dynamic linking.

---

### **Disassembly**

#### **1. `.text` Section**
```objdump
00000000 <main>:
   0:	55                   	push   ebp
   1:	89 e5                	mov    ebp,esp
   3:	83 ec 10             	sub    esp,0x10
   6:	e8 fc ff ff ff       	call   7 <main+0x7>
			7: R_386_PC32	__x86.get_pc_thunk.ax
   b:	05 01 00 00 00       	add    eax,0x1
			c: R_386_GOTPC	_GLOBAL_OFFSET_TABLE_
  10:	c7 45 fc 02 00 00 00 	mov    DWORD PTR [ebp-0x4],0x2
  17:	c7 45 f8 03 00 00 00 	mov    DWORD PTR [ebp-0x8],0x3
  1e:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  21:	0f af 45 f8          	imul   eax,DWORD PTR [ebp-0x8]
  25:	89 45 f4             	mov    DWORD PTR [ebp-0xc],eax
  28:	b8 00 00 00 00       	mov    eax,0x0
  2d:	c9                   	leave
  2e:	c3                   	ret
```
- This is the disassembled code for the `main` function. It matches the assembly code in the previous attachment:
  - Sets up the stack frame.
  - Initializes variables `a` and `b`.
  - Multiplies `a` and `b` using the `imul` instruction.
  - Stores the result in `c`.
  - Returns `0`.

#### **2. `.text.__x86.get_pc_thunk.ax` Section**
```text
00000000 <__x86.get_pc_thunk.ax>:
   0:	8b 04 24             	mov    eax,DWORD PTR [esp]
   3:	c3                   	ret
```
- This is the helper function `__x86.get_pc_thunk.ax`, which retrieves the program counter (PC) value for position-independent code.

---

### **Summary**
This `objdump` output provides a detailed view of the object file `mult_int.o`. It includes:
- Metadata about the file format and architecture.
- Section details, including their purpose and attributes.
- A symbol table listing functions and symbols.
- Disassembled machine code for the `main` function and the helper function `__x86.get_pc_thunk.ax`.

The `main` function performs integer multiplication (`a * b`) and returns `0`. The helper function supports position-independent code by retrieving the program counter.

## Project Code on GitHub
Project code and resources can be found on my GitHub repository: <br>
[GitHub](https://github.com/markkhusid/Disassembling-Binaries/tree/master/C/Intel_architecture/i386/Integer_Operations/Mult_Int)