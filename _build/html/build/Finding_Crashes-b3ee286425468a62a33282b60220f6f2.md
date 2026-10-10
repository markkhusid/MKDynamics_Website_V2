# CSE543 Information Assurance and Security - Finding Crashes

Created with Grok Build

The lab was a set of small C programs. The work was to find an input that made each one crash, and to say why. The listings below are the programs. The crash is a bad pointer or a smashed return address.

Several programs also contain a `win` function that prints a success line and exits. An input that redirects execution into `win` is an exploit, not a crash. Those addresses are not on this page.

## A constant used as a pointer

Any short input reaches the crash. The submitted text was `abcd`. The characters are never inspected.

```c
int main(void)
{
    printf("This is your first challenge.\n");
    getchar();
    puts((char *)1);
}
```

`getchar` only waits until one byte arrives. `puts` then treats the address 1 as a string. Address 1 is not a string, so the process faults. The text does not matter. The constant does.

## The character S

The second program stores one input byte and compares it with `0x53`, which is the character `S`.

```c
unsigned long long key = getchar();
if (key == 0x53) {
    puts((char *)key);
}
```

The submitted text was the line `S`. The comparison succeeds, and `puts` is called with the pointer value `0x53`. That is the same bug as the first program, behind a gate. Any other character skips the call and the process exits normally.

## A number called as a function

The third program reads two numbers. The first is compared with a constant. The second is called.

```c
int n = 0;
unsigned long long target;

scanf("%d", &n);
scanf("%llu", &target);
if (n == 0xc0decafe) {
    funcptr_t funcptr = (funcptr_t)target;
    funcptr();
}
```

If the first number does not match, nothing happens. If it matches, the second number is used as an instruction address. The value 1 is not code, so the call faults. That is the crash.

The binary also contains a `win` function. The submitted input called that function. The address is the exploit, so it is omitted here. A later program in the set used the same shape with a different comparison constant, and the same rule.

## A string longer than the array

```c
char buffer[40];

scanf("%s", buffer);
printf("You sent: %s\n", buffer);
exit(1);
```

`scanf` with `%s` writes until it sees whitespace. It does not stop at 40 bytes. The submitted text was a run of the letter `A` thousands of characters long.

Those bytes fill `buffer` and keep going, past the saved return address and off the stack. The process faults during the read. `exit(1)` is never reached. A shorter string that only overwrites the return address, and an input that aims that address at `win`, are a different exercise. Neither one is shown.

## The copy is into a smaller buffer

The outer read is bounded. The inner copy is not.

```c
int mycpy(char *input)
{
    char buffer[40];
    strcpy(buffer, input);
    return strlen(buffer);
}

int main(void)
{
    char buffer[256];

    scanf("%256s", buffer);
    mycpy(buffer);
    exit(1);
}
```

`%256s` allows a 256-character word into the outer array. `strcpy` then copies all of it into a 40-byte array. A run of `A` longer than 40 bytes overflows `mycpy`'s buffer and smashes its return address. The crash is the inner copy, not the outer read.

The submitted file continued past that crash and planted an address. That continuation is the exploit, and those bytes are not shown.

## A copy that starts too late in the array

```c
char buffer[256];

scanf("%256s", buffer);
if (update_crc(-1, buffer, sizeof(buffer)) == 0x4920cbc3) {
    memcpy(buffer + 128, buffer, sizeof(buffer));
}
```

When the check passes, `memcpy` writes 256 bytes starting at `buffer + 128`. The array only has 256 bytes total, so the write runs 128 bytes past the end. That is the crash. The CRC only decides whether the copy runs.

An input that satisfies the check is enough to demonstrate the bug on this binary. Building that input is left off the page. The lesson is the length of the copy, which is visible in the source.
