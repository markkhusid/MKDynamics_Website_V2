# CSE543 Information Assurance and Security - Fuzz Them All

Created with Grok Build

The submission is a mutational fuzzer in C. It was written in C so the loop would be fast. A seed is copied into a working buffer. Each iteration may replace a byte. Every 500 iterations, ten more bytes are appended. The buffer is then written out for a separate runner.

The runner and the course programs it fed stay off this page. The novelty is the mutator itself.

## One byte at a time, 13 percent of the time

For each byte, the fuzzer draws a number from 0 to 100. If that draw is 13 or less, the byte is replaced with a random value from 1 to 255. The identifier in the submission says "13 percent." The test is `<= 13` on a draw of `rand() % 101`, so the rate is a little higher than 13 percent. That off-by-one is part of what the code actually does.

```c
void mutate_buffer(char *buf, int size)
{
    int i;

    for (i = 0; i < size; i++) {
        if ((rand() % 101) <= 13) {
            buf[i] = (char)((rand() % 255) + 1);
        }
    }
}
```

Zero is never written. A mutated byte is always in 1..255, so a C string inside the buffer is less likely to end early on a fresh zero. That choice matters when the target treats the buffer as a string.

## Growing the input

Every 500th iteration appends ten new random bytes and returns the new length. A fixed seed can only reach bugs near the front of the input. Growing the buffer is how the same seed eventually reaches a bug that depends on length.

```c
int add_10_random_bytes(char *buf, int size)
{
    int i;

    for (i = 0; i < 10; i++) {
        buf[size + i] = (char)((rand() % 255) + 1);
    }
    return size + 10;
}
```

The main loop is those two calls. Mutate on every iteration. Grow when the iteration count is a multiple of 500. After the last iteration, write the buffer to stdout.

The header comments on the submitted file carried a name, an email, and an id. Those lines are not part of this page.
