	.arch armv8-a
	.file	"div_int.f08"
	.text
.Ltext0:
	.align	2
	.type	MAIN__, %function
MAIN__:
.LFB0:
	.file 1 "div_int.f08"
	.loc 1 1 15
	.cfi_startproc
	sub	sp, sp, #16
	.cfi_def_cfa_offset 16
	.loc 1 7 14
	mov	w0, 10
	str	w0, [sp, 12]
	.loc 1 8 13
	mov	w0, 5
	str	w0, [sp, 8]
	.loc 1 10 17
	ldr	w1, [sp, 12]
	ldr	w0, [sp, 8]
	sdiv	w0, w1, w0
	str	w0, [sp, 4]
	.loc 1 12 19
	nop
	add	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
	.cfi_endproc
.LFE0:
	.size	MAIN__, .-MAIN__
	.align	2
	.global	main
	.type	main, %function
main:
.LFB1:
	.loc 1 12 19
	.cfi_startproc
	stp	x29, x30, [sp, -32]!
	.cfi_def_cfa_offset 32
	.cfi_offset 29, -32
	.cfi_offset 30, -24
	mov	x29, sp
	str	w0, [sp, 28]
	str	x1, [sp, 16]
	.loc 1 12 19
	ldr	x1, [sp, 16]
	ldr	w0, [sp, 28]
	bl	_gfortran_set_args
	adrp	x0, options.0.0
	add	x1, x0, :lo12:options.0.0
	mov	w0, 7
	bl	_gfortran_set_options
	bl	MAIN__
	mov	w0, 0
	ldp	x29, x30, [sp], 32
	.cfi_restore 30
	.cfi_restore 29
	.cfi_def_cfa_offset 0
	ret
	.cfi_endproc
.LFE1:
	.size	main, .-main
	.section	.rodata
	.align	3
	.type	options.0.0, %object
	.size	options.0.0, 28
options.0.0:
	.word	2116
	.word	4095
	.word	0
	.word	1
	.word	1
	.word	0
	.word	31
	.text
.Letext0:
	.section	.debug_info,"",@progbits
.Ldebug_info0:
	.4byte	0xcd
	.2byte	0x4
	.4byte	.Ldebug_abbrev0
	.byte	0x8
	.uleb128 0x1
	.4byte	.LASF4
	.byte	0xe
	.byte	0x2
	.4byte	.LASF5
	.4byte	.LASF6
	.8byte	.Ltext0
	.8byte	.Letext0-.Ltext0
	.4byte	.Ldebug_line0
	.4byte	.Ldebug_macro0
	.uleb128 0x2
	.4byte	.LASF7
	.byte	0x1
	.byte	0xc
	.byte	0x13
	.4byte	0x74
	.8byte	.LFB1
	.8byte	.LFE1-.LFB1
	.uleb128 0x1
	.byte	0x9c
	.4byte	0x74
	.uleb128 0x3
	.4byte	.LASF0
	.byte	0x1
	.byte	0xc
	.byte	0x13
	.4byte	0x7b
	.uleb128 0x2
	.byte	0x91
	.sleb128 -4
	.uleb128 0x3
	.4byte	.LASF1
	.byte	0x1
	.byte	0xc
	.byte	0x13
	.4byte	0x80
	.uleb128 0x3
	.byte	0x91
	.sleb128 -16
	.byte	0x6
	.byte	0
	.uleb128 0x4
	.byte	0x4
	.byte	0x5
	.4byte	.LASF2
	.uleb128 0x5
	.4byte	0x74
	.uleb128 0x6
	.byte	0x8
	.4byte	0x86
	.uleb128 0x4
	.byte	0x1
	.byte	0x8
	.4byte	.LASF3
	.uleb128 0x7
	.4byte	.LASF8
	.byte	0x1
	.byte	0x1
	.byte	0xf
	.byte	0x2
	.8byte	.LFB0
	.8byte	.LFE0-.LFB0
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0x8
	.string	"a"
	.byte	0x1
	.byte	0x5
	.byte	0x1c
	.4byte	0x74
	.uleb128 0x2
	.byte	0x91
	.sleb128 -4
	.uleb128 0x8
	.string	"b"
	.byte	0x1
	.byte	0x5
	.byte	0x1f
	.4byte	0x74
	.uleb128 0x2
	.byte	0x91
	.sleb128 -8
	.uleb128 0x8
	.string	"c"
	.byte	0x1
	.byte	0x5
	.byte	0x22
	.4byte	0x74
	.uleb128 0x2
	.byte	0x91
	.sleb128 -12
	.byte	0
	.byte	0
	.section	.debug_abbrev,"",@progbits
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x11
	.byte	0x1
	.uleb128 0x25
	.uleb128 0xe
	.uleb128 0x13
	.uleb128 0xb
	.uleb128 0x42
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x1b
	.uleb128 0xe
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x10
	.uleb128 0x17
	.uleb128 0x2119
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x2116
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0xe
	.byte	0
	.byte	0
	.uleb128 0x5
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x6
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x6a
	.uleb128 0x19
	.uleb128 0x36
	.uleb128 0xb
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x2117
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_aranges,"",@progbits
	.4byte	0x2c
	.2byte	0x2
	.4byte	.Ldebug_info0
	.byte	0x8
	.byte	0
	.2byte	0
	.2byte	0
	.8byte	.Ltext0
	.8byte	.Letext0-.Ltext0
	.8byte	0
	.8byte	0
	.section	.debug_macro,"",@progbits
.Ldebug_macro0:
	.2byte	0x4
	.byte	0x2
	.4byte	.Ldebug_line0
	.byte	0x3
	.uleb128 0
	.uleb128 0x1
	.file 2 "/usr/include/finclude/aarch64-linux-gnu/math-vector-fortran.h"
	.byte	0x3
	.uleb128 0
	.uleb128 0x2
	.byte	0x4
	.byte	0x4
	.byte	0
	.section	.debug_line,"",@progbits
.Ldebug_line0:
	.section	.debug_str,"MS",@progbits,1
.LASF2:
	.string	"integer(kind=4)"
.LASF8:
	.string	"div_int"
.LASF6:
	.string	"/home/markkhusid/Documents/Engineering/Disassembling-Binaries/Fortran/ARM_architecture/ARM64/Integer_Operations/Div_Int/With_debug_info"
.LASF3:
	.string	"character(kind=1)"
.LASF0:
	.string	"argc"
.LASF5:
	.string	"div_int.f08"
.LASF7:
	.string	"main"
.LASF4:
	.string	"GNU Fortran2008 10.2.1 20210110 -mlittle-endian -mabi=lp64 -ggdb3 -fintrinsic-modules-path /usr/lib/gcc/aarch64-linux-gnu/10/finclude -fpre-include=/usr/include/finclude/aarch64-linux-gnu/math-vector-fortran.h"
.LASF1:
	.string	"argv"
	.ident	"GCC: (Debian 10.2.1-6) 10.2.1 20210110"
	.section	.note.GNU-stack,"",@progbits
