#include <stdio.h>

int main(void)
{
    int *p;
    int x = 0;
    p = &x;

    printf("sizeof(int)  = %zu\n", sizeof(int));
    printf("sizeof p     = %zu  (size of the pointer itself)\n", sizeof p);
    printf("sizeof *p    = %zu  (size of the pointed-to int)\n", sizeof *p);
    printf("sizeof(int*) = %zu\n", sizeof(int *));
}
