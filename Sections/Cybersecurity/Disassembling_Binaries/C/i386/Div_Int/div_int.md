# Dividing Integers: i386

```{image} images/div_int_C_i386_splash.png
:height: 500
:width: 800
```

## Introduction
In this section we will examine the disassembly of a simple C program that divides two integers. The program is compiled for the i386 architecture, which is a 32-bit architecture commonly used in older computers and embedded systems. The disassembly will help us understand how the C code translates into assembly instructions, and how these instructions are executed by the CPU.

## The C Program
```{literalinclude} code/div_int.c
```

## Compilation of the C Program to Produce Assembly Code and Object Code
The C program is compiled using the GCC compiler with the `-m32` flag to specify the i386 architecture. The `-masm=intel` flag creates assembly code in the Intel format. The `-S` flag generates assembly code, the `-fverbose-asm` flag includes C source code in the assembly code, and the `-c` flag compiles the assembly code into an object file.

```bash
gcc --sysroot=/ -m32 -masm=intel -S -fverbose-asm div_int.c -o div_int.s
gcc --sysroot=/ -m32 -c div_int.s -o div_int.o
```

## Viewing the Assembly Code
The assembly code is in Intel syntax, which is commonly used for x86 assembly language.

```{literalinclude} code/div_int.s
```

## Explanation of the Assembly Code
The attached code is an assembly file (`div_int.s`) generated from a C program (`div_int.c`) using the GCC compiler. It is written in Intel syntax and targets the x86 architecture in 32-bit mode (`-m32`). Below is a detailed explanation of the code:

---

### **Header Information**
1. **`.file "div_int.c"`**  
   Indicates that this assembly file was generated from the source file `div_int.c`.

2. **`.intel_syntax noprefix`**  
   Specifies that the assembly code uses Intel syntax (as opposed to AT&T syntax) and does not require prefixes like `%` for registers.

3. **Compiler Metadata**  
   - The code was compiled using GCC version 14.2.0.
   - It includes information about the compiler's configuration, such as GMP, MPFR, and MPC versions, as well as the target architecture (`x86_64-conda-linux-gnu`).
   - The options used during compilation include:
     - `-m32`: Generate 32-bit code.
     - `-masm=intel`: Use Intel assembly syntax.
     - `-mtune=generic`: Optimize for a generic x86 processor.
     - `-march=x86-64`: Target the x86-64 architecture.

---

### **Main Function**
The main function is defined as a global symbol (`.globl main`) and is marked as a function (`.type main, @function`). It begins at the label `main:`.

#### **Prologue**
The prologue sets up the stack frame for the function:
1. **`push ebp`**  
   Saves the base pointer (`ebp`) of the caller function onto the stack.
2. **`mov ebp, esp`**  
   Sets the current base pointer (`ebp`) to the value of the stack pointer (`esp`), establishing a new stack frame.
3. **`sub esp, 16`**  
   Allocates 16 bytes of space on the stack for local variables.

#### **Global Offset Table Setup**
1. **`call __x86.get_pc_thunk.ax`**  
   Calls a helper function to get the program counter (PC) value.
2. **`add eax, OFFSET FLAT:_GLOBAL_OFFSET_TABLE_`**  
   Adjusts the PC value to point to the Global Offset Table (GOT), which is used for position-independent code.

#### **Variable Initialization**
The C code initializes three variables: `a`, `b`, and `c`. These are represented as local variables on the stack:
1. **`mov DWORD PTR -4[ebp], 10`**  
   Stores the value `10` (for `a`) at the memory location `-4[ebp]`.
2. **`mov DWORD PTR -8[ebp], 5`**  
   Stores the value `5` (for `b`) at the memory location `-8[ebp]`.

#### **Division Operation**
The C code performs the division `c = a / b`:
1. **`mov eax, DWORD PTR -4[ebp]`**  
   Loads the value of `a` into the `eax` register.
2. **`cdq`**  
   Converts the value in `eax` to a 64-bit value by sign-extending it into the `edx:eax` pair. This is required for signed division.
3. **`idiv DWORD PTR -8[ebp]`**  
   Performs signed integer division of `edx:eax` by the value of `b`. The quotient is stored in `eax`, and the remainder is stored in `edx`.
4. **`mov DWORD PTR -12[ebp], eax`**  
   Stores the result of the division (the quotient, `c`) into the memory location `-12[ebp]`.

#### **Return Value**
1. **`mov eax, 0`**  
   Sets the return value of the function to `0` (as per the C standard for `int main()`).

#### **Epilogue**
The epilogue restores the stack frame and returns control to the caller:
1. **`leave`**  
   - Restores the stack pointer (`esp`) to the base pointer (`ebp`).
   - Pops the old base pointer from the stack into `ebp`.
2. **`ret`**  
   Returns control to the caller by popping the return address from the stack.

---

### **Helper Function: `__x86.get_pc_thunk.ax`**
This function is used to retrieve the program counter (PC) value for position-independent code:
1. **`mov eax, DWORD PTR [esp]`**  
   Loads the return address (stored at the top of the stack) into the `eax` register.
2. **`ret`**  
   Returns control to the caller.

---

### **Additional Sections**
1. **`.ident`**  
   Contains a string identifying the compiler version used to generate the assembly code.

2. **`.section .note.GNU-stack`**  
   Marks the stack as non-executable, which is a security feature.

---

### **Summary**
This assembly code implements a simple C program that initializes two integers (`a = 10` and `b = 5`), performs integer division (`c = a / b`), and returns `0`. The code is optimized for 32-bit x86 architecture and includes standard prologue and epilogue for stack management.

## Compilation to Produce Executable Code
The object file is linked to create an executable file using the `-o` flag.

```bash
/usr/bin/gcc -m32 div_int.o -o div_int_C_i386
```

## Disassembly of the Executable Code
The executable file is disassembled using the `objdump` command with the `-d` flag to display the disassembly.

```bash
objdump -x -D -s -t -Mintel div_int.o > objdump_of_dot_o.txt
objdump -x -D -s -t -Mintel div_int_C_i386 > objdump_of_dot_exe.txt
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
The attached file is the output of the `objdump` tool, which is used to analyze binary files. Specifically, this is the disassembly of an object file named `div_int.o` compiled for the `elf32-i386` architecture. Below is a detailed explanation of the file's contents:

---

### **File Header**
The first few lines provide metadata about the object file:

- **File Format**: `elf32-i386` indicates the file is in the ELF (Executable and Linkable Format) for the 32-bit Intel x86 architecture.
- **Architecture**: `i386` specifies the target CPU architecture.
- **Flags**: `0x00000011` indicates the file has relocation entries (`HAS_RELOC`) and symbols (`HAS_SYMS`).
- **Start Address**: `0x00000000` is the entry point address (not relevant for object files, as they are not executable).

---

### **Sections**
The object file is divided into sections, each serving a specific purpose. The table lists the sections with their attributes:

1. **.group**:
   - Size: `0x08` bytes.
   - Purpose: Groups related sections for optimization (e.g., `LINK_ONCE_DISCARD` ensures duplicate sections are discarded during linking).
   - Attributes: `CONTENTS, READONLY, GROUP`.

2. **.text**:
   - Size: `0x2f` bytes.
   - Purpose: Contains executable code (machine instructions).
   - Attributes: `CONTENTS, ALLOC, LOAD, RELOC, READONLY, CODE`.

3. **.data**:
   - Size: `0x00` bytes.
   - Purpose: Stores initialized global and static variables.
   - Attributes: `CONTENTS, ALLOC, LOAD, DATA`.

4. **.bss**:
   - Size: `0x00` bytes.
   - Purpose: Stores uninitialized global and static variables.
   - Attributes: `ALLOC`.

5. **.text.__x86.get_pc_thunk.ax**:
   - Size: `0x04` bytes.
   - Purpose: Contains a helper function for position-independent code (PIC).
   - Attributes: `CONTENTS, ALLOC, LOAD, READONLY, CODE`.

6. **.comment**:
   - Size: `0x28` bytes.
   - Purpose: Stores compiler version information.
   - Attributes: `CONTENTS, READONLY`.

7. **.note.GNU-stack**:
   - Size: `0x00` bytes.
   - Purpose: Marks the stack as non-executable (security feature).
   - Attributes: `CONTENTS, READONLY`.

8. **.note.gnu.property**:
   - Size: `0x28` bytes.
   - Purpose: Stores metadata about the binary (e.g., ABI compatibility).
   - Attributes: `CONTENTS, ALLOC, LOAD, READONLY, DATA`.

9. **.eh_frame**:
   - Size: `0x4c` bytes.
   - Purpose: Stores exception handling information (used for stack unwinding).
   - Attributes: `CONTENTS, ALLOC, LOAD, RELOC, READONLY, DATA`.

---

### **Symbol Table**
The symbol table lists symbols (functions, variables, etc.) defined or referenced in the object file:

- **`main`**:
  - Location: `.text` section.
  - Size: `0x2f` bytes.
  - Type: Global function (`g F`).

- **`__x86.get_pc_thunk.ax`**:
  - Location: `.text.__x86.get_pc_thunk.ax` section.
  - Size: `0x00` bytes.
  - Type: Hidden function (`.hidden`).

- **`_GLOBAL_OFFSET_TABLE_`**:
  - Location: Undefined (`*UND*`).
  - Purpose: Used for position-independent code (PIC).

---

### **Section Contents**
The contents of each section are displayed in hexadecimal and disassembled into assembly instructions.

#### **.group**
- Contains metadata for grouping sections.

#### **.text**
- Contains the implementation of the `main` function:
  ```objdump
  00000000 <main>:
     0: 55                    push   ebp
     1: 89 e5                 mov    ebp,esp
     3: 83 ec 10              sub    esp,0x10
     6: e8 fc ff ff ff        call   7 <main+0x7>
     b: 05 01 00 00 00        add    eax,0x1
    10: c7 45 fc 0a 00 00 00  mov    DWORD PTR [ebp-0x4],0xa
    17: c7 45 f8 05 00 00 00  mov    DWORD PTR [ebp-0x8],0x5
    1e: 8b 45 fc              mov    eax,DWORD PTR [ebp-0x4]
    21: 99                    cdq
    22: f7 7d f8              idiv   DWORD PTR [ebp-0x8]
    25: 89 45 f4              mov    DWORD PTR [ebp-0xc],eax
    28: b8 00 00 00 00        mov    eax,0x0
    2d: c9                    leave
    2e: c3                    ret
  ```
  - This function performs integer division:
    - Stores `10` and `5` in local variables.
    - Divides `10` by `5` using the `idiv` instruction.
    - Stores the result in another local variable.

#### **.text.__x86.get_pc_thunk.ax**
- Contains a helper function for position-independent code:
  ```objdump
  00000000 <__x86.get_pc_thunk.ax>:
     0: 8b 04 24              mov    eax,DWORD PTR [esp]
     3: c3                    ret
  ```

#### **.comment**
- Contains the compiler version:
  ```
  GCC: (conda-forge gcc 14.2.0-2) 14.2.0
  ```

#### **.note.gnu.property**
- Contains metadata about the binary.

#### **.eh_frame**
- Contains exception handling information.

---

### **Relocation Entries**
Relocation entries are present in the `.text` section:
- **`R_386_PC32`**: Relocation for position-independent code.
- **`R_386_GOTPC`**: Relocation for the Global Offset Table (GOT).

---

### **Disassembly**
The disassembly of each section shows the machine instructions and their corresponding assembly code. For example:

- **`main` function**:
  - Sets up the stack frame.
  - Performs integer division.
  - Cleans up and returns.

- **`__x86.get_pc_thunk.ax`**:
  - Retrieves the program counter for position-independent code.

---

### **Summary**
This object file (`div_int.o`) contains a simple program that performs integer division. It is compiled for the 32-bit x86 architecture and includes metadata, code, and relocation entries. The `main` function divides two integers (`10 / 5`) and stores the result. The file also includes helper functions and metadata for position-independent code and exception handling.

## Project Code on GitHub
Project code and resources can be found on my GitHub repository: <br>
[GitHub](https://github.com/markkhusid/Disassembling-Binaries/tree/master/C/Intel_architecture/i386/Integer_Operations/Mult_Int)