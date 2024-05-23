// Find the minimum of two ints.
#include <iostream>

int min(int x, int y)
{
    if (x < y)
        return x;
    else
        return y;
}

int main()
{
    int j, k, m;

    std::cout << "Input two integers: ";
    std::cin >> j >> k;
    m = min(j, k);
    std::cout << '\n' << m << " is the minimum of " << j
              << " and " << k << std::endl;
}