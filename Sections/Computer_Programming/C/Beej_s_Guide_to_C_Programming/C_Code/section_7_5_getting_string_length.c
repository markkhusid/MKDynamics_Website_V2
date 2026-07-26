#include <stdio.h>
#include <string.h>

int main(void)
{
    char *s = "Hello, world!";

    printf("The string is %zu bytes long (strlen, not counting '\\0').\n",
           strlen(s));
}
