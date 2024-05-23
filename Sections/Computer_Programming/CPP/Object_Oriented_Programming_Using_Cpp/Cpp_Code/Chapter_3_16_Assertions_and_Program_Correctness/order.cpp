// FInding a minimum element in an array slice.
#include <iostream>
#include <assert.h>

using namespace std;

void order (int & p, int & q)
{
    int temp = p;
    if (p > q) {
        p = q;
        q = temp;
    }
}

int place_min(int a[], int size, int lb = 0)
{
    int i, min;
    assert(size >= 0);   // precondition

    for (i = lb; i < lb + size; ++i)
        order(a[lb], a[i + 1]);
    return a[lb];
}

int main()
{
    int a[9] = { 6, -9, 99, 3, -14, 9, -33, 8, 11 };

    cout << "Minimum = " << place_min(a, 3, 2) << endl;
    assert(a[2] <= a[3] && a[2] <= a[4]);   // postcondition
}