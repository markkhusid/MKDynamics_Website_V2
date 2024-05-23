// Ring the bell using '\a' literal for the alarm.

#include <iostream>

const char BELL = '\a';

void ring()
{
    std::cout << BELL;
    std::cout << "Hello from function ring!" << std::endl;
}

int main()
{
    ring();
}