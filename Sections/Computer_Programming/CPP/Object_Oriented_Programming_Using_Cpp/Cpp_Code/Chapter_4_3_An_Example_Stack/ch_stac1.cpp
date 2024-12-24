// Test of ch_stack by reversing a string.
#include "ch_stac1.h"
#include <iostream>

using namespace std;

int main()
{
    ch_stack s;
    char str[40] = {"My name is Betty Dolsberry!"};
    int i = 0;

    cout << str << endl;
    reset(&s);
    while (str[i] && !full(&s))
        push (&s, str[i++]);
    while (!empty(&s))
        cout << pop(&s);
    cout << endl;
}