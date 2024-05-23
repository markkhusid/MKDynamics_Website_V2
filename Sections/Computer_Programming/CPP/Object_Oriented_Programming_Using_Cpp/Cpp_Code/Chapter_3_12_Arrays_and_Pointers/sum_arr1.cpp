// Simple array processing
#include <iostream>

using namespace std;

const int SIZE = 5;

int main()
{
    int a[SIZE];    // get space for a[0], ....., a[4]
    int i, sum = 0;

    for (i = 0; i < SIZE; ++i) {
        a[i] = i * i;
        cout << "a[" << i << "] = " << a[i] << "   ";
        sum += a[i];
    }
    cout << "\nsum = " << sum << endl;
}