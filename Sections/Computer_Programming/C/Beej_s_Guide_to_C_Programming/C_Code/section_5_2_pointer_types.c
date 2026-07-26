#include <stdio.h>

int main(void)
{
    int i = 42;
    int *p;          /* type: pointer to int */
    double d = 3.14;
    double *pd;      /* type: pointer to double */

    p = &i;
    pd = &d;

    printf("i = %d,  &i = %p,  p = %p,  *p = %d\n",
           i, (void *)&i, (void *)p, *p);
    printf("d = %f,  &d = %p,  pd = %p, *pd = %f\n",
           d, (void *)&d, (void *)pd, *pd);
    printf("sizeof(int) = %zu, sizeof(int *) = %zu\n",
           sizeof(int), sizeof(int *));
    printf("sizeof(double) = %zu, sizeof(double *) = %zu\n",
           sizeof(double), sizeof(double *));
}
