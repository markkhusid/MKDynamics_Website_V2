// Repeated bell ringing
#include <iostream>

const char BELL = '\a';

void ring(int k)
{
    int i;

    for (i=0; i<k; ++i) {
        std::cout << BELL;
        std::cout << "Ring!" << std::endl;
    }
        
}

int main ()
{
    int n;
    std::cout << "\nInput a small positive integer: " << std::endl;
    std::cin >> n;
    ring(n);
}