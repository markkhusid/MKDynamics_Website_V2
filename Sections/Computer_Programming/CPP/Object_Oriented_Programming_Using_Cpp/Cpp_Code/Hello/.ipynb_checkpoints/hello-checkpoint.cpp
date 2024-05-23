// Hello world in C++
#include <iostream>
#include <string>

using namespace std;

inline void pr_message(string s = "Hello World!")
{
    cout << s << endl;
}

int main()
{
    pr_message();
}