#include <stdio.h>

/* Manual strlen: count until NUL terminator */
int my_strlen(char *s)
{
    int count = 0;

    while (s[count] != '\0')
        count++;

    return count;
}

int main(void)
{
    char *s = "Hello!";  /* stored as Hello!\0 */

    printf("s = \"%s\"\n", s);
    printf("my_strlen(s) = %d\n", my_strlen(s));
    printf("chars including '\\0' occupy %zu bytes in a literal array sense\n",
           sizeof "Hello!");
}
