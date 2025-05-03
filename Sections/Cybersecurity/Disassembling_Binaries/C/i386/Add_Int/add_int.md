# Adding Integers: i386

```{image} images/add_int_C_i386_splash.jpg
:height: 500
:width: 800
```

## Introduction
In this section we will examine the disassembly of a simple C program that adds two integers. The program is compiled for the i386 architecture, which is a 32-bit architecture commonly used in older computers and embedded systems. The disassembly will help us understand how the C code translates into assembly instructions, and how these instructions are executed by the CPU.

## The C Program
```{literalinclude} code/add_int.c
```

## Compilation of the C Program to Produce Assembly Code and Object Code
The C program is compiled using the GCC compiler with the `-m32` flag to specify the i386 architecture. The `-masm=intel` flag creates assembly code in the Intel format. The `-S` flag generates assembly code, the -fverbose-asm flag includes C source code in the assembly code, and the `-c` flag compiles the assembly code into an object file.

```bash
gcc --sysroot=/ -m32 -masm=intel -S -fverbose-asm add_int.c -o add_int.s
gcc --sysroot=/ -m32 -c add_int.s -o add_int.o
```

## Viewing the Assembly Code
The assembly code is in Intel syntax, which is commonly used for x86 assembly language.

```{literalinclude} code/add_int.s
```

## Explanation of the Assembly Code
The attached file is an assembly code file (`add_int.s`) generated from a C program (`add_int.c`). It is written in Intel syntax and compiled for a 32-bit architecture (`-m32`) using GCC 14.2.0. Below is a detailed explanation of the code:

---

### **Header Information**
1. **File Metadata**:
   - `.file "add_int.c"`: Indicates that this assembly file was generated from the C source file `add_int.c`.

2. **Compiler Information**:
   - The file was compiled using GCC 14.2.0 with the `-m32` flag for 32-bit architecture.
   - Other flags include `-masm=intel` (Intel syntax), `-mtune=generic` (generic CPU tuning), and `-march=x86-64` (targeting x86-64 architecture).

3. **GCC Heuristics**:
   - Parameters like `ggc-min-expand` and `ggc-min-heapsize` are used for garbage collection optimization during compilation.

---

### **Main Function**
The main function (`main`) is defined as a global symbol (`.globl main`) and is marked as a function (`.type main, @function`).

#### **Prologue**
The prologue sets up the stack frame for the function:
1. `push ebp`: Saves the base pointer of the previous stack frame.
2. `mov ebp, esp`: Sets the base pointer (`ebp`) to the current stack pointer (`esp`).
3. `sub esp, 16`: Allocates 16 bytes of space on the stack for local variables.

#### **Global Offset Table Setup**
- `call __x86.get_pc_thunk.ax`: Calls a helper function to get the program counter (PC).
- `add eax, OFFSET FLAT:_GLOBAL_OFFSET_TABLE_`: Adjusts the PC to point to the Global Offset Table (GOT), used for position-independent code.

#### **Variable Initialization**
The C code initializes three variables (`a`, `b`, and `c`):
1. `mov DWORD PTR -4[ebp], 1`: Assigns `1` to `a` (stored at `-4[ebp]`).
2. `mov DWORD PTR -8[ebp], 9`: Assigns `9` to `b` (stored at `-8[ebp]`).

#### **Addition Operation**
The C code computes `c = a + b`:
1. `mov edx, DWORD PTR -4[ebp]`: Loads the value of `a` into `edx`.
2. `mov eax, DWORD PTR -8[ebp]`: Loads the value of `b` into `eax`.
3. `add eax, edx`: Adds `a` and `b`, storing the result in `eax`.
4. `mov DWORD PTR -12[ebp], eax`: Stores the result (`c`) at `-12[ebp]`.

#### **Return Value**
- `mov eax, 0`: Sets the return value of the function to `0` (standard for `int main()` in C).

#### **Epilogue**
The epilogue restores the stack frame:
1. `leave`: Restores the previous base pointer and stack pointer.
2. `ret`: Returns control to the caller.

---

### **Helper Function: `__x86.get_pc_thunk.ax`**
This function is used to retrieve the program counter (PC) for position-independent code:
1. `mov eax, DWORD PTR [esp]`: Loads the return address (PC) from the stack into `eax`.
2. `ret`: Returns to the caller.

---

### **Other Sections**
1. **`.ident` Section**:
   - Contains metadata about the compiler version: `"GCC: (conda-forge gcc 14.2.0-2) 14.2.0"`.

2. **`.note.GNU-stack` Section**:
   - Indicates that the stack is not executable (a security feature).

---

### **Summary**
This assembly code represents a simple C program that initializes two integers (`a = 1` and `b = 9`), adds them (`c = a + b`), and returns `0`. The code includes standard prologue and epilogue for stack management and uses a helper function for position-independent code.

## Compilation to Produce Executable Code
The object file is linked to create an executable file using the `-o` flag.

```bash
/usr/bin/gcc -m32 add_int.o -o add_int_C_i386
```

## Disassembly of the Executable Code
The executable file is disassembled using the `objdump` command with the `-d` flag to display the disassembly.

```bash
objdump -x -D -s -t -Mintel add_int.o > objdump_of_dot_o.txt
objdump -x -D -s -t -Mintel add_int_C_i386 > objdump_of_dot_exe.txt
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
This object code disassembly represents the compiled output of a C program for the i386 architecture. Below is an explanation of the key sections and their significance:

---

### **File Metadata**
```plaintext
add_int.o:     file format elf32-i386
architecture: i386, flags 0x00000011:
HAS_RELOC, HAS_SYMS
start address 0x00000000
```
- **File format**: `elf32-i386` indicates the ELF (Executable and Linkable Format) for the 32-bit i386 architecture.
- **Flags**:
  - `HAS_RELOC`: The file contains relocation entries.
  - `HAS_SYMS`: The file contains a symbol table.
- **Start address**: The starting address of the program is `0x00000000`.

---

### **Sections**
The disassembly lists various sections in the object file, each serving a specific purpose:

1. **`.group`**
   - Contains metadata for grouping related sections.
   - Flags: `CONTENTS, READONLY, GROUP, LINK_ONCE_DISCARD`.

2. **`.text`**
   - Contains the executable code (instructions).
   - Flags: `CONTENTS, ALLOC, LOAD, RELOC, READONLY, CODE`.

3. **`.data`**
   - Contains initialized global and static variables.
   - Flags: `CONTENTS, ALLOC, LOAD, DATA`.

4. **`.bss`**
   - Contains uninitialized global and static variables.
   - Flags: `ALLOC`.

5. **`.text.__x86.get_pc_thunk.ax`**
   - Contains helper code for position-independent code (PIC).
   - Flags: `CONTENTS, ALLOC, LOAD, READONLY, CODE`.

6. **`.comment`**
   - Contains compiler version information.
   - Flags: `CONTENTS, READONLY`.

7. **`.note.GNU-stack`**
   - Marks the stack as non-executable for security purposes.
   - Flags: `CONTENTS, READONLY`.

8. **`.eh_frame`**
   - Contains exception handling information for stack unwinding.
   - Flags: `CONTENTS, ALLOC, LOAD, RELOC, READONLY, DATA`.

---

### **Symbol Table**
The symbol table lists symbols (functions, variables, and sections) in the object file:
```plaintext
00000000 g     F .text	00000030 main
00000000 g     F .text.__x86.get_pc_thunk.ax	00000000 .hidden __x86.get_pc_thunk.ax
00000000         *UND*	00000000 _GLOBAL_OFFSET_TABLE_
```
- `main`: The main function is defined in the `.text` section and has a size of `0x30` bytes.
- `__x86.get_pc_thunk.ax`: A helper function for position-independent code.
- `_GLOBAL_OFFSET_TABLE_`: An undefined symbol used for dynamic linking.

---

### **Disassembly of `.text` Section**
This section contains the main function's instructions:
```asm
00000000 <main>:
   0:	55                   	push   ebp
   1:	89 e5                	mov    ebp,esp
   3:	83 ec 10             	sub    esp,0x10
   6:	e8 fc ff ff ff       	call   7 <main+0x7>
			7: R_386_PC32	__x86.get_pc_thunk.ax
   b:	05 01 00 00 00       	add    eax,0x1
			c: R_386_GOTPC	_GLOBAL_OFFSET_TABLE_
  10:	c7 45 f4 01 00 00 00 	mov    DWORD PTR [ebp-0xc],0x1
  17:	c7 45 f8 09 00 00 00 	mov    DWORD PTR [ebp-0x8],0x9
  1e:	8b 55 f4             	mov    edx,DWORD PTR [ebp-0xc]
  21:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  24:	01 d0                	add    eax,edx
  26:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  29:	b8 00 00 00 00       	mov    eax,0x0
  2e:	c9                   	leave  
  2f:	c3                   	ret    
```
- **Prologue**:
  - `push ebp`: Saves the base pointer of the previous stack frame.
  - `mov ebp, esp`: Sets up the current stack frame.
  - `sub esp, 0x10`: Allocates 16 bytes for local variables.

- **Position-Independent Code Setup**:
  - `call __x86.get_pc_thunk.ax`: Calls a helper function to get the program counter.
  - `add eax, _GLOBAL_OFFSET_TABLE_`: Adjusts the program counter for the Global Offset Table (GOT).

- **Variable Initialization**:
  - `mov DWORD PTR [ebp-0xc], 0x1`: Stores `1` in the local variable at `-0xc`.
  - `mov DWORD PTR [ebp-0x8], 0x9`: Stores `9` in the local variable at `-0x8`.

- **Addition**:
  - `mov edx, DWORD PTR [ebp-0xc]`: Loads the first variable (`1`) into `edx`.
  - `mov eax, DWORD PTR [ebp-0x8]`: Loads the second variable (`9`) into `eax`.
  - `add eax, edx`: Adds `edx` to `eax` (result: `10`).
  - `mov DWORD PTR [ebp-0x4], eax`: Stores the result (`10`) in the local variable at `-0x4`.

- **Return Value**:
  - `mov eax, 0x0`: Sets the return value to `0`.
  - `leave`: Restores the previous stack frame.
  - `ret`: Returns control to the caller.

---

### **Disassembly of `.text.__x86.get_pc_thunk.ax`**
This helper function retrieves the program counter for position-independent code:
```asm
00000000 <__x86.get_pc_thunk.ax>:
   0:	8b 04 24             	mov    eax,DWORD PTR [esp]
   3:	c3                   	ret    
```
- `mov eax, DWORD PTR [esp]`: Loads the return address (program counter) into `eax`.
- `ret`: Returns to the caller.

---

### **Disassembly of `.comment`**
Contains metadata about the compiler:
```asm
00000000 <.comment>:
   0:	00 47 43             	add    BYTE PTR [edi+0x43],al
   ...
```
- This section is not executable and contains the string `GCC: (Ubuntu 7.3.0-27ubuntu1~18.04) 7.3.0`.

---

### **Disassembly of `.eh_frame`**
Contains exception handling information for stack unwinding:
```asm
00000000 <.eh_frame>:
   0:	14 00                	adc    al,0x0
   ...
```
- This section is used by the runtime for exception handling and debugging.

---

### **Summary**
This object file disassembly shows:
1. **Code Structure**: The `.text` section contains the main function and helper code for position-independent execution.
2. **Relocation**: The GOT setup ensures compatibility with dynamically linked libraries.
3. **Metadata**: Sections like `.comment` and `.eh_frame` provide additional information for debugging and exception handling.

## Project Code on GitHub
Project code and resources can be found on my GitHub repository: <br>
[GitHub](https://github.com/markkhusid/Disassembling-Binaries/tree/master/C/Intel_architecture/i386/Integer_Operations/Add_Int)