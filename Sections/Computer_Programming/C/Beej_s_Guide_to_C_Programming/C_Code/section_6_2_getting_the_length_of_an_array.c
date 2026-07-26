#include <stdio.h>

void show_length_trick(void)
{
    int x[12];

    printf("sizeof x          = %zu bytes\n", sizeof x);
    printf("sizeof(int)       = %zu bytes\n", sizeof(int));
    printf("elements in x     = %zu\n", sizeof x / sizeof(int));
}

void foo(int x[12])
{
    /* x decays to a pointer here — sizeof no longer means "array size" */
    printf("inside foo: sizeof x = %zu (pointer width, not 12*int)\n", sizeof x);
    printf("inside foo: sizeof x / sizeof(int) = %zu (WRONG as element count)\n",
           sizeof x / sizeof(int));
}

int main(void)
{
    show_length_trick();
    int a[12] = {0};
    foo(a);
}
