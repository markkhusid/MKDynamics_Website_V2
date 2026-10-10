# CSE543 Information Assurance and Security - Finding Crashes

Created with Grok Build

The lab was a folder of small C programs. The work was to find an input that made each one crash, and to say why that input was enough.

## What failed

Some of the programs passed an integer to a string function. A character code, or any other small number, is not the address of a string. The library then reads memory that was never a string, and the process faults.

A later program read a number and called it as a function. An address that arrives on stdin is not a safe place to jump. The bug is the call. The particular bytes that reach it are only how the bug shows up.

Other programs in the set put a comparison in front of the bad call, or asked for a longer input. The comparison changes which input gets through. It does not make the call safe.

## What stayed off this page

The course binaries, the inputs that crash them, and the notes that record those inputs are not published. A crashing input is enough to show the bug on that exact binary. It does not belong on a public page.

## A safer reading

A string API needs a pointer to a terminated string that the program itself allocated. A function pointer needs to be one the program formed, not one it parsed out of input. A comparison against a constant is not a boundary when the call behind it is still unchecked.
