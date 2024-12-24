#include <iostream>

using namespace std;

// The this pointer

class c_pair {
    public:
        void init(char b) { c2 = 1 + (c1 = b); }
        c_pair increment() { c1++; c2++; return (*this); }
        c_pair* where_am_I() { return this; }
        void print() { cout << c1 << c2 << '\t'; }
    private:
        char c1, c2;
};

int main()
{
    c_pair a, b;

    a.init('A');
    a.print();
    cout << " is at " << a.where_am_I() << endl;

    b.init('B');
    b.print();
    cout << " is at " << b.where_am_I() << endl;
    b.increment().print();
}