# Pascal - AMD64 - Add Two Integers in a Function

Created with Grok Build

## Introduction

This page disassembles `add_functions_program` compiled for AMD64. The source is the debug build in [Functions](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Pascal/Intel_Architecture/AMD64/Functions/With_Debug_Info). The assembly is Intel syntax. The compiler is Free Pascal 3.0.4+dfsg-18ubuntu2, dated 2018/08/29, for x86_64. The banner is the `.fpc.n_version` section. `main` and `PASCALMAIN` are the same entry. On this build `INTEGER` is a 16-bit Smallint. The variables are BSS symbols. The code is in `.text.n_main`. The `.text` section is empty, so `objdump --section=.text` prints nothing useful. The notes after `//` were added to the listing. A `call` whose displacement is zero is an unapplied relocation, and objdump prints the next instruction as the target.

## The program *add_functions.pp*

```{literalinclude} code/add_functions.pp
:language: pascal
```

The debug build recorded these commands:

```bash
fpc -al -g add_functions.pp
mv add_functions add_functions_Pascal_AMD64_ggdb3
objdump -x -D -S -s -g -t -Mintel add_functions.o > objdump_of_dot_o.txt
```

The listing on this page is `.text` of the function and of `PASCALMAIN` from that object. The saved objdump also walks headers and debug sections.

The function symbol spells the parameters `SMALLINT`. `INTEGER` in this program is that 16-bit type. `a`, `b`, and `c` share one BSS block: `a` at offset 0, `b` at offset 2, and `c` at offset 4.


## add_function

The function is its own section, `.text.n_p$add_functions_program_$$_add_function$smallint$smallint$$smallint`. Its address in the object is 0, the same way `main` is at 0 in its own section.

```bash
0000000000000000 (P$ADD_FUNCTIONS_PROGRAM_$$_ADD_FUNCTION$SMALLINT$SMALLINT$$SMALLINT):
FUNCTION add_function(f_a : INTEGER; f_b : INTEGER) : INTEGER;

BEGIN
    0: 55                   push rbp                                    // Save the caller's frame pointer.
    1: 4889e5               mov rbp, rsp                                // This frame starts at the current stack pointer.
    4: 488d6424e0           lea rsp, [rsp-0x20]                         // Open 32 bytes for the two arguments and the result.
	add_function := f_a + f_b;
    9: 66897df8             mov WORD PTR [rbp-0x8], di                  // Spill f_a. The first Smallint arrives in di.
    d: 668975f0             mov WORD PTR [rbp-0x10], si                 // Spill f_b. The second Smallint arrives in si.
   11: 0fbf55f8             movsx edx, WORD PTR [rbp-0x8]               // edx = f_a, sign-extended.
   15: 0fbf45f0             movsx eax, WORD PTR [rbp-0x10]              // eax = f_b, sign-extended.
   19: 678d0402             lea eax, [edx+eax*1]                        // eax = f_a + f_b, the same lea-with-scale-1 encoding as the main program's sum.
   1d: 668945ec             mov WORD PTR [rbp-0x14], ax                 // Store the low 16 bits of the sum at rbp-0x14.
   21: 0fbf45ec             movsx eax, WORD PTR [rbp-0x14]              // eax = that sum, sign-extended. The caller reads the result from ax.
END;
   25: c9                   leave                                       // Release this frame.
   26: c3                   ret                                         // Return to the caller.
```

| Slot | Variable |
| --- | --- |
| `rbp-0x8` | `f_a` |
| `rbp-0x10` | `f_b` |
| `rbp-0x14` | the 16-bit sum |

The result goes back in `ax`.

## PASCALMAIN

`a` is 2, `b` is 3, and `c` is `add_function(a, b)`.

```bash
0000000000000000 (main):
BEGIN
    0: 55                   push rbp                                    // Save the caller's frame pointer.
    1: 4889e5               mov rbp, rsp                                // This frame starts at the current stack pointer.
    4: e800000000           call 9 <main+0x9>                           // Call FPC_INITIALIZEUNITS. The displacement is unapplied.
	a := 2;
    9: 66c70425000000000200 mov WORD PTR ds:0x0, 0x2                    // a = 2. The relocation is R_X86_64_32S to .bss.
	b := 3;
   13: 66c70425000000000300 mov WORD PTR ds:0x0, 0x3                    // b = 3, at .bss+2.
	c := add_function(a, b);
   1d: 0fbf042500000000     movsx eax, WORD PTR ds:0x0                  // eax = b, sign-extended from the halfword at .bss+2.
   25: 0fbf3c2500000000     movsx edi, WORD PTR ds:0x0                  // edi = a, sign-extended from the halfword at .bss.
   2d: 89c6                 mov esi, eax                                // esi = b. f_a goes in edi and f_b goes in esi.
   2f: e800000000           call 34 <main+0x34>                         // Call add_function. The displacement is the unapplied relocation to the function symbol.
   34: 6689042500000000     mov WORD PTR ds:0x0, ax                     // c = the low 16 bits of ax, at .bss+4.
END.
   3c: e800000000           call 41 <main+0x41>                         // Call FPC_DO_EXIT. The displacement is unapplied.
   41: c9                   leave                                       // Release this frame.
   42: c3                   ret                                         // Return.
```

| Offset | Variable | Value |
| --- | --- | --- |
| `.bss` | `a` | 2 |
| `.bss+2` | `b` | 3 |
| `.bss+4` | `c` | the low 16 bits of `add_function(2, 3)` |

The call loads `b` into `eax`, loads `a` into `edi`, then copies `eax` to `esi`. The function therefore receives `f_a` in `di` and `f_b` in `si`.

