// Reverse a string with a ch_stack.
#include <iostream>
#include "ch_stac3.h"

using namespace std;

int main ()
{
    ch_stack s;
    char str[40] = {"My name is Don Knuth!"};
    int i = 0;

    cout << str << endl;
    s.reset();  // s.top = EMPTY would be illegal

    while (str[i] && !s.full())
    {
        s.push(str[i++]);
    }

    while (!s.empty())      // print the reverse
    {
        cout << s.pop();
    }

    cout << endl;
}