	.file	"div_int.c"
	.intel_syntax noprefix
# GNU C17 (conda-forge gcc 14.2.0-2) version 14.2.0 (x86_64-conda-linux-gnu)
#	compiled by GNU C version 14.2.0, GMP version 6.2.1, MPFR version 4.1.0, MPC version 1.2.1, isl version isl-0.24-GMP

# GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
# options passed: -m32 -masm=intel -mtune=generic -march=x86-64
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	push	ebp	#
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	mov	ebp, esp	#,
	.cfi_def_cfa_register 5
	sub	esp, 16	#,
	call	__x86.get_pc_thunk.ax	#
	add	eax, OFFSET FLAT:_GLOBAL_OFFSET_TABLE_	# tmp98,
# div_int.c:7: 	a = 10;
	mov	DWORD PTR -4[ebp], 10	# a,
# div_int.c:8: 	b = 5;
	mov	DWORD PTR -8[ebp], 5	# b,
# div_int.c:10: 	c = a / b;
	mov	eax, DWORD PTR -4[ebp]	# tmp104, a
	cdq
	idiv	DWORD PTR -8[ebp]	# b
	mov	DWORD PTR -12[ebp], eax	# c, c_3
	mov	eax, 0	# _4,
# div_int.c:11: }
	leave	
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret	
	.cfi_endproc
.LFE0:
	.size	main, .-main
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
.LFE1:
	.ident	"GCC: (conda-forge gcc 14.2.0-2) 14.2.0"
	.section	.note.GNU-stack,"",@progbits
