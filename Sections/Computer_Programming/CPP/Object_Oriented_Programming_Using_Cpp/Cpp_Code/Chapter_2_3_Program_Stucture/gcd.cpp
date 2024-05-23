// Greatest common divisor program.
#include <iostream>
#include <assert.h>

int gcd(int m, int n)   // function declartion
{                       // block
    int r;              // declaration of remainder

    while (n != 0) {    // not equal
        r = m % n;      // modulo operator
        m = n;          // assignment
        n = r;
    }                   // end while loop

    return m;           // exit gcd with value m
}

int main()
{
    int x, y, g;

    std::cout << "\nProgram GCD C++";
    do {
        std::cout << "\nEnter two integers: ";
        std::cin >> x >> y;
        assert(x * y != 0); // precondition on GCD
        std::cout << "\nGCD(" << x << ", " << y << ") = "
             << (g = gcd(x, y)) << std::endl;
        assert(x % g == 0 && y % g ==0); // postcondition
    } while (x != y);
}
