#include <stdio.h>

int main(void)
{
    int a = 1, b = 2;
    int *p, q;       /* p is int*, q is int */
    int *r, *s;      /* both pointers */

    p = &a;
    q = b;           /* not a pointer */
    r = &a;
    s = &b;

    printf("a=%d b=%d q=%d\n", a, b, q);
    printf("*p=%d *r=%d *s=%d\n", *p, *r, *s);
    printf("Note: 'int *p, q' makes only p a pointer.\n");
}
