#include <stdio.h>

int main(void)
{
    char *s = "Hello, world!";

    printf("%s\n", s);
    printf("s points to address %p\n", (void *)s);
}
