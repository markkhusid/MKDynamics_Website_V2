#include <stdio.h>
#include <string.h>

int main(void)
{
    char s[] = "Hello, world!";
    char *t_ptr;
    char t_copy[100];

    /* Pointer assignment: no string copy */
    t_ptr = s;
    t_ptr[0] = 'z';
    printf("after pointer assign + mutate: s = %s\n", s);

    /* Restore s */
    s[0] = 'H';

    /* True string copy */
    strcpy(t_copy, s);
    t_copy[0] = 'z';
    printf("after strcpy + mutate copy: s = %s\n", s);
    printf("copy t_copy = %s\n", t_copy);
}
