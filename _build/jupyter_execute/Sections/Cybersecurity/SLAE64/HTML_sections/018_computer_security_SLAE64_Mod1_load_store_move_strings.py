#!/usr/bin/env python
# coding: utf-8

# # <span style="font-family:Papyrus; font-size:2em;">Module 1 Section 18 - Load, Store and Move Strings</span>
# ### <span style="font-family:Papyrus; font-size:1em;">Moving Data in 64-bit Assembly Language on Linux</span>

# ## <span style="font-family:Papyrus; font-size:2em;">Introduction</span>

# <span style="font-family:Papyrus; font-size:1.25em;">In this section we will be following along with and completing course material from the Pentester Academy's SecurityTube Linux Assembly language Expert 64 Bit course.</span>
#     
# <span style="font-family:Papyrus; font-size:1.25em;">In this section we will be focusing on moving data using 64-Bit Assembly Language on Linux.  Specifically, we will be loading, storing and moving data using the lodsx, stosx, and movsx instructions.  The x stands for either b for byte, w for word, d for double-word, q for quad-word.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">Project code is contained in my <a href="https://github.com/markkhusid/SLAE64">github</a>.</span>

# ## <span style="font-family:Papyrus; font-size:1.75em;">The Program <i>Strings-64.nasm</i></span>

# <span style="font-family:Papyrus; font-size:1.25em;">The code below displays the contents of the program <i>Strings-64.nasm</i></span>

# ```python
# ; Filename: Strings-64.nasm
# ; Author:  Vivek Ramachandran
# ; Website:  http://securitytube.net
# ; Training: http://securitytube-training.com 
# ;
# ;
# ; Purpose: String Operations in 64-bit CPU
# 
# ; Added line below to satisfy Vim error checking.  MK.
# BITS 64
# 
# global _start			
# 
# section .text
# _start:
# 
# 	; Movsb/w/d/q
# 	; Memory to Memory 
# 	cld
# 	lea rsi, [HelloWorld]
# 	lea rdi, [Copy]
# 	movsq
# 
# 	cld
# 	lea rsi, [HelloWorld]
# 	xor rax, rax
# 	mov qword [Copy], rax
# 	lea rdi, [Copy]
# 	mov rcx, len
# 	rep movsb
# 
# 
# 	; stosb/w/d/q
# 	; Register to Memory 
# 
# 	mov rax, 0x0123456789abcdef
# 	lea rdi, [var1]
# 	stosq
# 
# 	; lodsb/w/d/q 
# 	; Memory to Register 
# 
# 	xor rax, rax 
# 	lea rsi, [var1]
# 	lodsq
# 
# 		
# 	; exit the program gracefully  
# 
# 	mov rax, 0x3c
# 	mov rdi, 0		
# 	syscall
# 
# 
# section .data
# 
# 	HelloWorld:	db	"Hello World"
# 	len:	equ	$-HelloWorld
# 
# section .bss
# 
# 	Copy:	resb	len
# 	var1:	resb	8
# ```

# <span style="font-family:Papyrus; font-size:1.25em;">The program contains a string variable called <i>p</i> that holds the password "PentesterAcademyPass". It then does a string compare of the variable <i>p</i> with the first argument passed to the executable from the command line. If the first argument is the same string as <i>p</i>, the strcmp function returns a zero. The enveloping if statement checks for this condition and if true, executes the statement:</span>

# ```C
# printf("\nWelcome to the SLAE 64-bit course! Please proceed to the next video!\n");
# ```

#   

# <span style="font-family:Papyrus; font-size:1.25em;">One way to crack this simple password checking routine is to run this program in GDB and trick the program into thinking that any randomly entered command line argument is the password.  This is done by setting the register that contains the randomly entered password to the hardcoded password "PentesterAcademyPass" from within GDB.  The executable then continues running thinking that the correct password was entered.<span>
# 
# <span style="font-family:Papyrus; font-size:1.25em;">We will now demonstrate the entire process.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">To do this, we need to first compile the program into an executable. The program is compiled with:</span>

#  ```Bash
#  $ gcc -ggdb3 gdb_test.c -o gdb_test 
#  ```

#   

# <span style="font-family:Papyrus; font-size:1.25em;">This produces an executable called <i>gdb_test</i>.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">In the next section, we run the executable <i>gdbtest</i> in GDB + GEF.</span>

# ## <span style="font-family:Papyrus; font-size:1.75em;">Running <i>gdbtest</i> in GDB + GEF</span>

# <span style="font-family:Papyrus; font-size:1.25em;">The screenshot below shows the executable <i>gdbtest</i> being run in GDB + GEF.</span>

# <figure>
#     <div class="img">
#         <img 
#             src="../../images/SLAE64/Module_1/003_GDB_Test/running_gdb_test_in_GEF.png"
#             width="1920"
#             height="1800"
#             title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Running the executable <i>gdbtest</i> in GDB + GEF
#         <p>
#     </div> <!-- .desc -->
# </figure>

# ## <span style="font-family:Papyrus; font-size:1.75em;">Examining the Disassembly of Main in Detail</span>

# <span style="font-family:Papyrus; font-size:1.25em;">In this section, we will examine the disassembly of the function <i>main</i> in more detail.  We will use the ATT format to become accustomed to it, but generally, the Intel format seems to be more prevalent.  In the screenshot below, we show the disassembly of the function <i>main</i> in both formats.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">First we start with the ATT format...</span>

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/disassembly_of_main_ATT.png"
#         width="1920"
#         height="1800"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Disassembly of the function <i>main</i> in the ATT format.
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">Next, we display the Intel format...</span>

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/disassembly_of_main_Intel.png"
#         width="1920"
#         height="1800"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Disassembly of the function <i>main</i> in the Intel format.
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">In the next section, we will zoom in to the function <i>main</i> shown in ATT format for clarity.</span>

# ## <span style="font-family:Papyrus; font-size:1.75em;">Examining the Disassembly of Main in Detail in the ATT Format</span>

# <span style="font-family:Papyrus; font-size:1.25em;">In the screenshot below, we can see the disassembly of the function <i>main</i> in ATT format and zoomed in for better viewing.  When viewing the assembly instructions, one instruction stands out as particularly interesting.  It is the string compare instruction, at <i>main</i> + 47.  If we could alter the return value of this function to satisfy the test that indeed a correct password was entered, then we can crack this password checking program.</span>

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/disassembly_of_main_ATT.png"
#         width="1920"
#         height="1800"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Disassembly of the function <i>main</i> in the ATT format and zoomed in.
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">In the next section, we will highlight the <i>strcmp</i> (string compare) instruction for clarity.</span>

# ## <span style="font-family:Papyrus; font-size:1.75em;">Highlighting the <i>strcmp</i> Instruction for Clarity</span>

# <span style="font-family:Papyrus; font-size:1.25em;">In the screenshot below, we can see the disassembly of the function <i>main</i> and the strcmp (string compare) highlighted.</span>

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/disassembly_of_main_strcpy_highlighted.png"
#         width="1920"
#         height="1800"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Disassembly of the function <i>main</i> and the strcmp (string compare) instruction highlighted.
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">In the screenshot above, we can see the disassembly of the function <i>main</i> and the strcmp (string compare) highlighted.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">We see a couple of <i>mov</i> instructions prior to the string compare, and a <i>test eax, eax</i> instruction following it.  The idea is that the <i>strcmp</i> function returns a zero into eax if the command line argument to the gdb_test executable matches the hardcoded password.  If the strings match, then the <i>test eax, eax</i> instruction performs a bitwise <i>AND</i> on the operands and sets the zero flag if the strings matched.  The result of the bitwise <i>AND</i> is not stored back into the register eax, only the zero flag is set.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">After the <i>test eax, eax</i> instruction, we see a <i>jne</i> or a Jump if Not Equal instruction, and then a series of <i>puts</i> function calls.  If the zero flag is not set, the program jumps to main+70, prints a string and then exits.  If they are equal, the <i>puts</i> function call at main+63 executes and then jumps to main + 82 near the end of the program.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">We can see a graphical visualization of this with the help of Radare2.</span>

# ## <span style="font-family:Papyrus; font-size:1.75em;">Disassembly of the Function <i>main</i> in Radare2</span>

# <span style="font-family:Papyrus; font-size:1.25em;">In the screenshot below, we disassemble the function <i>main</i> in Radare2

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/radare2_disassembly_of_gdb_test.png"
#         width="1920"
#         height="1800"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Disassembly of the function <i>main</i> and visualization in Radare2
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">In the screenshot above, we can see the disassembly of the function <i>main</i> in Radare2.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">In Radare2, we can clearly see the flow graph of the branching after the test for zero in eax is performed.  If we could modify eax to be a zero after this test, no matter what the command line argument was, then we can effectively always force the program to print the string that we want.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">In the next section, we will setup a breakpoint just before the <i>test eax, eax</i>.  Before executing this instruction, we will mov a zero into eax, effectively negating the results of the string compare.  The program will then continue as if the correct password was entered, effectively being cracked.</span>

# ## <span style="font-family:Papyrus; font-size:1.75em;">Setting Up a Break Point at the Instruction <i>test eax, eax</i></span>

# <span style="font-family:Papyrus; font-size:1.25em;">In this section we will setup a breakpoint at just before the instruction <i>test eax, eax</i>.  But first we must run the program with an arbitrary argument.  We will use the string "AAAA" for its ease of recognition in either ASCII format or its hex equivalent, 0x41414141.</span>

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/running_gdb_test_with_AAAA.png"
#         width="1920"
#         height="1800"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Running <i>gdb_test</i> with the argument AAAA
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">In the screenshot above, we can see that <i>gdb_test</i> was run with the argument AAAA.  This has been highlighted for clarity.  The program will then execute a number of instructions that set up the stack for the local variables.  We will not go into the details here in this section, because here will concentrate on using GDB to crack the program.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">What is important to note is that the arguments to the vulnerable <i>strcmp</i> function are passed through the registers RDI and RSI.  We will now set a breakpoint just before <i>test eax, eax</i> and also highlight RDI and RSI for clarity.</span>

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/set_breakpoint_before_test_eax_eax.png"
#         width="1920"
#         height="1800"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Breakpoint set at <i>test eax, eax</i>
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">In the screenshot above, we can see that a breakpoint was set at <i>*main+52</i>, which corresponds to the <i>test eax, eax</i> instruction.  We can also see that the two lines prior to the <i>strcmp</i> call were highlighted, to emphasize that the arguments to <i>strcmp</i> are passed via the registers RDI and RSI, per calling convention.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">We will now continue execution until the breakpoint at <i>*main+52</i>.</span>

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/before_test_eax_eax_showing_rdi_and_rsi.png"
#         width="1920"
#         height="1800"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Breakpoint hit at <i>test eax, eax</i>.  Also, RDI and RSI are highlighted for emphasis.
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">In the screenshot above, we can see that the breakpoint at <i>*main+52</i> was hit.  The arguments to <i>strcmp</i> are passed via the registers RDI and RSI, per calling convention.  The RDI contains the memory address of the passed command line argument "AAAA", while RSI contains the address of the hardcoded password "PentesterAcademyPass".</span>

# <span style="font-family:Papyrus; font-size:1.25em;">The two strings pointed to RDI and RSI are obviously different.  The result of the <i>strcmp</i> call will place a non-zero result into <i>rax</i>, as shown in the screenshot below:</span>

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/result_of_strcmp_showing_rax.png"
#         width="1910"
#         height="1800"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             RAX highlighted to show result of the <i>strcmp</i> call.
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">We can see in the screenshot above that the result of the <i>strcmp</i> call results in a non-zero value being returned into the <i>rax</i> register.  The next instructions is:</span>

# ><pre style='color:#1f1c1b;background-color:#ffffff; font-family:Courier; font-size:1.25em;'>
# ><b><span style='color:#644a9b;'>test</span></b> <b>eax</b>, <b>eax</b></pre>

# <span style="font-family:Papyrus; font-size:1.25em;">What this instruction will do is to perform a bitwise AND operation on the register <i>eax</i> with itself.  If <i>eax</i> contains zero, its bitwise and is also zero.  This will set the zero flag and a subsequent jump operation can be performed based on the state of this flag.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">What we want to do is to make the output of the <i>strcmp</i> function return a zero into the <i>eax</i> register, or just zero out the register <i>eax</i> using GDB prior to the <span style='color:#644a9b;'><b>test</b></span> <b>eax</b>, <b>eax</b> instruction.

# <span style="font-family:Papyrus; font-size:1.25em;">We choose to set the register <i>rdi</i> and <i>rsi</i> equal to each other using GDB.  With this change, the output of the <i>strcmp</i> function call will return a zero into the register <i>rax</i>.  This will effectively crack the password checking program.</span>

# <span style="font-family:Papyrus; font-size:1.25em;">In the next section, we will set the register <i>rdi</i> equal to <i>rsi</i>.</span>

# ## <span style="font-family:Papyrus; font-size:1.75em;">Setting the Register <i>rdi</i> Equal to the Register <i>rsi</i> Using GDB</span>

# <span style="font-family:Papyrus; font-size:1.25em;">In the screenshot below, we use the GDB command:</span>

# ><span style="font-family:Papyrus; font-size:1.25em;">$\large set\; rdi=rsi$</span>

# <span style="font-family:Papyrus; font-size:1.25em;">To set the registers <i>rdi</i> equal to the register <i>rsi</i>.

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/setting_rdi_equal_to_rsi.png"
#         width="1920"
#         height="1800"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Using GDB to set rdi equal to rsi
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">The result of this operation is shown in the screenshot below:</span>

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/result_of_setting_rdi_to_rsi.png"
#         width="1920"
#         height="1800"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Result of setting rdi to rsi using GDB
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">As we can see in the screenshot above, the register <i>rdi</i> has the same contents as the register <i>rsi</i>.  When the <i>strcmp</i> function is executed, the result this comparison will result in a zero being returned into the register <i>rax</i>.  Since there is a zero in rax, the <span style='color:#644a9b;'><b>test</b></span> <b>eax</b>, <b>eax</b> instruction will cause the zero flag to be set.  Following the <b><span style='color:#644a9b;'>test</span></b> <b>eax</b>, <b>eax</b> instruction, we have the instruction:

# ><pre style='color:#1f1c1b;background-color:#ffffff; font-family:Courier; font-size:1.25em;'>
# <b>jne</b>    <span style='color:#b08000;'>0x</span><span style='color:#b08000;'>55555555518b</span> &lt;main+<span style='color:#b08000;'>70</span>&gt;</pre>

# <span style="font-family:Papyrus; font-size:1.25em;">This instruction will not be taken because the status of the zero flag is not equal to zero.  The program execution then continues to the <i>puts</i> function call that will print the string that we are after.  The program then jumps to the exit stage, at which time it exits gracefully.  This is shown in the screenshot below.</span>

# <figure>
#     <div class="img">
#         <img 
#         src="../../images/SLAE64/Module_1/003_GDB_Test/successful_hack_of_gdbtest.png"
#         width="1800"
#         height="900"
#         title=""
#         >
#     </div> <!-- .img -->
#     <div class="desc">
#         <p>
#             Successful hack of gdbtest
#         <p>
#     </div> <!-- .desc -->
# </figure>

# <span style="font-family:Papyrus; font-size:1.25em;">Since we obtained the output string that we wanted, despite entering the wrong password, the password checking program <i>gdbtest</i> is effectively cracked.</span>
