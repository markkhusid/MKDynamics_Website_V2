#include <stdio.h>

int main(void)
{
    int *p = NULL;   /* safe default: points nowhere */

    printf("p is %p\n", (void *)p);

    if (p == NULL) {
        printf("p is NULL — not dereferencing it.\n");
    }

    /* Uncommenting the next line is undefined behavior / likely crash:
     * *p = 12;
     */

    int x = 7;
    p = &x;
    if (p != NULL) {
        printf("p now points to x; *p = %d\n", *p);
    }
}
