# ARM 32 - Bit

**Under Contruction**

---

## **Introduction**

In this section, we will complete the set of exploit exercises known as Protostar. The first challenge is called Stack0. The idea is to change an internal variable in a running program from the command line. The technique involves overflowing a buffer to overwrite the contents of the internal variable. The link is shown below.

[Exploit-Exercises: Protostar (v2) on Vulnhub](https://www.vulnhub.com/entry/exploit-exercises-protostar-v2,32/)

We will perform this exercise using the ARM32 platform instead of the original i386 platform. The C code should run the same way, while the underlying assembly code is very different. We will explore the similarities as well as the differences between the two platforms.

---

## **The Vulnerable C Program `stack0.c`**

We start with the vulnerable C Program `stack0.c`. The program is vulnerable because the `gets` function does not have any bounds checking. In other words, it will take whatever amount of data is given to it and put this data into the `buffer` argument, even if the amount of data exceeds the storage space allocated for `buffer`. In this case, `buffer` is allocated 64 bytes.

If a properly coded payload is input into the `gets` function, it could overwrite the `buffer` variable and even other variables. In this case, the variable we wish to overwrite is called `modified`.

```{figure} images/stack0_c_3.jpg
:name: stack0_c_3
:alt: stack0_c_3
:align: center

The vulnerable program *stack0.c*
```

[Click here to download `stack0.c`](code/stack0.c)

---

## **Running the Vulnerable C Program `stack0.c` Through GDB+GEF**

In this section, we start the program in GDB+GEF and observe its behavior. As shown in the image below, the program waits for input on stdin. After inputting four *A's*, it replies with "Try again?"

```{figure} images/executing_stack0_in_cmd_line.png
:name: executing_stack0_in_cmd_line
:alt: executing_stack0_in_cmd_line
:align: center

Program execution in the command line
```

Clearly, we need to disassemble the program to understand its behavior and figure out how we can change the `modified` variable. We enter a breakpoint at `*main` (note: not `main`). Using `*main` allows us to get to the beginning of the main function's assembly code. Otherwise, breaking at `main` would only reach the beginning of the variable assignments, missing the important stack setup.

```{figure} images/parrot_gef3_redirect_payload_4_A_into_exe.png
:name: parrot_gef3_redirect_payload_4_A_into_exe
:alt: parrot_gef3_redirect_payload_4_A_into_exe
:align: center

Program execution in GDB+GEF
```

---

## **Disassembling The Vulnerable C Program `stack0.c` with GDB+GEF**

### **Visualizing Main's Stack Frame**

The command line arguments to `main` are pushed onto the stack in reverse order. Then `main`'s return address to `libc` is pushed onto the stack. Once the executable is ready to run, the stack pointer `ESP` points to `main`'s return address at the top of the stack. Everything else pushed onto the stack will go into lower addresses since the stack grows downward in memory.

```{figure} images/gef_start_run_with_4_A_highlight_main_ret_argc_argv.png
:name: gef_start_run_with_4_A_highlight_main_ret_argc_argv
:alt: gef_start_run_with_4_A_highlight_main_ret_argc_argv
:align: center

Main's stack frame highlighted
```
We now summarize the state of the stack in the following table:

| High Memory       | Stack Entry Name                                         | Size (bytes) |
|--------------------|----------------------------------------------------------|--------------|
|                   | `ARGV` (Address of array of strings)                     | 4            |
|                   | `ARGC` (Number of command line arguments)                | 4            |
| **`SP ->`**       | `RET` (Main's return address back to `libc`)             | 4            |
|                   | `garbage`                                                | 4            |
| Low Memory        | `garbage`                                                | 4            |

---

** Under Construction **

## **Disassembling and Executing the Vulnerable C Program `stack0.c`**

### **Stepping From `main+0` to `main+1`**

The instruction `push ebp` saves `main`'s `ebp` so that it can be restored after execution. The state of the stack changes as follows:

| High Memory       | Stack Entry Name                 | Size (bytes) |
|--------------------|----------------------------------|--------------|
|                   | `ARGV`                           | 4            |
|                   | `ARGC`                           | 4            |
|                   | `RET` (Return address)           | 4            |
| **`ESP ->`**      | `main`'s saved `EBP`             | 4            |
| Low Memory        | `garbage`                        | 4            |

![State of execution after `push ebp`](../images/Protostar/Stack0/gef_step_1_push_ebp.jpg)

---

### **Stepping From `main+1` to `main+3`**

The instruction `mov ebp, esp` moves the current stack pointer `esp` into `ebp`, allowing stack data to be referenced with respect to the base pointer `ebp`. The state of the stack does not change.

![State of execution after `mov ebp, esp`](../images/Protostar/Stack0/gef_step_2_mov_ebp_esp.jpg)

---

### **Stepping From `main+3` to `main+6`**

The instruction `and esp, 0xfffffff0` clears out the last 4 bits of the `esp` register, effectively subtracting 8 bytes from the current stack address. The updated stack layout is:

| High Memory       | Stack Entry Name                 | Size (bytes) |
|--------------------|----------------------------------|--------------|
|                   | `ARGV`                           | 4            |
|                   | `ARGC`                           | 4            |
|                   | `RET`                            | 4            |
|                   | `main`'s saved `EBP`             | 4            |
| **`ESP ->`**      | `0xf7f99000`                     | 4            |

![State of execution after `and esp, 0xfffffff0`](../images/Protostar/Stack0/gef_step_3_and_esp_0xfffffff0.jpg)

---

### **Layout of the Stack in Program `stack0.c` After `and esp, 0xfffffff0` Instruction**

The table below illustrates the layout of the stack once `and esp, 0xfffffff0` is executed:

| High Memory       | Stack Entry Name                                       | Size (bytes) |
|--------------------|--------------------------------------------------------|--------------|
|                   | `ARGV` (Address of array of strings)                   | 4            |
|                   | `ARGC` (Number of command line arguments)              | 4            |
|                   | `RET` (Main's return address back to `libc`)           | 4            |
| **`ESP ->`**      | `Main's saved EBP`                                     | 4            |
|                   | `garbage`                                              | 4            |
| Low Memory        | `garbage`                                              | 4            |

---

## **Disassembling and Executing The Vulnerable C Program `stack0.c` with GDB+GEF**

### **Stepping From `main+6` to `main+9`**

In this section, we advance a single assembly instruction, describe what happened, and show the state of the stack.

Execution was advanced a single step in GDB+GEF by using the `si` instruction. `EIP` now points to `main+9`.

![State of execution after `sub esp, 0x60`](../images/Protostar/Stack0/gef_step_4_sub_esp_0x60.jpg)

---

### **Layout of the Stack in Program `stack0.c` After `sub esp, 0x60` Instruction**

The table below illustrates the layout of the stack once `sub esp, 0x60` is executed:

| High Memory       | Stack Entry Name                                       | Size (bytes) |
|--------------------|--------------------------------------------------------|--------------|
|                   | `ARGV` (Address of array of strings)                   | 4            |
|                   | `ARGC` (Number of command line arguments)              | 4            |
|                   | `RET` (Main's return address back to `libc`)           | 4            |
| **`ESP ->`**      | `Main's saved EBP`                                     | 4            |
|                   | `garbage`                                              | 4            |
| Low Memory        | `buffer[64]` (Local buffer storage)                    | 64           |

---

## **Disassembling and Executing The Vulnerable C Program `stack0.c` with GDB+GEF**

### **Stepping From `main+9` to `main+17`**

In this section, we advance a single assembly instruction, describe what happened, and show the state of the stack.

Execution was advanced a single step in GDB+GEF by using the `si` instruction. `EIP` now points to `main+17`.

![State of execution after `mov DWORD PTR [esp+0x5c], 0x0`](../images/Protostar/Stack0/gef_step_5_mov_DWORD_PTR_esp+0x5c_0x0.jpg)

---

### **Layout of the Stack in Program `stack0.c` After `mov DWORD PTR [esp+0x5c], 0x0` Instruction**

The table below illustrates the layout of the stack once `mov DWORD PTR [esp+0x5c], 0x0` is executed:

| High Memory       | Stack Entry Name                                       | Size (bytes) |
|--------------------|--------------------------------------------------------|--------------|
|                   | `ARGV` (Address of array of strings)                   | 4            |
|                   | `ARGC` (Number of command line arguments)              | 4            |
|                   | `RET` (Main's return address back to `libc`)           | 4            |
| **`ESP ->`**      | `Main's saved EBP`                                     | 4            |
|                   | `garbage`                                              | 4            |
| Low Memory        | `modified` (Local variable set to 0)                   | 4            |

---

## **Disassembling and Executing The Vulnerable C Program `stack0.c` with GDB+GEF**

### **Stepping From `main+17` to `main+21`**

In this section, we advance a single assembly instruction, describe what happened, and show the state of the stack.

Execution was advanced a single step in GDB+GEF by using the `si` instruction. `EIP` now points to `main+21`.

![State of execution after `lea eax, [esp+0x1c]`](../images/Protostar/Stack0/gef_step_6_lea_eax_[esp+0x1c].jpg)

---

### **Layout of the Stack in Program `stack0.c` After `lea eax, [esp+0x1c]` Instruction**

The table below illustrates the layout of the stack once `lea eax, [esp+0x1c]` is executed:

| High Memory       | Stack Entry Name                                       | Size (bytes) |
|--------------------|--------------------------------------------------------|--------------|
|                   | `ARGV` (Address of array of strings)                   | 4            |
|                   | `ARGC` (Number of command line arguments)              | 4            |
|                   | `RET` (Main's return address back to `libc`)           | 4            |
| **`ESP ->`**      | `buffer[64]` (Start of buffer)                         | 64           |

---

## **Disassembling and Executing The Vulnerable C Program `stack0.c` with GDB+GEF**

### **Stepping From `main+21` to `main+24`**

In this section, we advance a single assembly instruction, describe what happened, and show the state of the stack.

Execution was advanced a single step in GDB+GEF by using the `si` instruction. `EIP` now points to `main+24`.

![State of execution after `mov DWORD PTR [esp], eax`](../images/Protostar/Stack0/gef_step_7_mov_DWORD_PTR_[esp]_eax.jpg)

---

### **Layout of the Stack in Program `stack0.c` After `mov DWORD PTR [esp], eax` Instruction**

The table below illustrates the layout of the stack once `mov DWORD PTR [esp], eax` is executed:

| High Memory       | Stack Entry Name                                       | Size (bytes) |
|--------------------|--------------------------------------------------------|--------------|
|                   | `ARGV` (Address of array of strings)                   | 4            |
|                   | `ARGC` (Number of command line arguments)              | 4            |
|                   | `RET` (Main's return address back to `libc`)           | 4            |
| **`ESP ->`**      | `0xffffd11c` (Address of `buffer[64]`)                 | 4            |

---

### **Creating the Payload to Overwrite the Variable `modified`**

We will create a Python script to build a payload. This payload will contain 64+4 characters, which is the 68 bytes necessary to completely overwrite the variable `modified`.

![Python program to generate payload to input into `stack0.c`](../images/Protostar/Stack0/exploit_py.jpg)

The goal of this program is to generate 66 bytes. The reason it is not 68 bytes is because we need to account for the carriage return (CR) character that Python's `print` statement appends to the end. Below is the output of `exploit.py` and a view of the `xxd` output of the payload file.

![Python program to generate payload to input into `stack0.c`](../images/Protostar/Stack0/exploit_py_output_and_xxd.jpg)

---

### **Layout of the Stack in Program `stack0.c` After `mov DWORD PTR [esp], eax` Instruction**

The table below illustrates the layout of the stack once `mov DWORD PTR [esp], eax` is executed:

| Stack Address - High Memory | Stack Entry Name                     | Value           | Size (bytes) |
|-----------------------------|--------------------------------------|-----------------|--------------|
| `0xffffd174`                | `ARGV` (Address of array of strings) | `0xffffd204`    | 4            |
| `0xffffd170`                | `ARGC` (Number of command line arguments) | `0x00000001`  | 4            |
| `0xffffd16c`                | `RET` (Main's return address back to `libc`) | `0xf7ddc9a1` | 4            |
| `0xffffd168`                | `Main's saved EBP`                   | `0x00000000`    | 4            |
| `0xffffd164`                | `unknown`                            | `0xf7f99000`    | 4            |
| `0xffffd160`                | `unknown`                            | `0xf7f99000`    | 4            |
| `0xffffd15c`                | `Local variable modified = 0`        | `0x00000000`    | 4            |
| `0xffffd100 ...`            | `Local Variable Data`                | `unknown`       | 92           |

---

### **Conclusion**

We have now successfully created a payload and executed the vulnerable program. By carefully stepping through the disassembly and manipulating the stack, we have been able to overwrite the `modified` variable and achieve the intended outcome. The process demonstrates how buffer overflows can be used to manipulate the behavior of a program by controlling stack


