# Pascal Sources: i386

Created with Grok Build

```{figure} ../../images/Pascal/pascal_splash.jpg
:height: 500
:width: 800
:align: center
:class: clickable-figure

Pascal splash.
```


## Introduction

The i386 directory in the [Disassembling-Binaries Pascal tree](https://github.com/markkhusid/Disassembling-Binaries/tree/master/Pascal/Intel_Architecture/i386) saves the Pascal source for the integer add, the real add, and the function. An object file for those three programs was not saved, so this page shows the source.

The InputOutput directory also saves `writelin.pp` and `writelin.o`. That object is ELF 64-bit x86-64. Its `.fpc.n_version` banner is Free Pascal 3.0.4+dfsg-18ubuntu2 for x86_64, dated 2018/08/29. The 80 bytes of `.text.n_main` match the [AMD64 writeln](../AMD64/WRITELN/writeln.md) object. The shortstring in this object is `Hello World`, length byte `0x0b`:

```text
0b 48 65 6c 6c 6f 20 57 6f 72 6c 64 00 00 00 00
```

The AMD64 page prints `Hello World!`, length byte `0x0c`. The instructions are the same.

## Add two integers

```{literalinclude} code/add_int.pp
:language: pascal
```

## Add two reals

```{literalinclude} code/add_floats.pp
:language: pascal
```

## Add two integers in a function

```{literalinclude} code/add_functions.pp
:language: pascal
```

## Writeln

```{literalinclude} code/writelin.pp
:language: pascal
```
