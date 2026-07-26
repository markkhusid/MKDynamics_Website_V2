#include <stdio.h>

int main(void)
{
    char s[] = "Hello, world!";  /* mutable array copy of the literal */

    for (int i = 0; i < 13; i++)
        printf("%c", s[i]);
    printf("\n");

    s[0] = 'J';
    printf("%s\n", s);
}
